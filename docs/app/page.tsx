import {
  ArrowRight,
  BookOpenText,
  Cloud,
  Code2,
  FileCode2,
  Gamepad2,
  GitBranch,
  HardDrive,
  KeyRound,
  MessageSquareText,
  Radio,
  ShoppingBag,
  Sparkles,
  Terminal,
  type LucideIcon,
} from 'lucide-react';
import { readFileSync, readdirSync } from 'node:fs';
import { extname, join, parse } from 'node:path';
import { source } from '@/lib/source';
import styles from './page.module.css';

const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? '';

function internalHref(path: string) {
  return `${basePath}${path}`;
}

const scriptIcons: Partial<Record<string, LucideIcon>> = {
  alipan: Cloud,
  enshan: Radio,
  tieba: MessageSquareText,
  wzyd: Gamepad2,
  quark: HardDrive,
  smzdm: ShoppingBag,
  mihoyo: Sparkles,
  pojie52: Code2,
};

function getScripts() {
  const scriptsDirectory = join(process.cwd(), '..', 'scripts');

  return readdirSync(scriptsDirectory, { withFileTypes: true })
    .filter((entry) => entry.isFile() && ['.py', '.js'].includes(extname(entry.name)))
    .map((entry) => {
      const slug = parse(entry.name).name;
      const detailPage = source.getPage(['scripts', slug]);
      if (!detailPage) throw new Error(`脚本 ${entry.name} 缺少 docs/content/docs/scripts/${slug}.mdx`);

      const scriptSource = readFileSync(join(scriptsDirectory, entry.name), 'utf8');
      const cron = scriptSource.match(/^\s*cron:\s*([^\r\n]+)/m)?.[1].trim();
      if (!cron) throw new Error(`脚本 ${entry.name} 缺少 cron 文件头`);

      const fields = cron.split(/\s+/);
      const minute = Number(fields[0]);
      const hour = Number(fields[1]);
      const isDailyTime = fields.length === 5
        && Number.isInteger(minute)
        && minute >= 0
        && minute < 60
        && Number.isInteger(hour)
        && hour >= 0
        && hour < 24
        && fields.slice(2).every((field) => field === '*');

      return {
        href: detailPage.url,
        time: isDailyTime
          ? `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`
          : cron,
        sortOrder: isDailyTime ? hour * 60 + minute : Number.MAX_SAFE_INTEGER,
        name: detailPage.data.title,
        file: entry.name,
        runtime: extname(entry.name) === '.py' ? 'Python' : 'Node.js',
        icon: scriptIcons[slug] ?? FileCode2,
      };
    })
    .sort((left, right) => left.sortOrder - right.sortOrder || left.name.localeCompare(right.name, 'zh-CN'));
}

const scripts = getScripts();
const runtimeSummary = [...new Set(scripts.map((script) => script.runtime))]
  .map((runtime) => `${scripts.filter((script) => script.runtime === runtime).length} 个 ${runtime} 任务`)
  .join(' · ');

const guideLinks = [
  {
    href: '/docs/guide/getting-started',
    title: '拉取与依赖',
    description: '使用仓库命令拉取任务，并确认 Python、Node.js 与 requests。',
    icon: Terminal,
  },
  {
    href: '/docs/guide/environment',
    title: '填写环境变量',
    description: '按脚本填写 Cookie、token 或请求 JSON，支持多账号配置。',
    icon: KeyRound,
  },
  {
    href: '/docs/guide/troubleshooting',
    title: '运行与排障',
    description: '先手动运行单个任务，再按日志定位依赖、凭据与通知问题。',
    icon: BookOpenText,
  },
];

export default function HomePage() {
  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <nav className={styles.nav} aria-label="主导航">
          <a className={styles.brand} href={internalHref('/')} aria-label="QLscript 首页">
            <span className={styles.brandMark} aria-hidden="true">
              <Terminal size={17} strokeWidth={2.2} />
            </span>
            <span>QLscript</span>
          </a>

          <div className={styles.navLinks}>
            <a href={internalHref('/docs')}>文档</a>
            <a href={internalHref('/docs/guide/scripts')}>脚本</a>
            <a href={internalHref('/docs/guide/getting-started')}>使用指南</a>
          </div>

          <div className={styles.navActions}>
            <a
              className={styles.iconLink}
              href="https://github.com/Elykia093/QLscript"
              target="_blank"
              rel="noreferrer"
              aria-label="在 GitHub 查看 QLscript"
              title="GitHub"
            >
              <GitBranch size={19} aria-hidden="true" />
            </a>
          </div>
        </nav>
      </header>

      <div className={styles.content}>
        <section className={styles.hero} aria-labelledby="hero-title">
          <div className={styles.heroCopy}>
            <h1 id="hero-title">QLscript</h1>
            <p className={styles.heroSummary}>
              青龙面板自动化脚本库，集中维护常用任务、运行时间和配置文档。
            </p>

            <div className={styles.heroActions}>
              <a className={styles.primaryAction} href={internalHref('/docs/guide/getting-started')}>
                <BookOpenText size={16} aria-hidden="true" />
                快速开始
              </a>
            </div>
          </div>
        </section>

        <section className={styles.ecosystem} aria-labelledby="scripts-title">
          <div className={styles.sectionHeading}>
            <h2 id="scripts-title">当前脚本</h2>
            <p>{runtimeSummary}</p>
          </div>

          <ul className={styles.scriptCloud}>
            {scripts.map((script) => {
              const Icon = script.icon;

              return (
                <li key={script.href}>
                  <a href={internalHref(script.href)}>
                    <Icon size={26} strokeWidth={1.7} aria-hidden="true" />
                    <strong>{script.name}</strong>
                    <span>{script.file} · {script.time}</span>
                  </a>
                </li>
              );
            })}
          </ul>
        </section>

        <section className={styles.docsShowcase} aria-labelledby="docs-title">
          <div className={styles.sectionHeading}>
            <h2 id="docs-title">使用文档</h2>
            <p>安装、环境变量、脚本行为和常见错误都在同一套文档里维护</p>
          </div>

          <div className={styles.guideGrid}>
            {guideLinks.map((item) => {
              const Icon = item.icon;

              return (
                <a key={item.href} href={internalHref(item.href)}>
                  <Icon size={21} strokeWidth={1.8} aria-hidden="true" />
                  <span>
                    <strong>{item.title}</strong>
                    <small>{item.description}</small>
                  </span>
                  <ArrowRight size={17} aria-hidden="true" />
                </a>
              );
            })}
          </div>

          <a className={styles.docsPreview} href={internalHref('/docs')} aria-label="打开 QLscript 文档">
            <img
              src={internalHref('/home-docs-preview.jpg')}
              alt="QLscript 文档页面，包含导航、快速入口和维护说明"
              width={1265}
              height={712}
              loading="lazy"
            />
          </a>
        </section>
      </div>

      <footer className={styles.footer}>
        <div className={styles.footerInner}>
          <a className={styles.footerBrand} href={internalHref('/')}>QLscript</a>
          <nav className={styles.footerLinks} aria-label="页脚导航">
            <a href={internalHref('/docs')}>文档</a>
            <a href={internalHref('/docs/guide/scripts')}>脚本</a>
            <a href={internalHref('/docs/guide/environment')}>环境变量</a>
            <a href="https://github.com/Elykia093/QLscript" target="_blank" rel="noreferrer">GitHub</a>
          </nav>
          <span className={styles.footerNote}>青龙面板自动化脚本库</span>
        </div>
      </footer>
    </main>
  );
}
