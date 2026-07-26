---
layout: page
title: 插件
permalink: /plugins/
nav: false
description: al-folio v1.x 的精选与内置插件生态目录
---

`al-folio` `v1.x` 是一个由插件提供运行时特性的 starter 模板。
本页面列出生态目录（`_data/featured_plugins.yml`）中收录的插件。

## 命名约定

- 与主题耦合的插件：
  - 仓库：`al-folio-<feature>`
  - gem/插件 id：`al_folio_<feature>`
- 可复用插件：
  - 仓库：`al-<feature>` 或中性名称
  - gem/插件 id 与插件命名空间对齐

第三方的非 `al-*` 插件也可以申请收录。

## 内置插件

{% assign bundled_plugins = site.data.featured_plugins | where: "status", "bundled" %}

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Gem</th>
      <th>Plugin ID</th>
      <th>Compatibility</th>
      <th>Owner</th>
      <th>Demo</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    {% for plugin in bundled_plugins %}
      <tr>
        <td>{{ plugin.name }}<br><small><code>{{ plugin.repo_url }}</code></small></td>
        <td><code>{{ plugin.gem_name }}</code></td>
        <td><code>{{ plugin.jekyll_plugin_id }}</code></td>
        <td><code>{{ plugin.compat.al_folio_min }}</code> - <code>{{ plugin.compat.al_folio_max }}</code></td>
        <td>{{ plugin.owner }}</td>
        <td><code>{{ plugin.demo_path }}</code></td>
        <td>{{ plugin.notes }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>

## 仅精选插件

{% assign featured_only_plugins = site.data.featured_plugins | where: "status", "featured" %}
{% if featured_only_plugins.size == 0 %}
目前还没有仅精选的条目。
如果你想让自己的插件被考虑收录，请提交一个 **Plugin Feature Proposal** issue。
{% else %}

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Gem</th>
      <th>Plugin ID</th>
      <th>Compatibility</th>
      <th>Owner</th>
      <th>Demo</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    {% for plugin in featured_only_plugins %}
      <tr>
        <td>{{ plugin.name }}<br><small><code>{{ plugin.repo_url }}</code></small></td>
        <td><code>{{ plugin.gem_name }}</code></td>
        <td><code>{{ plugin.jekyll_plugin_id }}</code></td>
        <td><code>{{ plugin.compat.al_folio_min }}</code> - <code>{{ plugin.compat.al_folio_max }}</code></td>
        <td>{{ plugin.owner }}</td>
        <td><code>{{ plugin.demo_path }}</code></td>
        <td>{{ plugin.notes }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
{% endif %}

## 申请收录插件

1. 在本仓库提交一个 **Plugin Feature Proposal** issue。
2. 提供插件元信息（仓库 URL、gem 名称、插件 id、兼容性、demo 路径、维护者联系方式）。
3. 提交一个 PR 更新 `_data/featured_plugins.yml`。
4. 如果申请默认内置到 starter，请在同一个 PR 中包含 `Gemfile` 和 `_config.yml` 的配套修改。

精选与内置是维护者的两个独立决定。
