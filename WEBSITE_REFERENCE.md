# Personal Website Reference

这份文档用于后续开发者或新的 AI 对话快速理解、查找和修改当前网站。

## 项目概览

- 项目类型：单页个人网站 landing page。
- 入口文件：`index.html`。
- 页面结构：React app 挂载到 `#root`。
- 实现方式：CDN-only，无构建工具，无 npm 安装流程。
- 当前本地预览地址：`http://127.0.0.1:4173/`。

启动本地静态服务：

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

## 技术栈

所有依赖都在 `index.html` 里通过 CDN 引入：

- Tailwind CDN：`https://cdn.tailwindcss.com`
- React 18.3.1 UMD
- ReactDOM 18.3.1 UMD
- Babel standalone 7.29.0，用于浏览器内转换 `type="text/babel"`
- Framer Motion 11.11.17 UMD
- hls.js 1.5.20，用于播放 Mux 的 `.m3u8` 视频流

注意：这是原型/展示型实现。若后续要生产化，建议迁移到 Vite/Next.js，并把 Babel 浏览器转换改成构建期转换。

## 字体与视觉系统

Google Fonts：

- `Instrument Serif`：艺术字标题，当前 Hero 主标题使用它，且为 italic。
- `Barlow`：正文、导航、按钮。

Tailwind 扩展：

```js
font-heading: ["Instrument Serif", "serif"]
font-body: ["Barlow", "sans-serif"]
borderRadius.DEFAULT: "9999px"
```

重要 CSS 工具类：

- `.liquid-glass`：轻量液态玻璃效果，用于导航、badge、卡片。
- `.liquid-glass-strong`：更强 blur 的玻璃效果，用于强调按钮。当前 Hero CTA 已移除，但类还保留。
- `.video-surface`：视频初始 opacity 为 `0`，由 JS 淡入。

## 页面结构

`App` 只渲染两个 section：

```jsx
<main>
  <Hero />
  <Capabilities />
</main>
```

### Hero

位置：`function Hero()`

主要内容：

- 背景视频：Mux HLS 视频。
- 固定顶部导航：`<Navbar />`
- Hero 主标题：AI 产品方向文案。
- 简介段落。
- 新闻 badge：位于页面底部偏上，整个页面居中。

当前 Hero 已移除：

- `Start Your Voyage`
- `View Liftoff`
- 两个统计卡片
- 底部合作伙伴名称行

### Capabilities

位置：`function Capabilities()`

仍保留旧的第二屏能力展示区：

- 背景视频：CloudFront `.mp4`
- 标题：`Production evolved`
- 三张卡片：`AI Scenery`、`Batch Production`、`Smart Lighting`

如果未来要改成个人主页项目/经历区，优先从 `Capabilities()` 的 `cards` 数组和标题文案开始改。

## 导航

位置：`function Navbar()`

当前导航数组：

```js
const links = ["Home", "About", "Projects", "Resume", "WeChat"];
```

Logo：

```jsx
<span className="-translate-y-0.5">g</span>
```

右侧按钮仍为：

```text
Claim a Spot
```

如果要更贴近个人主页，可以改为 `Contact`、`Let's Talk`、`Book a Call` 等。

## 视频机制

位置：`function FadingVideo({ src, className, style, seamlessLoop = false })`

职责：

- 渲染 `<video autoplay muted playsInline preload="auto">`
- 首次 `loadeddata` 后用 `requestAnimationFrame` 淡入到 opacity `1`
- 对普通 `.mp4` 视频，默认在结束前淡出并手动重播
- 对 `seamlessLoop={true}` 的视频，使用原生 `loop`，不做结束前淡出，避免黑屏
- 如果 `src` 是 `.m3u8` 并且浏览器支持 hls.js，则通过 hls.js 播放

Hero 当前视频：

```jsx
<FadingVideo
  src="https://stream.mux.com/O9KR2ldtszUeixlGSG01vh164FE7WxayyiOuKPGNKJMU.m3u8"
  className="absolute inset-0 z-0 h-full w-full object-cover object-center"
  seamlessLoop
/>
```

关键点：

- Hero 视频是无缝循环素材，所以必须保留 `seamlessLoop`。
- 不要再加结束前 fade-out，否则循环时会黑屏。
- 当前背景用 `object-cover object-center`。如果想显示更多背景画面，可以考虑改成 `object-contain`，但会出现黑边；当前做法优先保持满屏。

Capabilities 当前视频：

```jsx
<FadingVideo
  src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260418_094631_d30ab262-45ee-4b7d-99f3-5d5848c8ef13.mp4"
  className="absolute inset-0 z-0 h-full w-full object-cover"
/>
```

## Hero 当前文案

主标题：

```text
Building useful AI products with LLM, AI Agent and prompt design
Exploring the underlying principles of artificial intelligence
```

简介：

```text
I’m an AI enthusiast skilled in AI application development, familiar with LLM fundamentals, AI agent logic and prompt engineering. Aiming to create real-world, usable artificial intelligence solutions.
```

新闻 badge：

```text
New
Maiden Crewed Voyage to Mars Arrives 2026
```

这个 badge 目前仍是旧模板内容，后续建议改成更贴合个人主页的内容，例如：

- `Now building AI-native products`
- `Open to AI product collaborations`
- `LLM / Agent / Prompt Design`

## Hero 布局关键点

Hero section：

```jsx
<section id="hero" className="relative flex min-h-screen overflow-hidden bg-black">
```

主内容容器：

```jsx
<div className="flex flex-1 items-start justify-start px-8 pt-40 text-left md:px-16 lg:px-20 lg:pt-48">
```

主标题样式：

```jsx
className="hero-title max-w-[36rem] text-left font-heading text-5xl italic leading-[1.02] tracking-[-2px] text-white md:text-[3.4rem] lg:text-[3.85rem]"
```

副标题样式：

```jsx
className="mt-6 block max-w-[31rem] text-4xl leading-[1.02] tracking-[-1.5px] text-white/90 md:text-[2.65rem] lg:text-[2.8rem]"
```

新闻 badge 位置：

```jsx
<div className="absolute left-1/2 bottom-[6vh] z-20 -translate-x-1/2">
```

注意：Framer Motion 会写入 transform。需要页面居中的元素如果也使用 motion，最好像当前这样外层负责定位和 `translate-x`，内层负责动画，避免 transform 覆盖。

## 常见修改位置

### 修改导航文字

找：

```js
const links = ["Home", "About", "Projects", "Resume", "WeChat"];
```

### 修改 Logo 字母

找：

```jsx
<span className="-translate-y-0.5">g</span>
```

### 修改 Hero 主标题

找：

```jsx
<motion.h1 className="hero-title ...">
```

### 修改 Hero 简介

找包含以下文字的 `<motion.p>`：

```text
I’m an AI enthusiast...
```

### 修改 Hero badge

找：

```text
Maiden Crewed Voyage to Mars Arrives 2026
```

### 修改 Hero 背景视频

找 Hero 内第一个 `<FadingVideo />`。

如果是 Mux 播放器 URL：

```text
https://player.mux.com/PLAYBACK_ID
```

通常需要改成 HLS：

```text
https://stream.mux.com/PLAYBACK_ID.m3u8
```

并保持：

```jsx
seamlessLoop
```

### 修改第二屏卡片

找：

```js
const cards = [
  ...
]
```

## 当前已知注意事项

1. `index.html` 里有少量中文环境导致的编码显示痕迹，例如 `I鈥檓`。如果编辑器以 UTF-8 正确打开，建议把它修成 `I'm` 或 `I’m`。
2. 当前页面依赖外部 CDN 和远程视频，离线时无法完整展示。
3. Tailwind CDN 和浏览器 Babel 会有开发警告，这是预期行为。
4. Hero 背景视频是 hls.js 接 Mux HLS；如果 CDN 加载失败，背景视频可能不播放。
5. 当前 second section 仍保留原“Capabilities / Production evolved”的视觉模板，后续可改成项目展示或履历模块。

## 推荐给新 AI 对话的提示

如果后续新开 AI 对话，可以直接复制下面这段：

```text
这是我的个人网站项目。请先阅读 WEBSITE_REFERENCE.md 和 index.html。
项目是 CDN-only 单页 React app，入口是 index.html。
请保持现有 liquid-glass 视觉系统、Instrument Serif 艺术字标题、Hero Mux HLS 背景视频无缝循环。
除非我明确要求，不要整体重构为 Vite/Next，也不要删除现有视频机制。
修改时请优先定位 Hero、Navbar、Capabilities 这些函数。
```

