# 脚本索引

## 已维护脚本

| 脚本 | 文件 | 默认 cron | 环境变量 | 说明 |
| --- | --- | --- | --- | --- |
| 阿里云盘 | `alipan.py` | `10 8 * * *` | `ALIYUNDRIVE_TOKEN` | 阿里云盘签到与奖励领取 |
| 恩山无线论坛 | `enshan.py` | `20 8 * * *` | `ENSHAN_COOKIE` | 查询恩山币和积分 |
| 百度贴吧 | `tieba.py` | `30 8 * * *` | `TIEBA_COOKIE` | 贴吧批量签到，支持完整 Cookie 或 BDUSS |
| 王者营地 | `wzyd.js` | `40 8 * * *` | `WZYD_TOKEN`, `WZYD_BODY` | 王者营地签到 |
| 夸克网盘 | `quark.py` | `50 8 * * *` | `QUARK_COOKIE` | 夸克网盘签到领取空间 |
| 什么值得买 | `smzdm.py` | `55 8 * * *` | `SMZDM_COOKIE` | 什么值得买每日签到 |
| 米游社 | `mihoyo.py` | `0 9 * * *` | `MIHOYO_COOKIE`, `MIHOYO_GIDS` | 米游社社区签到，默认原神、星铁、绝区零 |
| 吾爱破解 | `pojie52.py` | `5 9 * * *` | `POJIE52_COOKIE` | 吾爱破解论坛签到与积分查询 |

## 环境变量

更完整的配置说明、账号分隔和排错步骤见 [环境变量与排错](/guide/environment)。

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `ALIYUNDRIVE_TOKEN` | 是 | 阿里云盘 refresh_token |
| `ENSHAN_COOKIE` | 是 | 恩山论坛 Cookie |
| `TIEBA_COOKIE` | 是 | 百度贴吧完整 Cookie 或 BDUSS |
| `WZYD_TOKEN` | 是 | 王者营地签到请求头 JSON |
| `WZYD_BODY` | 是 | 王者营地签到请求体 JSON，账号数量需和 `WZYD_TOKEN` 一致 |
| `QUARK_COOKIE` | 是 | 夸克网盘 Cookie，需要包含 `kps`、`sign`、`vcode` |
| `SMZDM_COOKIE` | 是 | 什么值得买 Cookie |
| `MIHOYO_COOKIE` | 是 | 米游社 Cookie |
| `MIHOYO_GIDS` | 否 | 米游社社区分区 id，默认 `2,6,8` |
| `POJIE52_COOKIE` | 是 | 吾爱破解论坛 Cookie |

## 配置提醒

- README、脚本头注释和代码读取的环境变量名必须一致。
- 不要把 token、cookie、Authorization 或完整请求头写死到代码里。
- 日志和通知只输出账号序号、成功失败和关键原因，不输出完整敏感凭据。
