# 苋在营销网站

静态多页面网站：首页位于 `index.html`；《用户协议》与《隐私政策》分别位于 `/terms/` 和 `/privacy/`，提供 `.html` 备用路径。法律正文的唯一源文件在 `content/`，运行 `python3 build.py` 后重新渲染到 `dist/`。

预览：`cd dist && python3 -m http.server 4173`，访问 `http://localhost:4173/`。

网站展示 29 款官方片方和 12 款氛围预设，图库提供分类筛选与展开全部。示例素材均按 AI 生成视觉示例标注，不展示价格。
