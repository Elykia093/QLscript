# QLscript 脚本标准模板

本仓库后续新增或重构脚本，默认按本标准执行。除非目标平台必须特殊处理，否则不要临时发明另一套结构。

## 文件命名

- 任务脚本放在 `scripts/` 目录，使用短文件名，例如 `scripts/alipan.py`、`scripts/enshan.py`、`scripts/tieba.py`、`scripts/wzyd.js`。
- 公共依赖放在 `utils/`，或放在青龙 `ql repo` 的 `dependence` 参数会拉取到的根文件。
- 模板文件放在 `templates/`，避免被青龙当成任务。

## 文件头

每个任务脚本顶部必须写：

- `cron: <表达式>`：默认定时。
- `new Env('任务名')`：青龙任务名。
- `环境变量`：变量名、用途、是否必填、多账号格式。
- `依赖`：Python/Node 依赖，以及仓库内公共文件依赖。

推荐格式：

```text
cron: 10 8 * * *
new Env('示例任务')

环境变量:
  QL_TEMPLATE_TOKEN 必填，多账号建议用换行分隔，兼容 & 或 #。

依赖:
  Python: requests
  青龙通知: notify.py
```

## 环境变量

- 变量名使用全大写和下划线，例如 `ALIYUNDRIVE_TOKEN`。
- README、脚本头注释和代码读取的变量名必须一致。
- 不把 token、cookie、Authorization、完整请求头写死到代码里。
- 日志和通知不得打印完整 token/cookie，只能打印脱敏后的账号标识或账号序号。
- 多账号默认用换行分隔；兼容 `&`、`#` 只用于旧脚本迁移。不要默认用分号分隔 Cookie，因为 Cookie 本身常包含分号。

## 运行结构

每个脚本保持同一条主线：

1. 读取并校验环境变量。
2. 拆分多账号。
3. 逐账号执行，账号之间互不影响。
4. 聚合结果。
5. 打印日志并发送通知。
6. 有配置缺失或全部失败时返回非零退出码。

Python 复制 `templates/python_script_template.py` 后再改业务逻辑。

JavaScript 复制 `templates/javascript_script_template.js` 后再改业务逻辑。

## 请求与错误处理

- 所有外部请求必须设置 timeout。
- 只在明确安全的场景做有限重试，不默认重试非幂等写操作。
- 网络错误、HTTP 错误、业务错误要分开记录。
- 不用裸 `except:` / 空 `catch` 吞错误。
- Python 中除非有明确证据，不使用 `verify=False`；如必须关闭 TLS 校验，要在注释说明原因。
- JS 中 `Promise` 必须 `await` 或 `return`，不要留下浮空请求。

## 通知

- Python 优先兼容青龙 `notify.py` 的 `send(title, content)`。
- JavaScript 优先兼容青龙 `sendNotify.js` 的 `sendNotify(title, content)`。
- 通知模块缺失时降级为 `print`/`console.log`，不能让任务直接失败。
- 通知内容包含账号序号、成功/失败、关键原因；不包含完整敏感凭据。

## ql repo 建议

仓库正式整理后推荐使用 `scripts/` 目录作为白名单：

```bash
ql repo https://github.com/Elykia093/QLscript.git "scripts/" "templates|README|SCRIPT_STANDARD" "utils" "main" "py js"
```

如果脚本还没有迁移到 `scripts/` 目录，先不要直接使用上面的白名单。

## 提交前检查

- 文件是否放在 `scripts/` 目录，命名是否短且清楚。
- 文件头是否包含 `cron`、`new Env`、环境变量、依赖。
- README 是否同步新增脚本说明。
- README 的脚本列表是否包含真实 `scripts/` 文件，且不引用不存在的脚本。
- 变量名在 README、脚本头和代码里是否完全一致。
- 多账号是否按账号隔离，单个账号失败不会阻断全部账号。
- 外部请求是否都有 timeout。
- 通知缺失时是否能降级打印。
- 提交前至少对改动脚本做语法检查。
- Python 单文件可执行 `python -m py_compile <file>`。
- JS 单文件可执行 `node --check <file>`。
