# -*- coding: utf-8 -*-
"""生成汇报用折线/柱状图 (PNG), 主题色对齐 PPT 暗红 C00000."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

CJK = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc')
plt.rcParams['axes.unicode_minus'] = False
RED = '#C00000'; BLUE = '#2E75B6'; ORANGE = '#E69F00'; GREY = '#888888'; GREEN = '#2E7D32'
UPS = [3, 6, 12, 24, 48, 97, 197, 400]

# DeepSeek 数据 (46 key)
D = {
    'G0':            [0.96,0.92,0.85,0.83,0.79,0.73,0.54,0.44],
    'G8s':           [0.78,0.18,0.31,0.50,0.68,0.69,0.71,0.62],
    'G2+G8s':        [0.75,0.18,0.30,0.51,0.71,0.79,0.79,0.55],
    'G4':            [0.95,0.91,0.86,0.87,0.73,0.57,0.43,0.50],
    'G2+G4+G3+G8s':  [0.72,0.17,0.30,0.51,0.69,0.76,0.78,0.65],
    'G2+G7+G8s':     [0.85,0.16,0.30,0.50,0.71,0.77,0.75,0.61],
}


def setup(ax, title, xlabel='每个 key 被更新的次数', ylabel='准确率'):
    ax.set_title(title, fontproperties=CJK, fontsize=14, color=RED, fontweight='bold')
    ax.set_xlabel(xlabel, fontproperties=CJK, fontsize=11)
    ax.set_ylabel(ylabel, fontproperties=CJK, fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_xticks(range(len(UPS)))
    ax.set_xticklabels([f'u{u}' for u in UPS])
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontproperties(CJK); lab.set_fontsize(9)
    ax.legend(prop=CJK, fontsize=10, loc='best')


# ① 下降后上升
fig, ax = plt.subplots(figsize=(8.2, 4.3))
ax.plot(UPS, D['G0'], '-o', color=GREY, lw=2, label='G0 baseline（无干预）')
ax.plot(UPS, D['G8s'], '-o', color=RED, lw=2.3, label='G8s（语义重启）')
ax.plot(UPS, D['G2+G8s'], '-o', color=BLUE, lw=2.3, label='G2+G8s（王牌组合）')
ax.set_ylim(-0.05, 1.0)
ax.annotate('u6 陷阱：线索干扰\n简单回忆，反降到 0.18', xy=(1, 0.18), xytext=(2.2, 0.02),
            fontproperties=CJK, fontsize=9, color=ORANGE, arrowprops=dict(arrowstyle='->', color=ORANGE))
ax.annotate('高负载区回升\n(rescue from PI)', xy=(7, 0.79), xytext=(4.5, 0.88),
            fontproperties=CJK, fontsize=9, color=BLUE, arrowprops=dict(arrowstyle='->', color=BLUE))
setup(ax, '现象① 下降后上升：Release 低负载反伤、高负载救命')
fig.tight_layout(); fig.savefig('c_dip_rise.png', dpi=140); plt.close()

# ③ G4 反转
fig, ax = plt.subplots(figsize=(8.2, 4.3))
for lab, key, c in [('G0 baseline', 'G0', GREY), ('G4 alone（glitch token）', 'G4', ORANGE),
                    ('G2+G8s', 'G2+G8s', BLUE), ('G2+G4+G3+G8s（含G4）', 'G2+G4+G3+G8s', RED)]:
    ax.plot(UPS, D[key], '-o', color=c, lw=2.3, label=lab)
ax.set_ylim(-0.05, 1.0)
ax.annotate('u400 反转：含 G4 组合\n=0.65 反成全场最强', xy=(7, 0.65), xytext=(3.5, 0.78),
            fontproperties=CJK, fontsize=9, color=RED, arrowprops=dict(arrowstyle='->', color=RED))
setup(ax, '现象③ G4 glitch“先破坏后组合”：极端高负载下反转')
fig.tight_layout(); fig.savefig('c_g4_reversal.png', dpi=140); plt.close()

# B-1 PI 累积
NPC = [25, 50, 75, 100, 125, 150, 175, 200]
PI_diff = [21, 54, 69, 97, 118, 138, 150, 164]
PI_equal = [24, 48, 71, 99, 114, 132, 146, 168]
fig, ax = plt.subplots(figsize=(8.2, 4.3))
ax.plot(NPC, PI_diff, '-o', color=RED, lw=2.3, label='diff（目击者信誉度不同）')
ax.plot(NPC, PI_equal, '-s', color=BLUE, lw=2.3, label='equal（信誉度相同）')
ax.set_ylim(0, 180)
ax.annotate('cred<gold ≈ 80%\n→ 真正 PI（旧值侵入）', xy=(150, 138), xytext=(40, 160),
            fontproperties=CJK, fontsize=9, color=RED, arrowprops=dict(arrowstyle='->', color=RED))
setup(ax, 'Slot-PI：PI 侵入随目击者数线性增长（信誉度不影响 PI）',
      xlabel='目击者数（NPC）', ylabel='PI 侵入次数')
fig.tight_layout(); fig.savefig('c_pi_buildup.png', dpi=140); plt.close()

# B-2 正交 dual-task
import numpy as np
groups = ['AA\n纯仓库', 'BB\n纯盗车', 'AB\n仓库→盗车', 'BA\n盗车→仓库']
c1 = [77, 0, 23, 47]
c2 = [0, 77, 73, 17]
x = np.arange(4)
fig, ax = plt.subplots(figsize=(8.2, 4.3))
ax.bar(x - 0.2, c1, 0.4, label='Case1（仓库案）', color=BLUE)
ax.bar(x + 0.2, c2, 0.4, label='Case2（盗车案）', color=RED)
ax.set_xticks(x); ax.set_xticklabels(groups, fontproperties=CJK, fontsize=10)
ax.set_ylim(0, 100)
ax.set_title('Slot-PI 正交槽位：cross=0 但 dual-task cost 显著（切换组 AB/BA 崩塌）',
             fontproperties=CJK, fontsize=13, color=RED, fontweight='bold')
ax.set_ylabel('Q10 准确率 (%)', fontproperties=CJK, fontsize=11)
ax.grid(alpha=0.3, axis='y')
for lab in ax.get_xticklabels() + ax.get_yticklabels():
    lab.set_fontproperties(CJK); lab.set_fontsize(9)
ax.legend(prop=CJK, fontsize=10)
fig.tight_layout(); fig.savefig('c_orthogonal.png', dpi=140); plt.close()

print('✓ 4 张图生成完毕')
