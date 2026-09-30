# sTBook

我的课程笔记库，同时作为 [个人网站](https://guojl06.github.io) 笔记/知识库模块的数据源（wiki 风格，可在线浏览 md / typst / pdf / 图片 / 数据文件）。

## 结构

- 课程文件夹：英文 slug 命名，展示名见 [`wiki.yml`](wiki.yml)
  （`dsa` 数据结构与算法 · `oop` 面向对象 · `discrete-math` 离散数学（二）· `physics` 大学物理 · `ai4s` 小学期 …）
- `Assets/`、`module/`：共享图片与 Typst 工具模块，笔记内以相对路径引用，**勿改名**
- `templates/`：简历等模板；`tools/`：OJ→Markdown 等脚本；`misc/`：个人杂项

## 网站同步

把笔记 push 到本仓库后，网站仓库的 GitHub Action 会自动拉取本仓库并重建
[guojl06.github.io/notes](https://guojl06.github.io/notes/)，无需手动同步。
