---
layout: post
title: 参考文献示例
date: 2023-07-12 09:56:00-0400
description: 包含参考文献的博客文章示例
tags: 排版 文献
categories: 示例文章
giscus_comments: true
related_posts: false
related_publications: true
---

This post shows how to add bibliography to simple blog posts. We support every citation style that [jekyll-scholar](https://github.com/inukshuk/jekyll-scholar) does. That means simple citation like {% cite einstein1950meaning %}, multiple citations like {% cite einstein1950meaning einstein1905movement %}, long references like {% reference einstein1905movement %} or also quotes:

{% quote einstein1905electrodynamics %}
Lorem ipsum dolor sit amet, consectetur adipisicing elit,
sed do eiusmod tempor.

Lorem ipsum dolor sit amet, consectetur adipisicing.
{% endquote %}

If you would like something more academic, check the [distill style post]({% post_url 2018-12-22-distill %}).
