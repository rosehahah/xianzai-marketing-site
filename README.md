# 苋在营销网站

静态多页面营销网站：首页位于 `index.html`；《用户协议》与《隐私政策》分别位于 `/terms/` 和 `/privacy/`，并提供 `.html` 备用路径。法律正文的源文件位于 `content/`。

## GitHub Pages

公开地址：`https://rosehahah.github.io/xianzai-marketing-site/`。仓库使用 Actions 自动构建，法律页面地址分别为 `/terms/` 和 `/privacy/`。

## 腾讯 EdgeOne Pages 部署

- 构建命令：`pip install -r requirements.txt && python3 build.py`
- 输出目录：`dist`
- 入口页面：`dist/index.html`

GitHub Pages 会在推送到 `main` 后自动构建并发布；输出目录为 `dist`。腾讯 EdgeOne Pages 也可连接此公开仓库的 `main` 分支，本项目不依赖 Node.js，也没有价格页面。

本地预览：`python3 build.py` 后运行 `cd dist && python3 -m http.server 4173`，访问 `http://localhost:4173/`。

网站展示 29 款官方片方和 12 款氛围预设，图库提供分类筛选与展开全部。示例素材均按 AI 生成视觉示例标注。
