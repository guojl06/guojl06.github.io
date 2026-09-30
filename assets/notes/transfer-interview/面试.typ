#set page(
  paper: "a4",
  margin: (left: 6.5cm, right: 2cm, y: 2.5cm),
  background: [
    // 侧边极简灰色块
    #place(left, rect(width: 4.8cm, height: 100%, fill: luma(252)))
    // 左上角装饰线：修正 angle 为 90deg
    #place(top + left, dx: 1.2cm, dy: 1.2cm)[
      #stack(dir: ltr, spacing: 6pt, ..(line(angle: 90deg, length: 6pt, stroke: 0.5pt + luma(200)),) * 4)
    ]
  ]
)

#set text(
  font: ("Lantinghei SC","New Computer Modern", "Source Han Serif SC"),
  size: 10pt,
)

// --- 侧边栏 ---
#place(
  left,
  dx: -5.2cm,
  block(width: 2.8cm)[
    #set align(left)
    
    #v(1em)
    #rect(width: 1.5cm, height: 1.5pt, fill: black)
    #v(6pt)
    #block(
      width: 2.5cm,
      height: 3.5cm,
      stroke: 0.5pt + luma(230),
      radius: 2pt,
      clip: true,
    )[
      #set align(center + horizon)
      #image("照片照片照片.jpg", width: 100%, height: 100%, fit: "cover")
      // #rect(width: 100%, height: 100%, fill: white)[
      //   #text(fill: luma(200), size: 8pt)[ELECTRONIC\ PHOTO]
      // ]
    ]
    
    #v(2.5em)
    #text(size: 15pt, weight: 700, tracking: 0.15em)[郭嘉乐] \
    #text(size: 8pt, fill: gray, tracking: 0.1em)[GUO JIALE]
    
    #v(1.5em)
    #line(length: 100%, stroke: 0.5pt + luma(220))
    #v(1.5em)
    
    #set text(size: 8.5pt, fill: luma(50))
    #stack(
      spacing: 1.5em,
      [#text(size: 7pt, fill: gray)[STUDENT ID] \ #strong[2025013332]],
      [#text(size: 7pt, fill: gray)[FROM] \ #strong[紫荆书院]],
      [#text(size: 7pt, fill: gray)[TARGET] \ #strong[计算机科学与技术系]],
      [#text(size: 7pt, fill: gray)[GPA] \ #strong[3.7]],
      [#text(size: 7pt, fill: gray)[CONTACT] \ 18795398001 stgooac\@gmail.com],
    )
  ]
)

// --- 主体内容 ---

// 标题设计
#grid(
  columns: (auto, 1fr),
  column-gutter: 1.2em,
  align: bottom,
  text(size: 32pt, weight: "bold", fill: luma(235))[01],
  pad(bottom: 0.6em, text(size: 18pt, weight: "light", tracking: 0.4em)[个人基本情况])
)
#v(-0.8em)
#line(length: 100%, stroke: 0.8pt + black)



// 段落设置
#set par(leading: 1em, justify: true, first-line-indent: 2em)

// 标题花纹装饰
#show heading: it => [
  #v(1.5em)
  #stack(
    dir: ltr,
    spacing: 0.8em,
    rect(width: 4pt, height: 4pt, fill: black), 
    text(size: 11pt, weight: "bold", it.body)
  )
  #v(0.8em)
]

== 学习研究情况

院系排名 41/84。

总绩点不尽人意，但是我的微积分、线性代数、人工智能导论等基础课程在优秀水平。尤其得益于英文线性代数体系，我更加熟悉部分英文数学概念与延伸计算机概念知识。同时我这学期选修了面向对象程序设计基础、高等线性代数选讲、离散数学（2），收益颇丰。

热爱马拉松运动，2023、2024 银川马拉松半马完赛，校马 10 公里完赛。已完成游泳测试。

熟练掌握仓库管理与贡献，具有个人博客运维、云服务器运维、小型本地服务器运维知识，搭建紫荆书院 3D 打印机共享平台，自己筹建紫荆书院学习资源企划。对常见项目所需程序设计语言基本有所了解并且可以快速上手理解架构和部分复现。参与一清华大学-中国人民大学跨院系具身智能研究小组，预计学期末产出学术成果。

熟练掌握提示词工程。对常见大模型agent基本熟练操作，利用智谱 Coding Plan 搭建了本地流畅运行的 openclaw 工作流。利用 vibe coding 基本重构了 THU Info 与 LearnX，将 LearnX 冗长且高风险的 Cookie 管理统一交给 THU Info 的 WebVPN，搭建了二合一 app。

== 社会工作情况

紫荆书院科协竞赛部副部长，负责比赛策划、与其他院系协调国际学生参赛事宜，成功组织紫荆书院循迹车比赛。曾主动组织约 6 支国际学生队伍报名尝试 ICPC 网络预选赛，期间沟通打通了很多渠道，可能是去年全国仅有的纯留学生参赛队伍。

清华算协平台系统部成员，负责了 THUPC 初赛报名表单制作、决赛参赛 OS 制作封装。

寒假自动化系“清闽智航”实践支队宣传组组长，基本全面负责推送制作与送审。

参与海淀马拉松志愿者。

== 获奖情况

暂无学术奖项。校马十公里完赛证明、游泳测试完成证明。

“清闽智航”支队获得自动化系寒假实践银奖。

#grid(
  columns: (auto, 1fr),
  column-gutter: 1.2em,
  align: bottom,
  text(size: 32pt, weight: "bold", fill: luma(235))[02],
  pad(bottom: 0.6em, text(size: 18pt, weight: "light", tracking: 0.4em)[转系理由])
)
#v(-0.8em)
#line(length: 100%, stroke: 0.8pt + black)

相比当前院系比较浅显和偏部分行业应用的计算机培养方向，计算机系的完善健全的培养方案、多元深厚的院系文化和丰富的资源更加贴合我的学习风格和学习意愿，更加符合我对自己人生目标的定位，其更加成熟的学术路径能给我的学术梦想提供更多支持，同时具有更加激烈的竞争鞭策我时刻前进、放弃幻想、准备战斗。

从感性的角度说，我对清华园最开始的向往是和计算机系绑定的：清华计算机是我学习成长路上的图腾，是一个不知能不能至、但始终心向往之的锚点。在高考中规中矩的发挥之后，我遗憾发现自己离直接进入计算机系略有门槛，于是选择了紫荆书院这一具有电子信息科学技术方向的书院；但是上学期期中过去时，在现有培养方案中屡屡碰壁、诸多渴望学习的课程无法加入列表，让我意识到，这里固然有丰富的课程资源和开放包容的氛围，但我可能实际上仍然属于另一个世界，另一个代码、指令与激情更加充分燃烧的世界。留在这里，固然也能获取不少新知、拓宽国际视野、广交各国朋友，但总和我真正的愿景有所出入；而计算机系才是真正适合我大展宏图的那个平台，一个机遇无限、你追我赶、燃烧热血的世界。

我经常自诩我是宁夏 25 届学生中文化课最好的 OIer，OI 最烂的文化课选手。这倒不错，但学了 5 年 OI 真正给我带来的不是什么弱省省一这种微薄奖项，而是将一种更内在、更深层的精神培植到我的胸膛里。我学会了 Markdown 和 LaTex，学会了基础的算法思想，学会了仓库的使用，养成了命令行的使用习惯，更重要的是，再塑了我对计算机学科的信仰。在宁夏想要坚持这样的路是很难的，除了几个并肩而行的战友，没有人能理解你，更别提还有人想阻挠你。未曾经历过的人很难想象那种久旱逢甘霖的畅快，当你在历经万番阻挠穿越算法的荒漠，第一次知道并查集的路径压缩、知道线段树的懒标记下发原理，你真的仿佛穿越了时空，亲手接下了先辈们赐予你的知识的雨露，清冽甘甜，有时竟令人稍有泪下。那时支撑我走下去这条路的堪称唯一的图腾，就是清华九井。

选择计算机系还有一个原因，就是我希望主动把自己投入一个更加激烈的竞争环境，以此鞭策我更加努力付出、不再内耗与摆烂。我清楚地知道计算机系的竞争激烈程度冠绝全校，但是我不怕；我知道我的绩点目前来看不尽人意，但我也不惧。来到九井，在 peer pressure 下，我能爆发出更大的力量。
