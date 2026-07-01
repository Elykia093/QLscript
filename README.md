# ql-scripts

青龙面板自用脚本库。

## 青龙拉库

```bash
ql repo <repo_url> "scripts/" "templates|README|SCRIPT_STANDARD" "utils" "main" "py js"
```

其中 `<repo_url>` 替换成当前仓库地址。脚本依赖：

- Python：`requests`
- Node.js：>= 18

## 开发标准

新增或重构脚本先看 [SCRIPT_STANDARD.md](./SCRIPT_STANDARD.md)。

- Python 模板：[templates/python_script_template.py](./templates/python_script_template.py)
- JavaScript 模板：[templates/javascript_script_template.js](./templates/javascript_script_template.js)

后续脚本默认放在 `scripts/` 目录，使用短文件名，例如 `alipan.py`、`enshan.py`、`tieba.py`、`wzyd.js`，并在文件头写清 `cron`、`new Env`、环境变量、依赖和多账号格式。

## 脚本列表

| 脚本 | 文件 | 环境变量 | 说明 |
| --- | --- | --- | --- |
| 阿里云盘 | `scripts/alipan.py` | `ALIYUNDRIVE_TOKEN` | 阿里云盘签到与奖励领取 |
| 恩山无线论坛 | `scripts/enshan.py` | `ENSHAN_COOKIE` | 查询恩山币和积分 |
| 百度贴吧 | `scripts/tieba.py` | `TIEBA_COOKIE` | 贴吧批量签到，支持完整 Cookie 或 BDUSS |
| 王者营地 | `scripts/wzyd.js` | `WZYD_TOKEN`, `WZYD_BODY` | 王者营地签到 |

多账号建议使用换行分隔，兼容 `&` 或 `#`。Cookie 内容本身常包含分号，默认不要用分号分隔账号。

## 本地检查

```bash
python tools/check_repo.py
```

如果已经安装 Node.js，也可以使用：

```bash
npm run check
```

## 参考仓库

1. **[smzdm_script](https://github.com/hex-ci/smzdm_script)**  
   用于青龙面板的自用脚本，支持App端签到、转盘抽奖、每日任务等功能。

2. **[jdpro](https://github.com/6dylan6/jdpro)**  
   通过 GitHub 帐户创建，支持京东相关的自动化脚本。

3. **[ken-iMoutai-Script](https://github.com/AkenClub/ken-iMoutai-Script)**  
   青龙脚本，支持 i茅台预约申购、登录、短信验证码、耐力值和小茅运领取等功能。

4. **[naro-scripts](https://github.com/NaroisCool/naro-scripts)**  
   自用青龙脚本，支持云闪付签到、京东读书签到、王者营地签到、三国桃园签到等功能。

5. **[sign_script](https://github.com/imoki/sign_script)**  
   WPS 签到定时重放脚本，兼容青龙，支持多种平台（例如夸克网盘、屈臣氏、百度贴吧等）的签到。

6. **[dailycheckin](https://github.com/Sitoi/dailycheckin)**  
   基于 Docker、青龙面板、群晖的每日签到脚本，支持多账号，涵盖爱奇艺、全民K歌、阿里云盘等平台。

7. **[ELM](https://github.com/lu0b0/ELM)**  
   饿了么游乐园乐园币获取程序。

8. **[AutoTaskScript](https://github.com/sudojia/AutoTaskScript)**  
   自动化任务脚本，支持青龙面板。

9. **[ArcadiaScriptPublic](https://github.com/zjk2017/ArcadiaScriptPublic)**  
   公共的 Arcadia 脚本，支持自动化任务管理。

10. **[zyqinglong](https://github.com/linbailo/zyqinglong)**  
   青龙面板的自动化脚本，提供多种自动化任务。

11. **[QLScriptPublic](https://github.com/smallfawn/QLScriptPublic)**  
   公开的青龙脚本，包含多个自动化功能，适用于青龙面板。



