# 苋在营销网站

中英文静态多页面营销网站。根路径会根据用户上一次选择或浏览器语言进入对应版本：

- 中文首页：`/zh/`
- English home: `/en/`
- 中文法律页面：`/zh/terms/`、`/zh/privacy/`
- English legal pages: `/en/terms/`, `/en/privacy/`

原有 `/terms/`、`/privacy/` 和 `.html` 地址继续提供中文版，避免 App 内及外部旧链接失效。首页源文件为 `index.html` 和 `index.en.html`，法律正文源文件位于 `content/`。

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

- 横屏素材：`assets/video/hero-zh.mp4` / `hero-en.mp4`，3840 × 1646，约 8 秒，每版约 26.8 MB，保留原片画面码流。
- 竖屏素材：`assets/video/hero-zh-portrait.mp4` / `hero-en-portrait.mp4`，1620 × 2880，约 8 秒，采用 PNG 中间帧与 CRF 16 高画质编码。复用原动画素材、配乐与时间线，重新安排手机、模板、角色与标题。
- 屏幕宽高比不超过 4:5 时选择竖屏版，其他比例选择横屏版；旋转屏幕时同步切换视频与封面，不预加载另一种语言。
- 默认开启声音循环播放；浏览器拦截有声自动播放时保留声音设置，显示「播放并开启声音 / Play with sound」入口，由用户点击后播放。进入可视区域后加载播放，滚出画面或切到其他标签页时暂停。手动暂停后不会因滚动自动恢复。
- 减少动态效果或节省流量时默认展示封面，仍可手动播放。提供中英文播放、声音与放大观看控件；弹窗可关闭或按 Escape 退出。
- 示例画面标注为 AI 生成。无 JavaScript 时提供原视频文件入口。

横版素材更新：在本站目录运行 `sh scripts/prepare-hero-media.sh`，可传入其他原片目录，默认读取 `../remotion-xiannow/out/`。生成需要 ffmpeg；横版使用码流复制，仅整理网页播放所需的文件结构，不再降低分辨率或重新压缩画面。

竖版素材更新：运行 `python3 scripts/render-portrait-hero.py`，需要兄弟目录 `../remotion-xiannow/` 的原动画源码、素材、已安装的 Remotion 依赖，以及本机 Chrome。脚本在临时目录重排场景，保留原动画源码和原片。普通网站构建与部署直接使用已生成的素材，不需要安装视频工具。


## 发布与存储

官网使用独立版本标签（首次发布为 `v1.0.0`），不对应 iOS / TestFlight 的产品版本。版本变化见 [CHANGELOG.md](CHANGELOG.md)，GitHub Release 仅记录说明与验证，不重复上传一份站点压缩包或视频。

`assets/` 保留页面实际使用的高清素材；`dist/` 由 `build.py` / GitHub Actions 生成并由 Git 忽略。完成预览后可删除 `dist/` 和旧 `site-dist.tar.gz`，下次预览时重新构建即可。素材原片与原动画源码保留在兄弟目录 `remotion-xiannow/`。
