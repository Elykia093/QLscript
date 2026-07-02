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

以下状态通过 GitHub API 于 2026-07-02 核对；简介取自仓库 `description` 字段，未设置时按空简介标注，并已剔除不可访问项。

| 仓库 | Stars | 状态 | GitHub 仓库简介 |
| --- | ---: | --- | --- |
| [dailycheckin](https://github.com/Sitoi/dailycheckin) | 8644 | 可访问 | 基于「Docker」/「青龙面板」/「群晖」的每日签到脚本（支持多账号）签到列表: ｜爱奇艺｜全民K歌｜有道云笔记｜百度贴吧｜Bilibili｜V2EX｜AcFun｜什么值得买｜阿里云盘｜i茅台申购｜小米运动｜百度搜索资源平台｜恩山论坛｜奥拉星｜ |
| [jdpro](https://github.com/6dylan6/jdpro) | 4428 | 可访问 | GitHub 未设置仓库简介 |
| [QLScriptPublic](https://github.com/smallfawn/QLScriptPublic) | 3179 | 可访问 | 青龙面板脚本公共仓库 企鹅交流1021185005 |
| [quark-auto-save](https://github.com/Cp0204/quark-auto-save) | 2894 | 可访问 | 夸克网盘签到、自动转存、命名整理、发推送提醒和刷新媒体库一条龙 |
| [faker2](https://github.com/shufflewzc/faker2) | 2891 | 可访问 | 不破楼兰终不还 |
| [checkbox](https://github.com/Wenmoux/checkbox) | 2538 | 可访问 | 签到本地/云函数/青龙脚本( 刺猬猫小说\|Acfun\| 时光相册\|书香门第论坛\|绅士领域\|好游快爆\|埋堆堆\|多看阅读\|闪艺app\|香网小说\|晋江\|橙光\|什么值得买\|网易蜗牛读书\|网易云游戏平台\|龙空论坛\|NGA论坛\|csdn\|mt论坛\|sf轻小说\|猫耳FM\|联想智选app\|联想智选\|数码之家\|AI风月\|togamemod\|好书友论坛\|鱼C论坛\|帆软社区\|村花论坛\|纪录片之家\|富贵论坛\|ug爱好者\|阅次元论坛\|菜鸟图库\|魅族社区\|经管之家\|有分享论坛\|bigfun社区\|阡陌居\|HiFiNi\|Hires后花园\|曲奇云盘\|游戏动力\|百度爱企查\|轻之文库\|Qoo\|天使动漫\|耽漫\|立创\|捷配\|花火论坛\|17k\|触站\|起点读书\|奥拉星商城\|共创\|麦当劳 |
| [zyqinglong](https://github.com/linbailo/zyqinglong) | 1928 | 可访问 | 青龙面板脚本自用库薅羊毛（✅ 滴滴出行领券✅ 滴滴加油领券✅ 滴滴代驾领券/滴滴签到领券打卡✅ 滴滴果园✅ mt论坛✅ 美团✅ 饿了么✅ 得物✅ 顺丰✅ 霸王茶姬✅ 益禾堂✅ 塔斯汀✅ 海底捞） |
| [faker3](https://github.com/shufflewzc/faker3) | 1912 | 可访问 | GitHub 未设置仓库简介 |
| [smzdm_script](https://github.com/hex-ci/smzdm_script) | 1614 | 可访问 | smzdm 自用脚本 for 青龙面板，支持 App 端签到、转盘抽奖、每日任务等功能 |
| [only_for_happly](https://github.com/wd210010/only_for_happly) | 1418 | 可访问 | manus自动写脚本 注册链接 https://manus.im/invitation/V9OIRPDYST3RAF8  1元机场 http://b.u9v.cn/dVMss 百度贴吧签到★小米运动刷步数★恩山签到★雨云签到白嫖服务器★小茅预约★天翼云盘签到★阿里云盘签到★富贵论坛签到★一点万向签到打卡★品赞代理签到★星空代理签到★什么值得买签到★值得买每日抽奖★小米社区签到★ddnsto自动续费七天★爱奇艺签到刷时长★双色球预测（娱乐） |
| [MihoyoBBSTools](https://github.com/Womsxd/MihoyoBBSTools) | 1323 | 可访问 | Womsxd/AutoMihoyoBBS，米游社相关脚本 |
| [AutoTaskScript](https://github.com/sudojia/AutoTaskScript) | 885 | 可访问 | 自动化任务脚本助手，支持青龙面板及 Docker 部署 |
| [CHERWIN_SCRIPTS](https://github.com/CHERWING/CHERWIN_SCRIPTS) | 813 | 可访问 | 永辉生活脚本 \| 顺丰速运脚本 \| 朴朴超市脚本 \| 统一茄皇脚本 \| 海底捞小程序脚本 \|  口味王会员中心小程序脚本 \|  霸王茶姬小程序脚本 \| 奈雪点单小程序脚本 \| 卡夫亨氏新厨艺公众号脚本 \|  韵达快递小程序脚本 \| 中通快递小程序脚本 \| 德邦快递小程序脚本 \|  极兔速递小程序脚本 \| 夸克云盘 \| 网易生活研究社小程序脚本 \| 顾家家居小程序脚本 \| 宽哥之家小程序脚本 \| 特步会员中心小程序脚本 \| 乐事心动社小程序脚本 \| EMS邮惠中心小程序脚本 \| hotwind热风微商城小程序脚本 \| 统一快乐星球小程序脚本 \|老板电器服务微商城小程序 |
| [sign_script](https://github.com/imoki/sign_script) | 808 | 可访问 | WPS 多定时脚本管理框架。适配airscript1.0、airscript2.0 |
| [ArcadiaScriptPublic](https://github.com/zjk2017/ArcadiaScriptPublic) | 524 | 可访问 | 青龙脚本库& Issues接投稿 天瑞地安\|移动云盘\|爱奇艺\|奇瑞\|金山小程序打卡\|雪花\|节卡\|厚工坊\|屈臣氏\|掌上瓯海积分\|上啥班\|永辉\|丽影云街\|杜蕾斯会员中心\|一点万象\|所有女生\|途虎\|沪碳行签到\|钉钉ai签到领算粒\|哪吒汽车\|新战马能量星球\|pp停车\|桃色\|江铃智行\|smart+\|统一不助力\|活力伊利库存\|沪上阿姨\|华润通\|商战\|上海宝山\|叮当快药py310\|品赞代理\|爷爷不泡茶\|青碳行\|鸿星尔克\|起飞线生活小兔快跑\|牙e家\|七彩虹\|交汇点\|喜马拉雅\|申工社\|福田e家\|艾克帮\|贴吧\|天翼网盘\|有赞通用 |
| [ken-iMoutai-Script](https://github.com/AkenClub/ken-iMoutai-Script) | 445 | 可访问 | 青龙脚本，完成 i茅台 预约申购、登录、短信验证码、耐力值和小茅运领取、旅行 等功能 |
| [naro-scripts](https://github.com/NaroisCool/naro-scripts) | 271 | 可访问 | 自用青龙脚本，京东读书签到，王者营地签到，百变小樱机场签到，百姓书房座位监控。 |
