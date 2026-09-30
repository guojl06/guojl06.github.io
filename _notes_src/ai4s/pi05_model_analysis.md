# Pi0.5 模型原理深度解析

> 基于 [openpi-core](https://github.com/Physical-Intelligence/openpi) 开源代码的完整分析，涵盖 Pi0、Pi0.5、Pi0-FAST 及其他变体。

---

## 目录

- [一、整体架构全景](#一整体架构全景)
- [二、视觉编码器 — SigLIP ViT](#二视觉编码器--siglip-vit)
- [三、双专家 Transformer — Gemma](#三双专家-transformer--gemma)
- [四、Pi0.5 的两大创新点](#四pi05-的两大创新点)
- [五、Flow Matching 训练详解](#五flow-matching-训练详解)
- [六、注意力掩码机制详解](#六注意力掩码机制详解)
- [七、推理过程详解](#七推理过程详解)
- [八、数据流水线](#八数据流水线)
- [九、微调策略](#九微调策略)
- [十、优化器与训练超参](#十优化器与训练超参)
- [十一、四种架构范式总览](#十一四种架构范式总览)
- [十二、模型架构深度对比](#十二模型架构深度对比)
- [十三、状态与动作表示对比](#十三状态与动作表示对比)
- [十四、训练 Loss 对比](#十四训练-loss-对比)
- [十五、推理过程对比](#十五推理过程对比)
- [十六、Tokenizer 对比](#十六tokenizer-对比)
- [十七、训练配置对比](#十七训练配置对比)
- [十八、PolaRiS 与 RoboArena 基线对比](#十八polaris-与-roboarena-基线对比)
- [十九、选择指南](#十九选择指南)

---

## 一、整体架构全景

Pi0.5 是一个 **视觉-语言-动作 (VLA)** 模型，核心思路是：**复用预训练视觉语言模型的理解能力，通过 Flow Matching 生成连续动作序列**。

```
输入侧                                         模型核心                                    输出侧
+--------------+                           +----------------------------+
| 3张224x224   |  +---------+  256 token/图  |  PaliGemma 2B (Expert 0)   |
| RGB图像      |->| SigLIP  | -------------> |  处理: 图像 + 语言 + 状态    |
| (base_0_rgb  |  | ViT     |               |  18层 x 2048维 x 8头       |
|  left_wrist  |  | So400m  |               +----------+-----------------+
|  right_wrist)|  | /14     |                          | 共享 Multi-Head Attention
+--------------+  +---------+                          |
                                                      v
+--------------+                           +----------------------------+
| 语言指令      |-> SentencePiece --------->|  共享 Attention 层           |
| (e.g. "pick  |   Tokenizer              |  Q/K/V 在两个专家间拼接       |
|  up")        |                          +----------+-----------------+
+--------------+                                     |
                                                      |
+--------------+  +--------------+                   |
| 机器人状态    |->|离散化->文本拼接| --- (Pi0.5) ---->|    PaliGemma前缀 token
| (关节角等)   |  | np.digitize  |                   |
+--------------+  +--------------+                   |
                                                      |
                           +----------------------------+
噪声动作 + 时间步           |  Action Expert 300M (Expert 1) |            +----------------+
x_t = t*noise+(1-t)*action |  处理: 噪声动作序列             |----------->| v_t (速度场预测) |
                ---------->|  18层 x 1024维 x 8头           |            |    | Euler积分
                           |  + adaRMSNorm 注入时间步        |            | x_{t+dt}=x_t+dt*v_t
                           +----------------------------+            +----------------+
                                                                  最终得到去噪动作序列
```

## 二、视觉编码器 — SigLIP ViT

定义在 `src/openpi/models/siglip.py`。

### 架构细节

- **变体**: So400m（约4亿参数），patch size 14x14
- **输入**: 224x224x3 RGB 图像
- **Patch 提取**: Conv 层，kernel=14, stride=14 -> 16x16 = 256 个 patch
- **位置编码**: 2D 正弦-余弦（`sincos2d`），**非学习型**
- **编码器**: 标准 ViT Encoder，27 层，1152 维，16 头注意力
- **池化**: `pool_type="none"` — 保留所有 256 个空间 token，**不做聚合**
- **精度**: patch 提取和位置编码在 float32 下完成，之后转换为 `bfloat16`
- **内存优化**: 使用 `nn.scan`（参数共享扫描）+ `nn.remat`（梯度检查点）

### 为什么保留所有 token?

机器人操作需要精细的空间理解（如定位物体），全局池化会丢失空间信息。256 token 保留完整的空间网格特征。

### 初始化

见 `src/openpi/models/pi0.py:81-91`：

```python
img = nnx_bridge.ToNNX(
    _siglip.Module(num_classes=paligemma_config.width,  # 2048，投影到PaliGemma维度
                   variant="So400m/14", pool_type="none", scan=True, dtype_mm=config.dtype))
img.lazy_init(next(iter(config.fake_obs().images.values())), train=False, rngs=rngs)
```

SigLIP 只在 **推理模式** 下运行 (`train=False`)，即视觉编码器在训练时**冻结**。

## 三、双专家 Transformer — Gemma

这是模型的核心，定义在 `src/openpi/models/gemma.py`。

### 3.1 双专家机制

```python
llm = nnx_bridge.ToNNX(
    _gemma.Module(
        configs=[paligemma_config, action_expert_config],  # 两个配置
        embed_dtype=config.dtype,
        adarms=config.pi05,  # Pi0.5启用自适应归一化
    ))
```

两个专家共享 **同一个 Transformer 结构**，但在每层中有 **独立的参数**：

| 参数 | Expert 0 (PaliGemma) | Expert 1 (Action Expert) |
|------|----------------------|--------------------------|
| width (d_model) | 2048 | 1024 |
| depth (层数) | 18 | 18 |
| mlp_dim | 16384 | 4096 |
| num_heads | 8 | 8 |
| num_kv_heads | 1 (GQA) | 1 (GQA) |
| head_dim | 256 | 256 |
| 参数量 | ~2B | ~300M |
| 处理数据 | 图像 + 语言 token | 噪声动作 + 时间步 |
| 初始化来源 | PaliGemma 预训练 | 从零初始化 |

### 3.2 共享注意力的具体实现

关键在 `src/openpi/models/gemma.py:158-249` 的 `Attention` 类：

```python
# 每个 expert 独立计算 Q/K/V
for i, (x, config) in enumerate(zip(xs, self.configs)):
    q, k, v = ...  # 使用各 expert 自己的权重

# 然后在维度1上拼接（token 维度）
q, k, v = (jnp.concatenate(y, axis=1) for y in zip(*qkvs))

# 统一计算注意力
logits = jnp.einsum("BTKGH,BSKH->BKGTS", q, k)  # [B, num_kv_heads, T, S]
probs = softmax(masked_logits)

# 输出后，按各 expert 的 token 长度切分
out_einsum = lora.Einsum(...)  # 每个 expert 有自己的输出投影
```

这意味着：**两个 expert 的 token 在同一个注意力矩阵中互相可见**，实现了跨模态的信息融合。

### 3.3 Grouped Query Attention (GQA)

两个 expert 都使用 `num_kv_heads=1`，即 **8 个 query head 共享 1 组 key/value head**：
- Q: `[B, T, 8, 256]` -> reshape 为 `[B, T, 1, 8, 256]`
- K/V: `[B, T, 1, 256]`
- 这极大减少了 KV Cache 大小，对推理效率至关重要。

### 3.4 RoPE 位置编码

见 `src/openpi/models/gemma.py:424-440`：标准 Rotary Position Embedding，`max_wavelength=10000`。值得注意的是 RoPE 在 float32 下计算后立即转回 bfloat16。

## 四、Pi0.5 的两大创新点

### 4.1 状态输入离散化 -> 语言 token

在 Pi0 中，机器人状态通过一个线性层投影后作为后缀 token；在 Pi0.5 中，状态被**离散化为文本**，混入语言 token 成为前缀的一部分。

见 `src/openpi/models/tokenizer.py:22-29`：

```python
# 将连续状态值离散化到 256 个 bin
discretized_state = np.digitize(state, bins=np.linspace(-1, 1, 256 + 1)[:-1]) - 1
state_str = " ".join(map(str, discretized_state))
full_prompt = f"Task: {cleaned_text}, State: {state_str};\nAction: "
tokens = self._tokenizer.encode(full_prompt, add_bos=True)
```

**为什么这样做?**

1. **统一输入格式**: 状态和语言都变成离散 token，简化了模型架构
2. **利用预训练知识**: PaliGemma 在大量文本上预训练，处理离散 token 能力更强
3. **无需额外投影层**: Pi0 需要 `state_proj` 和 `action_time_mlp_in/out`，Pi0.5 省略了这些

Pi0.5 的 `embed_suffix` 方法中，**不再有 state token**，只有 action tokens。

### 4.2 adaRMSNorm — 自适应归一化注入时间步

这是 Pi0.5 最核心的架构改进。

**Pi0 的方式** — 简单 MLP 拼接（`src/openpi/models/pi0.py:170-178`）：

```python
# 时间步编码 repeat 到每个动作 token
time_tokens = einops.repeat(time_emb, "b emb -> b s emb", s=action_horizon)
# 在特征维度上拼接
action_time_tokens = jnp.concatenate([action_tokens, time_tokens], axis=-1)
# 通过 MLP 融合 (2*width -> width)
action_time_tokens = self.action_time_mlp_in(action_time_tokens)  # Linear(2w, w)
action_time_tokens = swish(action_time_tokens)
action_time_tokens = self.action_time_mlp_out(action_time_tokens)  # Linear(w, w)
```

问题：时间步信息只在输入层注入一次，深层可能"遗忘"。

**Pi0.5 的方式** — adaRMSNorm（`src/openpi/models/gemma.py:113-131`）：

时间步编码（`src/openpi/models/pi0.py:161-168`）：

```python
time_emb = posemb_sincos(timestep, width, min_period=4e-3, max_period=4.0)
time_emb = self.time_mlp_in(time_emb)    # Linear(w, w)
time_emb = swish(time_emb)
time_emb = self.time_mlp_out(time_emb)   # Linear(w, w)
time_emb = swish(time_emb)
# time_emb 作为全局条件向量，注入到每个 Block 的 RMSNorm
```

RMSNorm 内部：

```python
# cond = time_emb -> 通过 Dense 生成 3 个调制信号
modulation = Dense(x.shape[-1] * 3)(cond)  # [batch, 3*width]
scale, shift, gate = split(modulation, 3, axis=-1)

# 归一化 + 调制
normed_inputs = x * rsqrt(mean(x^2) + eps)
normed_inputs = normed_inputs * (1 + scale) + shift  # 自适应缩放和平移
```

门控残差连接（`src/openpi/models/gemma.py:453-459`）：

```python
def _gated_residual(x, y, gate):
    if gate is None:
        return x + y           # Pi0: 简单残差
    return x + y * gate        # Pi0.5: 门控残差，gate 由 adaRMSNorm 生成
```

**adaRMSNorm 在每层都注入时间步信息**，而且通过 scale/shift/gate 三重调制，比简单拼接更灵活。这类似于 DiT (Diffusion Transformer) 的 conditioning 机制，但作用于 RMSNorm 而非 LayerNorm。

## 五、Flow Matching 训练详解

### 5.1 数学原理

Flow Matching 训练一个向量场 `v_theta(x_t, t)` 来建模从噪声分布到数据分布的变换。定义一条从噪声到数据的线性插值路径：

```
x_t = t * noise + (1 - t) * action,    t in [0, 1]
```

对应的目标速度场：

```
u_t = d(x_t)/dt = noise - action
```

训练目标就是让网络预测这个速度场：

```
loss = ||v_theta(x_t, t, obs) - (noise - action)||^2
```

推理时从 t=1（纯噪声）出发，沿 ODE 轨迹积分到 t=0 得到动作。

### 5.2 时间步采样策略

`src/openpi/models/pi0.py:197`：

```python
time = jax.random.beta(time_rng, 1.5, 1, batch_shape) * 0.999 + 0.001
```

- 使用 **Beta(1.5, 1)** 分布采样，不是均匀分布
- Beta(1.5, 1) 的 PDF: `f(t) ~ t^0.5`，偏向 t=1（噪声端）
- 再缩放到 [0.001, 1.0] 范围，避免 t=0 和 t=1 的边界问题
- **为什么偏向噪声端?** 在 Diffusion/Flow Matching 中，t 接近 1 时预测更难（输入几乎是纯噪声），需要更多训练样本。

### 5.3 Loss 计算

`src/openpi/models/pi0.py:189-214` 完整流程：

```python
def compute_loss(self, rng, observation, actions, *, train=False):
    # 1. 数据增强 (训练时)
    observation = preprocess_observation(preprocess_rng, observation, train=train)

    # 2. Flow Matching 采样
    noise = N(0, I)                          # 标准高斯噪声
    time ~ Beta(1.5, 1)                      # 时间步采样
    x_t = time * noise + (1 - time) * actions  # 插值
    u_t = noise - actions                      # 目标速度场

    # 3. 编码前缀（图像 + 语言）
    prefix_tokens, prefix_mask, prefix_ar_mask = embed_prefix(observation)

    # 4. 编码后缀（噪声动作 + 时间步）
    suffix_tokens, suffix_mask, suffix_ar_mask, adarms_cond = embed_suffix(observation, x_t, time)

    # 5. 拼接 -> Transformer 前向传播
    input_mask = concat(prefix_mask, suffix_mask)
    ar_mask = concat(prefix_ar_mask, suffix_ar_mask)
    attn_mask = make_attn_mask(input_mask, ar_mask)
    (prefix_out, suffix_out), _ = llm([prefix_tokens, suffix_tokens], mask=attn_mask, ...)

    # 6. 预测速度场并计算 MSE Loss
    v_t = action_out_proj(suffix_out[:, -action_horizon:])
    return mean((v_t - u_t)^2, axis=-1)  # 每个动作维度上的 MSE
```

## 六、注意力掩码机制详解

`src/openpi/models/pi0.py:19-44` 的 `make_attn_mask` 实现了一种灵活的混合注意力模式。

**核心思想**：`ar_mask` (auto-regressive mask) 控制注意力块边界。`cumsum(ar_mask)` 相同的 token 互互相可见。

Pi0.5 的序列布局：

```
Token:    [img1_0...img1_255] [img2_0...img2_255] [img3_0...img3_255] [lang_0...lang_N] | [act_0] [act_1] ... [act_49]
ar_mask:  [0  ...  0        ] [0  ...  0         ] [0  ...  0         ] [0 ...  0      ]   [1]      [0]          [0]
cumsum:   [1  ...  1        ] [1  ...  1         ] [1  ...  1         ] [1 ...  1      ]   [2]      [2]          [2]
```

- **前缀** (ar_mask 全 0): cumsum 全为 1 -> 所有前缀 token 互相可见（**双向注意力**）
- **后缀** (ar_mask=[1,0,0,...,0]): cumsum 从 2 开始 -> 所有后缀 token 互相可见
- **跨域**: cumsum(suffix) >= cumsum(prefix) -> 后缀能 attend 前缀, 但前缀不能 attend 后缀
- **动作因果性**: 在后缀内部，如果用 `[1,0,0,...]` 则所有动作 token 互相可见。实际上这里动作 token 不是因果的，而是**同时生成**的。

## 七、推理过程详解

`src/openpi/models/pi0.py:217-279`

### 7.1 KV Cache 优化

推理分两阶段：

**阶段1 — 前缀预填充**（只做一次）：

```python
prefix_tokens, prefix_mask, prefix_ar_mask = embed_prefix(observation)
prefix_attn_mask = make_attn_mask(prefix_mask, prefix_ar_mask)
_, kv_cache = llm([prefix_tokens, None], mask=prefix_attn_mask, positions=...)
# kv_cache 保存了所有 18 层的 K, V，shape: [18, B, prefix_len, 1, 256]
```

**阶段2 — 去噪循环**（迭代 num_steps 次）：

```python
def step(x_t, time):
    suffix_tokens, suffix_mask, suffix_ar_mask, adarms_cond = embed_suffix(observation, x_t, time)
    # 后缀 attend 到 前缀 + 后缀自身
    full_attn_mask = concat(prefix_attn_mask, suffix_attn_mask, axis=-1)
    (_, suffix_out), _ = llm([None, suffix_tokens], mask=full_attn_mask,
                              positions=positions, kv_cache=kv_cache, ...)
    v_t = action_out_proj(suffix_out[:, -action_horizon:])
    return x_t + dt * v_t, time + dt
```

每次 step 只需计算 suffix 的 Q/K/V（约 50 个 token），prefix 的 K/V 从 cache 读取。默认 `num_steps=10` 步。

### 7.2 位置计算

```python
positions = jnp.cumsum(input_mask, axis=1) - 1  # 累积有效 token 数 - 1
```

Padding token 的 position 保持和前一个有效 token 相同，确保 RoPE 编码正确。

## 八、数据流水线

### 8.1 数据变换管线

训练数据经过三级变换（见 `src/openpi/training/config.py:75-81`）：

```
原始数据 (LeRobot格式)
    |
    v RepackTransform: 重命名字段匹配模型期望格式
    |   e.g. "observation.images.top" -> "images/base_0_rgb"
    v
数据变换 (robot-specific)
    |   e.g. AlohaInputs: 适配关节角度范围、delta actions
    v Normalize / Unnormalize
    |   z-score: (x - mean) / (std + 1e-6)
    |   或 quantile: (x - q01) / (q99 - q01) * 2 - 1  <- 映射到 [-1, 1]
    v
模型变换 (model-specific)
    |   ResizeImages(224, 224)
    |   TokenizePrompt (PaligemmaTokenizer)
    |   PadStatesAndActions(32)  <- 填充到 action_dim
    v
Observation 对象 -> 输入模型
```

### 8.2 两种归一化方式

定义在 `src/openpi/transforms.py:115-181`：

- **Z-score** (Pi0 使用): `(x - mean) / (std + 1e-6)` — 对异常值敏感
- **分位数归一化** (Pi0.5 / FAST 使用): `(x - q01) / (q99 - q01) * 2 - 1` — 映射到 [-1, 1]，对异常值鲁棒

分位数归一化的好处是状态和动作都映射到 [-1, 1] 范围内，这与 Pi0.5 的离散化策略（256 bins in [-1, 1]）完美匹配。

### 8.3 Delta Actions

大多数机器人的原始数据是**绝对关节角度**，但模型训练时使用**增量动作**（相对当前状态的偏移量）。见 `src/openpi/training/config.py:263-268`：

```python
if use_delta_joint_actions:
    delta_action_mask = make_bool_mask(6, -1, 6, -1)  # 前6维和第13维用delta，其余绝对值
    data_transforms.push(
        inputs=[DeltaActions(delta_action_mask)],   # 训练时: action = target - current
        outputs=[AbsoluteActions(delta_action_mask)], # 推理时: target = action + current
    )
```

## 九、微调策略

### 9.1 Full Fine-tuning

```python
model = Pi0Config(pi05=True)  # 全部参数可训练
weight_loader = CheckpointWeightLoader("gs://openpi-assets/checkpoints/pi05_base/params")
```

加载预训练权重后，所有参数都参与训练。

### 9.2 LoRA 微调

```python
model = Pi0Config(
    pi05=True,
    paligemma_variant="gemma_2b_lora",      # PaliGemma 加 LoRA (rank=16)
    action_expert_variant="gemma_300m_lora",  # Action Expert 加 LoRA (rank=32)
)
freeze_filter = model.get_freeze_filter()  # 冻结除了 LoRA 参数外的所有权重
ema_decay = None  # LoRA 微调时关闭 EMA
```

LoRA 的实现见 `src/openpi/models/lora.py`：
- 在 Attention 的 QKV 投影 (`Einsum`) 和 FFN (`FeedForward`) 中添加低秩矩阵
- `result = W*x + (A*(B*x)) * (alpha / rank)`
- 支持 RSLoRA (Rank-Stabilized LoRA): scaling = alpha / sqrt(rank)

### 9.3 冻结策略

`src/openpi/models/pi0_config.py:88-117` 的 `get_freeze_filter`：
- 如果 `paligemma_variant` 含 "lora": 冻结 PaliGemma 的 LLM 权重（除 LoRA）
- 如果 `action_expert_variant` 含 "lora": 冻结 Action Expert 的 LLM 权重（除 LoRA）
- **视觉编码器 (SigLIP) 始终冻结**

## 十、优化器与训练超参

`src/openpi/training/optimizer.py` + `src/openpi/training/config.py` 中的 Pi0.5 默认配置：

| 超参数 | 默认值 | Pi0.5 典型值 |
|--------|--------|-------------|
| 优化器 | AdamW | AdamW(b1=0.9, b2=0.95, clip_norm=1.0) |
| 学习率 | CosineDecay(peak=2.5e-5) | CosineDecay(warmup=10000, peak=5e-5) |
| Batch size | 32 | 64-256 |
| 训练步数 | 30,000 | 20,000-100,000 |
| EMA 衰减 | 0.99 | 0.999 |
| 权重衰减 | 1e-10 | 1e-10 |
| 精度 | bfloat16 | bfloat16 |

学习率调度（`src/openpi/training/optimizer.py:16-31`）：

```
warmup 阶段: 从 peak_lr/(warmup_steps+1) 线性增长到 peak_lr
decay 阶段: 余弦衰减到 decay_lr
```

---

# 架构对比篇

## 十一、四种架构范式总览

```
                        +----------------------------------------------------+
                        |             OpenPI 模型家族全景                      |
                        +----------------------------------------------------+

  Pi0 (初代)                     Pi0.5 (改进版)
  +-----------------+            +-----------------+
  |  SigLIP ViT     |            |  SigLIP ViT     |
  |  | image tokens  |            |  | image tokens  |
  |  PaliGemma 2B   |< 共享Attn-> |  PaliGemma 2B   |
  |  +               |            |  +               |
  |  Action 300M    |            |  Action 300M    |
  |  (独立专家)       |            |  (独立专家+adaRMS)|
  |                  |            |                  |
  |  状态: 连续投影   |            |  状态: 离散化为文本 |
  |  时间: MLP拼接    |            |  时间: adaRMSNorm |
  |  动作: Flow Match|            |  动作: Flow Match |
  +-----------------+            +-----------------+
        | 连续动作                      | 连续动作

  Pi0-FAST (自回归版)              RoboArena Baselines
  +-----------------+            +---------------------+
  |  SigLIP ViT     |            |  SigLIP ViT         |
  |  | image tokens  |            |  | image tokens      |
  |  PaliGemma 2B   |            |  PaliGemma 2B       |
  |  (仅一个模型)     |            |  (仅一个模型)         |
  |                  |            |                      |
  |  动作: 自回归生成  |            |  动作: 自回归生成      |
  |  FAST Tokenizer  |            |  Binning / FAST / FSQ|
  |  (VQ-VAE变体)    |            |  多种tokenizer对比    |
  +-----------------+            +---------------------+
        | 离散token->连续               | 离散token->连续
```

## 十二、模型架构深度对比

### 12.1 Transformer 骨干对比

| 维度 | Pi0 | Pi0.5 | Pi0-FAST |
|------|-----|-------|----------|
| **LLM 实现** | `gemma.py` (多专家版) | `gemma.py` (多专家版) | `gemma_fast.py` (单模型版) |
| **模型数量** | 2 (PaliGemma + Action Expert) | 2 (PaliGemma + Action Expert) | **1** (仅 PaliGemma) |
| **PaliGemma** | Gemma 2B (2048维, 18层) | Gemma 2B (2048维, 18层) | Gemma 2B (2048维, 18层) |
| **Action Expert** | Gemma 300M (1024维, 18层) | Gemma 300M (1024维, 18层) | **无** |
| **总参数量** | ~2.3B (可训练) | ~2.3B (可训练) | **~2B** (可训练) |
| **共享注意力** | Q/K/V 跨专家拼接 | Q/K/V 跨专家拼接 | 不涉及 (单模型) |
| **归一化** | RMSNorm | **adaRMSNorm** (条件调制) | RMSNorm |
| **位置编码** | RoPE | RoPE | RoPE |
| **KV Cache** | 跨专家共享 | 跨专家共享 | 单模型独立 |

### 12.2 为什么 FAST 不需要 Action Expert?

Pi0/Pi0.5 需要 Action Expert 是因为 **Flow Matching 要求在连续空间中预测速度场**，这需要专门的动作处理模块。而 FAST 的动作被离散化为 token 后，**直接复用 PaliGemma 的语言生成能力**——生成动作 token 就像生成文本一样，不需要额外模块。

`gemma_fast.py` 的 Block 结构明显比 `gemma.py` 的 Block 简单：
- **无** adaRMSNorm 条件调制
- **无** 门控残差连接
- 标准 Pre-Norm Transformer + 简单残差

### 12.3 与 Pi0 和 Pi0-FAST 的完整参数对比

| 维度 | Pi0 | Pi0.5 | Pi0-FAST |
|------|-----|-------|----------|
| 视觉编码器 | SigLIP So400m | SigLIP So400m | SigLIP So400m |
| LLM 骨干 | Gemma 2B | Gemma 2B | Gemma 2B |
| 动作专家 | Gemma 300M (独立权重) | Gemma 300M (独立权重) | 无 (复用 PaliGemma) |
| 状态输入 | 连续投影 -> 后缀 token | 离散化 -> 语言 token (前缀) | 离散化 -> 语言 token |
| 时间步注入 | MLP 拼接 | adaRMSNorm | 无 (自回归，无时间步) |
| 动作生成 | Flow Matching | Flow Matching | 自回归 Token 预测 |
| Loss | MSE on velocity | MSE on velocity | Cross-entropy |
| 动作空间 | 连续 (32 dim x 50 steps) | 连续 (32 dim x 50 steps) | 离散 token (FAST tokenizer) |
| 归一化 | z-score | 分位数 (quantile) | 分位数 |
| max_token_len | 48 | 200 | 180-250 |
| 推理步数 | 10 步 ODE | 10 步 ODE | 自回归 decode (max 256 tokens) |

## 十三、状态与动作表示对比

### 13.1 状态输入方式

| 模型 | 方式 | 实现位置 | 细节 |
|------|------|----------|------|
| **Pi0** | 连续投影为后缀 token | `pi0.py:153-157` | `state_proj = Linear(action_dim, 1024)` -> 1个token |
| **Pi0.5** | 离散化为文本串 -> 前缀 | `tokenizer.py:26-28` | `np.digitize(state, 256 bins)` -> 文本拼入 prompt |
| **FAST** | 离散化为文本串 -> 前缀 | `tokenizer.py:69-75` | 与 Pi0.5 相同: `"Task: ..., State: 0 45 128 ...;\n"` |

**Pi0 的状态处理**:

```python
# 连续值 -> 线性投影 -> 成为后缀第一个 token
state_token = self.state_proj(obs.state)[:, None, :]  # [B, 1, 1024]
# ar_mask = [True] -> 前缀不能 attend 它
```

**Pi0.5/FAST 的状态处理**:

```python
# 连续值 -> 256-bin 离散化 -> 文本字符串 -> SentencePiece tokenize -> 语言 token
discretized_state = np.digitize(state, bins=np.linspace(-1, 1, 256+1)[:-1]) - 1
state_str = " ".join(map(str, discretized_state))  # e.g. "0 128 45 200 ..."
full_prompt = f"Task: {text}, State: {state_str};\nAction: "
```

这意味着 Pi0.5 的 prompt 格式是: `Task: pick up the cup, State: 0 45 128 200 15 78 230;` 后跟动作生成。**状态被当作"语言"来理解**，PaliGemma 预训练的文本理解能力直接适用于此。

### 13.2 动作输出方式

| 模型 | 输出类型 | 训练目标 | 推理方式 | 输出形状 |
|------|----------|----------|----------|----------|
| **Pi0** | 连续向量 | MSE (速度场预测) | ODE 积分 (10步) | `[B, 50, 32]` |
| **Pi0.5** | 连续向量 | MSE (速度场预测) | ODE 积分 (10步) | `[B, 50, 32]` |
| **FAST** | 离散 token | 交叉熵 (next token) | 自回归 decode (max 256步) | `[B, max_steps]` -> 解码为 `[B, ah, ad]` |
| **Binning** | 离散 token | 交叉熵 | 自回归 decode | `[B, ah*ad]` -> reshape |
| **FSQ** | 离散 token | 交叉熵 | 自回归 decode | `[B, num_tokens]` -> 解码器重建 |

## 十四、训练 Loss 对比

### 14.1 Pi0 / Pi0.5 — Flow Matching Loss

`src/openpi/models/pi0.py:189-214`：

```python
# 采样
noise ~ N(0, I)
time ~ Beta(1.5, 1) * 0.999 + 0.001
x_t = t * noise + (1-t) * actions
u_t = noise - actions              # 目标速度场

# 预测
v_t = model(obs, x_t, time)        # 网络预测速度场

# Loss
loss = MSE(v_t, u_t)               # 对每个动作维度求均方误差
```

- **优点**: 训练简单，只需一次前向传播；推理固定步数，速度快
- **缺点**: 动作空间被当作连续分布建模，对多模态分布（如二选一）可能不够精确

### 14.2 Pi0-FAST — 自回归交叉熵 Loss

`src/openpi/models/pi0_fast.py:198-233`：

```python
# 输入: 图像 tokens + 语言 tokens + 状态 tokens + 动作 tokens
# 全部都是离散 token，拼成一个长序列

# 自回归: 预测 next token
targets = one_hot(tokens[:, 1:], vocab_size)     # 目标: 下一个 token
pre_logits = llm(embedded_prefix[:, :-1])         # 输入: 去掉最后一个 token
logits = llm(pre_logits[:, -target_len:])         # 只对目标位置解码
logp = log_softmax(logits)

# Loss: 加权交叉熵
loss = -sum(logp * targets * loss_mask) / sum(loss_mask)
# loss_mask: 只在动作 token 位置计算 loss，忽略前缀
```

- **优点**: 直接利用 VLM 的 token 预测能力；天然处理多模态分布（每个位置有 vocab_size 种选择）
- **缺点**: 推理需要逐步 decode，可能较慢；动作精度受限于 tokenizer 的量化误差

### 14.3 Loss 数值特性对比

| 特性 | Flow Matching (Pi0/0.5) | 交叉熵 (FAST) |
|------|-------------------------|---------------|
| Loss 范围 | [0, +inf) — MSE | (-inf, 0] — log probability |
| 对动作精度的敏感度 | 高（连续值直接比较） | 低（量化后比较） |
| 多模态分布处理 | 弱（高斯混合） | 强（离散 token 天然多模态） |
| 训练稳定性 | 需要仔细调 Beta 采样 | 标准 LM 训练，非常稳定 |

## 十五、推理过程对比

### 15.1 Pi0/Pi0.5 — ODE 积分去噪

```python
# 从纯噪声出发
x = N(0, I)                          # shape: [B, 50, 32]
dt = -1/10                            # 10 步积分

# 第1步: 编码前缀，填充 KV Cache (只做一次)
kv_cache = llm([prefix_tokens, None])

# 第2步: 迭代去噪 (10次)
for step in range(10):
    suffix = embed_suffix(obs, x, t)  # 编码噪声动作 + 时间步
    v_t = llm([None, suffix], kv_cache)  # 预测速度 (只计算 suffix 部分)
    v_t = action_out_proj(v_t)           # 投影到动作维度
    x = x + dt * v_t                     # Euler 积分
    t = t + dt

# x 即为最终动作
```

**特点**:
- **10 步固定迭代**
- 每步需要完整 Transformer forward（但利用 KV Cache 只算 suffix）
- 所有动作维度**同时**生成（并行）
- 推理速度: ~10 x (suffix forward)

### 15.2 FAST — 自回归 Token 生成

`src/openpi/models/pi0_fast.py:236-313`：

```python
# 第1步: 编码前缀，填充 KV Cache
prefix_embeddings = embed_inputs(obs)       # 图像 + 语言 + 状态 tokens
logits, kv_cache = llm(prefix_embeddings)   # 预填充

# 第2步: 逐 token 自回归生成
output_tokens = []
last_logit = logits[:, -1:]

while not all_eos and step < max_steps:
    # 从 last_logit 采样一个 token
    token = argmax(last_logit) if T==0 else categorical(last_logit/T)
    output_tokens.append(token)

    if token == EOS:
        all_eos = True
        break

    # 单步 decode
    token_emb = embed(token)
    last_logit, kv_cache = llm(token_emb, kv_cache)  # 只算 1 个 token
    step += 1

# 第3步: 解码 token -> 连续动作
actions = fast_tokenizer.decode(output_tokens)
```

**特点**:
- **变长迭代**（直到遇到 EOS 或达到 max_steps）
- 每步只 decode 1 个 token，KV Cache 使每步计算量很小
- 动作序列逐 token 生成（串行）
- 支持 **temperature > 0** 的随机采样，增加输出多样性
- 推理速度取决于 token 数量，一般 ~50-256 步

### 15.3 推理效率对比

| 指标 | Pi0 / Pi0.5 | Pi0-FAST |
|------|-------------|----------|
| 前向传播次数 | 1 (prefix) + 10 (denoise) | 1 (prefix) + ~50-256 (decode) |
| 每步计算量 | ~50 action tokens (并行) | 1 token |
| 总推理时间 | 较快（固定10步） | 取决于 token 长度 |
| KV Cache | prefix cache 共享两专家 | prefix cache 单模型 |
| 支持温度采样 | 否（确定性 ODE） | **是** (`temperature` 参数) |
| 支持 early stop | 否（固定步数） | **是**（EOS token） |

## 十六、Tokenizer 对比

Pi0-FAST 框架支持多种 tokenizer，每种都是把连续动作转为离散 token 的不同方式：

### 16.1 FAST Tokenizer（默认）

定义在 `src/openpi/models/tokenizer.py:51-139`。

```
连续动作 [ah, ad] -> FAST Tokenizer (VQ-VAE变体) -> 离散 token 序列
                 <- FAST Tokenizer 解码 <- 离散 token 序列
```

- 使用 HuggingFace 模型 `"physical-intelligence/fast"`
- Token 映射到 PaliGemma vocab 的末尾部分：`pg_token = vocab_size - 1 - 128 - action_token`
- 序列格式: `"Action: " + action_tokens + "|"` + EOS
- **通用 tokenizer**: 在多数据集上预训练，适用于各种机器人

### 16.2 Binning Tokenizer

定义在 `src/openpi/models/tokenizer.py:148-243`。

```
连续动作 -> 每个 dimension 独立量化到 [0, 255] -> 直接用整数 token 表示
解码: action_value = token / 256 * 2 - 1
```

- 最简单的方案：每个动作维度直接用 256-bin 离散化
- 类似 RT-2 / OpenVLA 的做法
- Token 数量 = action_horizon x action_dim（可能很长）
- **不支持训练时编码**（仅用于推理解码）

### 16.3 FSQ Tokenizer

定义在 `src/openpi/models/utils/fsq_tokenizer.py`。

```
连续动作 -> 线性投影 -> tanh -> FSQ量化 -> 离散 token
         <- 线性投影 <- 反量化 <- 离散 token
```

- **Finite Scalar Quantization**: 将连续向量量化到有限离散 codebook
- 使用交叉注意力编码器-解码器架构（`fsq_tokenizer.py:341-382`）
- 编码器: 可学习的 query tokens 通过 cross-attention 从动作序列中提取信息
- Codebook 大小可配置: 2^8 ~ 2^16
- 支持**自定义 bin 分配** (custom codebook)

### 16.4 Tokenizer 对比总结

| Tokenizer | 压缩效率 | 精度 | 通用性 | Token 数量 |
|-----------|----------|------|--------|-----------|
| **FAST** | 高（VQ-VAE 学习压缩） | 高 | 高（预训练通用） | 较少（压缩后） |
| **Binning** | 无压缩 | 低（256级量化） | 通用但粗糙 | ah x ad（很长） |
| **FSQ** | 高（学习量化） | 中-高 | 需要训练 | 少（可配置） |

## 十七、训练配置对比

从 `src/openpi/training/config.py` 中提取的实际训练配置：

| 配置项 | Pi0 典型值 | Pi0.5 典型值 | FAST 典型值 |
|--------|-----------|-------------|------------|
| **action_dim** | 32 | 32 | 7-8 |
| **action_horizon** | 10-50 | 10-50 | 10-32 |
| **batch_size** | 32 | 64-256 | 32-256 |
| **学习率** | 2.5e-5 (cosine) | 5e-5 (cosine, warmup 10k) | 5e-5 (cosine) |
| **训练步数** | 20k-30k | 20k-100k | 20k-100k |
| **EMA** | decay=0.99 | decay=0.999 | decay=0.99 |
| **归一化** | z-score | **分位数** | **分位数** |
| **LoRA rank** | 16 | 16/32 | 16 |
| **预训练权重** | pi0_base | pi05_base | pi0_fast_base |

### Pi0.5 独有的训练差异

1. **更大的 batch size**: 64-256（vs Pi0 的 32），因为 adaRMSNorm 更稳定
2. **更长的 warmup**: 10,000 步（vs Pi0 的 1,000 步）
3. **更高的 EMA decay**: 0.999（vs Pi0 的 0.99），更慢的参数更新
4. **分位数归一化**: 映射到 [-1, 1]，与状态离散化的 bin 范围一致

## 十八、PolaRiS 与 RoboArena 基线对比

### 18.1 PolaRiS 基线

`src/openpi/training/misc/polaris_config.py` 是一个**数据混合训练**的基线方案，对比了三种架构在相同数据上的表现：

```python
# PolaRiS 使用 90% DROID + 10% PolaRiS 自有数据的混合训练
datasets = (
    RLDSDataset(name="droid", weight=0.9),
    RLDSDataset(name="polaris_droid_cotrain_dataset", weight=0.1),
)
```

| PolaRiS 变体 | 模型 | action_horizon | 训练步数 | batch_size |
|-------------|------|---------------|---------|-----------|
| pi05_droid_jointpos | **Pi0.5** | 15 | 1,000 | 128 |
| pi0_fast_droid_jointpos | **FAST** | 10 | 1,000 | 128 |
| pi0_droid_jointpos | **Pi0** | 10 | 1,000 | 128 |
| pi0_droid_jointpos_100k | **Pi0** | 10 | 1,000 | 128 |

所有变体使用相同的数据、相同的优化器配置，仅模型架构不同——这为公平对比提供了基准。

### 18.2 RoboArena Baselines

`src/openpi/training/misc/roboarena_config.py` 提供了**自回归 + 不同 tokenizer** 的消融实验：

| 变体 | Tokenizer | 动作编解码方式 | max_token_len |
|------|-----------|--------------|---------------|
| paligemma_binning_droid | **Binning** (256-bin) | 每维度独立量化 | 400 |
| paligemma_fast_droid | **FAST** (通用) | VQ-VAE 压缩 | 250 |
| paligemma_fast_specialist_droid | **FAST** (DROID专用) | 专用 VQ-VAE | 250 |
| paligemma_vq_droid | **FSQ** | 学习型有限量化 | 250 |

这组实验可以在相同骨干下对比**不同 tokenizer 对动作生成质量的影响**。

### 18.3 输入格式差异

Pi0/Pi0.5 和 FAST 使用**不同的图像 key 命名规范**（见 `src/openpi/policies/droid_policy.py:47-58`）：

```python
# Pi0 / Pi0.5: 3 张图, 右手腕可以是空图 (mask=False)
names = ("base_0_rgb", "left_wrist_0_rgb", "right_wrist_0_rgb")
image_masks = (True, True, False)  # 第三张图被 mask 掉

# FAST: 3 张图, 全部有效 (mask=True)
names = ("base_0_rgb", "base_1_rgb", "wrist_0_rgb")
image_masks = (True, True, True)
```

这暗示 **Pi0 模型假设双臂机器人的输入结构**（左手腕+右手腕），而 FAST 更灵活地处理3个通用视角。

### 18.4 序列长度对比

| 模型 | max_token_len | 原因 |
|------|---------------|------|
| Pi0 | 48 | 只有语言 prompt + `"\n"` 分隔符 |
| Pi0.5 | 200 | 语言 prompt + 离散化状态文本 (`"State: 0 45 128 ..."`) |
| FAST | 180-250 | 语言 prompt + 离散化状态 + 动作 token |

FAST 需要最长的 token 序列，因为训练时需要把**完整的动作 token 序列**也拼入输入。

## 十九、选择指南

```
你需要什么样的模型？
|
|-- 追求最佳动作精度 (连续动作空间)
|   |-- 有充足计算资源 -> Pi0.5 (adaRMSNorm + Flow Matching)
|   +-- 资源有限 -> Pi0 (简单高效)
|
|-- 追求泛化能力 / 利用 VLM 知识
|   |-- 有 FAST tokenizer -> FAST (完全复用 VLM)
|   +-- 需要简单 tokenizer -> Binning / FSQ baseline
|
|-- 低资源微调
|   |-- 单 GPU / 小数据 -> LoRA + Pi0.5 或 LoRA + FAST
|   +-- 多 GPU -> Full fine-tune
|
+-- 多模态动作分布 (动作有歧义)
    +-- FAST (离散 token 天然处理多模态)
```

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| 双臂机器人精细操作 | **Pi0.5** | adaRMSNorm 更好的时间步条件，连续动作精度高 |
| 单臂机器人快速部署 | **FAST** | 自回归生成，可利用 VLM 全部知识，泛化好 |
| 研究消融实验 | **RoboArena Baselines** | 同骨干下对比不同 tokenizer |
| 极少数据微调 | **LoRA Pi0.5** | 低秩适配，冻结骨干只训少量参数 |
| 大规模数据训练 | **Pi0.5 + RLDS** | 支持高效 RLDS 数据加载，分位数归一化鲁棒 |

---

## 关键设计直觉总结

1. **双专家而非单模型**: PaliGemma 2B 负责"理解"，Action Expert 300M 负责"行动"。理解需要大模型的语言知识，行动只需要学习动作空间的分布。分工带来效率。

2. **共享注意力而非独立编码**: 两个 expert 的 token 在同一个注意力矩阵中交互，动作生成可以直接利用视觉-语言理解的结果。

3. **Flow Matching 而非 Diffusion**: Flow Matching 用线性插值路径 + 简单 MSE loss，训练更稳定，推理更快（10 步 vs Diffusion 的数百步）。

4. **adaRMSNorm**: 让时间步信息在每一层都生效，而非只在输入层注入一次。这对 Flow Matching 的条件生成至关重要。

5. **离散化状态**: 将连续状态离散化为文本 token，复用 PaliGemma 的文本理解能力，简化了模型架构。
