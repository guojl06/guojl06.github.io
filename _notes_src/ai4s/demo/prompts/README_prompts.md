# Prompt Suites 使用说明（中文版）

本文件说明 `prompts/` 目录的作用、prompt suite 的配置方式、JSONL 数据格式、常见实验任务写法，以及如何用脚本校验和批量运行 prompt。它对应项目中的：

```text
prompts/
  README_prompts.md
  suites/
    factual_recall_capitals.jsonl
    entity_binding_colors.jsonl
    recency_interference.jsonl
    copy_task.jsonl
    activation_patching_pairs.jsonl
  generated/
```

本项目的目标不是单独测试某一句 prompt，而是把 prompt 组织成可重复、可批量、可统计的实验材料。推荐的实验单位是：

```text
model × prompt_suite × intervention × metric
```

例如：

```text
Qwen3-0.6B-Base
× recency_interference.jsonl
× layer_skip / zero_attention / zero_mlp / activation_patching
× KL / target_logit_drop / recovery_fraction
```

---

## 1. 为什么需要 prompt suite

早期单 prompt 实验适合调试，比如：

```text
The capital of France is
```

但如果要做系统性研究，单条 prompt 不够。你需要一组结构化 prompt，用来控制变量并形成统计结果。例如研究 recency/interference 时，至少需要系统改变：

```text
目标信息距离 target_distance
干扰项数量 num_distractors
干扰项相似性 distractor_similarity
实体名称 entity
属性类别 attribute_type
目标答案 target_text
```

所以本项目使用 `JSONL` 格式管理 prompt suite：每一行是一条实验样本，每条样本都有自己的 `prompt_id`、`task`、`condition`、`prompt`、`target_text` 和 `variables`。

---

## 2. 文件结构说明

```text
prompts/
  README_prompts.md
  suites/
    factual_recall_capitals.jsonl
    entity_binding_colors.jsonl
    recency_interference.jsonl
    copy_task.jsonl
    activation_patching_pairs.jsonl
  generated/
```

含义：

```text
README_prompts.md
  prompt suite 的说明文档。

suites/
  正式使用或手写维护的 prompt suite。
  一般建议把稳定实验材料放在这里。

generated/
  由脚本自动生成的大规模 prompt suite。
  例如系统性改变 target_distance、num_distractors、entity order 的材料。
```

推荐命名规则：

```text
任务名_变量名.jsonl
```

例如：

```text
factual_recall_capitals.jsonl
entity_binding_colors.jsonl
recency_interference.jsonl
activation_patching_pairs.jsonl
```

---

## 3. 为什么使用 JSONL

JSONL 是 “JSON Lines” 的缩写。它不是一个大 JSON 数组，而是每一行一个 JSON 对象。

例如：

```json
{"prompt_id":"capital_0001","task":"factual_recall","condition":"capital_europe","prompt":"The capital of France is","target_text":" Paris","expected_answer":"Paris"}
{"prompt_id":"capital_0002","task":"factual_recall","condition":"capital_europe","prompt":"The capital of Germany is","target_text":" Berlin","expected_answer":"Berlin"}
```

优点：

```text
1. 一行一个样本，适合大规模实验。
2. 可以逐行读取，不需要一次性加载全部 prompt。
3. 每条 prompt 可以带 metadata 和 variables。
4. 实验结果容易和 pandas DataFrame 对齐。
5. 后续可以方便地按 prompt_id 合并不同模型和不同干预实验的结果。
```

注意：JSONL 文件中不能写注释。每一行都必须是合法 JSON。

---

## 4. 标准 prompt schema

推荐每条 prompt 使用以下字段：

```json
{
  "prompt_id": "unique_prompt_id",
  "task": "factual_recall | entity_binding | copy_task | recency_interference | activation_patching",
  "condition": "experimental_condition_name",
  "prompt": "The actual prompt prefix.",
  "target_text": " target token",
  "expected_answer": "human-readable answer",
  "clean_prompt": null,
  "corrupt_prompt": null,
  "patch_position": -1,
  "variables": {},
  "tags": []
}
```

字段含义：

```text
prompt_id
  每条 prompt 的唯一编号。后续所有结果表都依赖它对齐。
  不建议使用随机编号，建议包含任务和条件信息。

task
  任务类型。例如 factual_recall、entity_binding、recency_interference、activation_patching。

condition
  实验条件。例如 target_recent、target_old、one_distractor、country_swap。

prompt
  普通 next-token 实验中直接输入模型的文本前缀。

target_text
  需要追踪 logit 的目标 token。当前脚本假设它最好被 tokenizer 分成一个 token。
  注意通常英文 token 前面要带空格，例如 " Paris"、" red"、" bird"。

expected_answer
  人类可读答案，方便检查和后续分析。

clean_prompt / corrupt_prompt
  activation patching 使用。
  普通 next-token 实验可以设为 null 或省略。

patch_position
  activation patching 中 patch 哪个 token 位置。
  默认 -1 表示最后一个 token。

variables
  实验自变量。建议把所有后续分组分析需要的信息都放在这里。
  例如 target_distance、num_distractors、country、entity、attribute。

tags
  标签。用于快速筛选、分组或记录任务属性。
```

---

## 5. 例子一：事实回忆 factual recall

用于研究模型如何输出事实性知识，例如国家首都、作者作品、化学元素等。

文件示例：

```text
prompts/suites/factual_recall_capitals.jsonl
```

示例行：

```json
{"prompt_id":"capital_0001","task":"factual_recall","condition":"capital_europe","prompt":"The capital of France is","target_text":" Paris","expected_answer":"Paris","variables":{"country":"France","capital":"Paris","region":"Europe"},"tags":["factual","capital","europe"]}
```

```json
{"prompt_id":"capital_0002","task":"factual_recall","condition":"capital_europe","prompt":"The capital of Germany is","target_text":" Berlin","expected_answer":"Berlin","variables":{"country":"Germany","capital":"Berlin","region":"Europe"},"tags":["factual","capital","europe"]}
```

适合运行：

```text
layer skip sweep
attention/MLP ablation
logit lens
activation patching
```

典型问题：

```text
哪几层对目标答案 logit 影响最大？
MLP 消融是否比 attention 消融影响更大？
目标答案在 logit lens 中从哪一层开始出现？
```

---

## 6. 例子二：实体-属性绑定 entity binding

用于研究模型能否根据上下文绑定实体与属性。

示例：

```json
{"prompt_id":"binding_color_0001","task":"entity_binding","condition":"one_distractor","prompt":"Alice's key is in the red box. Bob's key is in the blue box. Alice's key is in the","target_text":" red","expected_answer":"red","variables":{"target_entity":"Alice","target_attribute":"red","distractor_entity":"Bob","distractor_attribute":"blue","num_distractors":1},"tags":["binding","color"]}
```

```json
{"prompt_id":"binding_color_0002","task":"entity_binding","condition":"one_distractor","prompt":"Alice's key is in the red box. Bob's key is in the blue box. Bob's key is in the","target_text":" blue","expected_answer":"blue","variables":{"target_entity":"Bob","target_attribute":"blue","distractor_entity":"Alice","distractor_attribute":"red","num_distractors":1},"tags":["binding","color"]}
```

适合研究：

```text
attention 是否负责从上下文路由到目标实体；
MLP 是否负责写入或输出目标属性；
干扰实体是否降低目标 token logit；
实体顺序是否造成 recency bias。
```

---

## 7. 例子三：recency / proactive interference

用于研究目标信息距离和干扰项数量对模型输出的影响。

示例：

```json
{"prompt_id":"recency_0001","task":"recency_interference","condition":"target_recent","prompt":"Bob's key is in the blue box.\nCarol's key is in the green box.\nAlice's key is in the red box.\nAlice's key is in the","target_text":" red","expected_answer":"red","variables":{"target_entity":"Alice","target_attribute":"red","target_distance":1,"num_distractors":2},"tags":["recency","interference","binding"]}
```

```json
{"prompt_id":"recency_0002","task":"recency_interference","condition":"target_old","prompt":"Alice's key is in the red box.\nBob's key is in the blue box.\nCarol's key is in the green box.\nAlice's key is in the","target_text":" red","expected_answer":"red","variables":{"target_entity":"Alice","target_attribute":"red","target_distance":3,"num_distractors":2},"tags":["recency","interference","binding"]}
```

建议控制变量：

```text
target_distance
  目标信息距离查询位置有多远。

num_distractors
  目标信息之后有多少干扰项。

distractor_similarity
  干扰项是否与目标属于同一语义类别。

attribute_type
  属性类型，例如 color、location、number、object。
```

适合结果分析：

```text
target_old 是否比 target_recent 有更低 target_logit；
干扰项数量是否提高 KL 或 target_logit_drop；
后层 attention 消融是否对 target_old 条件影响更大。
```

---

## 8. 例子四：copy task

用于研究局部复制、最后 token 依赖和 recency-sensitive completion。

示例：

```json
{"prompt_id":"copy_0001","task":"copy_task","condition":"last_word","prompt":"Repeat the last word: cat dog bird ->","target_text":" bird","expected_answer":"bird","variables":{"sequence":["cat","dog","bird"],"target_position":"last"},"tags":["copy","recency"]}
```

```json
{"prompt_id":"copy_0002","task":"copy_task","condition":"last_word","prompt":"Repeat the last word: red green blue ->","target_text":" blue","expected_answer":"blue","variables":{"sequence":["red","green","blue"],"target_position":"last"},"tags":["copy","recency"]}
```

适合研究：

```text
copy 行为依赖哪些 attention heads 或哪些层；
最后 token 信息是否在浅层/中层就能从 logit lens 看到；
attention ablation 是否比 MLP ablation 更破坏 copy 任务。
```

---

## 9. 例子五：activation patching pairs

Activation patching 需要 clean/corrupt 成对 prompt。

示例：

```json
{"prompt_id":"patch_capital_0001","task":"activation_patching","condition":"country_swap","clean_prompt":"The capital of France is","corrupt_prompt":"The capital of Germany is","target_text":" Paris","expected_answer":"Paris","patch_position":-1,"variables":{"clean_subject":"France","corrupt_subject":"Germany","target":"Paris"},"tags":["patching","factual"]}
```

含义：

```text
clean_prompt
  正确目标为 Paris 的上下文。

corrupt_prompt
  不应该输出 Paris 的对照上下文。

target_text
  观察 clean activation patch 到 corrupt run 之后，Paris 的 logit 是否恢复。
```

当前脚本默认要求：

```text
clean_prompt 和 corrupt_prompt 的 tokenized length 最好一致。
target_text 最好是单 token。
patch_position 默认 -1，即最后一个 token 位置。
```

---

## 10. 如何在 config 中指定 prompt suite

每个模型 config 中可以指定默认 prompt suite：

```json
"prompt_suite": {
  "enabled": true,
  "path": "prompts/suites/factual_recall_capitals.jsonl",
  "format": "jsonl",
  "id_field": "prompt_id",
  "prompt_field": "prompt",
  "target_field": "target_text",
  "clean_prompt_field": "clean_prompt",
  "corrupt_prompt_field": "corrupt_prompt",
  "filter": {
    "tasks": [],
    "conditions": [],
    "tags": []
  },
  "max_examples": null,
  "validate_single_token_target": true,
  "validate_clean_corrupt_same_length": true
}
```

含义：

```text
enabled
  是否启用 prompt suite 配置。

path
  默认 prompt suite 路径。

format
  当前应为 jsonl。

id_field / prompt_field / target_field
  字段名映射。通常不需要改。

filter
  按 task、condition、tags 过滤 prompt。
  当前脚本支持程度取决于具体 batch runner，建议优先通过 --prompt-suite 指定文件。

max_examples
  最大读取样本数。调试时可设为 5 或 10。

validate_single_token_target
  是否检查 target_text 是否为单 token。

validate_clean_corrupt_same_length
  是否检查 activation patching 的 clean/corrupt token 长度一致。
```

运行 batch 脚本时，可以直接指定：

```bash
python scripts/12_batch_layer_skip_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --max-examples 5
```

如果不指定 `--prompt-suite`，脚本会尝试读取 config 中的 `prompt_suite.path`。

---

## 11. 如何校验 prompt suite

推荐每次新建或修改 prompt suite 后先校验。

基本校验：

```bash
python scripts/11_validate_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl
```

严格模式：

```bash
python scripts/11_validate_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --strict
```

不加载 tokenizer，只检查 JSONL 结构：

```bash
python scripts/11_validate_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --no-tokenizer
```

校验内容包括：

```text
prompt_id 是否存在；
prompt_id 是否重复；
task / condition / target_text 是否存在；
普通任务是否有 prompt；
activation_patching 任务是否有 clean_prompt 和 corrupt_prompt；
target_text 是否为单 token；
clean_prompt 和 corrupt_prompt 的 tokenized length 是否一致。
```

---

## 12. 如何运行 batch 实验

### 12.1 Batch layer skip

```bash
python scripts/12_batch_layer_skip_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --max-examples 5
```

输出：

```text
outputs/results/pythia_70m_batch_layer_skip.csv
```

### 12.2 Batch attention/MLP ablation

```bash
python scripts/13_batch_attn_mlp_ablation_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/entity_binding_colors.jsonl
```

输出：

```text
outputs/results/pythia_70m_batch_attn_mlp_ablation.csv
```

### 12.3 Batch activation patching

```bash
python scripts/14_batch_activation_patching_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/activation_patching_pairs.jsonl
```

输出：

```text
outputs/results/pythia_70m_batch_activation_patching.csv
```

### 12.4 Batch logit lens

```bash
python scripts/15_batch_logit_lens_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl
```

输出：

```text
outputs/results/pythia_70m_batch_logit_lens.csv
```

---

## 13. 如何查看 batch 结果

结果一般保存在：

```text
outputs/results/
```

用 pandas 查看：

```python
import pandas as pd

df = pd.read_csv("outputs/results/pythia_70m_batch_layer_skip.csv")
print(df.head())
print(df.columns)
```

常见字段：

```text
model_id
  使用的模型。

prompt_id
  prompt suite 中的样本编号。

task
  任务类型。

condition
  实验条件。

intervention
  干预类型，例如 skip_block、zero_attention、zero_mlp、activation_patch。

layer
  层编号。

target_text
  被追踪的目标 token。

kl_base_to_intervened
  干预前后 next-token distribution 的 KL 差异。

target_logit_drop
  干预后目标 token logit 下降量。

recovery_from_corrupt
  activation patching 中，patch 后相对 corrupt 的恢复量。

fraction_of_clean_effect
  activation patching 中，恢复量占 clean-corrupt 差异的比例。

variables_json
  prompt 中的 variables 字段，通常用于后续分组统计。
```

示例：按层和条件求平均：

```python
import pandas as pd

df = pd.read_csv("outputs/results/pythia_70m_batch_layer_skip.csv")
summary = (
    df.groupby(["condition", "layer"])["target_logit_drop"]
      .mean()
      .reset_index()
)
print(summary.head())
```

示例：按 prompt 变量分析 target_distance：

```python
import json
import pandas as pd

df = pd.read_csv("outputs/results/pythia_70m_batch_layer_skip.csv")

# variables_json 是字符串，需要解析成 dict
df["variables"] = df["variables_json"].apply(lambda s: json.loads(s) if isinstance(s, str) and s else {})
df["target_distance"] = df["variables"].apply(lambda d: d.get("target_distance"))

summary = (
    df.groupby(["target_distance", "layer"])["target_logit_drop"]
      .mean()
      .reset_index()
)
print(summary.head())
```

---

## 14. 如何新增一个 prompt suite

以新建一个颜色绑定任务为例。

第一步，新建文件：

```bash
nano prompts/suites/my_binding_colors.jsonl
```

第二步，写入每行一个 JSON 对象：

```json
{"prompt_id":"my_binding_0001","task":"entity_binding","condition":"one_distractor","prompt":"Alice's key is in the red box. Bob's key is in the blue box. Alice's key is in the","target_text":" red","expected_answer":"red","variables":{"target_entity":"Alice","target_attribute":"red","num_distractors":1},"tags":["binding","color"]}
```

```json
{"prompt_id":"my_binding_0002","task":"entity_binding","condition":"one_distractor","prompt":"Alice's key is in the red box. Bob's key is in the blue box. Bob's key is in the","target_text":" blue","expected_answer":"blue","variables":{"target_entity":"Bob","target_attribute":"blue","num_distractors":1},"tags":["binding","color"]}
```

第三步，校验：

```bash
python scripts/11_validate_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/my_binding_colors.jsonl
```

第四步，运行 batch 实验：

```bash
python scripts/13_batch_attn_mlp_ablation_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/my_binding_colors.jsonl
```

---

## 15. prompt 设计规范

### 15.1 target_text 尽量是单 token

当前 metric 脚本默认使用单 token 目标：

```python
target_ids = tokenizer.encode(target_text, add_special_tokens=False)
assert len(target_ids) == 1
```

英文中很多 token 需要前置空格，例如：

```text
" Paris"
" red"
" bird"
```

如果写成：

```text
"Paris"
```

不同 tokenizer 下可能切分方式不同，导致校验失败或结果解释变复杂。

### 15.2 activation patching 需要 token 对齐

当前 activation patching 脚本假设 clean/corrupt prompt token 长度一致，例如：

```text
The capital of France is
The capital of Germany is
```

但这不保证对所有 tokenizer 都一致，所以必须用校验脚本检查。

### 15.3 base model 和 instruct model 分开设计

Base model 适合 prefix completion：

```text
The capital of France is
```

Instruct model 更适合 chat/instruction 格式：

```text
User: What is the capital of France?
Assistant:
```

如果使用 Hugging Face tokenizer 的 chat template，后续需要单独在脚本中调用：

```python
tokenizer.apply_chat_template(...)
```

当前 prompt suite 默认按 base model 的 prefix-completion 方式设计。

### 15.4 一次只改变一个主要变量

例如研究 recency 时，不要同时改变：

```text
实体名
属性类别
目标距离
句长
干扰项数量
语言
```

否则很难判断结果来自哪个因素。

较好的设计是：

```text
固定实体和属性集合；
系统改变 target_distance；
系统改变 num_distractors；
把其他变量放进 variables 里记录。
```

### 15.5 prompt_id 必须稳定

不要每次生成随机 ID。建议：

```text
capital_europe_0001
binding_color_d1_0001
recency_distance3_0001
patch_capital_country_swap_0001
```

这样后续不同模型、不同干预实验的结果可以稳定合并。

---

## 16. 推荐研究流程

建议顺序：

```text
第一步：手写 5–10 条 prompt
  确认 prompt 逻辑和 target_text 没问题。

第二步：用 validate 脚本校验
  检查 JSONL、单 token target、clean/corrupt token 对齐。

第三步：用 Pythia-70M 跑 batch 实验
  先验证整个机制实验 pipeline。

第四步：扩展 prompt suite 到 50–100 条
  加入更多实体、属性、距离和干扰项。

第五步：换到 Qwen3-0.6B / Qwen3-1.7B / Gemma3-1B
  比较不同模型家族和规模下的机制结果。

第六步：做统计汇总
  重点看 condition × layer × intervention 的趋势，而不是单条 prompt。
```

最终你应该追求这类结论：

```text
在 entity-binding 任务中，target_old 条件相比 target_recent 条件，
后层 attention ablation 造成更大的 target_logit_drop，
说明远距离实体-属性绑定更依赖后层上下文路由。
```

而不是只报告：

```text
某条 prompt 下第 15 层很重要。
```

---

## 17. 常见问题

### 17.1 JSONL 文件报错

通常原因：

```text
某一行不是合法 JSON；
使用了单引号而不是双引号；
行末多了逗号；
把整个文件写成了 JSON 数组；
写了注释。
```

JSONL 每一行都必须是完整 JSON 对象，不能写注释。

### 17.2 target_text 不是单 token

解决方式：

```text
1. 给英文目标词加前置空格，例如 " Paris"；
2. 换一个更常见、更短的目标词；
3. 如果必须使用多 token 目标，需要修改 metrics 脚本，改成 multi-token log probability。
```

### 17.3 activation patching 校验失败

原因通常是 clean/corrupt token 长度不一致。

解决方式：

```text
1. 换成长度更接近的 clean/corrupt pair；
2. 手动检查 tokenizer 输出；
3. 后续实现 token alignment，而不是简单按位置 patch。
```

### 17.4 batch 实验太慢

解决方式：

```text
1. 先加 --max-examples 5；
2. 先用 pythia_70m；
3. 减少 prompt 长度；
4. 不保存 attention；
5. 对大模型先只跑 layer_skip 或 logit_lens 的小样本。
```

### 17.5 输出结果文件被覆盖

默认输出文件名通常和 config 的 `outputs.file_prefix` 有关。如果你多次跑不同 prompt suite，建议手动复制结果，或者后续在脚本中加入 `--out` 参数区分文件名。

---

## 18. 最小可行示例

下面是一套从校验到运行的最小流程：

```bash
# 1. 校验 prompt suite
python scripts/11_validate_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl

# 2. 批量 layer skip
python scripts/12_batch_layer_skip_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --max-examples 5

# 3. 查看结果
python - <<'PY'
import pandas as pd

df = pd.read_csv("outputs/results/pythia_70m_batch_layer_skip.csv")
print(df.head())
print(df.groupby("layer")["target_logit_drop"].mean().head())
PY
```

如果这套流程能跑通，就可以继续扩展 prompt suite 或更换更大的模型。
