# 开发规范

## 文件命名

- 任务脚本放在 `scripts/` 目录，使用短文件名，例如 `alipan.py`、`enshan.py`、`tieba.py`、`wzyd.js`。
- 公共依赖放在 `utils/`，或放在青龙 `ql repo` 的 `dependence` 参数会拉取到的根文件。
- 模板文件放在 `templates/`，避免被青龙当成任务。

## 文件头

每个任务脚本顶部必须写清：

- `cron: <表达式>`：默认定时。
- `new Env('任务名')`：青龙任务名。
- 环境变量：变量名、用途、是否必填、多账号格式。
- 依赖：Python / Node 依赖，以及仓库内公共文件依赖。

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

## 运行结构

每个脚本保持同一条主线：

1. 读取并校验环境变量。
2. 拆分多账号。
3. 逐账号执行，账号之间互不影响。
4. 聚合结果。
5. 打印日志并发送通知。
6. 有配置缺失或全部失败时返回非零退出码。

Python 复制 `templates/python_script_template.py` 后再改业务逻辑。JavaScript 复制 `templates/javascript_script_template.js` 后再改业务逻辑。

## 请求与错误处理

- 所有外部请求必须设置 timeout。
- 只在明确安全的场景做有限重试，不默认重试非幂等写操作。
- 网络错误、HTTP 错误、业务错误要分开记录。
- 不用裸 `except:` / 空 `catch` 吞错误。
- Python 中除非有明确证据，不使用 `verify=False`。
- JavaScript 中 `Promise` 必须 `await` 或 `return`，不要留下浮空请求。

## 提交前检查

- 文件是否放在 `scripts/` 目录，命名是否短且清楚。
- 文件头是否包含 `cron`、`new Env`、环境变量、依赖。
- README 和文档站是否同步新增脚本说明。
- README 的脚本列表是否包含真实 `scripts/` 文件，且不引用不存在的脚本。
- 变量名在 README、脚本头和代码里是否完全一致。
- 多账号是否按账号隔离，单个账号失败不会阻断全部账号。
- 外部请求是否都有 timeout。
- 通知缺失时是否能降级打印。
- 提交前至少对改动脚本做语法检查。

