import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 6))
fig.suptitle('南非拉霍马矿山项目 — 单吨成本费用分析', fontsize=20, fontweight='bold', y=0.98)

# 成本数据
cost_items = [
    ('生产成本', 26, '#4472C4'),
    ('南非国内铁路/陆路运费', 30, '#ED7D31'),
    ('港杂费', 15, '#A5A5A5'),
    ('海运+保险费', 24, '#FFC000'),
]

# 绘制成本堆叠条（中间层）
bottom = 0
for name, val, color in cost_items:
    bar = ax.barh(0, val, left=bottom, color=color, edgecolor='white', height=0.5, alpha=0.9)
    ax.text(bottom + val/2, 0, f'{val}', ha='center', va='center', fontsize=16, fontweight='bold', color='white')
    bottom += val

# 到岸总成本汇总条（下层）
ax.barh(-0.8, 95, color='#2E75B6', edgecolor='white', height=0.5, alpha=1.0)
ax.text(95/2, -0.8, '到岸总成本\n95 美元/吨', ha='center', va='center', fontsize=15, fontweight='bold', color='white')

# 售价与利润条（上层）
ax.barh(0.8, 100, left=0, color='#70AD47', edgecolor='white', height=0.5, alpha=0.9)
ax.text(100/2, 0.8, '平均到岸售价  100 美元/吨', ha='center', va='center', fontsize=15, fontweight='bold', color='white')

# 利润小条（售价右侧）
ax.barh(0.8, 5, left=100, color='#C55A11', edgecolor='white', height=0.5, alpha=0.9)
ax.text(102.5, 0.8, '利润\n5$', ha='center', va='center', fontsize=13, fontweight='bold', color='white')

# 连接箭头（累计示意）
cumulative_positions = [26, 56, 71, 95]
for i in range(len(cumulative_positions)-1):
    ax.annotate('', xy=(cumulative_positions[i+1], 0.3), xytext=(cumulative_positions[i], 0.3),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

# 图例
legend_patches = [
    mpatches.Patch(color='#4472C4', label='生产成本（26美元）'),
    mpatches.Patch(color='#ED7D31', label='南非国内运费（30美元）'),
    mpatches.Patch(color='#A5A5A5', label='港杂费（15美元）'),
    mpatches.Patch(color='#FFC000', label='海运+保险（24美元）'),
    mpatches.Patch(color='#2E75B6', label='到岸总成本（95美元）'),
    mpatches.Patch(color='#70AD47', label='平均售价（100美元）'),
    mpatches.Patch(color='#C55A11', label='单吨利润（5美元）'),
]
ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=4, fontsize=12, frameon=False)

ax.set_xlim(0, 115)
ax.set_ylim(-1.5, 1.5)
ax.axis('off')
ax.set_title('单吨钒钛磁铁矿全流程成本构成与利润（美元/吨产品）', fontsize=16, fontweight='bold', pad=20)

# 数据来源注释
fig.text(0.5, 0.01, '数据来源：《南非拉霍马矿山商业计划书V3》', ha='center', fontsize=10, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(r'C:\Users\lk\Desktop\拉霍马矿山成本费用分析图.png', dpi=300, bbox_inches='tight', facecolor='white')
print('Chart saved to Desktop!')
