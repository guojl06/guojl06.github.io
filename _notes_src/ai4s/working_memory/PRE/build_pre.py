# -*- coding: utf-8 -*-
"""合并 PPT: 同学A SD(原) + 我的 PI Release(加厚+图) + 同学B Slot-PI(加厚+图)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

SRC = "/Users/st/Documents/mynotebook/小学期AI4S/working_memory/PRE/pre.pptx"
OUT = "/Users/st/Documents/mynotebook/小学期AI4S/working_memory/PRE/pre_merged.pptx"
DIR = "/Users/st/Documents/mynotebook/小学期AI4S/working_memory/PRE/"

RED = RGBColor(0xC0, 0x00, 0x00); DARK = RGBColor(0x33, 0x33, 0x33)
GREEN = RGBColor(0x1B, 0x7A, 0x3A); LOWC = RGBColor(0xC0, 0x39, 0x2B)
GREY = RGBColor(0x70, 0x70, 0x70); WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HDR_BG = RGBColor(0x2A, 0x2A, 0x4A); ROW_A = RGBColor(0xF4, 0xF4, 0xF8); ROW_B = RGBColor(0xEA, 0xEA, 0xF0)
TITLE_FONT = "华文楷体"; BODY_FONT = "等线"

prs = Presentation(SRC)
L_CONTENT = prs.slide_layouts[1]; L_BLANK = prs.slide_layouts[6]


def _set(run, font=BODY_FONT, size=16, bold=False, color=DARK):
    run.font.name = font; run.font.size = Pt(size); run.font.bold = bold; run.font.color.rgb = color


def add_divider(title, subtitle=""):
    s = prs.slides.add_slide(L_BLANK)
    tb = s.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.7), Inches(2.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    _set(p.add_run(), TITLE_FONT, 38, True, RED); p.runs[0].text = title
    if subtitle:
        p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
        _set(p2.add_run(), TITLE_FONT, 20, False, GREY); p2.runs[0].text = subtitle
    return s


def add_content(title, bullets, size=16):
    s = prs.slides.add_slide(L_CONTENT)
    s.shapes.title.text = title
    for r in s.shapes.title.text_frame.paragraphs[0].runs:
        _set(r, TITLE_FONT, 22, True, RED)
    body = s.placeholders[1].text_frame; body.word_wrap = True
    first = True
    for b in bullets:
        lvl = 0; text = b
        if isinstance(b, tuple): text, lvl = b
        p = body.paragraphs[0] if first else body.add_paragraph(); first = False
        p.level = lvl; p.space_after = Pt(5)
        _set(p.add_run(), BODY_FONT, size if lvl == 0 else size - 2, lvl == 0, DARK)
        p.runs[-1].text = ("• " if lvl == 0 else "– ") + text
    return s


def add_table(title, headers, rows, note=""):
    s = prs.slides.add_slide(L_BLANK)
    tb = s.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.8))
    _set(tb.text_frame.paragraphs[0].add_run(), TITLE_FONT, 22, True, RED)
    tb.text_frame.paragraphs[0].runs[0].text = title
    nrow, ncol = len(rows) + 1, len(headers)
    gt = s.shapes.add_table(nrow, ncol, Inches(0.6), Inches(1.3), Inches(12.1), Inches(0.45 * nrow)).table
    for j, h in enumerate(headers):
        c = gt.cell(0, j); c.text = h; para = c.text_frame.paragraphs[0]; para.alignment = PP_ALIGN.CENTER
        _set(para.runs[0], BODY_FONT, 12, True, WHITE); c.fill.solid(); c.fill.fore_color.rgb = HDR_BG
    for i, row in enumerate(rows, 1):
        for j, val in enumerate(row):
            color = DARK
            if j > 0:
                try:
                    f = float(val); color = LOWC if f < 0.3 else (GREEN if f > 0.7 else DARK)
                except ValueError: pass
            c = gt.cell(i, j); c.text = str(val); para = c.text_frame.paragraphs[0]; para.alignment = PP_ALIGN.CENTER
            _set(para.runs[0], BODY_FONT, 11, j == 0, color if j > 0 else DARK)
            c.fill.solid(); c.fill.fore_color.rgb = ROW_A if i % 2 else ROW_B
    if note:
        nb = s.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.9))
        _set(nb.text_frame.paragraphs[0].add_run(), BODY_FONT, 12, False, GREY)
        nb.text_frame.paragraphs[0].runs[0].text = note
    return s


def add_chart(title, img, note=""):
    s = prs.slides.add_slide(L_BLANK)
    tb = s.shapes.add_textbox(Inches(0.4), Inches(0.2), Inches(12.5), Inches(0.7))
    _set(tb.text_frame.paragraphs[0].add_run(), TITLE_FONT, 22, True, RED)
    tb.text_frame.paragraphs[0].runs[0].text = title
    w = Inches(8.8); s.shapes.add_picture(DIR + img, Inches((13.333 - 8.8) / 2), Inches(1.0), width=w)
    if note:
        nb = s.shapes.add_textbox(Inches(0.6), Inches(6.55), Inches(12.1), Inches(0.85))
        _set(nb.text_frame.paragraphs[0].add_run(), BODY_FONT, 12.5, False, GREY)
        nb.text_frame.paragraphs[0].runs[0].text = note
    return s


# ═══════════════════ Part Ⅱ — 我的 PI Release ═══════════════════
add_divider("Part Ⅱ · Proactive Interference Release", "Feature-Update 范式 · DeepSeek + Qwen3.5-2B · 千条数据")

add_content("背景：什么是前摄干扰（PI）？为什么在 LLM 上做？", [
    "前摄干扰（Proactive Interference, PI）：先前学过的旧信息，干扰对后续新信息的提取。",
    "经典例子：连续背几组同类词表，越往后越难记——旧词在“抢”回忆通道。",
    "Wickens (1960s)：同类词表逐次变难（PI 累积）；一旦换成新类别，准确率跳升 = “PI Release / 范畴释放”。",
    "→ 这说明人类记忆是按“范畴”组织的；换范畴就能把旧干扰“卸载”。",
    "我们的问题：LLM（Transformer）有没有这种 PI？它的记忆检索是按范畴（category-based）还是按内容（content-addressable）？",
    "给一个“范畴切换/语义重启”线索，能不能像人一样触发 release？",
])

add_content("实验范式：Feature-Update（基于 Unable to Forget, arXiv:2506.08184）", [
    "任务：一条文本流里，N 个 key（如 dish / music / weapon …）各自被反复赋予新值。",
    ("流格式：“dish: sushi; music: bongos; dish: chicken kebab; music: gamelan; …”", 1),
    ("流被全随机打乱（禁止连续同一 key）——模型必须逐个搜索，不能只读末尾。", 1),
    "流结束后问：“What are the current value of each key (…) ?” 每个 key 答最新值。",
    "评分：exact-match，论文逐行移植（verbal + colon 正则，strip+lower 精确匹配）。",
    "为什么这测 PI：每个 key 被覆盖多次，模型须只取“最后一次”；但旧值（已被覆盖）会前摄干扰——模型常吐出旧值/中间值，而非最新值。",
    "负载 u（每个 key 的更新次数）越大，干扰越重 → G0 baseline 准确率随 u 单调下降。",
])

add_content("干预组设计：G0–G8s + 组合策略", [
    "G0 baseline：不加任何干预，看天然 PI 有多严重。",
    "G1–G7：各种 prompt 工程（语义遗忘提示 / mock-QA 重置 / 句法断崖 / glitch token …），多数无效或微效。",
    "G8s = hackreset：在流中注入一段“全新、无关的语义流”，强行让模型“重启”上下文——模拟 Wickens 的范畴切换。",
    "组合策略：在 G8s release 基础上叠加辅助干预，看能否进一步增强。",
    ("G2+G8s, G7+G2+G8s, G2+G5+G8s, G2+G7+G8s …", 1),
    ("G2+G4+G3+G8s（含 glitch token）等", 1),
    "扫参：17 策略 × 更新次数 u3→u400 × 注入位置；DeepSeek 2410 条 + Qwen3.5-2B 1025+ 条。",
])

add_content("数据规模与跨模型", [
    "DeepSeek-Chat（API，大规模）：2410 条",
    ("Batch1：46 key × 17 策略 × 8 updates = 1360", 1),
    ("Batch2：位置扫描 5 策略 × 3 updates × 7 位置 = 1050", 1),
    "Qwen3.5-2B（本地，24 层）：1025 条（15 key，u3–u97，17 策略）+ 位置扫描 1050 条",
    "temperature=0 / greedy，确定性；评分与论文逐行对齐。",
    "→ 两个数量级不同的模型交叉验证，看现象是否稳健。",
])

add_chart("现象 ①：Release 的“下降后上升”（DeepSeek, 46 key）", "c_dip_rise.png",
    "G8s / G2+G8s 呈典型“下降后上升”：低负载（u6）时 release 线索反而干扰简单回忆，准确率掉到 ~0.18；"
    "高负载（u97+）PI 严重时，release 把准确率从 0.54 拉回 0.79。G0 baseline 单调下降。"
    "结论：release 线索是“PI 解药”，但它只在 PI 真正发生时起效。")

add_table("现象 ②：G2+G8s 王牌组合（高 PI 区最强，DeepSeek）",
    ["策略", "u97", "u197", "u400"],
    [
        ["G0 baseline", "0.73", "0.54", "0.44"],
        ["G8s",         "0.69", "0.71", "0.62"],
        ["G2+G8s",      "0.79", "0.79", "0.55"],
        ["G2+G7+G8s",   "0.77", "0.75", "0.61"],
        ["G2+G5+G8s",   "0.80", "0.74", "0.47"],
    ],
    "高 PI（u97–u400）下 G2+G8s 及变体达 0.75–0.80，显著超 G0（u197：0.79 vs 0.54）。"
    "G2（mock-QA 自我重置）+ G8s（语义重启）是大多数情况下的王牌组合。")

add_chart("现象 ③：G4 glitch token 的“先破坏后组合”反转（DeepSeek）", "c_g4_reversal.png",
    "G4（一个“glitch token”干扰词）单独使用 ≈ G0，低负载甚至略伤；"
    "但极端高负载（u400）下，含 G4 的组合（G2+G4+G3+G8s=0.65）反成全场最强。"
    "猜测：glitch 的“破坏性”在高 PI 下打断了旧值锚定，配合 G8s release 实现奇异提升——先破坏，后组合。")

add_table("跨模型复现：Qwen3.5-2B（24 层）同样出现 Release",
    ["update", "G0", "G8s", "G2+G8s", "G7+G2+G8s"],
    [
        ["u3",  "0.71", "0.60", "0.77", "0.61"],
        ["u12", "0.13", "0.33", "0.27", "0.24"],
        ["u48", "0.00", "0.47", "0.25", "0.42"],
        ["u97", "0.00", "0.49", "0.55", "0.64"],
    ],
    "小模型（2B）同样复现：u48/u97 G0=0 → G8s/G7+G2+G8s=0.47–0.64。Release 跨模型规模一致。"
    "（注：2B 上 G8s 单独比 G2+G8s 更强，与 DeepSeek 相反，疑因小模型注意力带宽窄，G2 反而稀释。）")

add_content("机制假说（⚠ 待验证 — 机制实验尚未进行）", [
    "H1（层级定位）：Layer 11（24 层的 46%）是 release 核心层——G0 vs G8s activation cosine 在该层最大分叉（0.77）。待 logit-lens / attention diff 验证。",
    "H2（G8s 为何起效）：G8s 提供“干净语义重启”，重定向查询位置注意力、打断旧值锚定——比温和 category-switch 更激进（与 Part Ⅲ 对照）。",
    "H3（G4 glitch 反转）：glitch token 在高 PI 下扰动已固化的旧值表征，使其更易被 G2+G8s 覆盖。",
    "H4（失败模式依赖）：release 是否奏效取决于 PI 失败模式（首因锚定 vs 中间值检索失败）。",
    "以上为基于行为数据的合理猜测；logit-lens / attention / activation patching 等机制实验待开展。",
])

# ═══════════════════ Part Ⅲ — 同学B Slot-PI ═══════════════════
add_divider("Part Ⅲ · Slot-PI 范式", "PI 稳健存在，但 Release 缺失 · 同学 PZH · DeepSeek + Qwen3-4B")

add_content("Slot-PI 范式：警探·目击者·信誉度", [
    "情景：你是警探，收到 N 个目击者对嫌疑人的描述；每个目击者有信誉度 1–5★。",
    "6 个固定槽位：height / clothing / hair / item / exit / time。",
    "每个目击者更新其中几个槽位；覆盖规则：仅当 cred_new ≥ cred_old 才覆盖该槽位。",
    "Query：每个槽位引用**最高信誉**目击者的原话（不转述）。",
    "PI 指标：**cred<gold**——若回答里出现“信誉低于 gold 的旧值”= 真正 PI（被覆盖的旧值本不该记得却记得了）。",
    "→ 这套范式能区分“真 PI”（旧值侵入）和“同信誉选错”（primacy/recency 竞争）。",
])

add_content("Slot-PI 数据规模", [
    "DeepSeek-Chat（temp=0）为主模型，Qwen3-4B（GPU, greedy）交叉验证。",
    "6 类实验：PI 累积（25→200 NPC）/ 槽位数 s 扫描 / Batch vs Sequential / Dual-Case 分案 / 正交槽位 / Context 控制。",
    "每个条件 3–5 次重复；唯一值池（无放回），避免名字/值重复混淆。",
])

add_chart("现象：PI 稳健存在（DeepSeek, s=2）", "c_pi_buildup.png",
    "PI 侵入随目击者数线性增长（21→164）；cred<gold ≈ 80% 证明大部分侵入是真正 PI；"
    "diff（信誉不同）≈ equal（信誉同）两条曲线几乎重合——信誉度不影响 PI，PI 是纯槽位值的记忆竞争。"
    "（consistent 对照 100% 准确，确认 PI 源自信息矛盾而非信息量。）")

add_content("进一步结果：PI 是稳健的结构性现象", [
    "s（每目击者更新槽位数）无主效应：1→6 槽位，PI 总量与 cred<gold 比例都稳定（~80%）。",
    "Sequential ≈ Batch：逐人确认 vs 一次性呈现，PI 几乎无差异。",
    "PI vs Context Length：固定 NPC 数、只变目标信息量，PI 仍随信息量线性增长——",
    ("→ PI 是独立因素，不是“长文本副作用”。", 1),
    "height / time 是 PI 重灾区（连续数值维度易混淆），clothing 最抗 PI（关键词独特）。",
])

add_content("PI Release 实验①：Dual-Case（同槽位双案）——无法释放", [
    "设计：两个案件（仓库 / 盗车）的目击者混在一起；query 显式要求分案回答，目击者前加 [WAREHOUSE]/[CAR THEFT] 标签。",
    "逻辑：如果模型只是“没动力”分案，那显式要求分案应能 release。",
    "结果：**跨案污染 cross = 93%（2.8/3）无法消除**——即使分案 + 标签，仓库案目击者的身高值仍混进盗车案描述。",
    "→ 同槽位的旧值永远竞争当前提取，温和的“分案/范畴线索”无效。",
])

add_chart("PI Release 实验②：Orthogonal（零槽位重叠）——cross=0 但有注意力代价", "c_orthogonal.png",
    "把两案槽位完全分离（仓库用 height/clothing/…，盗车用 license_plate/car_model/…），cross 结构上=0。"
    "但切换组 AB（仓库→盗车）、BA 仍崩塌：旧案信息被新案稀释 → dual-task cost -20%~-63%。"
    "证明存在第二种 PI：注意力竞争（discourse-level），与槽位重叠无关。")

add_table("跨模型一致性：Qwen3-4B + DeepSeek 结论一致",
    ["现象", "Qwen3-4B", "DeepSeek", "一致性"],
    [
        ["cred<gold ≈ 80%",      "✓",   "✓",   "完美"],
        ["s 无主效应",            "✓",   "✓",   "完美"],
        ["PI 由信息量驱动",        "✓",   "✓",   "一致"],
        ["同槽位 cross > 0",      "67%", "93%", "方向一致"],
        ["正交 cross = 0",        "✓",   "✓",   "结构必然"],
        ["Dual-task cost",        "-33~-50%", "-20~-63%", "方向一致"],
        ["PI Release",            "✗",   "✗",   "一致 null"],
    ],
    "规模（0.6B→4B→671B）改变绝对性能，但不改变定性结论：PI Release 在 Transformer 上不存在。")

add_content("结论：LLM 缺 category-based memory filtering", [
    "Wickens PI Release 需两条件：(a) 提取线索切换 + (b) category-based filtering。LLM 有 (a) 无 (b)。",
    "两种 PI 机制：",
    ("Slot-level PI：同槽位旧值永远竞争（content-addressable 汇聚，不经 category 过滤）", 1),
    ("Discourse-level PI：处理新信息稀释旧信息（注意力竞争）", 1),
    "★ 与 Part Ⅱ 对照：温和 category-switch 无效（Part Ⅲ），而激进 G8s 语义重启能诱发 release（Part Ⅱ）——暗示 release 的关键不是“范畴标签”，而是“打断 content-addressable 汇聚”。",
])

prs.save(OUT)
print("OK 合并完成:", OUT)
print("总 slide 数:", len(prs.slides))
