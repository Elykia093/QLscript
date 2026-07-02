# QLscript Scripts

本目录只放青龙实际执行的任务脚本。新增脚本时请保持短文件名、标准文件头、环境变量说明和多账号格式一致。

## 脚本索引

| 脚本 | 文件 | cron | 环境变量 | 说明 |
| --- | --- | --- | --- | --- |
| 阿里云盘 | `alipan.py` | `10 8 * * *` | `ALIYUNDRIVE_TOKEN` | 阿里云盘签到与奖励领取 |
| 恩山无线论坛 | `enshan.py` | `20 8 * * *` | `ENSHAN_COOKIE` | 查询恩山币和积分 |
| 百度贴吧 | `tieba.py` | `30 8 * * *` | `TIEBA_COOKIE` | 贴吧批量签到，支持完整 Cookie 或 BDUSS |
| 王者营地 | `wzyd.js` | `40 8 * * *` | `WZYD_TOKEN`, `WZYD_BODY` | 王者营地签到 |

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
| `WZYD_TOKEN` | 是 | 王者营地签到请求头 JSON |
| `WZYD_BODY` | 是 | 王者营地签到请求体 JSON，账号数量需和 `WZYD_TOKEN` 一致 |

## 通知

Python 脚本优先调用青龙 `notify.py`，JavaScript 脚本优先调用青龙 `sendNotify.js`。通知模块不存在时会降级为控制台输出。
