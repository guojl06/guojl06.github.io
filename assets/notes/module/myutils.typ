#import "@preview/simple-plot:0.3.0": plot
// 专门把 figure 的标题改为黑体

#import "@preview/cuti:0.2.1": show-cn-fakebold
#import "@preview/diagraph:0.3.6":*

#let mgraph(num: 1, gap: 20pt, captions: (), prefix: "图", start: 1, nodesep: 0.8, ranksep: 1.0, ..graphs) = {
  let inject-defaults(src) = {
    let spacing = "nodesep=" + str(nodesep) + "\nranksep=" + str(ranksep) + "\n"
    src.replace(
      "{",
      "{\nnode [shape=circle]\nedge [color=black]\n" + spacing,
      count: 1
    )
  }

  let caps = if type(captions) == array { captions } else { (captions,) }
  let gs = graphs.pos()

  let cols = gs.enumerate().map(((i, g)) => {
    let engine = if g.text.contains("digraph") { "dot" } else { "neato" }
    let r = render(inject-defaults(g.text), engine: engine)
    let cap = if i < caps.len() { caps.at(i) } else { none }
    if cap != none {
      stack(dir: ttb, spacing: 4pt,
        align(center, r),
        align(center, [#prefix#(start + i) #cap]),
      )
    } else {
      align(center, r)
    }
  })

  align(center, stack(dir: ltr, spacing: gap, ..cols))
}
#mgraph(```
graph G {
    A -- 1
    A -- C
    B -- C
    B -- D
}
```)



#let conf(body) = {
  // 字体 fallback 链：找不到前面的自动用后面的
  let serif-fonts = ("Times New Roman", "SimSun", "Songti SC","Linux Libertine", "Georgia", "serif")
  let cjk-fonts   = ("SimSun", "WenQuanYi Zen Hei", "Songti SC","Noto Serif CJK SC", "serif")
  let math-fonts  = ("New Computer Modern Math", "Songti SC","SimSun", "Latin Modern Math")
  let mono-fonts  = ("DejaVu Sans Mono", "SimHei", "Noto Sans Mono", "monospace")

  show math.equation: set text(font: math-fonts)
  set text(
    font: serif-fonts,
    size: 10.5pt,
    lang: "zh"
  )
  show: show-cn-fakebold
  show raw.where(block: true): it => block(
    fill: luma(240),
    inset: 8pt,
    radius: 4pt,
    width: 100%,
    stroke: luma(200),
    text(font: mono-fonts, size: 9pt, it)
  )
  set page(
    paper: "a4",
    margin: (
      top: 1.5cm,
      bottom: 1.5cm,
      left: 1.5cm,
      right: 1.5cm,
    ),
    footer: context {
      let page_num = counter(page).display()
      align(center, text(size: 10pt, page_num))
    }
  )

  let z(it) = text(font: cjk-fonts, style: "normal", it)

  body
}
#show:conf

*123哇哇哇*哇哇哇哇哇哇搜索

#let fgraph(
  funcs, 
  names: (), 
  domain: (-5, 5, -2, 2), 
  step: (1, 0.5), 
  labels: ($x$, $y$), 
  colors: (blue, red, green, orange, purple),
  legend_pos: "bottom",
  grid_type: "both",
  density: 5          
) = {
  let ms = (
    sin: calc.sin, cos: calc.sin, tan: calc.tan,
    log: calc.log, ln: calc.ln, sqrt: calc.sqrt,
    abs: calc.abs, pi: calc.pi, pow: calc.pow, exp: calc.exp
  )

  let func_list = if type(funcs) == str { (funcs,) } else { funcs }
  
  // 1. 提取自变量名和纯文本名
  let var_label = labels.at(0)
  // 获取纯字符用于计算环境映射
  let var_str = repr(var_label).replace("$", "").trim()
  
  // 2. 构造图例项
  let items = func_list.enumerate().map(((i, f_str)) => {
    let c = colors.at(calc.rem(i, colors.len()))
    let f_name = if names.len() > i { eval("$" + names.at(i) + "$") } else { $ f_#(i+1) $ }
    
    grid(
      columns: (auto, auto),
      column-gutter: 6pt,
      align: horizon,
      box(fill: c, width: 1.2em, height: 0.3em, radius: 0.1em),
      // --- 关键修正：不再手动拼接 eval 字符串 ---
      // 先用标准的 x 渲染公式，然后利用 show 规则把公式里的 x 替换为 var_label
      {
        show "x": var_label
        $ #f_name (#var_label) = #eval("$" + f_str + "$") $
      }
    )
  })

  // 3. 绘图核心
  let plot_obj = plot(
    xmin: domain.at(0), xmax: domain.at(1),
    ymin: domain.at(2), ymax: domain.at(3),
    xlabel: labels.at(0), ylabel: labels.at(1),
    x-tick-step: step.at(0), y-tick-step: step.at(1),
    show-grid: grid_type,
    minor-grid-step: density,
    ..func_list.enumerate().map(((i, f_str)) => (
      fn: x_val => {
        // 计算时：同时支持 x 和用户自定义的变量名
        let safe_expr = f_str.replace(regex("x\^2"), "(x * x)").replace(regex("x\^3"), "(x * x * x)")
        let final_expr = safe_expr.replace(regex(var_str + "\^2"), "(" + var_str + " * " + var_str + ")")
        
        let scope = ms + (x: x_val) + ((var_str): x_val)
        float(eval(final_expr, scope: scope, mode: "code"))
      },
      stroke: colors.at(calc.rem(i, colors.len()))
    ))
  )

  // 4. 最终布局 (保持居中)
  let legend_content = if legend_pos == "bottom" {
    align(center, stack(dir: ltr, spacing: 20pt, ..items))
  } else {
    align(left + horizon, stack(dir: ttb, spacing: 12pt, ..items))
  }

  align(center, {
    if legend_pos == "bottom" {
      stack(spacing: 15pt, plot_obj, legend_content)
    } else {
      grid(columns: (auto, auto), column-gutter: 20pt, align: horizon, plot_obj, legend_content)
    }
  })
}

#let dfrac(x, y) = $ (dif #x) / (dif #y) $
#let vct(x) = $arrow(#x)$
#let uv(x,y) = $vct(#x _#y)$ 
#let bsum(ut:$i$,x,y) = $sum_ (#ut=#x) ^ #y$
#let ulim(ul:$Delta t$,ur:$0$) = $lim_(#ul -> #ur)$

#let lst(x, num: $n$, hl: 3, tl: 2, pun: $,$, upn: 163252573) = {
  // 1. 类型转换
  let hl_v = if type(hl) == int { hl } else { int(hl.text) }
  let tl_v = if type(tl) == int { tl } else { int(tl.text) }
  let n_v = if type(num) == int { num } 
            else if type(num) == content and num.has("text") { 
              let t = num.text
              if t.match(regex("^\d+$")) != none { int(t) } else { none }
            } else { none }

  // 2. 定义连接符逻辑函数
  // 如果 upn 是那个质数，就只返回 pun；否则根据索引 i 交替返回
  let get_sep(i) = {
    if upn == 163252573 { return [#pun ] }
    if calc.even(i) { [#pun ] } else { [#upn ] }
  }

  // 3. 辅助函数：将数组按交替符号拼接成 content
  let join_alt(arr, start_idx: 0) = {
    let res = ()
    for i in range(arr.len()) {
      res.push(arr.at(i))
      if i != arr.len() - 1 {
        res.push(get_sep(start_idx + i))
      }
    }
    return res.join()
  }

  // 4. 渲染逻辑
  if n_v != none {
    if n_v <= hl_v + tl_v {
      let items = range(1, n_v + 1).map(i => $#x _#i$)
      return join_alt(items)
    }
    
    let head_items = range(1, hl_v + 1).map(i => $#x _#i$)
    let tail_items = range(n_v - tl_v + 1, n_v + 1).map(i => $#x _#i$)
    
    // 拼接：头部 + (衔接处符号) + 省略号 + (衔接处符号) + 尾部
    let sep_before_dots = get_sep(hl_v - 1)
    let sep_after_dots = get_sep(hl_v)
    
    return $ #join_alt(head_items) #sep_before_dots dots.h #sep_after_dots #join_alt(tail_items, start_idx: hl_v + 1) $
    
  } else {
    let head_items = range(1, hl_v + 1).map(i => $#x _#i$)
    let tail_items = range(tl_v - 1, -1, step: -1).map(i => {
      if i == 0 { $#x _#num$ } else { $#x _(#num - #i)$ }
    })
    
    let sep_before_dots = get_sep(hl_v - 1)
    let sep_after_dots = get_sep(hl_v)

    return $ #join_alt(head_items) #sep_before_dots dots.h #sep_after_dots #join_alt(tail_items, start_idx: hl_v + 1) $
  }
}

// 辅助函数：强制转整数，防止报错
#let _to_int(val) = {
  if type(val) == int { val }
  else if type(val) == content and val.has("text") { int(val.text) }
  else { 0 }
}

// 1. 等差数列
#let aseq(end, begin: 0, hi: 1, tol: 1) = {
  let (e, b) = (_to_int(end), _to_int(begin))
  let get_val(n) = hi + (n - 1) * tol
  if b == 0 { $#get_val(e)$ } else { range(b, e + 1).map(i => $#get_val(i)$).join($,$) }
}

// 2. 等比数列
#let gseq(end, begin: 0, hi: 1, crt: 2) = {
  let (e, b) = (_to_int(end), _to_int(begin))
  let get_val(n) = hi * calc.pow(crt, n - 1)
  if b == 0 { $#get_val(e)$ } else { range(b, e + 1).map(i => $#get_val(i)$).join($,$) }
}

// 3. 斐波那契数列
#let fseq(end, begin: 0) = {
  let (e, b) = (_to_int(end), _to_int(begin))
  let fib(n) = {
    if n <= 0 { return 0 }
    if n <= 2 { return 1 }
    let (v1, v2) = (1, 1)
    for _ in range(n - 2) {
      let temp = v1 + v2
      v1 = v2
      v2 = temp
    }
    return v2
  }
  if b == 0 { $#fib(e)$ } else { range(b, e + 1).map(i => $#fib(i)$).join($,$) }
}

// 将名字改为 cal，避开系统内置的 calc 模块冲突
#let cal(expr, mode: 0, digits: 3, scope: (:), result: 0) = {
  let m = int(mode)
  let d = if digits == none { if m == 0 { 0 } else { 3 } } else { int(digits) }
  
  // 1. 构建作用域
  let mathScope = (
    sin: calc.sin, cos: calc.cos, tan: calc.tan,
    log: calc.log, ln: calc.ln, sqrt: calc.sqrt,
    abs: calc.abs, round: calc.round, pi: calc.pi,
    exp: calc.exp, pow: calc.pow, calc: calc
  ) + scope

  // 2. 幂运算逻辑预处理 (split 方案最稳)
  let cleanExpr = expr.replace(" ", "").replace("×", "*").replace("÷", "/").replace("**", "^")
  let finalExpr = cleanExpr
  if cleanExpr.contains("^") {
    let parts = cleanExpr.split("^")
    if parts.len() == 2 {
      finalExpr = "calc.pow(" + parts.at(0) + "," + parts.at(1) + ")"
    }
  }

  // 3. 核心计算
  let rawResult = eval(finalExpr, scope: mathScope)
  
  // 4. 数字格式化逻辑
  let isCleanInt(v) = { calc.abs(v - calc.round(v)) < 1e-10 }
  let formatStr(val, precision) = {
    let rounded = calc.round(val, digits: precision)
    if precision <= 0 { return str(int(rounded)) }
    let s = str(rounded)
    if not s.contains(".") { s += "." }
    let parts = s.split(".")
    let decimalPart = parts.at(1)
    while decimalPart.len() < precision { decimalPart += "0" }
    return parts.at(0) + "." + decimalPart
  }

  let processedResult = if m == 0 {
    if isCleanInt(rawResult) and d == 0 { str(int(rawResult)) } else { formatStr(rawResult, d) }
  } else {
    if rawResult == 0 { "0" } else {
      let magnitude = int(calc.floor(calc.log(calc.abs(rawResult))))
      let precision = d - 1 - magnitude
      formatStr(rawResult, calc.max(0, precision))
    }
  }

  // 5. 渲染公式内容
  let displayExpr = expr.replace(" ", "").replace("**", " ^ ").replace("*", " times ")
  let mathContent = eval(displayExpr, mode: "math")
  let formula = $ #mathContent = #processedResult $

  // 6. 根据开关返回不同类型
  if result == 0 {
    return formula
  } else {
    return (v: rawResult, g: formula)
  }
}

// --- 终极建议 ---
#cal("sin(pi/4)**2") 依然因为嵌套报错

#cal("11")
// --- 调用示例 ---
#cal("15 * 3 / 5")     // 自动生成：15 × 3 / 5 (带分式) = 9
#cal("4-(1/200-cos(2))",mode:1,digits:5)  // 自动生成分式 = 10

// 画一个抛物线，x范围 -3 到 3，y范围 -9 到 9
#fgraph(
  labels:($a$,$b$),
  // var:"t",
  ("x", "x - 1", "sin(x)","-x^3"), 
  domain: (-3, 3, -2, 4),
  step: (1, 1),
  names: ("f", "g", "h", "k"),
  legend_pos: "right"
)

#figure(
  fgraph(("x^2", "sin(x)")),
  caption: [这是我的函数图像], // 自动生成“图 1：这是我的函数图像”
) <my-plot>

$fseq(6,begin:1)$

$gseq(begin:1,6)$

$aseq(6,begin:1)$

// --- 调用示例 ---
$ lst(a,hl:4,tl:3,num:m,pun:+,upn:-) $    // 结果：a_1, a_2, a_3, a_4, a_5 (完美解决！)
//$ lst(a,num:13,lth:8) $    // 结果：a_1, a_2, a_3, ..., a_5, a_6 (此时才开始省略)


// 这样即便传入复杂内容也能正确处理
$ dfrac(x^2, t),vct(1),uv(e,omega),bsum(3,2),ulim(ul:1,ur:2)$ 

#let t-node(body) = {
  rect(inset: 8pt, radius: 4pt, stroke: 0.6pt + black, fill: white)[#body]
}

#let simple-tree(root, children) = {
  align(center, stack(spacing: 12pt,
    t-node(root),
    if children.len() > 0 {
      grid(
        columns: children.len(),
        column-gutter: 20pt,
        ..children.map(child => {
          if type(child) == array {
            // 递归处理子树
            simple-tree(child.at(0), child.slice(1))
          } else {
            t-node(child)
          }
        })
      )
    }
  ))
}

1111