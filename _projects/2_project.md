---
layout: page
title: 项目 2
description: 带背景图片和 giscus 评论的项目
img: assets/img/3.jpg
importance: 2
category: work
giscus_comments: true
---

每个项目都有一个漂亮的功能展示页面。
你可以轻松地用灵活的三列网格来排版图片，
让图片占 1/3、2/3 或整行宽度。

要给项目在作品集页面上设置背景图，只需在 front matter 中加上 img 字段，像这样：

    ---
    layout: page
    title: 项目
    description: 一个带背景图片的项目
    img: /assets/img/12.jpg
    ---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/1.jpg" title="示例图片" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/3.jpg" title="示例图片" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="示例图片" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    轻松地为照片添加说明。左边，一条公路穿过隧道；中间，树叶在文艺照片里艺术地飘落；右边，在另一张文艺照片里，一个伐木工抓着一把松针。
</div>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="示例图片" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    这张图片也可以有说明文字，就像魔法一样。
</div>

你也可以在图片行之间插入普通文字。
假设你想在发布其余图片之前，先写一点关于项目的内容。
你描述自己如何为项目操劳、流汗、_流血_，然后……在下一行图片中展示它的精彩。

<div class="row justify-content-sm-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/6.jpg" title="示例图片" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/11.jpg" title="示例图片" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    你也可以像这样排版成艺术感的 2/3 + 1/3 图片组合。
</div>

代码很简单。
只需用 `<div class="col-sm">` 包裹你的图片，再把它们放进 `<div class="row">` 里（了解更多请看 <a href="https://getbootstrap.com/docs/4.4/layout/grid/">Bootstrap 栅格</a>系统）。
要让图片自适应，给每张图片加上 `img-fluid` 类；要圆角和阴影效果，就用 `rounded` 和 `z-depth-1` 类。
上面最后一行图片的代码如下：

{% raw %}

```html
<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/6.jpg" title="示例图片" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm-4 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/11.jpg" title="示例图片" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
```

{% endraw %}
