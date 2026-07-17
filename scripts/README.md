# QLscript Scripts

本目录只放青龙实际执行的任务脚本。新增脚本时请保持短文件名、标准文件头、环境变量说明和多账号格式一致。

更完整的凭据说明、执行流程和常见失败原因见 [脚本详解页](../docs/content/docs/scripts/)。

## 脚本索引

| 脚本 | 文件 | cron | 环境变量 | 说明 |
| --- | --- | --- | --- | --- |
| 阿里云盘 | `alipan.py` | `10 8 * * *` | `ALIYUNDRIVE_TOKEN` | 阿里云盘签到与奖励领取 |
| 恩山无线论坛 | `enshan.py` | `20 8 * * *` | `ENSHAN_COOKIE` | 查询恩山币和积分 |
| 百度贴吧 | `tieba.py` | `30 8 * * *` | `TIEBA_COOKIE` | 贴吧批量签到，支持完整 Cookie 或 BDUSS |
| 王者营地 | `wzyd.js` | `40 8 * * *` | `WZYD_HEADERS`, `WZYD_BODY` | 王者营地签到 |
| 夸克网盘 | `quark.py` | `50 8 * * *` | `QUARK_COOKIE` | 夸克网盘签到领取空间 |
| 什么值得买 | `smzdm.py` | `55 8 * * *` | `SMZDM_COOKIE` | 什么值得买每日签到 |
| 米游社 | `mihoyo.py` | `0 9 * * *` | `MIHOYO_COOKIE`, `MIHOYO_GIDS` | 米游社社区签到，默认原神、星铁、绝区零 |
| 吾爱破解 | `pojie52.py` | `5 9 * * *` | `POJIE52_COOKIE` | 吾爱破解论坛签到与积分查询 |

## 多账号格式

优先使用换行分隔账号：

```text
account_1
account_2
account_3
```

兼容 `&` 或 `#` 分隔。Cookie 内容本身常包含分号，默认不要用分号分隔账号。

## 环境变量说明

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `ALIYUNDRIVE_TOKEN` | 是 | 阿里云盘 refresh_token |
| `ENSHAN_COOKIE` | 是 | 恩山论坛 Cookie |
| `TIEBA_COOKIE` | 是 | 百度贴吧完整 Cookie 或 BDUSS |
| `WZYD_HEADERS` | 是 | 王者营地签到请求头 JSON 对象，兼容旧变量 `WZYD_TOKEN` |
| `WZYD_BODY` | 是 | 王者营地签到请求体 JSON 对象，账号数量需和 `WZYD_HEADERS` 一致 |
| `QUARK_COOKIE` | 是 | 夸克网盘 Cookie，需要包含 `kps`、`sign`、`vcode` |
| `SMZDM_COOKIE` | 是 | 什么值得买 Cookie |
| `MIHOYO_COOKIE` | 是 | 米游社 Cookie |
| `MIHOYO_GIDS` | 否 | 米游社社区分区 id，默认 `2,6,8` |
| `POJIE52_COOKIE` | 是 | 吾爱破解论坛 Cookie |

## 通知

Python 脚本优先调用青龙 `notify.py`，JavaScript 脚本优先调用青龙 `sendNotify.js`。通知模块不存在时会降级为控制台输出。
