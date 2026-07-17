# QLscript

青龙面板脚本库，主要收纳个人常用的自动化任务脚本。脚本默认放在 `scripts/` 目录，公共方法放在 `utils/`，后续新增脚本按统一文件头、环境变量和多账号格式维护。

## 青龙拉库

```bash
ql repo https://github.com/Elykia093/QLscript.git "scripts/" "templates|README|SCRIPT_STANDARD" "utils" "main" "py js"
```

拉库后只会执行 `scripts/` 下的任务脚本，`templates/`、README 和维护规范不会作为任务执行。

## 运行依赖

- Python 脚本：Python 3.10+、`requests`
- JavaScript 脚本：Node.js 18+
- 文档站开发：Node.js 20.19+

本地运行完整质量检查前，可执行 `python -m pip install -r requirements.txt -r requirements-dev.txt` 安装运行与审计依赖。

## 脚本列表

脚本详情见 [scripts/README.md](scripts/README.md)。

| 脚本 | 文件 | 环境变量 | 说明 |
| --- | --- | --- | --- |
| 阿里云盘 | `scripts/alipan.py` | `ALIYUNDRIVE_TOKEN` | 阿里云盘签到与奖励领取 |
| 恩山无线论坛 | `scripts/enshan.py` | `ENSHAN_COOKIE` | 查询恩山币和积分 |
| 百度贴吧 | `scripts/tieba.py` | `TIEBA_COOKIE` | 贴吧批量签到，支持完整 Cookie 或 BDUSS |
| 王者营地 | `scripts/wzyd.js` | `WZYD_HEADERS`, `WZYD_BODY` | 王者营地签到，兼容旧变量 `WZYD_TOKEN` |
| 夸克网盘 | `scripts/quark.py` | `QUARK_COOKIE` | 夸克网盘签到领取空间 |
| 什么值得买 | `scripts/smzdm.py` | `SMZDM_COOKIE` | 什么值得买每日签到 |
| 米游社 | `scripts/mihoyo.py` | `MIHOYO_COOKIE`, `MIHOYO_GIDS` | 米游社社区签到，默认原神、星铁、绝区零 |
| 吾爱破解 | `scripts/pojie52.py` | `POJIE52_COOKIE` | 吾爱破解论坛签到与积分查询 |

多账号建议使用换行分隔，兼容 `&` 或 `#`。Cookie 内容本身常包含分号，默认不要用分号分隔账号。

## 文档站

`docs/` 是 Fumadocs UI 文档站，包含安装、环境变量、脚本详解、开发规范和排障说明。

在线文档：[https://elykia093.github.io/QLscript/](https://elykia093.github.io/QLscript/)

```bash
cd docs
npm install
npm run dev
```

发布或提交前建议在仓库根目录运行：

```bash
python -m compileall -q scripts templates utils tests tools
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/*.test.js
python tools/check_repository_consistency.py
pip-audit --strict -r requirements.txt
npm --prefix docs run types:check
npm --prefix docs run build
npm --prefix docs audit
```

## 目录结构

| 路径 | 用途 |
| --- | --- |
| `scripts/` | 青龙实际拉取和执行的任务脚本 |
| `utils/` | Python / JavaScript 公共工具方法 |
| `templates/` | 新脚本模板，不作为任务执行 |
| `docs/` | Fumadocs UI 文档站 |
| `SCRIPT_STANDARD.md` | 新增或重构脚本时参考的维护规范 |
| `requirements.txt` | Python 脚本依赖清单 |
| `requirements-dev.txt` | 本地与 CI 的 Python 质量审计依赖 |

## 维护约定

- 文件名使用小写短命名，例如 `alipan.py`、`enshan.py`。
- 脚本头写清 `cron`、`new Env`、环境变量、依赖和多账号格式。
- README、脚本头注释和代码读取的环境变量名保持一致。
- 日志和通知不要输出完整 token、cookie、Authorization 或完整请求头。
- 单个账号失败不应阻断其他账号执行，最终汇总成功和失败原因。

## 参考仓库

- [dailycheckin](https://github.com/Sitoi/dailycheckin)
- [jdpro](https://github.com/6dylan6/jdpro)
- [QLScriptPublic](https://github.com/smallfawn/QLScriptPublic)
- [quark-auto-save](https://github.com/Cp0204/quark-auto-save)
- [faker2](https://github.com/shufflewzc/faker2)
- [checkbox](https://github.com/Wenmoux/checkbox)
- [zyqinglong](https://github.com/linbailo/zyqinglong)
- [faker3](https://github.com/shufflewzc/faker3)
- [smzdm_script](https://github.com/hex-ci/smzdm_script)
- [only_for_happly](https://github.com/wd210010/only_for_happly)
- [MihoyoBBSTools](https://github.com/Womsxd/MihoyoBBSTools)
- [AutoTaskScript](https://github.com/sudojia/AutoTaskScript)
- [CHERWIN_SCRIPTS](https://github.com/CHERWING/CHERWIN_SCRIPTS)
- [sign_script](https://github.com/imoki/sign_script)
- [ArcadiaScriptPublic](https://github.com/zjk2017/ArcadiaScriptPublic)
- [ken-iMoutai-Script](https://github.com/AkenClub/ken-iMoutai-Script)
- [naro-scripts](https://github.com/NaroisCool/naro-scripts)
