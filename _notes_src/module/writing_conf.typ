// conf.typ ── 文章格式配置
// 依据《文章格式及样例》整理
// 纸张：A4；页边距：上下 2.54cm，左右 3.18cm
// 字体回退顺序：macOS → Windows → Linux (Noto)

// ─── 字体别名 ──────────────────────────────────────────────────
#let font-song  = ("Times New Roman", "Songti SC", "SimSun",    "Noto Serif CJK SC")
#let font-hei   = ("Arial",           "Heiti SC",  "SimHei",    "Noto Sans CJK SC")
#let font-kai   = ("Times New Roman", "Kaiti SC",  "STKaiti",   "FZKai-Z03")

// ─── 字号 ──────────────────────────────────────────────────────
#let size-4     = 14pt    // 四号
#let size-5     = 10.5pt  // 五号
#let size-xs    = 9pt     // 小五号

// 1.5 倍行距对应的 leading（Typst leading = 行距 − 字号）
#let leading-15x(sz) = sz * 0.5


// ══════════════════════════════════════════════════════════════
//  主模板函数
// ══════════════════════════════════════════════════════════════
#let article(
  title:      none,   // 标题（字符串或 content）
  author:     none,   // 姓名
  student-id: none,   // 学号
  email:      none,   // 邮箱
  body,
) = {

  // ── 页面 ──────────────────────────────────────────────────
  set page(
    paper:  "a4",
    margin: (top: 2.54cm, bottom: 2.54cm, left: 3.18cm, right: 3.18cm),
  )

  // 脚注间距：分隔线 + 条目间距
  set footnote.entry(
    separator: line(length: 30%, stroke: 0.5pt),
    gap:       0.5em,
    clearance: 1em,
    indent:    0em,
  )

  // ── 正文默认样式：宋体五号，1.5倍行距，首行缩进2字符 ──
  set text(font: font-song, size: size-5, lang: "zh")

  set par(
    leading:           leading-15x(size-5),
    first-line-indent: 2em,
    justify:           false,
  )

  // ── 脚注字体 ─────────────────────────────────────────────
  show footnote.entry: it => {
    set text(font: font-song, size: size-xs)
    set par(leading: 0pt, first-line-indent: 0em)
    it
  }

  // ── 标题层级（节标题：黑体五号居中，无首行缩进）──────
  set heading(numbering: none)
  show heading: it => {
    set text(font: font-hei, size: size-5, weight: "regular")
    set par(first-line-indent: 0em, leading: leading-15x(size-5))
    align(center)[#it.body]
    v(0.3em, weak: true)
  }

  // ── 表格默认样式 ──────────────────────────────────────
  // 三线表：仅保留上框线、表头下分割线、下框线
  set table(
    stroke: none,
    align:  center,
    inset:  (x: 0.5em, y: 0.4em),
  )
  show table: it => {
    set text(font: font-song, size: size-xs)
    set par(leading: leading-15x(size-xs), first-line-indent: 0em)
    it
  }
  // 三线表的 stroke 由调用处用 table.hline() 控制（见下方 tbl 辅助函数）

  // ── 图表题注 ──────────────────────────────────────────
  set figure(gap: 0.6em)
  show figure.caption: it => {
    set text(font: font-song, size: size-5)
    set par(first-line-indent: 0em, leading: leading-15x(size-5))
    align(center)[#it]
  }


  // ══════════════════════════════════════════════════════
  //  文首信息区
  // ══════════════════════════════════════════════════════
  if title != none {
    // 标题：黑体四号居中，1.5倍行距
    set par(first-line-indent: 0em, leading: leading-15x(size-4))
    align(center, text(font: font-hei, size: size-4, weight: "bold")[#title])
    v(0.6em, weak: true)
  }

  if author != none or student-id != none or email != none {
    // 作者行：楷体五号居中，1.5倍行距
    let parts = ()
    if author     != none { parts.push(author)     }
    if student-id != none { parts.push(student-id) }
    if email      != none { parts.push(email)       }
    set par(first-line-indent: 0em, leading: leading-15x(size-5))
    align(center, text(font: font-kai, size: size-5)[#parts.join("　")])
    v(1em, weak: true)
  }

  body
}


// ══════════════════════════════════════════════════════════════
//  辅助函数
// ══════════════════════════════════════════════════════════════

// 三线表包装器
// 用法：#tbl(caption: [表1 表题], columns: (…), …)
#let tbl(caption: none, note: none, columns: (), ..cells) = {
  let n = columns.len()
  figure(
    caption: caption,
    kind:    table,
    supplement: [表],
    {
      table(
        columns: columns,
        // 上框线
        table.hline(stroke: 0.75pt),
        // 表头行（第1行）后加分割线
        ..cells,
      )
      // 下框线由 table 内最后一行的 hline 实现；
      // 实践中建议在 cells 末尾手动追加 table.hline(stroke: 0.75pt)
    }
  )
  if note != none {
    par(first-line-indent: 2em)[
      #text(font: font-song, size: size-5)[#note]
    ]
  }
}

// 带题注的图片
// 用法：#img(caption: [图1 图题], image("foo.jpg"))
#let img(caption: none, body) = {
  figure(
    caption: caption,
    kind:    image,
    supplement: [图],
    body,
  )
}

// 表注（独立使用时）
#let table-note(body) = {
  par(first-line-indent: 2em)[
    #text(font: font-song, size: size-5)[#body]
  ]
}
