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

GitHub Pages 会在推送到 `main` 后自动构建并发布；输出目录为 `dist`。腾讯 EdgeOne Pages 也可连接此公开仓库的 `main` 分支，本项目不依赖 Node.js，也没有价格页面。

本地预览：`python3 build.py` 后运行 `cd dist && python3 -m http.server 4173`，访问 `http://localhost:4173/`。如需生成线上 sitemap，可在构建时设置 `SITE_URL`；部署到项目子路径时同时设置 `SITE_BASE_PATH`。

网站展示 29 款官方片方和 12 款氛围预设，图库提供分类筛选与展开全部。示例素材均按 AI 生成视觉示例标注。
