import {
  ArrowRight,
  BookOpenText,
  Check,
  Cloud,
  Code2,
  ExternalLink,
  Gamepad2,
  GitBranch,
  HardDrive,
  KeyRound,
  MessageSquareText,
  Radio,
  ShoppingBag,
  Sparkles,
  Terminal,
} from 'lucide-react';
import styles from './page.module.css';

const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? '';

function internalHref(path: string) {
  return `${basePath}${path}`;
}

const scripts = [
  {
    href: '/docs/scripts/alipan',
    time: '08:10',
    name: '阿里云盘',
    file: 'alipan.py',
    runtime: 'PY',
    env: 'ALIYUNDRIVE_TOKEN',
    icon: Cloud,
  },
  {
    href: '/docs/scripts/enshan',
    time: '08:20',
    name: '恩山论坛',
    file: 'enshan.py',
    runtime: 'PY',
    env: 'ENSHAN_COOKIE',
    icon: Radio,
  },
  {
    href: '/docs/scripts/tieba',
    time: '08:30',
    name: '百度贴吧',
    file: 'tieba.py',
    runtime: 'PY',
    env: 'TIEBA_COOKIE',
    icon: MessageSquareText,
  },
  {
    href: '/docs/scripts/wzyd',
    time: '08:40',
    name: '王者营地',
    file: 'wzyd.js',
    runtime: 'JS',
    env: 'WZYD_HEADERS + WZYD_BODY',
    icon: Gamepad2,
  },
  {
    href: '/docs/scripts/quark',
    time: '08:50',
    name: '夸克网盘',
    file: 'quark.py',
    runtime: 'PY',
    env: 'QUARK_COOKIE',
    icon: HardDrive,
  },
  {
    href: '/docs/scripts/smzdm',
    time: '08:55',
    name: '什么值得买',
    file: 'smzdm.py',
    runtime: 'PY',
    env: 'SMZDM_COOKIE',
    icon: ShoppingBag,
  },
  {
    href: '/docs/scripts/mihoyo',
    time: '09:00',
    name: '米游社',
    file: 'mihoyo.py',
    runtime: 'PY',
    env: 'MIHOYO_COOKIE',
    icon: Sparkles,
  },
  {
    href: '/docs/scripts/pojie52',
    time: '09:05',
    name: '吾爱破解',
    file: 'pojie52.py',
    runtime: 'PY',
    env: 'POJIE52_COOKIE',
    icon: Code2,
  },
];

const guideLinks = [
  {
    number: '01',
    href: '/docs/guide/getting-started',
    title: '拉取与依赖',
    description: '拉取任务脚本，确认 Python、Node.js 和 requests。',
    icon: Terminal,
  },
  {
    number: '02',
    href: '/docs/guide/environment',
    title: '填写环境变量',
    description: '按脚本配置 Cookie、token 或请求 JSON。',
    icon: KeyRound,
  },
  {
    number: '03',
    href: '/docs/guide/troubleshooting',
    title: '运行与排障',
    description: '先运行单个脚本，再检查日志、凭据与通知。',
    icon: BookOpenText,
  },
];

export default function HomePage() {
  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <div className={styles.container}>
          <a className={styles.brand} href={internalHref('/')} aria-label="QLscript 首页">
            <span className={styles.brandMark} aria-hidden="true">
              <Terminal size={17} strokeWidth={2.2} />
            </span>
            <span>QLscript</span>
          </a>

          <nav className={styles.nav} aria-label="主导航">
            <div className={styles.navLinks}>
              <a href={internalHref('/docs')}>文档</a>
              <a href={internalHref('/docs/guide/scripts')}>脚本</a>
              <a href={internalHref('/docs/guide/environment')}>环境变量</a>
            </div>
            <a
              className={styles.githubLink}
              href="https://github.com/Elykia093/QLscript"
              target="_blank"
              rel="noreferrer"
              aria-label="在 GitHub 查看 QLscript"
            >
              <GitBranch size={17} aria-hidden="true" />
              <span>GitHub</span>
              <ExternalLink size={12} aria-hidden="true" />
            </a>
          </nav>
        </div>
      </header>

      <section className={styles.hero} aria-labelledby="hero-title">
        <div className={`${styles.container} ${styles.heroInner}`}>
          <div className={styles.heroCopy}>
            <p className={styles.eyebrow}>青龙面板自动化脚本库</p>
            <h1 id="hero-title">QLscript</h1>
            <p className={styles.statement}>集中维护个人常用自动化任务。</p>
            <p className={styles.lead}>
              集中维护 8 个青龙任务脚本，并提供环境变量、凭据、运行依赖和常见失败说明。
            </p>
            <div className={styles.actions}>
              <a className={styles.primaryAction} href={internalHref('/docs/guide/getting-started')}>
                开始使用
                <ArrowRight size={17} aria-hidden="true" />
              </a>
              <a className={styles.secondaryAction} href={internalHref('/docs/guide/scripts')}>
                查看脚本
              </a>
            </div>
          </div>

          <div className={styles.heroEmblem} aria-hidden="true">
            <Terminal size={84} strokeWidth={1.55} />
          </div>

          <div className={styles.previewShell} aria-label="QLscript 文档界面预览">
            <div className={styles.previewBar} aria-hidden="true">
              <span className={styles.windowDots}><i /><i /><i /></span>
              <span>docs / QLscript</span>
              <span>localhost:3000</span>
            </div>
            <img
              src={internalHref('/home-docs-preview.jpg')}
              alt="QLscript 文档首页，包含导航、快速入口和脚本说明"
              width={1265}
              height={712}
              loading="eager"
            />
          </div>
        </div>
      </section>

      <section className={styles.taskStrip} aria-labelledby="task-strip-title">
        <div className={styles.container}>
          <div className={styles.taskStripIntro}>
            <h2 id="task-strip-title">当前任务</h2>
            <p>7 个 Python 脚本，1 个 Node.js 脚本</p>
          </div>
          <ul>
            {scripts.map((script) => {
              const Icon = script.icon;

              return (
                <li key={script.href}>
                  <span aria-hidden="true"><Icon size={18} strokeWidth={1.8} /></span>
                  <strong>{script.name}</strong>
                </li>
              );
            })}
          </ul>
        </div>
      </section>

      <section className={styles.schedule} aria-labelledby="schedule-title">
        <div className={styles.container}>
          <div className={styles.sectionIntro}>
            <div>
              <p className={styles.eyebrow}>Daily schedule</p>
              <h2 id="schedule-title">默认从 08:10 开始，错峰执行。</h2>
            </div>
            <p>时间取自脚本文件头声明的默认 cron；点击任务可查看环境变量、执行流程和常见失败。</p>
          </div>

          <ol className={styles.jobGrid}>
            {scripts.map((script) => {
              const Icon = script.icon;

              return (
                <li key={script.href}>
                  <a className={styles.job} href={internalHref(script.href)}>
                    <span className={styles.jobTopline}>
                      <time>{script.time}</time>
                      <span>{script.runtime}</span>
                    </span>
                    <span className={styles.jobIdentity}>
                      <span className={styles.jobIcon} aria-hidden="true">
                        <Icon size={18} strokeWidth={1.8} />
                      </span>
                      <strong>{script.name}</strong>
                    </span>
                    <span className={styles.jobMeta}>
                      <code>{script.file}</code>
                      <code>{script.env}</code>
                    </span>
                    <ArrowRight className={styles.jobArrow} size={17} aria-hidden="true" />
                  </a>
                </li>
              );
            })}
          </ol>
        </div>
      </section>

      <section className={styles.workflow} aria-labelledby="workflow-title">
        <div className={styles.container}>
          <div className={styles.sectionIntro}>
            <div>
              <p className={styles.eyebrow}>Start here</p>
              <h2 id="workflow-title">首次接入，按这个顺序。</h2>
            </div>
            <p>完成拉库和环境变量配置后，先手动运行单个脚本；失败时按排障页检查依赖、凭据和通知。</p>
          </div>

          <div className={styles.guideGrid}>
            {guideLinks.map((item) => {
              const Icon = item.icon;

              return (
                <a key={item.href} className={styles.guideItem} href={internalHref(item.href)}>
                  <span className={styles.guideNumber}>{item.number}</span>
                  <span className={styles.guideIcon} aria-hidden="true">
                    <Icon size={20} strokeWidth={1.8} />
                  </span>
                  <span className={styles.guideCopy}>
                    <strong>{item.title}</strong>
                    <span>{item.description}</span>
                  </span>
                  <ArrowRight className={styles.guideArrow} size={18} aria-hidden="true" />
                </a>
              );
            })}
          </div>

          <div className={styles.repoPanel}>
            <div className={styles.repoHeading}>
              <span className={styles.repoPrompt} aria-hidden="true">$</span>
              <div>
                <span>Repository command</span>
                <strong>复制到青龙订阅管理</strong>
              </div>
            </div>
            <code className={styles.repoCommand}>
              ql repo https://github.com/Elykia093/QLscript.git &quot;scripts/&quot; &quot;templates|README|SCRIPT_STANDARD&quot; &quot;utils&quot; &quot;main&quot; &quot;py js&quot;
            </code>
          </div>

          <div className={styles.qualityLine} aria-label="维护基线">
            <span><Check size={15} aria-hidden="true" />账号级失败隔离</span>
            <span><Check size={15} aria-hidden="true" />通知模块自动降级</span>
            <span><Check size={15} aria-hidden="true" />语法、测试与依赖审计</span>
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <div className={styles.container}>
          <span>QLscript</span>
          <span>青龙任务脚本库 · 代码与文档同步维护</span>
        </div>
      </footer>
    </main>
  );
}
