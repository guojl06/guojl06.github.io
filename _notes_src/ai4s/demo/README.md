# Local LLM Research Package 中文说明

本项目是一个用于本地研究开放权重语言模型的脚手架。它的目标不是部署聊天机器人，而是支持 **mechanistic interpretability / 机制解释实验**：在本地加载模型、读取内部状态、修改中间 activation，并系统性比较不同模型、不同 prompt、不同干预方式下的变化。

核心用途包括：

- 通过 Hugging Face Transformers 在本地加载开放权重模型；
- 查看 hidden states、logits、attention 输出、MLP 输出、近似 residual stream 的中间表示；
- 运行 layer skipping、attention/MLP ablation、activation patching、logit lens、recency/interference probe；
- 使用 JSONL prompt suite 系统性批量运行同一类实验；
- 将 Hugging Face 模型文件预下载并缓存到你指定的本地路径。

建议从小模型开始，例如 `EleutherAI/pythia-70m`。当环境和实验流程跑通后，再切换到 `Qwen/Qwen3-0.6B-Base`、`Qwen/Qwen3-1.7B-Base`、`Qwen/Qwen3-4B-Base` 或 `google/gemma-3-1b-pt`。

---

## 1. 文件结构说明

项目结构如下：

```text
local_llm_research_v2/
  configs/
    _template_model_config.json
    pythia_70m.json
    pythia_160m.json
    qwen3_0_6b_base.json
    qwen3_1_7b_base.json
    qwen3_4b_base.json
    gemma3_1b_pt.json
    gemma3_1b_it.json
    gpt_neox_20b.json

  prompts/
    README_prompts.md
    suites/
      factual_recall_capitals.jsonl
      entity_binding_colors.jsonl
      recency_interference.jsonl
      copy_task.jsonl
      activation_patching_pairs.jsonl
    generated/

  src/
    config_utils.py
    model_utils.py
    hook_utils.py
    metrics.py
    prompt_utils.py
    experiment_utils.py
    plotting.py

  scripts/
    00_check_env.py
    00_download_models.py
    01_check_model.py
    02_forward_cache.py
    03_layer_skip_sweep.py
    04_attn_mlp_ablation.py
    05_activation_patching.py
    06_logit_lens.py
    07_recency_probe.py
    08_plot_results.py
    09_transformerlens_demo.py
    10_nnsight_demo.py
    11_validate_prompt_suite.py
    12_batch_layer_skip_prompt_suite.py
    13_batch_attn_mlp_ablation_prompt_suite.py
    14_batch_activation_patching_prompt_suite.py
    15_batch_logit_lens_prompt_suite.py

  outputs/
    activations/
    results/
    figures/

  logs/
  requirements.txt
  README.md
```

浅显解释：

- `configs/`：模型配置文件。每个 JSON 文件对应一个模型，决定加载哪个 Hugging Face 模型、运行时参数、prompt suite、输出路径等。
- `prompts/suites/`：系统性 prompt 数据集。每个 `.jsonl` 文件是一组实验 prompt，每一行是一条 prompt 样本。
- `src/`：可复用 Python 工具函数。底层加载模型、读取 config、注册 hook、计算指标、读取 prompt suite 等逻辑主要放在这里。
- `scripts/`：命令行实验入口。你平时主要运行这里的脚本。
- `outputs/results/`：实验结果表格，通常是 `.csv`。
- `outputs/activations/`：保存的 activation 张量，通常是 PyTorch `.pt` 文件。
- `outputs/figures/`：生成的图像。
- `logs/`：模型下载记录、缓存记录和其他日志。

---

## 2. 安装 Miniconda

你可以使用已有 Python 环境，但推荐用 Miniconda 创建隔离环境，避免包版本冲突。

### 2.1 Linux 安装 Miniconda

下载并安装：

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
```

重启终端，或者执行：

```bash
source ~/.bashrc
```

检查 conda 是否可用：

```bash
conda --version
```

### 2.2 macOS 安装 Miniconda

Apple Silicon Mac，例如 M1/M2/M3/M4，使用 arm64 安装包：

```bash
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init zsh
```

Intel Mac 使用 x86_64 安装包：

```bash
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init zsh
```

重启终端，或者执行：

```bash
source ~/.zshrc
```

检查 conda 是否可用：

```bash
conda --version
```

---

## 3. 创建 Python 环境

进入项目根目录：

```bash
cd local_llm_research_v2
```

创建并激活环境：

```bash
conda create -n llm-research python=3.11 -y
conda activate llm-research
```

安装依赖：

```bash
pip install -r requirements.txt
```

注意：由于 transform-lens 对 torch 版本有严格限制，如果后续实验无法进行，可以执行如下命令：

```bash
pip uninstall -y torch torchvision torchaudio

pip install --no-cache-dir \
  torch==2.7.1 \
  torchvision==0.22.1 \
  torchaudio==2.7.1
```

检查环境：

```bash
python scripts/00_check_env.py
```

预期结果：

- Linux + NVIDIA GPU：通常应看到 `cuda available: True`。
- Apple Silicon Mac：通常应看到 `mps available: True`。
- 只有 CPU 的机器：CUDA/MPS 不可用，小模型仍可运行，但速度较慢。

---

## 4. Hugging Face 模型缓存

你不需要把模型部署成一个本地服务。你需要的是：**把模型 tokenizer、config、权重文件下载到本地缓存，然后由 Python 脚本直接加载模型。**

第一次使用某个模型时，Hugging Face 会自动下载模型文件。之后再次使用同一个模型，会直接复用本地缓存。

默认缓存路径通常是：

```bash
~/.cache/huggingface/hub
```

本项目支持三种方式自定义模型缓存路径。

### 4.1 方式 A：每次命令显式指定缓存路径

例如将模型缓存到项目内的 `./hf_cache`：

```bash
python scripts/00_download_models.py \
  --config configs/pythia_70m.json \
  --cache-dir ./hf_cache
```

这会在本地生成：

```text
./hf_cache/hub
```

之后运行实验时也使用同一个缓存路径：

```bash
python scripts/01_check_model.py \
  --config configs/pythia_70m.json \
  --cache-dir ./hf_cache
```

### 4.2 方式 B：设置全局环境变量

Linux/macOS：

```bash
export HF_HOME=/Volumes/YourDisk/hf_cache
export HF_HUB_CACHE=/Volumes/YourDisk/hf_cache/hub
```

然后正常运行：

```bash
python scripts/01_check_model.py --config configs/pythia_70m.json
```

如果你希望每次打开终端都生效，可以把这两行写入 `~/.bashrc` 或 `~/.zshrc`。

### 4.3 方式 C：写入 config 文件

在某个 config 文件中加入：

```json
"cache_dir": "/Volumes/YourDisk/hf_cache",
"runtime": {
  "cache_dir": "/Volumes/YourDisk/hf_cache"
}
```

然后运行：

```bash
python scripts/00_download_models.py --config configs/pythia_70m.json
python scripts/01_check_model.py --config configs/pythia_70m.json
```

### 4.4 预下载模型

如果网络不稳定，或者你准备运行较大的模型，建议先预下载模型。

按 config 预下载：

```bash
python scripts/00_download_models.py \
  --config configs/qwen3_0_6b_base.json \
  --cache-dir ./hf_cache
```

直接指定 Hugging Face model id 预下载：

```bash
python scripts/00_download_models.py \
  --model-id EleutherAI/pythia-70m \
  --cache-dir ./hf_cache
```

如果下载过慢或者被终止，有可能是内陆需要镜像，可以在终端先设置默认镜像：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

对于需要授权的模型，例如部分 Gemma checkpoint，需要先登录：

```bash
huggingface-cli login
```

然后到对应模型页面接受 license，再重新下载。

### 4.5 离线模式

模型下载完成后，如果希望强制只读本地缓存，可以在 config 中设置：

```json
"local_files_only": true,
"runtime": {
  "local_files_only": true
}
```

或者设置环境变量：

```bash
export HF_HUB_OFFLINE=1
```

---

## 5. configs 如何使用

每个模型对应 `configs/` 目录下的一个 JSON 文件，例如：

```text
configs/pythia_70m.json
configs/qwen3_0_6b_base.json
configs/gemma3_1b_pt.json
```

config 文件可以理解成“实验入口参数表”：它告诉脚本加载哪个模型、怎么运行模型、使用哪个 prompt、结果保存到哪里。

### 5.1 顶层兼容字段

为了兼容单 prompt 脚本，config 中保留了这些顶层字段：

```json
"model_id": "EleutherAI/pythia-70m",
"device": "auto",
"dtype": "auto",
"attn_implementation": "eager",
"use_cache": false,
"prompt": "The capital of France is",
"target_text": " Paris",
"clean_prompt": "The capital of France is",
"corrupt_prompt": "The capital of Germany is"
```

这些字段不要随意删除，否则旧的单 prompt 脚本可能无法运行。

其中最重要的是：

```json
"model_id": "EleutherAI/pythia-70m"
```

它决定加载哪个 Hugging Face 模型。

### 5.2 结构化字段

新版 config 还包含这些结构化区域：

```json
"model": {...},
"runtime": {...},
"experiments": {...},
"prompts": {...},
"prompt_suite": {...},
"outputs": {...}
```

含义如下：

- `model`：模型元信息，例如模型家族、大小、是否需要授权、推荐用途。
- `runtime`：运行时设置，例如 device、dtype、cache_dir、use_cache、attn_implementation。
- `experiments`：各类机制实验的默认设置。
- `prompts`：单 prompt 或少量内置 prompt 设置。
- `prompt_suite`：批量 prompt suite 设置。
- `outputs`：输出路径和文件名前缀。

批量脚本会读取这一部分：

```json
"prompt_suite": {
  "enabled": true,
  "path": "prompts/suites/factual_recall_capitals.jsonl",
  "format": "jsonl"
}
```

### 5.3 新增模型

复制模板：

```bash
cp configs/_template_model_config.json configs/my_model.json
```

至少修改这些字段：

```json
"name": "my_model",
"model_id": "namespace/model-name",
"model": {
  "id": "namespace/model-name",
  "family": "model_family",
  "architecture_hint": "model.model.layers",
  "variant": "base",
  "size_label": "unknown",
  "requires_auth": false,
  "trust_remote_code": true,
  "memory_tier": "medium"
},
"outputs": {
  "file_prefix": "my_model"
}
```

然后测试：

```bash
python scripts/01_check_model.py --config configs/my_model.json
```

---

## 6. Prompt suites 如何使用

系统性 prompt 放在：

```text
prompts/suites/
```

它们使用 JSONL 格式：**每一行是一个 JSON 对象，每个对象是一条实验 prompt。**

### 6.1 标准 next-token prompt

例如：

```json
{"prompt_id":"capital_0001","task":"factual_recall","condition":"capital_europe","prompt":"The capital of France is","target_text":" Paris","expected_answer":"Paris","variables":{"country":"France","capital":"Paris"},"tags":["factual","capital"]}
```

这个样本表示：给模型输入 `The capital of France is`，追踪目标 token ` Paris` 的 logit。

### 6.2 Activation patching prompt

例如：

```json
{"prompt_id":"patch_capital_0001","task":"activation_patching","condition":"country_swap","clean_prompt":"The capital of France is","corrupt_prompt":"The capital of Germany is","target_text":" Paris","patch_position":-1,"variables":{"clean_subject":"France","corrupt_subject":"Germany"},"tags":["patching","factual"]}
```

这个样本用于 clean/corrupt activation patching：把 clean prompt 中某层某位置的 hidden state patch 到 corrupt prompt 中，观察目标 token ` Paris` 是否恢复。

### 6.3 Prompt suite 规则

建议遵守：

1. `prompt_id` 必须唯一。
2. `target_text` 最好被 tokenizer 切成一个 token。当前指标脚本默认按单 token 计算。
3. 对 activation patching，`clean_prompt` 和 `corrupt_prompt` 的 tokenized length 最好一致。
4. 自变量写入 `variables`，例如 `target_distance`、`num_distractors`、`country`、`category`、`target_order`。
5. 用 `tags` 做后续筛选和分组。

### 6.4 校验 prompt suite

推荐每次批量实验前先校验 prompt suite。

普通校验：

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

只检查 JSONL 结构、不加载 tokenizer：

```bash
python scripts/11_validate_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --no-tokenizer
```

---

## 7. 运行单 prompt 实验

建议先用最小模型跑通流程：

```bash
python scripts/01_check_model.py --config configs/pythia_70m.json
```

### 7.1 Forward cache

保存 logits 和 hidden states：

```bash
python scripts/02_forward_cache.py --config configs/pythia_70m.json
```

输出：

```text
outputs/activations/pythia_70m_forward_cache.pt
```


### 7.2 Layer skip sweep：层跳过实验

该实验用于测试某一层或某一组层对当前 prompt 的因果贡献。实现方式是通过 PyTorch forward hook，把指定 Transformer block 的输出替换为该 block 的输入：

```text
block_out := block_in
```

因此，该层对 residual stream 的更新被移除，相当于让信息流“跳过”该层。

需要注意：这是 **activation-level intervention**，不是实际剪层，也不节省计算。被跳过的层仍然会完成 forward，hook 只是在 forward 后替换输出。该实验适合机制分析，不适合作为推理加速方法。

#### 默认：逐层 sweep 所有层

```bash
python scripts/03_layer_skip_sweep.py \
  --config configs/pythia_70m.json \
  --cache-dir ./hf_cache
```

等价于对每一层分别做一次干预：

```text
实验 1：只跳过第 0 层
实验 2：只跳过第 1 层
实验 3：只跳过第 2 层
...
```

输出：

```text
outputs/results/pythia_70m_layer_skip_sweep_all.csv
```

如果你的脚本仍是旧版本，输出文件名可能是：

```text
outputs/results/pythia_70m_layer_skip_sweep.csv
```

结果表中常见字段包括：

```text
layer                     被跳过的层编号
intervention              干预类型，通常为 skip_block_single
kl_base_to_intervened     原模型输出分布与干预后输出分布的 KL 差异
target_logit_drop         目标 token logit 的下降幅度
top1_base                 原模型 top-1 token
top1_intervened           干预后 top-1 token
top1_change               top-1 token 是否发生变化
```

#### 只测试指定单层

例如只跳过第 4 层：

```bash
python scripts/03_layer_skip_sweep.py \
  --config configs/pythia_70m.json \
  --cache-dir ./hf_cache \
  --layers 4
```

输出：

```text
outputs/results/pythia_70m_layer_skip_sweep_4.csv
```

#### 只 sweep 指定若干层

例如分别测试第 4、5、6 层：

```bash
python scripts/03_layer_skip_sweep.py \
  --config configs/pythia_70m.json \
  --cache-dir ./hf_cache \
  --layers 4,5,6
```

这会分别运行：

```text
只跳过第 4 层
只跳过第 5 层
只跳过第 6 层
```

输出：

```text
outputs/results/pythia_70m_layer_skip_sweep_4_5_6.csv
```

#### 只 sweep 一个连续层段

例如分别测试第 4 到第 8 层：

```bash
python scripts/03_layer_skip_sweep.py \
  --config configs/pythia_70m.json \
  --cache-dir ./hf_cache \
  --layers 4-8
```

等价于：

```bash
--layers 4,5,6,7,8
```

输出：

```text
outputs/results/pythia_70m_layer_skip_sweep_4to8.csv
```

#### 同时跳过多个层

如果加入 `--skip-together`，则不是逐层 sweep，而是在同一次 forward 中同时跳过这些层。

例如同时跳过第 4、5、6 层：

```bash
python scripts/03_layer_skip_sweep.py \
  --config configs/pythia_70m.json \
  --cache-dir ./hf_cache \
  --layers 4,5,6 \
  --skip-together
```

这只会产生一行主要结果，表示：

```text
同时跳过 [4, 5, 6] 三层
```

输出：

```text
outputs/results/pythia_70m_skip_layers_4_5_6_together.csv
```

#### 两种模式的区别

不加 `--skip-together`：

```bash
--layers 4,5,6
```

表示分别测试每一层的单独贡献：

```text
skip layer 4
skip layer 5
skip layer 6
```

适合回答：

```text
哪一层对当前任务最关键？
```

加上 `--skip-together`：

```bash
--layers 4,5,6 --skip-together
```

表示同时移除一段层的贡献：

```text
skip layers [4, 5, 6] together
```

适合回答：

```text
某一段连续层整体是否重要？
跳过中间层段会不会导致输出分布显著改变？
```


### 7.3 Attention / MLP ablation

逐层将 attention 分支或 MLP 分支置零：

```bash
python scripts/04_attn_mlp_ablation.py --config configs/pythia_70m.json
```

输出：

```text
outputs/results/pythia_70m_attn_mlp_ablation.csv
```

### 7.4 Activation patching

将 clean run 的 hidden state patch 到 corrupt run 中：

```bash
python scripts/05_activation_patching.py --config configs/pythia_70m.json
```

输出：

```text
outputs/results/pythia_70m_activation_patching.csv
```

### 7.5 Logit lens

把每层 hidden state 投影到词表 logits：

```bash
python scripts/06_logit_lens.py --config configs/pythia_70m.json
```

输出：

```text
outputs/results/pythia_70m_logit_lens.csv
```

### 7.6 Recency / interference probe

运行简单的 recency 和干扰项探针：

```bash
python scripts/07_recency_probe.py --config configs/pythia_70m.json
```

输出：

```text
outputs/results/pythia_70m_recency_probe.csv
```

---

## 8. 运行 prompt-suite 批量实验

批量实验会对 JSONL prompt suite 中的每一行运行同一种机制干预。

### 8.1 批量 layer skip

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

如果已经指定了缓存路径：

```bash
python scripts/12_batch_layer_skip_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --cache-dir ./hf_cache \
  --max-examples 5
```

### 8.2 批量 attention / MLP ablation

```bash
python scripts/13_batch_attn_mlp_ablation_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/entity_binding_colors.jsonl
```

输出：

```text
outputs/results/pythia_70m_batch_attn_mlp_ablation.csv
```

### 8.3 批量 activation patching

```bash
python scripts/14_batch_activation_patching_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/activation_patching_pairs.jsonl
```

输出：

```text
outputs/results/pythia_70m_batch_activation_patching.csv
```

### 8.4 批量 logit lens

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

## 9. 查看结果

### 9.1 查看 CSV 结果

大多数实验结果保存在：

```text
outputs/results/
```

可以用 Excel、Numbers、VSCode 或 pandas 打开。

例如：

```python
import pandas as pd

df = pd.read_csv("outputs/results/pythia_70m_batch_layer_skip.csv")
print(df.head())
```

常见字段：

- `model_id`：使用的模型。
- `prompt_id`：prompt suite 中的样本 ID。
- `task`：任务类型。
- `condition`：实验条件。
- `intervention`：干预方式，例如 `skip_block`、`zero_attention`、`zero_mlp`、`activation_patch`。
- `layer`：层编号。
- `target_text`：追踪的目标 token。
- `kl_base_to_intervened`：干预后 next-token distribution 的变化幅度。
- `target_logit_drop`：干预后目标 token logit 的下降量。
- `recovery_from_corrupt`：activation patching 中从 corrupt 状态恢复的程度。
- `fraction_of_clean_effect`：标准化 patching 效果。
- `variables_json`：prompt 中记录的实验自变量。

### 9.2 画某个层级指标

例如对 layer skip 的 target logit drop 画图：

```bash
python scripts/08_plot_results.py \
  --csv outputs/results/pythia_70m_layer_skip_sweep.csv \
  --metric target_logit_drop \
  --out outputs/figures/pythia_70m_layer_skip_target_drop.png
```

输出：

```text
outputs/figures/pythia_70m_layer_skip_target_drop.png
```

### 9.3 查看 activation 张量

Forward cache 的输出位于：

```text
outputs/activations/
```

它们是 PyTorch `.pt` 文件，可以这样读取：

```python
import torch

obj = torch.load("outputs/activations/pythia_70m_forward_cache.pt", map_location="cpu")
print(obj.keys())
print(len(obj["hidden_states"]))
print(obj["hidden_states"][0].shape)
```

---

## 10. 推荐运行流程

第一次使用时，建议严格按这个顺序来。

先检查环境：

```bash
python scripts/00_check_env.py
```

下载小模型到本地缓存：

```bash
python scripts/00_download_models.py \
  --config configs/pythia_70m.json \
  --cache-dir ./hf_cache
```

检查模型是否能加载和 forward：

```bash
python scripts/01_check_model.py \
  --config configs/pythia_70m.json \
  --cache-dir ./hf_cache
```

校验 prompt suite：

```bash
python scripts/11_validate_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --cache-dir ./hf_cache
```

运行一个小批量 layer skip 实验：

```bash
python scripts/12_batch_layer_skip_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --cache-dir ./hf_cache \
  --max-examples 5
```

确认流程正常后，再换到较大模型：

```bash
python scripts/00_download_models.py \
  --config configs/qwen3_0_6b_base.json \
  --cache-dir ./hf_cache

python scripts/01_check_model.py \
  --config configs/qwen3_0_6b_base.json \
  --cache-dir ./hf_cache

python scripts/12_batch_layer_skip_prompt_suite.py \
  --config configs/qwen3_0_6b_base.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl \
  --cache-dir ./hf_cache
```

对于 `Qwen3-4B`，建议先少量样本测试，不要一开始保存 attention，也不要跑太长 prompt。

---

## 11. 常见错误

### 11.1 Gated model / 401 / 403

典型报错：

```text
401 Unauthorized
403 Forbidden
You are trying to access a gated repo
```

解决：

```bash
huggingface-cli login
```

然后到 Hugging Face 对应模型页面接受 license，再重新运行下载命令。

### 11.2 MPS 或 CUDA out of memory

可以尝试：

```text
1. 先使用 Pythia-70M；
2. 缩短 prompt；
3. 设置 output_attentions=false；
4. 大模型不要保存所有 hidden states；
5. 批量脚本先加 --max-examples 1；
6. 如果是磁盘不够，把 Hugging Face cache 移到外置硬盘；
7. 如果是显存/内存不够，换更小模型或减少保存内容。
```

注意：把 cache 移到外置硬盘只能解决磁盘空间问题，不能解决 RAM/VRAM 不足。

### 11.3 target_text 不是单 token

当前指标脚本默认 `target_text` 被 tokenizer 切成一个 token。

先运行校验：

```bash
python scripts/11_validate_prompt_suite.py \
  --config configs/pythia_70m.json \
  --prompt-suite prompts/suites/factual_recall_capitals.jsonl
```

如果失败，可以换一个 target 写法，或者修改指标函数以支持 multi-token target。

### 11.4 clean/corrupt token 长度不一致

Activation patching 当前默认 clean prompt 和 corrupt prompt token 对齐。如果长度不一致，需要换 prompt，或实现专门的 token alignment 策略。

---

## 12. 这个包不是什么

这个包不是部署栈。

它不会启动本地 API server，不提供聊天 UI，也不优化高吞吐推理。

如果目标是部署服务，可以使用 Ollama、llama.cpp、vLLM、TGI 等工具。

如果目标是研究模型内部状态、读取中间 activation、做 causal intervention、跑 prompt suite 批量机制实验，那么使用这个包更合适。

---

## 13. 建议研究路线

推荐按以下顺序推进：

```text
阶段 1：Pythia-70M
  目标：跑通环境、模型下载、单 prompt 实验、prompt suite 批量实验。

阶段 2：Pythia-160M 或 Qwen3-0.6B-Base
  目标：验证同一套实验是否能迁移到更现代或稍大模型。

阶段 3：Qwen3-1.7B-Base / Gemma3-1B-pt
  目标：比较不同模型家族在层跳过、MLP/attention ablation、activation patching 上的机制差异。

阶段 4：Qwen3-4B
  目标：在更强模型上复查关键结果，注意控制内存和 prompt 数量。
```

最终建议形成这种结果矩阵：

```text
model × prompt_suite × intervention × metric
```

例如：

```text
Qwen3-0.6B-Base / Qwen3-1.7B-Base / Gemma3-1B-pt
× factual_recall / entity_binding / recency_interference
× layer_skip / zero_attention / zero_mlp / activation_patching
× KL / target_logit_drop / recovery_fraction / top1_change
```

这样得到的结果比单独观察一个 prompt 更稳定，也更接近可以写进报告或论文的分析形式。
