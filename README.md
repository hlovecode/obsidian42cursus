### This is my personal notes on the 42 cursus projects using Obsidian.
### Ce sont mes notes personnelles sur les projets du 42 cursus avec Obsidian.

# 42 Common Core 中文学习笔记

这是一个使用 Obsidian 管理的 42 Common Core 中文学习笔记仓库。

## 工作流程

本仓库使用以下自动化流程管理和发布笔记：

1. 使用 Obsidian 编写和编辑 Markdown 笔记。
2. Obsidian Git 插件自动提交并推送修改到 GitHub 的 `main` 分支。
3. GitHub Actions 检测到笔记更新后，自动执行构建流程。
4. `scripts/build_site.py` 将原始 Markdown 笔记处理并生成到 `docs/`。
5. MkDocs Material 将 `docs/` 构建为静态网站。
6. GitHub Pages 自动部署生成的网站。

## 自动备份

Obsidian Git 插件配置为每 5 分钟自动提交和推送。

自动备份正常运行需要满足以下条件：

- Obsidian 正在运行。
- Obsidian Git 插件已启用。
- 本地 Git 仓库及 GitHub 身份验证配置正常。
- 电脑能够连接互联网。

如果 Obsidian 没有运行、电脑关机或自动推送尚未完成，GitHub 上的笔记就不会及时更新。

## 本地预览网站

如果需要在本地构建和预览网站，可以在仓库根目录执行：

```
python3 -m venv .venv-pages
source .venv-pages/bin/activate
python -m pip install mkdocs-material
python scripts/build_site.py
python -m mkdocs serve

```
