# 快速开始

## 青龙拉库

在青龙面板中使用下面的拉库命令：

```bash
ql repo https://github.com/Elykia093/QLscript.git "scripts/" "templates|README|SCRIPT_STANDARD" "utils" "main" "py js"
```

这条命令只会让青龙执行 `scripts/` 目录下的任务脚本，`templates/`、README 和维护规范不会作为任务执行。

## 运行依赖

| 类型 | 依赖 |
| --- | --- |
| Python 脚本 | `requests` |
| JavaScript 脚本 | Node.js 18+ |

Python 依赖也记录在仓库根目录的 `requirements.txt`。

## 多账号格式

优先使用换行分隔账号：

```text
account_1
account_2
account_3
```

兼容 `&` 或 `#` 分隔。Cookie 内容本身常包含分号，默认不要用分号分隔账号。

完整变量清单和常见问题见 [环境变量与排错](/guide/environment)。

## 通知机制

Python 脚本优先调用青龙 `notify.py`，JavaScript 脚本优先调用青龙 `sendNotify.js`。通知模块不存在时会降级为控制台输出，不会因为缺少通知模块直接失败。

## 本地检查

Python 单文件语法检查：

```bash
python -m py_compile scripts/alipan.py
```

JavaScript 单文件语法检查：

```bash
node --check scripts/wzyd.js
```

文档站本地预览：

```bash
npm install
npm run docs:dev
```

## 下一步

- 查看 [脚本索引](/guide/scripts)，确认要启用的脚本和默认 cron。
- 打开 [环境变量与排错](/guide/environment)，按变量名逐项配置。
- 新增脚本前阅读 [开发规范](/guide/development)，保持命名、文件头和通知格式一致。
