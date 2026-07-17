import Link from 'next/link';
import { ArrowRight, BookOpen, FileCode2, TerminalSquare } from 'lucide-react';

const links = [
  {
    href: '/docs/guide/getting-started',
    title: '快速开始',
    description: '拉库命令、依赖和首次配置。',
    icon: TerminalSquare,
  },
  {
    href: '/docs/scripts/alipan',
    title: '脚本详解',
    description: '凭据、执行行为和失败原因。',
    icon: BookOpen,
  },
  {
    href: '/docs/guide/development',
    title: '开发规范',
    description: '新增脚本的文件头、账号拆分、通知和检查项。',
    icon: FileCode2,
  },
];

export default function HomePage() {
  return (
    <main className="ql-home">
      <section className="mx-auto flex min-h-screen w-full max-w-5xl flex-col justify-center px-6 py-12">
        <div className="max-w-3xl">
          <p className="mb-4 text-sm font-medium text-fd-muted-foreground">青龙面板脚本库文档</p>
          <h1 className="text-4xl font-semibold tracking-normal text-fd-foreground sm:text-5xl">QLscript</h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-fd-muted-foreground sm:text-lg">
            个人常用自动化任务脚本的维护手册，覆盖拉库、环境变量、Cookie 填写、脚本开发和排障。
          </p>
          <div className="mt-8">
            <Link
              href="/docs"
              className="inline-flex items-center gap-2 rounded-md bg-fd-primary px-4 py-2 text-sm font-medium text-fd-primary-foreground transition-colors hover:bg-fd-primary/90"
            >
              打开文档
              <ArrowRight className="size-4" aria-hidden="true" />
            </Link>
          </div>
        </div>
        <div className="mt-14 grid gap-4 md:grid-cols-3">
          {links.map((item) => {
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-lg border bg-fd-card p-5 text-fd-card-foreground transition-colors hover:bg-fd-accent/60"
              >
                <Icon className="mb-4 size-5 text-fd-muted-foreground" aria-hidden="true" />
                <h2 className="text-base font-medium">{item.title}</h2>
                <p className="mt-2 text-sm leading-6 text-fd-muted-foreground">{item.description}</p>
              </Link>
            );
          })}
        </div>
      </section>
    </main>
  );
}
