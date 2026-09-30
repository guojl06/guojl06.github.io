// ============================================================
//  Typst 简历模板 · 双栏紧凑风格
//  编译: typst compile resume-template.typ
// ============================================================

#let sidebar-w   = 6.3cm
#let sidebar-bg  = rgb("#eef2f7")
#let c-primary   = rgb("#1f3a5f")   // 深蓝 主色
#let c-secondary = rgb("#4a6fa5")   // 中蓝 辅助
#let c-accent    = rgb("#8b5a2b")   // 暖棕 日期
#let c-muted     = rgb("#6b6b6b")   // 灰 次要文字
#let c-rule      = rgb("#c9d3df")   // 浅蓝 分隔线

#set page(
  paper: "a4",
  margin: 0pt,
  // 左栏背景色块（每页重绘）
  background: {
    place(top + left, rect(width: sidebar-w, height: 100%, fill: sidebar-bg, stroke: none))
  },
)

#set text(
  font: ("New Computer Modern", "PingFang SC"),
  size: 9.5pt,
  lang: "zh",
  fill: rgb("#222222"),
)

#set par(leading: 0.72em, spacing: 0.55em, justify: false)
#set list(indent: 0pt, body-indent: 0.4em, spacing: 0.4em)

// ---------- 左栏组件 ----------
#let side-title(title) = {
  v(0.3em)
  block[
    #text(size: 11pt, weight: "bold", fill: c-primary, tracking: 0.4pt)[#title]
  ]
  v(-0.5em)
  line(length: 100%, stroke: 0.5pt + c-rule)
  v(0.2em)
}

#let kv-line(label, content-text) = {
  block(width: 100%)[
    #grid(
      columns: (1.3cm, 1fr),
      column-gutter: 0.2cm,
      text(size: 8.8pt, weight: "bold", fill: c-secondary)[#label],
      text(size: 8.8pt, fill: rgb("#333"))[#content-text],
    )
  ]
  v(0.12em)
}

// ---------- 右栏组件 ----------
#let main-title(title) = {
  v(0.2em)
  block[
    #text(size: 12.5pt, weight: "bold", fill: c-primary, tracking: 0.4pt)[#title]
  ]
  v(-0.5em)
  line(length: 100%, stroke: 0.6pt + c-secondary)
  v(0.2em)
}

// 经历条目：标题左对齐，日期右对齐到同一行，正文可选
#let job(date, title, ..body) = {
  let bc = body.pos()
  block(width: 100%)[
    #grid(
      columns: (1fr, auto),
      column-gutter: 0.4cm,
      text(weight: "bold", size: 10pt, fill: rgb("#1a1a1a"))[#title],
      text(size: 8.8pt, fill: c-accent)[#date],
    )
    #if bc.len() > 0 [
      #v(0.1em)
      #text(size: 9.3pt)[#bc.first()]
    ]
  ]
  v(0.4em)
}

// ============================================================
//  正文
// ============================================================
#grid(
  columns: (sidebar-w, 1fr),
  gutter: 0pt,

  // ===================== 左栏 =====================
  pad(left: 0.75cm, right: 0.7cm, top: 0.85cm, bottom: 0.85cm)[
    // —— 照片占位 ——
    // 替换为你的证件照：把下面整个 #block(...) 换成
    //   #image("photo.jpg", width: 3.8cm, height: 5cm)
    #align(center)[
      #block(
        width: 3.8cm, height: 5cm,
        fill: rgb("#d9dee6"),
        stroke: 2pt + white,
        radius: 4pt,
        align(center + horizon)[
          #text(9pt, c-muted)[照片]
          #v(0.2em)
          #text(7.5pt, c-muted)[image("photo.jpg")]
        ],
      )
    ]
    #v(0.5em)

    #side-title[联系方式]
    #kv-line[电话][010-1234-5678]
    #kv-line[邮箱][zhangsan\@email.com]
    #kv-line[主页][zhangsan.dev]
    #kv-line[地址][北京市海淀区]

    #side-title[技能]
    #kv-line[编程][Python · C++ · Rust · SQL]
    #kv-line[框架][PyTorch · Transformers · Ray]
    #kv-line[工具][Git · Linux · LaTeX · Typst]

    #side-title[语言]
    #kv-line[中文][母语]
    #kv-line[英语][托福 108 / GRE 328]
    #kv-line[日语][N2]

    #side-title[奖项]
    - ACM-ICPC 亚洲赛 银奖（2024）
    - 数学建模 国一（2023）
    - NOI 银牌（2022）
    - 国家奖学金（2024）

    #side-title[兴趣]
    马拉松 · 古典吉他 · 开源社区
  ],

  // ===================== 右栏 =====================
  pad(left: 0.7cm, right: 0.9cm, top: 0.85cm, bottom: 0.85cm)[
    // 姓名 + 标语
    #block[
      #text(size: 26pt, weight: "bold", fill: c-primary, tracking: 3pt)[张 三]
      #v(-0.1em)
      #text(size: 11pt, fill: c-muted)[计算机科学 · 机器学习方向]
    ]
    #v(0.4em)

    #main-title[个人简介]
    清华大学计算机系本科在读，专注自然语言处理与大语言模型。GPA 3.92 / 4.00，专业排名 2 / 156，具备扎实的算法基础与一线实验室科研经验，对高效推理与可信 AI 有深入研究。

    #main-title[教育背景]
    #job[2022.09 – 2026.06][清华大学 · 计算机科学与技术（工学学士）][
      GPA: 3.92 / 4.00（排名 2 / 156） · 国家奖学金（2024）\
      核心课程：算法（97）、机器学习（95）、操作系统（94）、概率论（98）
    ]

    #main-title[科研经历]
    #job[2024.07 – 至今][清华大学 NLP 实验室 · 本科生研究员（指导：李教授）][
      - 提出基于稀疏注意力的长文本上下文压缩方法，降低推理延迟 38%；
      - 搭建数据处理流水线与微调框架，论文投递 ACL 2026（一作）。
    ]
    #job[2023.09 – 2024.06][可信 AI 课题组 · 学生助理][
      - 复现并扩展对抗样本生成算法，覆盖 5 个基准数据集；
      - 协助撰写综述章节，收录于实验室年度报告。
    ]

    #main-title[论文发表]
    #job[2026][Zhang, Wang & Li. *Efficient Long-Context Inference via Sparse Context Compression.* ACL 2026（在投）.]
    #job[2025][Wang, Zhang, et al. *A Unified Framework for Robust Representation Learning.* NeurIPS 2025 Workshop.]

    #main-title[实习经历]
    #job[2025.06 – 2025.09][字节跳动 AI Lab · 算法实习生][
      - 参与搜索相关性模型迭代，离线指标提升 4.2%；
      - 搭建自动化评测平台，评估周期由 3 天缩短至半天，获「优秀实习生」。
    ]
  ],
)
