// main.typ ── 使用示例
#import "writing_conf.typ": *

#show: article.with(
  title:      [论中国近代社会变迁与知识分子的角色],
  author:     [张三],
  student-id: [2024012345],
  email:      "zhangsan@mails.tsinghua.edu.cn",
)

// 正文直接写，首行自动缩进 2 字符
清末以降，中国社会经历了前所未有的深刻变革。士人阶层在这一历史转折中，既是观察者，亦是参与者。本文试图从...

= 一、历史背景

这是一个节标题下的段落，自动居中、黑体、无首行缩进。正文段落仍保持宋体五号、首行缩进、1.5倍行距。

= 二、核心论点

这里是第二节的内容。可以引用文献 #footnote[戴裔煊：《〈明史·佛郎机传〉笺正》，北京：中国社会科学出版社，1984年，第6页。]，脚注会自动排在当页底部，小五号宋体，单倍行距。

// 三线表示例
#tbl(
  caption: [表1 示例数据表],
  columns: (1fr, 1fr, 1fr),
  note: [注：数据来源于……],
  table.hline(stroke: 0.75pt),  // 上框线（也可省略，conf.typ 已设默认）
  table.header(
    [*指标*], [*数值*], [*单位*],
  ),
  table.hline(stroke: 0.5pt),   // 表头下分割线
  [甲], [100], [万元],
  [乙], [200], [万元],
  table.hline(stroke: 0.75pt),  // 下框线
)

// 图片示例
// #img(caption: [图1 示意图], image("example.png", width: 60%))

= 三、结论

综上所述，……
