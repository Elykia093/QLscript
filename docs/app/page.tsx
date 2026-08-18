import { GitBranch, Search } from 'lucide-react';
import styles from './page.module.css';

const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? '';

function internalHref(path: string) {
  return `${basePath}${path}`;
}

const featureCards = [
  {
    icon: '🌐',
    title: '常用平台脚本',
    description: '集中维护签到、网盘与社区任务，拉取仓库后即可统一运行。',
  },
  {
    icon: '🐍',
    title: 'Python 任务',
    description: '覆盖常见自动化场景，依赖与环境变量均有对应文档说明。',
  },
  {
    icon: '🟢',
    title: 'Node.js 任务',
    description: '同时支持 JavaScript 脚本，与 Python 任务共用一套维护流程。',
  },
  {
    icon: '⏰',
    title: '定时任务管理',
    description: '脚本内声明默认 cron，可直接交由青龙面板定时调度。',
  },
  {
    icon: '👥',
    title: '多账号配置',
    description: '按脚本文档填写 Cookie、token 或请求数据，支持多账号运行。',
  },
  {
    icon: '📖',
    title: '配套使用文档',
    description: '安装、变量、脚本行为与常见问题跟随仓库同步维护。',
  },
];

export default function HomePage() {
  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <nav className={styles.nav} aria-label="主导航">
          <a className={styles.brand} href={internalHref('/')} aria-label="QLscript 首页">
            <span className={styles.brandLogo} aria-hidden="true">QL</span>
            <span>QLscript</span>
          </a>

          <div className={styles.navActions}>
            <a className={styles.searchLink} href={internalHref('/docs')} aria-label="搜索文档">
              <Search size={18} aria-hidden="true" />
              <span>搜索</span>
            </a>
            <div className={styles.navLinks}>
              <a href={internalHref('/docs/guide/getting-started')}>指南</a>
              <a href={internalHref('/docs/guide/scripts')}>脚本</a>
            </div>
            <a
              className={styles.githubLink}
              href="https://github.com/Elykia093/QLscript"
              target="_blank"
              rel="noreferrer"
              aria-label="在 GitHub 查看 QLscript"
              title="GitHub"
            >
              <GitBranch size={22} aria-hidden="true" />
            </a>
          </div>
        </nav>
      </header>

      <section className={styles.home}>
        <div className={styles.hero}>
          <div className={styles.heroCopy}>
            <h1 id="hero-title">QLscript</h1>
            <p className={styles.heroTitle}>青龙面板自动化脚本库</p>
            <p className={styles.heroTagline}>常用签到与网盘任务，支持 Python 与 Node.js</p>

            <div className={styles.heroActions}>
              <a className={styles.primaryButton} href={internalHref('/docs/guide/getting-started')}>
                快速开始
              </a>
              <a className={styles.secondaryButton} href={internalHref('/docs/guide/scripts')}>
                浏览脚本
              </a>
            </div>
          </div>

          <div className={styles.heroArtwork} aria-hidden="true">
            <svg className={styles.heroLogo} viewBox="0 0 400 400">
              <defs>
                <linearGradient id="qlscript-hero-gradient" x1="48" y1="48" x2="352" y2="352">
                  <stop offset="0" stopColor="#36d7dc" />
                  <stop offset="0.52" stopColor="#16b8c7" />
                  <stop offset="1" stopColor="#168fdf" />
                </linearGradient>
              </defs>
              <circle cx="200" cy="200" r="178" fill="url(#qlscript-hero-gradient)" />
              <circle cx="200" cy="200" r="151" fill="none" stroke="rgba(255,255,255,.28)" strokeWidth="2" />
              <path d="M150 132 92 200l58 68" fill="none" stroke="#fff" strokeLinecap="round" strokeLinejoin="round" strokeWidth="26" />
              <path d="m250 132 58 68-58 68" fill="none" stroke="#fff" strokeLinecap="round" strokeLinejoin="round" strokeWidth="26" />
              <path d="m226 105-52 190" fill="none" stroke="#fff" strokeLinecap="round" strokeWidth="22" opacity=".96" />
            </svg>
          </div>
        </div>

        <section className={styles.features} aria-label="项目能力">
          {featureCards.map((feature) => (
            <article className={styles.featureCard} key={feature.title}>
              <span className={styles.featureIcon} aria-hidden="true">{feature.icon}</span>
              <h2>{feature.title}</h2>
              <p>{feature.description}</p>
            </article>
          ))}
        </section>
      </section>

      <footer className={styles.footer}>
        <p>© 2026 QLscript. 青龙面板自动化脚本库</p>
      </footer>
    </main>
  );
}
