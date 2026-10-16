# 现场活动拍摄：支持与隐私页交付

日期：2026-10-16（Asia/Shanghai）。本记录对应网站分支 `codex/event-photo-support-20261016` 的本地交付，尚未推送或公开部署；实际部署由主任务核对后推进。

## 路由与内容

| 用途 | 预期公共 URL |
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

客户端可以核实请求载荷、本地处理和 Keychain 行为，不能证明 Supabase 托管日志的项目实际保留天数、完整访问主体或部署地区。正文披露可能存在的 IP / 路径等连接数据，说明服务约定和实际配置的边界，并提供查询 / 删除请求渠道；不虚构固定期限或“即时删除”。管理员与支持邮件的保留按用途说明，不承诺不存在的自助删除功能或回复时限。

服务商政策核对日期为 2026-10-16：[Supabase 隐私政策](https://supabase.com/privacy)、[Supabase DPA](https://supabase.com/legal/customer-resources/data-processing-addendum)、[GitHub 隐私声明](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)。服务商一般政策不替代具体项目后台配置核实，App Store 隐私标签仍由主任务结合最终二进制及服务配置判断。

主任务需要检查正文与最终 App 行为一致，再合并 / 推送本网站 `main`，等待 GitHub Pages 部署成功，并从公共 URL 重新读取四页。公共可用性验证之前，不应把预期 URL 写成“已上线”或将页面部署当作 App 已提交审核。
