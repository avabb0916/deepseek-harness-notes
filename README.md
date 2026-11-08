# 一切皆插件 · 我的 DeepSeek Harness 学习笔记

> 这不是教程，是我从 0 到 1 学 DeepSeek Harness（`dsh`）的笔记。**我先学会，才发出来。**
> 24 篇 ｜ 基于 `dsh 0.2.2-rc.1`（2026-11-04）｜ 更新于 2026-11-08

## 这是什么

- 一个普通使用者拆开 DeepSeek Harness 的学习记录：它是什么、怎么跑、为什么这样设计、我能改哪里。
- 每篇都有：我带着的问题、读之前我以为、读完的答案、**读完能答的三个问题**（答不出就不发）、术语小抄、我还没搞懂。
- 不是官方文档的翻译，也不是"教你用"的教程；是一个还在学的人留下的路标。

## 在线阅读

GitHub Pages 部署后：`https://<你的用户名>.github.io/<仓库名>/`

本地看：直接双击 `docs/index.html`（全部自包含，离线可读）。

## 内容

| 部分 | 篇目 |
|---|---|
| 起点 | 01 我为什么搬进来 · 02 没有核心的运行时 · 03 前世今生 |
| 上手 | 04 三种装法 · 05 会话与目录 · 06 模型与成本 · 07 工具系统 · 08 上下文 |
| 设计原理 | 09 一切皆插件 · 10 接缝 · 11 事件三分 · 12 一次 turn · 13 系统提示 |
| 底层架构 | 14 profile 与 bundle · 15 两半结构 · 16 会话存储 · 17 安全 · 18 多 agent |
| 建设者 | 19 写第一个插件 · 20 插件界面 · 21 研究台全过程 · 22 什么该插件化 |
| 判断 | 23 三种 Agent 形态 · 24 一年后回看 |

另有 [7 天学习 + 14 天发布计划](docs/plan.html) 与 19 张手绘配图（`docs/images/`）。

## 部署到 GitHub Pages

```bash
# 在 GitHub 新建一个公开仓库（不要勾选初始化 README）
git init
git add .
git commit -m "DSH 学习笔记 24 篇 v1.0"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

然后仓库 **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / 文件夹: `/docs` → Save**。
一两分钟后 `https://<用户名>.github.io/<仓库名>/` 就能打开。

## 重新构建

```bash
python3 build.py
```

它会从 `../dsh-series/03-文章/` 重新生成 `docs/`（24 章 + 首页 + 学习计划页 + 配图）。

## 目录

```
dsh-book/
├── README.md
├── build.py            # 构建脚本（读取 dsh-series 的 md → docs/）
└── docs/               # GitHub Pages 站点（已构建）
    ├── index.html      # 封面 + 目录 + 配图墙
    ├── plan.html       # 7 天学习 + 14 天发布
    ├── ch01.html … ch24.html
    ├── images/         # 19 张 PNG
    └── .nojekyll
```

## 说明

- 基于 **developer preview**：官方明确会有破坏性变更；文中所有结论都标了版本与时间。
- 非官方资料；引用请注明出处。发现错误欢迎提 Issue。
- 文字与配图：个人学习笔记，转载注明「大鱼出海 · 一切皆插件」即可。
