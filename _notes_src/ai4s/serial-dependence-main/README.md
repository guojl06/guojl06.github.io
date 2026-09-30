# serial-dependence

一个用于通过 **DMXAPI 提供的 OpenAI 兼容 `/chat/completions` 接口**，复现并研究实验心理学中**序列依赖效应（serial dependence）**的项目。

本项目以三件事为核心：

1. **可复现**：每次运行都会生成独立的 `outputs/<run_tag>/` 目录，保存本次运行的配置、抽样词表、原始结果和汇总结果。
2. **可追溯**：实验条件、数据来源、抽样方式、模型参数和分析输入都尽量写回输出目录。
3. **实验与分析解耦**：实验脚本只负责生成标准化 run 数据；分析脚本只读取某个 run 目录并输出分析结果，不直接改写实验逻辑。

---

## 1. 项目目标

这个项目通过大模型给词语在某个语义维度上的评分研究语义的序列依赖效应。项目流程：

- 从规范化刺激材料中抽样词项
- 让模型完成单词评分任务（ **Exp1 isolated rating** 与 **Exp2 sequential rating**）
- 为不同维度和控制条件生成统一格式的输出
- 使用多个分析脚本，从不同角度检验序列依赖效应

在当前实现中，主流程由 `src/main.py` 驱动，运行时会合并 `config.yaml` 与命令行参数，自动创建带语义标签的输出目录，并写出 `run_config.yaml`、`sampled_words.csv`、实验结果以及 `combined_overview.csv`。fileciteturn1file30

---

## 2. 支持的实验模式

项目当前支持以下评分维度/模式：

- `concreteness`
- `valence`
- `arousal`
- `emotion`
- `none`
- `mixed`
- `2d`

其中：

- `emotion` 支持 8 种情绪子类型：`anger / anticipation / disgust / fear / joy / sadness / surprise / trust`。具体可见NRC-Emotion-Intensity-Lexicon-v1.txt中。
- `none` 是 number-only 控制条件，不输入词义判断任务，而是要求模型连续生成 1–100 的整数，用于自回归基线分析。（这个实验是用于排除序列依赖的artefacts之一——重复效应，但是由于没有观察到序列依赖效应，所以并没有仔细进行）
- `mixed` 支持两种维度交替出现。（这个实验也是用于排除序列依赖的artefacts，由于没有观察到序列依赖效应，所以并没有仔细进行）
- `2d` 支持在一个更复杂的设置里处理两个维度。

提示词由 `src/prompts.py` 统一管理，system prompt 强制模型只输出 `1–100` 的单个整数；不同任务对应不同 user prompt。fileciteturn1file29

---

## 3. 两个核心实验

### Exp1：isolated rating
- 对单个词进行重复评分
- 可使用 95% CI 半宽作为自适应停止条件
- 输出原始评分和每个词的汇总统计量（均值、标准差、样本数、CI95 半宽）

这一逻辑由 `ExperimentRunner.run_experiment1_isolated()` 与 `ci_utils.py` 配合实现。fileciteturn1file31turn1file20

### Exp2：sequential rating
- 在**同一对话上下文**中顺序呈现多个词
- 支持上下文窗口裁剪
- 支持断点续跑
- 支持紧凑 prompt
- 输出完整顺序评分数据

这一逻辑由 `ExperimentRunner.run_experiment2_sequential()` 实现；续跑与重建 `combined_overview.csv` 的脚本为 `src/continue_exp2.py`。fileciteturn1file31turn1file28

---

## 4. 数据来源

项目当前支持三类刺激源：

### 4.1 旧版 concreteness Excel
适用于 legacy concreteness 数据，读取词列和第六列基准值。fileciteturn1file32

### 4.2 Warriner VAD CSV
适用于人类数据 `valence / arousal / dominance` 规范数据，项目会：

- 读取原始 1–9 分制均值
- 映射到 1–100
- 用 `SD.Sum` 和 `|Mean.M - Mean.F|` 做质量过滤
- 在需要时进行分箱均匀抽样

对应逻辑在 `src/data_loader.py` 与 `src/main.py` 中。fileciteturn1file32turn1file30

### 4.3 NRC Emotion Intensity Lexicon
适用于 `emotion` 任务，项目会：

- 按目标情绪筛选词项
- 将 0–1 强度映射到 1–100
- 进行尽量均匀的抽样

对应逻辑同样在 `src/data_loader.py` 与 `src/main.py`。fileciteturn1file32turn1file30

---

## 5. 当前目录结构

```text
serial-dependence-lyf-experiment/
├── src/
│   ├── main.py
│   ├── continue_exp2.py
│   ├── rerun_exp2_from_prev_exp1.py
│   ├── params.yaml
│   ├── api_client.py
│   ├── experiment.py
│   ├── prompts.py
│   ├── data_loader.py
│   ├── ci_utils.py
│   └── utils.py
├── ana_none/
│   ├── analyze_none.py
│   └── results/
├── ana_prevclass_bar/
│   ├── analyze_prevclass_bar.py
│   ├── batch_prevclass_bar_report.py
│   └── results/
├── ana_prev_n_class/
│   ├── analyze_prevclass_bar.py
│   ├── batch_prev_n_class_report.py
│   ├── params.yaml
│   └── results/
├── ana_norms_bias_sd/
│   ├── analyze_norms_bias_sd.py
│   ├── batch_norms_bias_sd_report.py
│   ├── params.yaml
│   └── results/
├── outputs/
│   └── <run_tag>/
│       ├── run_config.yaml
│       ├── sampled_words.csv
│       ├── exp1_isolated_raw.csv
│       ├── exp1_isolated_summary.csv
│       ├── exp2_sequential_raw.csv
│       ├── none_autoregressive.csv
│       ├── combined_overview.csv
│       └── ...
├── config.yaml
├── requirements.txt
└── README.md
```

---

## 6. 各目录作用说明

### `src/`
主实验逻辑目录。

- `main.py`：主入口，负责读配置、抽样、运行 Exp1/Exp2/none，并输出标准 run 目录。fileciteturn1file30
- `continue_exp2.py`：从已有 Exp2 JSONL 续跑，并自动重建 `combined_overview.csv`。fileciteturn1file28
- `rerun_exp2_from_prev_exp1.py`：复用旧 Exp1 结果，重新生成新的 Exp2。fileciteturn1file35
- `api_client.py`：DMXAPI 客户端封装，支持失败重试与指数退避。fileciteturn1file18
- `experiment.py`：`ExperimentRunner`，实现 Exp1 / Exp2 / none 三类实验过程。fileciteturn1file31
- `prompts.py`：统一管理 system prompt 和各任务 user prompt。fileciteturn1file29
- `data_loader.py`：统一加载与清洗不同刺激源。fileciteturn1file32
- `ci_utils.py`：均值、标准差、CI95 半宽等统计工具。fileciteturn1file20
- `utils.py`：输出目录、CSV/JSONL 保存、抽样等通用函数。fileciteturn1file26

### `ana_none/`
用于 `dimension='none'` 条件的自回归分析。`analyze_none.py` 会读取 `none_autoregressive.csv`，构造 lag-1 对并做线性回归。fileciteturn1file21

### `ana_prevclass_bar/`
用于基于前一试次（或 low/high 分类）的条形图分析，以及批量汇总报告。批处理脚本会扫描 `outputs/`，自动补跑缺失分析并生成 Word 报告。fileciteturn1file24

### `ana_prev_n_class/`
用于更一般的 `n-back` low/high 分类分析，输出 `delta = mean(rating_t | high) - mean(rating_t | low)` 随 n 的变化图。fileciteturn1file27

### `ana_norms_bias_sd/`
用于 **norms-based / bias-removed serial dependence** 分析。脚本会先定义刺激值 `s`，拟合并移除 stimulus-specific bias，再对残差做 DoG 拟合与 permutation test。支持使用 human norms，部分情形也支持使用 Exp1 mean 作为刺激值。fileciteturn1file34turn1file33

### `outputs/`
所有实验运行结果的统一出口。每个 `run_tag` 都应该被视为一个完整、可复查、可独立分析的 run 单元。`main.py` 会自动生成带语义标签的运行目录名。fileciteturn1file30turn1file26

---

## 7. 一个标准 run 会产出什么

一个典型的 `outputs/<run_tag>/` 目录通常包含：

- `run_config.yaml`：本次运行的完整配置快照
- `sampled_words.csv`：本次抽样到的词表
- `exp1_isolated_raw.csv`：Exp1 原始评分
- `exp1_isolated_summary.csv`：Exp1 汇总统计
- `exp2_sequential_raw.csv`：Exp2 顺序评分结果
- `none_autoregressive.csv`：仅 `dimension='none'` 时存在
- `combined_overview.csv`：整合 baseline、Exp1、Exp2 的统一分析输入表

其中 `combined_overview.csv` 是多个分析脚本共享的关键输入。`main.py` 和 `continue_exp2.py` 都会负责生成或重建它。fileciteturn1file30turn1file28

---

## 8. 安装方式

建议使用虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 9. 配置说明

项目默认从 `config.yaml` 读取运行配置，例如：

- `base_url`
- `api_key`
- `model`
- `temperature`
- `which`
- `dimension`
- `n_words`
- `excel_path`
- `ci95_enable`
- `ci95_threshold`
- `max_trials_per_word`

`src/main.py` 会把 **命令行参数覆盖到配置文件之上**。fileciteturn1file30




---

## 10. 运行示例

### 10.1 concreteness 任务
```bash
python src/main.py \
  --which both \
  --dimension concreteness \
  --n_words 400 \
  --excel_path "testing_data/Estimates concreteness words Brysbaert et al.xlsx"
```

### 10.2 valence 任务（Warriner）
```bash
python src/main.py \
  --which both \
  --dimension valence \
  --n_words 400 \
  --excel_path "testing_data/Warriner_et_alemotratings.csv"
```

### 10.3 emotion 任务（NRC）
```bash
python src/main.py \
  --which both \
  --dimension emotion \
  --emotion_type joy \
  --n_words 400 \
  --excel_path "testing_data/NRC-Emotion-Intensity-Lexicon-v1.txt"
```

### 10.4 none 控制条件
```bash
python src/main.py \
  --none \
  --n_trials_none 200 \
  --temperature 0.7
```

### 10.5 从中断处继续 Exp2
```bash
python src/continue_exp2.py \
  --run-dir outputs/<run_tag> \
  --resume
```

### 10.6 复用旧 Exp1，重新跑 Exp2
```bash
python src/rerun_exp2_from_prev_exp1.py \
  --prev_outdir outputs/<old_run_tag> \
  --n_words_exp2 200
```

---

## 11. 分析示例

### 11.1 none 自回归分析
```bash
python ana_none/analyze_none.py --run-dir outputs/<run_tag>
```

### 11.2 prev-class bar 分析
```bash
python ana_prevclass_bar/analyze_prevclass_bar.py --run-dir outputs/<run_tag>
```

### 11.3 批量生成 prev-class 报告
```bash
python ana_prevclass_bar/batch_prevclass_bar_report.py
```

### 11.4 prev-n-class 分析
```bash
python ana_prev_n_class/analyze_prevclass_bar.py \
  --run_dir outputs/<run_tag> \
  --params ana_prev_n_class/params.yaml
```

### 11.5 norms-based / bias-removed SD 分析
```bash
python ana_norms_bias_sd/analyze_norms_bias_sd.py \
  --run-dir outputs/<run_tag> \
  --config ana_norms_bias_sd/params.yaml
```

### 11.6 批量生成 norms-bias-SD 报告
```bash
python ana_norms_bias_sd/batch_norms_bias_sd_report.py
```
---

## 12. 命令行参数与参数文件说明

这一节专门说明各主脚本的 **命令行参数**，以及 `config.yaml` / 各分析目录下 `params.yaml` 的作用。

### 12.1 参数优先级

项目里大体遵循下面这个优先级：

- **命令行参数优先**
- 若命令行未提供，则读取对应的 **YAML 参数文件**
- 若 YAML 也未提供，则使用脚本内部的 **默认值**

对 `src/main.py` 来说，典型顺序是：

```text
命令行参数 > config.yaml > 代码默认值
```

对分析脚本来说，典型顺序是：

```text
命令行参数 > ana_xxx/params.yaml > 代码默认值
```

---

### 12.2 `src/main.py`

这是主实验入口，用于运行 Exp1、Exp2、mixed、2d、emotion 和 `none` 条件。

#### 基本用法

```bash
python src/main.py --config config.yaml
```

也可以直接用命令行覆盖关键参数：

```bash
python src/main.py \
  --config config.yaml \
  --which both \
  --dimension valence \
  --n_words 400 \
  --n_words_exp2 200 \
  --seed 42
```

#### 参数说明

**基础连接与模型参数**

- `--config`：配置文件路径，默认是项目根目录下的 `config.yaml`
- `--base_url`：DMXAPI 的 base URL
- `--api_key`：DMXAPI key。建议不要直接写进将要提交到 Git 的正式配置中
- `--model`：模型名，例如 `gpt-4o-mini`
- `--temperature`：采样温度

**实验控制参数**

- `--which {exp1,exp2,both}`：运行 Exp1、Exp2 或两者都跑
- `--n_words`：抽样词数；通常是 Exp1 的词数，也是 Exp2 默认词池大小
- `--n_words_exp2`：若 `which=both`，可在 Exp1 完成后从 Exp1 的 summary 中再挑选一个子集给 Exp2
- `--seed`：随机种子；不提供时会自动生成
- `--excel_path`：刺激源文件路径，可指向 concreteness Excel、Warriner CSV 或 NRC emotion lexicon

**维度选择参数**

下面几组参数是互斥的，通常只用一种：

- `--dimension concreteness|valence|arousal|emotion|none|mixed|2d`
- `--concreteness`
- `--valence`
- `--arousal`
- `--emotion`
- `--none`
- `--mixed DIM1 DIM2`
- `--2D DIM1 DIM2`

推荐做法：

- 单维任务优先用 `--dimension valence` 这种显式写法
- mixed 用 `--mixed valence arousal`
- 2D 用 `--2D valence arousal`
- emotion 任务同时配合 `--emotion_type`

**emotion 任务参数**

- `--emotion_type`：当 `dimension=emotion` 时指定情绪类型。项目当前支持：
  - `anger`
  - `anticipation`
  - `disgust`
  - `fear`
  - `joy`
  - `sadness`
  - `surprise`
  - `trust`

**Exp1 自适应停止参数**

- `--ci95_enable`：开启基于 95% CI half-width 的自适应停止
- `--ci95_threshold`：CI95 半宽阈值，例如 `0.1`
- `--max_trials_per_word`：Exp1 每个词最多重复评分多少次

**Exp2 序列参数**

- `--exp2_context_window`：Exp2 保留最近多少个已完成 trial 作为上下文；不设则使用完整上下文
- `--n_words_exp2`：Exp2 使用的词数（通常是 Exp1 结果筛选出的子集）
- `--exp2_resume`：如果配置里开启，可在已有 `exp2_sequential_raw.jsonl` 上继续跑
- `--exp2_compact_prompt`：是否使用更紧凑的 Exp2 prompt

**`none` 控制条件参数**

- `--n_trials_none`：`dimension='none'` 时生成多少个连续整数响应

**Warriner 数据过滤 / 分层抽样参数**

- `--warriner_max_sd_sum`：过滤条件，通常表示 `SD.Sum < 阈值`
- `--warriner_max_mf_diff`：过滤条件，通常表示 `|Mean.M - Mean.F| <= 阈值`
- `--warriner_n_bins`：按分箱做均匀抽样时的 bin 数

#### `config.yaml` 参数含义

常见字段如下：

```yaml
base_url: "https://www.dmxapi.cn/v1"
api_key: "YOUR_KEY"
model: "gpt-4o-mini"
temperature: 0.0
which: "both"
n_words: 400
seed: 42
excel_path: "testing_data/Estimates concreteness words Brysbaert et al.xlsx"
ci95_enable: true
ci95_threshold: 0.1
max_trials_per_word: 20
# n_words_exp2: 200
dimension: "concreteness"
```

各字段含义：

- `base_url`：API 服务入口
- `api_key`：API 密钥
- `model`：模型名
- `temperature`：采样温度
- `which`：默认跑哪个实验
- `n_words`：默认抽样词数
- `seed`：默认随机种子
- `excel_path`：默认刺激源路径
- `ci95_enable`：是否在 Exp1 启用自适应停止
- `ci95_threshold`：目标 CI95 半宽
- `max_trials_per_word`：Exp1 单词最大重复次数
- `n_words_exp2`：Exp2 子集大小；不写则默认用全部抽样词
- `dimension`：默认维度

也可以在 `config.yaml` 中补充这些可选字段：

- `emotion_type`
- `n_trials_none`
- `exp2_context_window`
- `exp2_resume`
- `exp2_compact_prompt`
- `warriner_max_sd_sum`
- `warriner_max_mf_diff`
- `warriner_n_bins`
- `mixed_dimensions`
- `two_d_dimensions`

其中：

- `mixed_dimensions: [valence, arousal]` 对应 mixed 条件
- `two_d_dimensions: [valence, arousal]` 对应 2D 条件

---

### 12.3 `src/continue_exp2.py`

用于在某个已有 run 上继续执行 Exp2，适合中断续跑。

#### 用法

```bash
python src/continue_exp2.py --run-dir outputs/<run_tag> --resume
```

#### 参数说明

- `--run-dir`：必须提供，目标 run 目录
- `--config`：项目级 `config.yaml` 路径，用于补充 `api_key` 等
- `--api_key`：命令行覆盖 API key
- `--base_url`：命令行覆盖 base URL
- `--resume`：若发现已有 `exp2_sequential_raw.jsonl`，则从现有进度继续

#### 说明

这个脚本会：

1. 读取 `run_dir/run_config.yaml`
2. 读取 `sampled_words.csv`
3. 读取已有的 `exp2_sequential_raw.jsonl`（若 `--resume`）
4. 继续把后续 trial 补齐
5. 重建 `exp2_sequential_raw.csv` 与 `combined_overview.csv`

---

### 12.4 `src/rerun_exp2_from_prev_exp1.py`

用于复用以前某个 run 的 Exp1 结果，再启动一个新的 Exp2。

#### 用法

```bash
python src/rerun_exp2_from_prev_exp1.py \
  --prev_outdir outputs/<old_run_tag> \
  --config config.yaml \
  --n_words_exp2 200 \
  --seed 42
```

#### 参数说明

- `--prev_outdir`：旧 run 目录，里面至少应有 `sampled_words.csv` 和 `exp1_isolated_summary.csv`
- `--base_url` / `--api_key` / `--model` / `--temperature`：与主实验相同，用于覆盖配置
- `--seed`：新 Exp2 的随机种子
- `--n_words_exp2`：新 Exp2 词数；不设则使用旧 run 的全部词
- `--dimension`：评分维度。当前脚本里可选 `concreteness / valence / arousal`
- `--config`：配置文件路径

适合的场景：

- 已经跑完 Exp1，不想再重复调用 Exp1
- 想基于同一组 Exp1 结果反复测试不同 Exp2 顺序或采样子集

---

### 12.5 `ana_none/analyze_none.py`

用于分析 `dimension='none'` 条件下的自回归数字序列。

#### 用法

```bash
python ana_none/analyze_none.py --run-dir outputs/<run_tag>
```

#### 参数说明

- `--outputs-dir`：输出根目录，默认 `outputs`
- `--run-dir`：指定某个具体 run；不指定时通常会取最新 run
- `--save-scatter-csv`：是否额外保存散点数据 CSV

#### 输出

通常会输出到 `ana_none/results/<run_tag>/`，包括：

- lag-1 散点图
- 线性拟合结果
- 统计摘要 JSON/CSV

---

### 12.6 `ana_bin/analysis_bin.py`

这是经典 `e-R` 分箱分析脚本：

- `e = exp2_rating - exp1_mean`
- `R = exp1_mean[t-1] - exp1_mean[t]`

然后对 `R` 分箱，计算每个箱的平均 `e`，并在分箱曲线上拟合 DoG 或 single-peak。

#### 用法

```bash
python ana_bin/analysis_bin.py --run-dir outputs/<run_tag> --n-bins 20 --save-binned-csv
```

#### 参数说明

- `--outputs-dir`：根输出目录，默认 `outputs`
- `--run-dir`：指定 run 目录；不设时取最新 run
- `--n-bins`：`R` 轴分箱数，默认 `20`
- `--save-binned-csv`：是否保存分箱后的曲线数据 CSV

#### 输出

通常输出到 `ana_bin_result/<run_tag>/`：

- `scatter_with_binned_curve.png`
- `binned_dog_fit.png`
- `binned_curve.csv`（若开启）
- 拟合参数和摘要 JSON

---

### 12.7 `ana_prev_n_class/analyze_prevclass_bar.py`

该脚本做更直接的 prev-class / prev-n-class 分析：

- 先取 `rating_{t-n}` 作为锚点
- 再按 low/high 两类分组
- 比较当前 `rating_t` 的均值差：
  - `delta = mean(rating_t | high) - mean(rating_t | low)`

#### 用法

```bash
python ana_prev_n_class/analyze_prevclass_bar.py \
  --run_dir outputs/<run_tag> \
  --params ana_prev_n_class/params.yaml
```

如果只想跑单个 n：

```bash
python ana_prev_n_class/analyze_prevclass_bar.py \
  --run_dir outputs/<run_tag> \
  --params ana_prev_n_class/params.yaml \
  --k 1
```

#### 参数说明

- `--run_dir`：必须提供，目标 run 目录
- `--params`：参数 YAML 路径
- `--k`：只跑单个 n-back；会覆盖 `params.yaml` 中的 `n_values`
- `--exp2_csv`：显式指定 Exp2 CSV 路径；当自动识别失败时很有用
- `--rating_col`：显式指定评分列名；当自动识别失败时很有用

#### `ana_prev_n_class/params.yaml` 常见字段

从代码看，这个参数文件通常支持以下字段：

- `n_values`：要分析的一组 n，例如 `[-5, -3, -2, -1, 1, 2, 3, 5]`
- `prev_resp_low_max`：将 `rating_{t-n}` 判为 low 的上界
- `prev_resp_high_min`：将 `rating_{t-n}` 判为 high 的下界
- `rating_min`：合法评分最小值，通常为 `1`
- `rating_max`：合法评分最大值，通常为 `100`
- `test`：显著性检验方法，通常是 `welch` 或 `permutation`
- `n_perm`：若 `test=permutation`，置换次数
- `seed`：随机种子
- `dpi`：图像分辨率
- `save_png`：是否输出 PNG 图
- `save_pdf`：是否输出 PDF 图

---

### 12.8 `ana_prevclass_bar/batch_prevclass_bar_report.py`

这个批处理脚本会扫描 `outputs/`，自动补跑缺失的 prev-class 分析，并汇总生成 Word 报告。

#### 用法

```bash
python ana_prevclass_bar/batch_prevclass_bar_report.py \
  --outputs-dir outputs \
  --n-perm 10000 \
  --perm-seed 0
```

#### 参数说明

- `--outputs-dir`：扫描的 outputs 根目录
- `--report-dir`：报告输出目录，默认 `ana_prevclass_bar`
- `--n-perm`：传给 prevclass 分析脚本的置换次数
- `--perm-seed`：置换种子
- `--report-name`：最终 Word 报告文件名
- `--dry-run`：只扫描并打印，不真正运行分析或写报告

---

### 12.9 `ana_norms_bias_sd/analyze_norms_bias_sd.py`

这是 norms-based / bias-removed serial dependence 的主分析脚本。基本思路是：

1. 定义刺激值 `s`
2. 估计 stimulus-specific bias `b(s)`
3. 去除 `b(s)` 后，在残差上对 k-back 序列效应做 DoG 拟合与置换检验

#### 用法

```bash
python ana_norms_bias_sd/analyze_norms_bias_sd.py \
  --run-dir outputs/<run_tag> \
  --config ana_norms_bias_sd/params.yaml
```

只跑单个 k：

```bash
python ana_norms_bias_sd/analyze_norms_bias_sd.py \
  --run-dir outputs/<run_tag> \
  --config ana_norms_bias_sd/params.yaml \
  --k 1
```

emotion 任务若要用 Exp1 mean 作为刺激值：

```bash
python ana_norms_bias_sd/analyze_norms_bias_sd.py \
  --run-dir outputs/<run_tag> \
  --config ana_norms_bias_sd/params.yaml \
  --exp1
```

#### 参数说明

- `--outputs-dir`：输出根目录，默认 `outputs`
- `--run-dir`：指定 run；不设则取最新 run
- `--config`：参数文件路径；不设时默认 `ana_norms_bias_sd/params.yaml`
- `--k`：仅分析某个单独的 k-back
- `--n-perm`：命令行覆盖置换次数
- `--seed`：命令行覆盖随机种子
- `--exp1`：当 run 是 emotion 条件时，使用 Exp1 mean 作为刺激值 `s`

#### `ana_norms_bias_sd/params.yaml` 常见字段

从代码看，这个参数文件支持的关键字段包括：

**k-back 与置换控制**

- `k_values`：要 sweep 的 k-back 列表
- `n_permutations`：置换检验次数
- `random_seed`：随机种子
- `make_scatter_for_all_k`：是否为所有 k 都输出散点图；否则通常只保证 1-back 图

**norms 数据源**

- `norms_csv_path`：Warriner norms 文件路径
- `emotion_norms_path`：emotion norms 文件路径；如果不设，代码会回退到 `excel_path` 或默认 NRC 路径
- `default_norm_dimension`：当需要从 norms 中选维度时的默认值
- `default_emotion_type`：当 emotion 类型未明确给出时的默认情绪类型

**bias removal 方法**

- `bias_method`：去除 stimulus-specific bias 的方法，可见代码支持：
  - `bin`
  - `poly`
  - `kernel`
  - `knn_kernel`（或 `knn`）

对应参数：

- `bin_smooth_window`：`bias_method=bin` 时的平滑窗口
- `poly_degree`：`bias_method=poly` 时的多项式阶数
- `kernel_bandwidth`：`bias_method=kernel` 时的固定带宽
- `knn_k`：`bias_method=knn_kernel` 时的近邻数
- `knn_alpha`：自适应带宽缩放参数
- `knn_min_bandwidth`：最小带宽下限
- `knn_curve_n`：绘制 bias 曲线时的采样点数量

**delta 分箱图参数**

- `delta_bin_n_bins`：对 delta 分箱时的 bin 数
- `delta_bin_min_count`：每个 bin 的最小样本数阈值

#### 如何理解这些参数

- `bias_method=bin`：最稳妥，通常适合作为初始基线
- `bias_method=poly`：适合偏差曲线较平滑且可用低阶多项式近似时
- `bias_method=kernel`：适合想做平滑非参数拟合时
- `bias_method=knn_kernel`：适合刺激分布不均匀时，自适应带宽更灵活
- `n_permutations` 越大越稳，但耗时越久
- `k_values` 既可以看近邻效应，也可以用负 k 做控制比较

---

### 12.10 `ana_norms_bias_sd/batch_norms_bias_sd_report.py`

这个脚本会扫描多个 run，自动补跑缺失的 norms-bias 分析，并生成汇总 Word 报告。

#### 用法

```bash
python ana_norms_bias_sd/batch_norms_bias_sd_report.py \
  --outputs-dir outputs \
  --config ana_norms_bias_sd/params.yaml \
  --report-name norms_bias_sd_report.docx
```

#### 参数说明

- `--outputs-dir`：扫描的输出目录
- `--report-dir`：报告输出目录，默认 `ana_norms_bias_sd`
- `--config`：分析参数文件路径
- `--report-name`：最终 Word 报告名称
- `--dry-run`：只扫描不执行
- `--force`：即使已有结果也强制重跑

---

### 12.11 `ana_two_sources_bias/analyze_two_sources_bias.py`

这个脚本将总体偏差拆解为两部分：

- **stimulus-specific bias**
- **serial DoG bias**

并对不同 k-back 条件做 sweep。

#### 用法

```bash
python ana_two_sources_bias/analyze_two_sources_bias.py \
  --run-dir outputs/<run_tag> \
  --config ana_two_sources_bias/params.yaml
```

只跑单个 k：

```bash
python ana_two_sources_bias/analyze_two_sources_bias.py \
  --run-dir outputs/<run_tag> \
  --config ana_two_sources_bias/params.yaml \
  --k 1
```

#### 参数说明

- `--outputs-dir`：输出根目录
- `--run-dir`：指定 run；不设时取最新 run
- `--config`：参数文件路径，默认 `ana_two_sources_bias/params.yaml`
- `--k`：仅分析单个 k-back
- `--n-perm`：覆盖 `n_permutations`
- `--seed`：覆盖 `random_seed`
- `--target-dimension`：若 run 含 `asked_dimension`，则仅分析指定维度

#### `ana_two_sources_bias/params.yaml` 常见字段

从代码读取到的关键字段有：

- `k_values`：要分析的 k-back 列表
- `n_permutations`：置换次数
- `random_seed`：随机种子
- `make_scatter_for_all_k`：是否为所有 k 生成图
- `target_dimension`：对 mixed / 2d 输出做维度筛选时使用

这几个字段通常就足以完成批量 sweep。

---

### 12.12 `ana_two_sources_bias/batch_two_sources_bias_report.py`

用于扫描多个 run，补跑缺失的 two-sources bias 分析，并生成 Word 汇总报告。

#### 用法

```bash
python ana_two_sources_bias/batch_two_sources_bias_report.py \
  --outputs-dir outputs \
  --config ana_two_sources_bias/params.yaml
```

#### 参数说明

- `--outputs-dir`：扫描的 outputs 根目录
- `--report-dir`：最终报告目录，默认 `ana_two_sources_bias`
- `--config`：参数文件路径
- `--report-name`：报告文件名，默认 `two_sources_bias_report.docx`
- `--dry-run`：只扫描，不执行分析与报告生成


---

### 12.13 一个推荐的工作流

```bash
# 1) 跑主实验
python src/main.py --config config.yaml

# 2) 必要时续跑 Exp2
python src/continue_exp2.py --run-dir outputs/<run_tag> --resume

# 3) 做经典 e-R 分箱分析
python ana_bin/analysis_bin.py --run-dir outputs/<run_tag> --n-bins 20 --save-binned-csv

# 4) 做 prev-n-class 分析
python ana_prev_n_class/analyze_prevclass_bar.py --run_dir outputs/<run_tag> --params ana_prev_n_class/params.yaml

# 5) 做 norms-bias serial dependence 分析
python ana_norms_bias_sd/analyze_norms_bias_sd.py --run-dir outputs/<run_tag> --config ana_norms_bias_sd/params.yaml

# 6) 批量生成报告
python ana_norms_bias_sd/batch_norms_bias_sd_report.py --outputs-dir outputs --config ana_norms_bias_sd/params.yaml

# 7) 若检测到序列依赖效应，需要排除伪迹，做 none 控制分析
python ana_none/analyze_none.py --run-dir outputs/<run_tag>
```

