# QLscript Docs

这里是 QLscript 的 Fumadocs UI 文档站。

在线地址：[https://elykia093.github.io/QLscript/](https://elykia093.github.io/QLscript/)

## 开发

```bash
npm install
npm run dev
```

## 验证

```bash
npm run types:check
npm run build
npm audit
```

## 内容维护

- 正文内容在 `content/docs/`。
- 脚本详解在 `content/docs/scripts/`。
- 修改脚本环境变量、cron 或执行行为后，同步根 README、`scripts/README.md`、脚本索引和脚本详解页。
- `.next/`、`.source/`、`out/` 和日志文件不提交。
