# 现场活动拍摄：支持与隐私页交付

日期：2026-10-16（Asia/Shanghai）。已获本轮必要支持 / 隐私页发布授权，四页已公共可访问。首发源码为 `56f245cfe5fb7c83130a6bd1c475d9a223525807`，后续隐私事实修订为 `953f6fd4e2382ad7b9bd492ce5b66cc97641e9b9`；两次均正常 fast-forward 合并并推送 `main`，GitHub Pages 部署成功，最新公网核验见末节。

## 路由与内容

| 用途 | 已验证公共 URL |
| --- | --- |
| 中文支持 | https://rosehahah.github.io/xianzai-marketing-site/event-photo/ |
| 中文隐私 | https://rosehahah.github.io/xianzai-marketing-site/event-photo/privacy/ |
| 英文支持 | https://rosehahah.github.io/xianzai-marketing-site/event-photo/en/ |
| 英文隐私 | https://rosehahah.github.io/xianzai-marketing-site/event-photo/en/privacy/ |

开发者 / 运营者：韩月。支持及隐私邮箱：`hanr6969@gmail.com`，沿用开发者已有公开支持渠道。未写固定价格或仅中国大陆可用；英文说明 App 当前界面为简体中文，价格取 Apple 实际本地显示。

支持页覆盖首场核销、同场续拍、结束后新增、删除不返还、历史照片、三类已有 SKU 恢复、取消与退款、弱网与系统相册失败、重装 / 换设备、邮件排障信息。

隐私页依据 App 本地草稿及实际客户端核查，分别说明普通相机本地处理、Supabase 目录 / 下载请求、StoreKit 和白名单管理员认证 / 模板发布；未混入苋在的 RevenueCat、友盟、天气、推送行为。还说明 GitHub Pages 的网页连接数据，不将无页面追踪脚本等同于托管方完全无日志。

## 本地验证

- `python3 -m py_compile build.py` 通过。
- 根路径与 GitHub Pages 子路径均完成 `python3 build.py`，现有站点生成路径保留。
- 构建后的 HTML 静态检查：四页及所引用本地样式、目录锚点、语言互链均可解析；无脚本、外部字体、嵌入媒体、表单、占位符或固定价格。
- ego-browser Chromium 视口：四路由 × 320 / 390 / 768 / 1440 共 16 组，`scrollWidth == innerWidth`，目录锚点缺失为 0。
- 实际点击中文支持 → English 成功；中文隐私第 6 节目录点击后，URL 为 `#section-6`，正文目标在视口内。
- 人工查看中文 / 英文手机支持与隐私首屏、中文第 6 节正文、1440 桌面支持截图，文字、间距和换行可读。
- 本地预览及截图中的绿色悬浮球来自用户浏览器扩展；源 HTML 无该元素、脚本或第三方请求。

浏览器证据位于本机 `/tmp/event-photo-support-qa-20261016/`（`browser-checks.json` 与六张截图）。未把截图中的用户浏览器扩展作为网站产物发布。浏览器任务 space 11 验收结束后已关闭；工具提示 Ego Lite 有更新，本次未升级。

## 事实边界与发布核对

首次交付时，客户端核查仅能证明请求载荷、本地处理和 Keychain 行为，未核实 Supabase 日志保留期和地区。后续已通过管理 API 核实本项目位于 AWS `ap-northeast-2`；所属组织 entitlements 中 `log.retention_days` 为 `enabled=true,value=1,unit=days`，`log_drains` 和 `audit_log_drains` 均未启用。新版正文写明本项目服务配置的项目日志保留期为 1 天，并明确这不等于所有服务商安全日志、备份和法定资料在 24 小时内删除。完整访问主体及服务商独立日志仍不能仅凭客户端或 entitlement 响应证明。

管理员发布范围已复核：`TemplatePublishValidator` 在 POST 前拒绝本地 Logo 和 `user:` LUT；请求上传模板文本、排版 / 滤镜设置和内置 / 云端素材引用，后台通过 `auth.uid` 记录 `updated_by` / `published_by`。正文不再笼统称管理员上传本地 Logo。管理员与支持邮件的保留按用途说明，不承诺不存在的自助删除功能或回复时限。

服务商政策核对日期为 2026-10-16：[Supabase 隐私政策](https://supabase.com/privacy)、[Supabase DPA](https://supabase.com/legal/customer-resources/data-processing-addendum)、[GitHub 隐私声明](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)。服务商一般政策不替代具体项目后台配置核实，App Store 隐私标签仍由主任务结合最终二进制及服务配置判断。

主任务仍需检查正文与最终 App 行为及 App Store 隐私标签一致。页面发布仅代表支持网站已上线，不代表 App 已上传、已提交审核或已在 App Store 上线。

## 真实部署与公共验证

- 发布内容 commit：`56f245cfe5fb7c83130a6bd1c475d9a223525807`。
- 合并前网站工作区干净，`main` 与远端均为 `3855b9b6f5c0ac787f5dc67ea877785583cb8c10`；采用 fast-forward，无强制推送或冲突覆盖。
- [GitHub Pages workflow 38904154010](https://github.com/rosehahah/xianzai-marketing-site/actions/runs/38904154010) 的 `build`、`deploy` 均为 `success`，部署 job 完成于 2026-10-16 20:57:35 +08:00。
- 2026-10-16 20:58 +08:00 从公共 HTTPS URL 读取：中英文支持及隐私四页和 `event-photo.css` 全部 HTTP 200；HTML 与 CSS 逐字节匹配本地生产构建。
- 四页 canonical、语言标签、目录锚点、产品页及中英文互链检查通过；生成源 HTML 中脚本数量为 0。
- 原官网 `/zh/`、`/en/`、`/zh/privacy/`、`/en/privacy/` 公共读取均 HTTP 200。
- 逐页字节数与 SHA-256 见 [公共验证 JSON](event-photo-support-public-verification-20261016.json)。

平台构建提示 Node 20 action 兼容升级和 ubuntu-latest 后续版本迁移，未导致本次部署失败；本轮未扩大范围修改既有 workflow。

## 后续事实修订（已部署并公网验证）

本地分支：`codex/event-photo-privacy-facts-20261016`。已完成项目地区、1 天 API / 服务日志配置的实际适用范围，以及管理员上传范围的中英文修订。新版正文明确 IP 推导的大致地区（国家 / 城市）不是 GPS，日志用于提供功能、故障排查和安全运维。保留 1 天不适用于管理员账户和模板数据库，也不推定所有服务商副本在 24 小时内删除。

管理 API / 项目日志核查由 release_integrity 完成：项目恢复为 ACTIVE_HEALTHY，Auth health 及三个 catalog 请求均 HTTP 200。恢复后的实际 `edge_logs` 样本 6 条，IP、方法、路径、User-Agent、响应状态、耗时和 IP 派生国家 / 城市均为 6/6 非空，经纬度为 0/6；仅取字段存在计数，未读取或输出实际 IP 或地区值。另有 2 条 storage 日志及 64 条 Auth 服务启动日志，本轮未进行管理员登录，不能把启动日志当作管理员个人登录样本。组织有效 `log.retention_days` 仍为 1 天，额外 drains 关闭；Auth 的 Postgres 审计写入关闭不等于外部认证事件日志关闭。

主任务已确认本轮正式 Release 构建和 135 项 Release 单元测试通过；检查中 MediaPipe / Clearcut 等相关符号、Google 指标日志字符串及 SDK 框架 / force_load 配置均为 0。由主任务据此授权发布全本机 Vision 的正式政策，最终 iPhoneOS Archive 仍会再次核对。本记录不把 Debug 研发功能描述为公众发行功能，公众产品页不加入研发 SDK 开关或同意流程。

- 修订内容 commit：`953f6fd4e2382ad7b9bd492ce5b66cc97641e9b9`，由 `codex/event-photo-privacy-facts-20261016` fast-forward 合并至 `main` 并推送。
- [GitHub Pages workflow 38909273604](https://github.com/rosehahah/xianzai-marketing-site/actions/runs/38909273604) 的 build / deploy 均成功，平台状态更新于 2026-10-16 21:38:02 +08:00。
- 2026-10-16 21:38 +08:00 公网验证：四个中英文产品页及 CSS 全部 HTTP 200，逐字节匹配本地生产构建；两份隐私正文均包含新 IP 大致地区、1 天范围和管理员发布说明，canonical / 锚点 / 语言及产品页互链通过。
- 原官网四个中英文首页 / 隐私路由仍为 HTTP 200；本次不修改原官网正文。
- 最新逐页字节数、SHA-256 和检查结果见 [隐私事实修订公共验证 JSON](event-photo-privacy-facts-public-verification-20261016.json)，首发验证 JSON 作为历史保留。
