# think2:PI Release 实验调试记录与关键发现

> 2026-07-06。承接 [think1.md](think1.md)(实验设计)。本文记录把设计落地的过程中踩的坑、修的 bug,以及一个**意料之外的科研发现**:v4-pro 的 PI 失败模式与论文模型不同,导致论文的 release 干预在它身上失效。

---

## 一、本轮做了什么

1. 在 [小学期AI4S/pi-release-exp/](../pi-release-exp/) 搭起完整实验框架(独立 git 仓库 → github.com/smartThise/pi-release-exp,私有):
   - 9 组干预(G0-G7 + S3/S5)、PI 流生成器、OpenAI 兼容 client、runner、metrics(RE/CP/Robustness)、浅色中文 dashboard
2. 用论文原版词表替换了我们手写的 8 类小词表(论文仓库 `zhuangziGiantfish/Unable-to-Forget` 的 `dict_category_double-word_46-400_v1-1.json`,46 类 × 400 词)
3. **修了一个致命的方法论 bug**(详见第三节)
4. 发现 v4-pro 的失败模式与论文不同(详见第六节)

---

## 二、DeepSeek API 接入要点(以后复用)

- base_url:`https://api.deepseek.com`(框架自己补 `/chat/completions`)
- model:`deepseek-v4-pro`(推理模型)
- **必须关 thinking**,否则 64 个 max_tokens 全被推理吃掉,返回空 content。配置走 `extra_body`(框架已通用支持,合并进 payload):
  ```yaml
  extra_body:
    thinking:
      type: disabled    # enabled / disabled,不是 "none"
  ```
- 关掉后:单次调用 41 token / 1.7s(推理开启时 1738 token / 30s)
- 同一 key 也能切 `deepseek-chat`(V3,原生非推理,论文同款 DeepSeek 条目)

---

## 三、★ 致命 bug:流的排列结构

### 现象
v4-pro 在 46 key × 97 updates 下基线 accuracy = **0.957**,看似"模型太强、没有 PI"。但论文里同负载下多数模型已塌陷。

### 根因
我们的 `_interleave` 是**按轮次填充**(round-robin):每轮放全 46 个 key,共 97 轮。后果——**每个 key 的最后一次更新全挤在流的最后 46 个位置**,等于把答案打包放在末尾。模型只要读尾部 46 行就 ~100% 正确。**不是模型强,是我们在喂饭。**

验证:46 个 key 最后一次出现的位置 min=4416、max=4461(流长 4462),全部挤在最后 46 个位置。

### 论文的做法
`pseudo_randomize(list_all_pairs, max_key_repeat=0)`:**全随机打乱**,只禁止连续同一 key。每个 key 的最后出现**散布在整条流里**,模型必须逐个搜索。

### 修复
把 `_interleave` 换成等价的 `_pseudo_randomize`(随机洗牌 + 禁连续同 key)。修复后:
| 负载 | 修复前 | 修复后 |
|---|---|---|
| 46×97 | 0.957 | **0.043** |
| 46×48 | — | 0.000 |

deepseek-v4-pro 现在老老实实表现出 PI。

### 教训
**永远对比原版实现,不要自己想当然。** 我们以为"避免连续同 key"就够了,但轮次结构偷偷把任务从"搜索"降级成"读尾部"。这个 bug 在小规模(3 key)时看不出问题,放大到 46 key 才暴露。

---

## 四、方法学对齐情况(诚实版:核心对齐,细节有差)

逐行比对了论文 `pi_flow_upgrade.py` 与我们 `groups.py` / `pi_test.py` / `metrics.py` 后,结论是**不是百分百对齐**。PI 现象相关的核心对齐,但 prompt 组装和评分细节有真差异。

### 4.1 核心对齐(影响 PI 现象本身,这些没问题)

| 维度 | 论文 | 我们 | 状态 |
|---|---|---|---|
| 词表 | 46 类 × 400 词 | 同一文件 | ✅ |
| 采样 | sample_replacement=0 | 不放回(rng.sample) | ✅ |
| 流排列 | pseudo_randomize(全随机) | _pseudo_randomize | ✅(已修) |
| 流格式 | `f"{key}: {item}; "` | 同 | ✅ |
| 负载 | 46 key,updates 扫 [2..400] | 46 key | ✅ |
| system prompt | 无 | 无 | ✅ |
| 推理模型 | 排除/单列 | thinking 关闭 | ✅ |

### 4.2 真差异 1:G0 指令措辞

| | 文本 |
|---|---|
| 论文 | `As my secretary, **I need you to** carefully read a text stream...` |
| 我们 | `As my secretary, carefully read a text stream...`(缺 "I need you to") |

影响:极小(语义等价)。但不是字面对齐。

### 4.3 真差异 2:prompt 组装结构

| | 结构 |
|---|---|
| 论文 | `instruction\n\nThe text stream starts on the next line.\n {stream}\n\n{question}`——"starts"独立成段,流前是 `\n `(换行+一个空格) |
| 我们 | `instruction. The text stream starts on the next line.\n\n{stream}\n\n{query}`——"starts"接在指令句尾,流前是 `\n\n` |

差异:"starts on the next line" 的段落归属不同,以及流前的分隔符(`\n ` vs `\n\n`)。

### 4.4 论文的一个源码 bug,我们"修"了

论文:`instruction += f"...continuously updated.The {n} keys..."`——`updated.` 和 `The` 之间**没空格**(他们的字符串拼接 bug)。
我们:`"...continuously updated. The..."`(正确空格)。

无实质影响,但确实不是字面照搬。

### 4.5 真差异 3(重要):评分抽取逻辑不一样

**这个会影响绝对准确率数字的可比性。**

| | 抽取方式 |
|---|---|
| 论文 | 3 个 verbal 正则 + 1 个 colon 正则合并;value 捕获 **1–2 词**(`\w+(?:\s+\w+)?`);严格 strip 引号/括号 |
| 我们 | `extract_value_for_key` 用 `f"{key}[^.]*?\bis\s+(...)"` 然后 **只取第一个词**(`.split()[0]`);2 词值抽不全。但有 fallback:`target 子串出现在 key 最后一次出现之后`就算对 |

后果:
- 对 v4-pro 这种输出规整的(`The current value of bug is blister beetle.`),fallback 能兜住 2 词值,数字基本可信。
- 但和论文评分**不严格可比**:我们偏宽松(fallback 是子串包含),论文是严格模式匹配。边界情况(模型没按格式答)下分歧更大。

如要论文级定量对比,应把 `metrics.py` 换成论文的 `_extract_verbal_matches` + `_extract_colon_matches`。

### 4.6 没实现的机制

| 论文机制 | 我们 | 影响 |
|---|---|---|
| `balanced_sample` | 没实现 | 单流影响小(它是跨 session 平衡采样的) |
| 多 session + CI95 bootstrap 停止 | 固定 n_trials × k_repeats | 统计框架不同,非方法论错误 |

### 4.7 query 文本(对齐 ✓,顺带记一个论文 bug)

论文 query = `"What are the current value of each key ({keys}) you are tracking? End your response with: 'The current value of <key> is <value>.'"`

注:论文源码 verbal 分支里有一行 `f"Ensure that you report each key exactly once in this manner. "`——这是个 no-op(漏写 `question +=`),所以论文实际 query **不含**这句话。我们的 `build_base_query` 也不含,正好对齐。

### 4.8 结论

- **对"v4-pro 失败模式不同"这个定性结论**:不受这些差异影响——PI 是真实复现的,失败模式分析基于实际输出文本,与评分细节无关。
- **对"和论文横向定量对比"**:4.3 / 4.5 两处(组装结构、评分)会让数字不严格可比。要写正式对比需先修齐。
- think1 / 之前 think2 草稿里"已对齐论文"的说法是**过度自信**,实际是"实质对齐、细节有差"。

### 4.9 ★ 已修齐(2026-07-06)

三处真差异已全部修齐到论文原版:

1. **G0 指令措辞**(4.2):补回 "I need you to",并**逐字保留论文的 `updated.The` 无空格拼接 bug**(加注释说明是论文原版行为)。
2. **prompt 组装结构**(4.3):改为 `instruction\n\nThe text stream starts on the next line.\n {stream}\n\n{question}`——"starts"独立成段,流前用 `\n `(换行+空格),与论文逐字节一致。
3. **评分抽取**(4.5):`src/metrics.py` 移植了论文的 `extract_pieces_response_to_dict` + `_extract_verbal_matches`(3 个 verbal 正则)+ `_extract_colon_matches` + `compute_accuracy`(精确 strip+lower 字符串匹配,key 查找大小写敏感)。

**移植时踩的一个坑**:论文 pattern 2/3 的 KEY 捕获组字符类 `[\"'\]\>?)` 漏了闭合 `]`(把 `?` 和 `)` 吃进类里),正则结构崩塌,第一版移植后 accuracy=0.000。改用干净的非捕获组 `(?:["'\[\]<>])?` 代替手写转义后修复。验证:干净行 `The current value of quodruped is Heck cattle.` 正确抽出 `('quodruped', 'Heck cattle')`,46×8 基线 accuracy=0.130(与旧评分一致,确认对规整输出两者等价)。

### 4.10 仍未对齐(已知,非阻塞)

- ~~**干预组 G1-G7 / S3 / S5 的 prompt 不共享 G0 的基线结构**~~ → **已修(2026-07-06)**:重构 `groups.py`,所有组统一为「论文基线 instruction + stream + [干预注入] + query」,组间唯一差异就是注入内容或 query 改写。验证:G0/G1/G2 前 200 字符完全相同。G2(Mock-QA)真实调用 acc=0.130,与 G0 同(符合"v4-pro 失败模式不是首因,Mock-QA 无效"的诊断)。
- `balanced_sample` / 多 session CI95 bootstrap(4.6):统计框架差异,非方法论错误,暂不实现。

---

## 五、实验结果(46×97,9 组,5 试次)

跑到一半(22/45 记录)停掉,因为信号已明确:

| 组 | 平均 acc | 含义 |
|---|---|---|
| G0 baseline | 0.020 | 饱和地板 |
| G1 semantic-forget | 0.019 | ≈基线,复现"自然语言无效" |
| G2 mock-qa-reset | 0.020 | **零提升** |
| G3 syntactic-cliff | 0.016 | 零提升 |

**结论**:46×97 负载下所有组全在饱和地板(~0.02),Mock-QA 完全不起效。继续跑只会浪费预算。

在更轻的 46×4(基线 0.22,有 headroom)下重测 G0 vs G2(各 3 试次):G0=0.217,G2=0.210,**仍然零提升**。说明 G2 失效不是负载太重的问题,而是更根本的原因(见下节)。

---

## 六、★ 核心发现:失败模式不同

### 诊断
在 46×4 下,对 v4-pro 的 46 个回答逐 key 分类:

| 错误类型 | 数量(/46) | 占比 |
|---|---|---|
| 正确 | 6 | 13% |
| **首因错误**(输出了首次值) | **5** | **11%** |
| **中间值错误**(输出了中途某次) | **35** | **76%** |
| 没答 | 0 | 0% |

### 论文模型的失败模式
论文 Figure 5:错误**集中在 early bins(首因锚定)**——模型倾向于检索最早出现的旧 value。

### v4-pro 的失败模式
76% 的错误是**中间值**——取了"差不多的最近"但不是真最新。只有 11% 是首因。

### 这解释了为什么 Mock-QA 无效
Mock-QA reset 的机制是**打破首因锚定**(伪造"任务结束/新会话",让模型不再被早期 value 拉扯)。它针对的病是**首因**。v4-pro 的病是**中间值检索失败**(注意力过载,取到一个 recent-but-not-latest 的值),根本不是首因。**药不对症**,所以零提升。

### 这是真正的科研发现
- 复现了 PI 现象(方法学正确)
- 但更强/更新的模型表现出**不同的 PI 失败模式**
- 论文的 release 干预是 failure-mode-specific 的,**不能跨失败模式迁移**
- 暗示:要 release v4-pro 的 PI,需要针对"中间值错误"设计新干预(强化"严格取最后一次更新"),而不是照搬论文的首因破解法

---

## 七、论文 hackreset 的真相

对比论文 `get_fake_conversation`("hackreset" 的核心):它把**正确答案伪造成一轮 assistant 回合**注入:
```
<question> }
{ role: assistant, content: "Okay, here are the current values:
  The current value of key1 is <正确val1>.     ← 用真实最新值伪造
  ..." }
{ role: user, content: <instruction> }
```
这是**激进的欺骗式注入**(基本等于把答案喂进去),不是我们 G2 那种温和的"伪造任务结束对话"。两者不是一回事。论文的"有效"部分来自这种近乎作弊的注入,不能直接对标。

---

## 八、待决策:三条 forward paths

**A. 把差异本身当发现**:"在 v4-pro 上复现 PI,失败模式从首因转为中间值,论文 release 干预因此失效"——干净的负结果/差异结果,可写进报告。

**B. 换论文同款模型**(deepseek-chat/V3):它的失败模式大概率是首因(论文同款),Mock-QA 才有用武之地,实验才能横向对比论文。**先验证工具链在它身上 G2 真能起效。**

**C. 为 v4-pro 设计针对性干预**:针对"中间值错误",强化"严格取最后一次更新"(query 工程 G7、自生成 G6 强制复述最后 N 个更新、或设计新组)。

**建议路径**:先 B(验证框架在论文同款模型上正确),再 A/C(回 v4-pro 报告差异 + 针对性干预)。待用户拍板。

---

## 九、当前仓库状态

- `pi-release-exp/` 已推送 github.com/smartThise/pi-release-exp(私有,branch=main)
- venv 在 `.venv/`,装了 requests + pyyaml
- dashboard 在 http://127.0.0.1:8765(浅色中文,跑 `python dashboard/server.py`)
- 论文词表已替换进 `data/word_categories.json`(46 类)
- `src/pi_test.py`:`_pseudo_randomize` 已替换 `_interleave`(关键修复)
- `src/api_client.py`:`extra_body` 通用支持(厂商参数透传)
- `config/config.yaml`:deepseek-v4-pro + thinking disabled + max_tokens 1024
- `config/experiment.yaml`:46 key × 97 updates(已验证太重,待调成更轻或换模型)
- runs/ 有两个半成品 run(46×97 饱和的、早期 G0 失败的),可清

### 未提交的改动
- pi_test.py 的 _pseudo_randomize 修复
- api_client.py 的 extra_body
- groups.py 的 OVERRIDES(去 max_tokens、改注释)
- experiment.yaml 改 46×97
- config.example.yaml 加 extra_body 文档
- data/word_categories.json 换论文原版

下一会话应先 `git add -A && git commit && git push` 把这些固定下来。
