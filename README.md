# 苋在营销网站

中英文静态多页面营销网站。根路径会根据用户上一次选择或浏览器语言进入对应版本：

- 中文首页：`/zh/`
- English home: `/en/`
- 中文法律页面：`/zh/terms/`、`/zh/privacy/`
- English legal pages: `/en/terms/`, `/en/privacy/`

原有 `/terms/`、`/privacy/` 和 `.html` 地址继续提供中文版，避免 App 内及外部旧链接失效。首页源文件为 `index.html` 和 `index.en.html`，法律正文源文件位于 `content/`。

## 现场活动拍摄产品支持

独立产品“现场活动拍摄”的支持页和隐私页使用单独正文与样式，不复用苋在 App 的服务说明：

- 中文支持：`/event-photo/`；中文隐私：`/event-photo/privacy/`
- English support: `/event-photo/en/`; privacy: `/event-photo/en/privacy/`
- 正文：`content/event-photo-*.md`；样式：`event-photo.css`；由同一 `build.py` 生成。

四页均为纯静态内容，无页面脚本、追踪 SDK、第三方字体、账号或站外购买入口。保留普通拍摄、网络素材、Apple 购买和授权管理员发布的不同数据边界。英文页面说明当前 App 界面为简体中文，价格按 Apple 当地实际显示。部署与 App Store 审核是独立状态；页面的本地验收见 [支持页交付记录](docs/event-photo-support-20261016.md)。

## GitHub Pages

公开地址：`https://rosehahah.github.io/xianzai-marketing-site/`。仓库使用 Actions 自动构建，并生成语言路由、`hreflang`、canonical、`robots.txt` 和 `sitemap.xml`。

## 腾讯 EdgeOne Pages 部署

- 构建命令：`pip install -r requirements.txt && python3 build.py`
- 输出目录：`dist`
- 入口页面：`dist/index.html`

GitHub Pages 会在推送到 `main` 后自动构建并发布；输出目录为 `dist`，该目录不再提交到 Git。腾讯 EdgeOne Pages 也可连接此公开仓库的 `main` 分支，本项目不依赖 Node.js，也没有价格页面。

本地预览：`python3 build.py` 后运行 `cd dist && python3 -m http.server 4173`，访问 `http://localhost:4173/`。如需生成线上 sitemap，可在构建时设置 `SITE_URL`；部署到项目子路径时同时设置 `SITE_BASE_PATH`。

网站展示 29 款官方片方和 12 款氛围预设，图库提供分类筛选与展开全部。示例素材均按 AI 生成视觉示例标注。

## 双语沉浸式首页视频

首页打开即展示 100svh 的全屏视频舞台，导航和下载入口浮在画面上。视频内的标题承担首屏主文案，不再在视频上方重复排版。常见桌面与手机比例铺满首屏，其他比例完整保留构图；中文与英文分别使用当前页面语言的素材。

- 首页横版使用 `assets/video/hero-zh-web.mp4` / `hero-en-web.mp4`，2560 × 1098，约 8 秒，每版约 3.76 MB；竖版使用 `hero-zh-portrait-web.mp4` / `hero-en-portrait-web.mp4`，1080 × 1920，每版约 3.05–3.08 MB。保持 30 帧、动画时间线和配乐，采用 H.264 / CRF 22、AAC 128 kbps 与 faststart。
- 保留横版 `hero-zh.mp4` / `hero-en.mp4`（3840 × 1646，约 26.8 MB）和竖版 `hero-zh-portrait.mp4` / `hero-en-portrait.mp4`（1620 × 2880，约 17.8 MB）高清原片，只在用户展开观看时加载。
- 屏幕宽高比不超过 4:5 时选择竖屏版，其他比例选择横屏版；旋转屏幕时同步切换视频与封面，不预加载另一种语言或另一方向的影片。首屏由单一 `picture` 封面层选择横竖 WebP（约 139–150 KB），视频真正显示首帧后再淡出封面，避免重复请求横竖封面。
- 默认静音循环播放，点击声音按钮后开启配乐；浏览器仍拦截自动播放时显示明确播放入口。进入可视区域后加载播放，滚出画面或切到其他标签页时暂停。手动暂停后不会因滚动自动恢复。
- 减少动态效果或节省流量时默认展示封面，仍可手动播放。提供中英文播放、声音与放大观看控件；弹窗可关闭或按 Escape 退出。
- 首屏图标使用 256 × 256 WebP（约 10 KB），保留原 PNG。图库和页面后续图片到视口附近 250px 时才挂载图片源，避免浏览器原生懒加载提前取回多张高清 PNG 并抢占视频带宽；关闭 JavaScript 时保留静态原图。
- 示例画面标注为 AI 生成。无 JavaScript 时提供原视频文件入口。

横版素材更新：在本站目录运行 `sh scripts/prepare-hero-media.sh`，可传入其他原片目录，默认读取 `../remotion-xiannow/out/`。生成需要 ffmpeg；横版使用码流复制，仅整理网页播放所需的文件结构，不再降低分辨率或重新压缩画面。

竖版素材更新：运行 `python3 scripts/render-portrait-hero.py`，需要兄弟目录 `../remotion-xiannow/` 的原动画源码、素材、已安装的 Remotion 依赖，以及本机 Chrome。脚本在临时目录重排场景，保留原动画源码和原片。普通网站构建与部署直接使用已生成的素材，不需要安装视频工具。

网页素材更新：准备好上述横竖原片与 JPEG 封面后，运行 `sh scripts/optimize-hero-media.sh`。需要带 libx264 的 ffmpeg，以及安装 Pillow 并支持 WebP 的 Python 3；可用 `HERO_PYTHON` 指定 Python 路径。脚本生成四版网页视频与四张 WebP 封面，不覆盖原片或原 JPEG；全部编码成功后才更新网页衍生素材。可选传入输入和输出目录，或通过 `HERO_THREADS` / `HERO_CRF` / `HERO_POSTER_QUALITY` 调整参数。修改素材时必须复核小字、人物边缘、暗部渐变与首帧过渡。


## 发布与存储

官网使用独立版本标签（首次发布为 `v1.0.0`），不对应 iOS / TestFlight 的产品版本。版本变化见 [CHANGELOG.md](CHANGELOG.md)，GitHub Release 仅记录说明与验证，不重复上传一份站点压缩包或视频。

`assets/` 保留页面实际使用的高清素材；`dist/` 由 `build.py` / GitHub Actions 生成并由 Git 忽略。完成预览后可删除 `dist/` 和旧 `site-dist.tar.gz`，下次预览时重新构建即可。素材原片与原动画源码保留在兄弟目录 `remotion-xiannow/`。
