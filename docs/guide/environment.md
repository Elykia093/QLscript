# 环境变量与排错

## 配置位置

在青龙面板进入 `环境变量`，按脚本索引里的变量名新增变量。变量值只放在青龙面板里，不写入仓库、README、Issue 或截图。

多账号优先使用换行分隔：

```text
account_1
account_2
account_3
```

兼容 `&` 或 `#` 分隔。Cookie 内容本身常包含分号，默认不要用分号拆账号。

## 变量清单

| 变量 | 必填 | 对应脚本 | 说明 |
| --- | --- | --- | --- |
| `ALIYUNDRIVE_TOKEN` | 是 | `alipan.py` | 阿里云盘 refresh_token |
| `ENSHAN_COOKIE` | 是 | `enshan.py` | 恩山无线论坛 Cookie |
| `TIEBA_COOKIE` | 是 | `tieba.py` | 百度贴吧完整 Cookie 或 BDUSS |
| `WZYD_TOKEN` | 是 | `wzyd.js` | 王者营地签到请求头 JSON |
| `WZYD_BODY` | 是 | `wzyd.js` | 王者营地签到请求体 JSON，账号数量需和 `WZYD_TOKEN` 一致 |
| `QUARK_COOKIE` | 是 | `quark.py` | 夸克网盘 Cookie，需要包含 `kps`、`sign`、`vcode` |
| `SMZDM_COOKIE` | 是 | `smzdm.py` | 什么值得买 Cookie |
| `MIHOYO_COOKIE` | 是 | `mihoyo.py` | 米游社 Cookie |
| `MIHOYO_GIDS` | 否 | `mihoyo.py` | 米游社社区分区 id，默认 `2,6,8` |
| `POJIE52_COOKIE` | 是 | `pojie52.py` | 吾爱破解论坛 Cookie |

## 配置要点

- `WZYD_TOKEN` 和 `WZYD_BODY` 必须一一对应；两个变量的账号数量不一致时脚本会直接停止。
- `MIHOYO_GIDS` 用英文逗号分隔，默认覆盖 `2,6,8`。
- `TIEBA_COOKIE` 可以填完整 Cookie，也可以只填 `BDUSS`。
- `QUARK_COOKIE` 缺少关键字段时，多半会出现登录态异常或签到失败。
- 所有 Cookie、token、请求头都按敏感信息处理，日志和通知只保留账号序号或脱敏标识。

## 常见问题

### 提示未配置环境变量

检查青龙环境变量名是否和文档完全一致，尤其是大小写和下划线。变量新增后建议重新运行任务，不要只看旧日志。

### 只有部分账号失败

先看失败账号的 Cookie 是否过期，再确认多账号分隔符是否正确。脚本会尽量让单个账号失败不影响其他账号。

### 王者营地账号数量不一致

`WZYD_TOKEN` 和 `WZYD_BODY` 都支持多账号，但数量必须一致。建议两个变量都使用换行分隔，按相同顺序粘贴。

### 通知模块不存在

Python 脚本会尝试调用青龙 `notify.py`，JavaScript 脚本会尝试调用 `sendNotify.js`。模块不存在时会降级为控制台输出，不影响任务主体执行。

### 依赖缺失

Python 脚本需要 `requests`。如果青龙没有自动安装，进入依赖管理手动安装，或在容器里按青龙环境补依赖。

### Cookie 失效或平台风控

重新抓取 Cookie 后先单账号运行。平台接口、风控或签到规则变化时，旧 Cookie 正确也可能失败，需要结合日志更新脚本。
