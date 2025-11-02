#!/usr/bin/env python3
"""
Regenerate Figure 2 with better D panel (significance bar plot instead of text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Read correlation results
corr_df = pd.read_csv("../outputs/tcga_full_cohort/correlation_results.csv")
print(f"Loaded {len(corr_df)} correlations")

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("TCGA Pan-Cancer Analysis (n=1,300): PD-L1 Regulatory Network",
             fontsize=16, fontweight='bold')

# 1. Create correlation matrix for heatmap
genes = ['CD274', 'CMTM6', 'STUB1', 'HIP1R', 'SQSTM1']
corr_matrix = np.zeros((len(genes), len(genes)))

for i, g1 in enumerate(genes):
    for j, g2 in enumerate(genes):
        if i == j:
            corr_matrix[i, j] = 1.0
        else:
            row = corr_df[((corr_df['gene1'] == g1) & (corr_df['gene2'] == g2)) |
                         ((corr_df['gene1'] == g2) & (corr_df['gene2'] == g1))]
            if not row.empty:
                corr_matrix[i, j] = row.iloc[0]['r']

# Panel A: Correlation heatmap
ax1 = axes[0, 0]
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, annot=True, fmt=".3f", cmap='RdBu_r',
            center=0, vmin=-0.5, vmax=0.5, square=True,
            cbar_kws={'label': 'Pearson r'},
            xticklabels=genes, yticklabels=genes,
            mask=mask, ax=ax1, linewidths=1, linecolor='gray')
ax1.set_title('A. Correlation Matrix', fontweight='bold', fontsize=12)

# Panel B: Correlation strength bar plot
ax2 = axes[0, 1]
gene_pairs = []
r_abs = []
colors_b = []

for _, row in corr_df.iterrows():
    label = f"{row['gene1'][:4]}-{row['gene2'][:4]}"
    gene_pairs.append(label)
    r_abs.append(abs(row['r']))

    # Color by correlation direction
    if row['r'] > 0:
        colors_b.append('#d62728')  # Red for positive
    else:
        colors_b.append('#1f77b4')  # Blue for negative

sorted_idx = np.argsort(r_abs)[::-1]
gene_pairs_sorted = [gene_pairs[i] for i in sorted_idx]
r_abs_sorted = [r_abs[i] for i in sorted_idx]
colors_sorted = [colors_b[i] for i in sorted_idx]

y_pos = np.arange(len(gene_pairs_sorted))
ax2.barh(y_pos, r_abs_sorted, color=colors_sorted, alpha=0.7)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(gene_pairs_sorted, fontsize=9)
ax2.set_xlabel('|Pearson r|', fontsize=11)
ax2.set_title('B. Correlation Strength', fontweight='bold', fontsize=12)
ax2.axvline(x=0.3, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax2.text(0.3, len(gene_pairs_sorted)-0.5, 'Strong (|r|=0.3)', rotation=90,
         va='top', ha='right', fontsize=8, alpha=0.7)
ax2.grid(axis='x', alpha=0.3)
ax2.invert_yaxis()

# Panel C: Novel findings highlight
ax3 = axes[1, 0]
novel_findings = [
    ('CMTM6-STUB1', -0.295, 0.0),
    ('CMTM6-SQSTM1', -0.142, 0.0),
    ('CD274-CMTM6', 0.161, 0.0),
    ('CD274-STUB1', -0.132, 0.0),
    ('SQSTM1-STUB1', 0.208, 0.0),
]

labels = [f[0] for f in novel_findings]
r_vals = [f[1] for f in novel_findings]
colors_c = ['#d62728' if r > 0 else '#1f77b4' for r in r_vals]

bars = ax3.bar(range(len(labels)), r_vals, color=colors_c, alpha=0.7, edgecolor='black')
ax3.set_xticks(range(len(labels)))
ax3.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)
ax3.set_ylabel('Pearson r', fontsize=11)
ax3.set_title('C. Key Correlations', fontweight='bold', fontsize=12)
ax3.axhline(y=0, color='black', linewidth=0.8)
ax3.grid(axis='y', alpha=0.3)

# Add significance stars
for i, (label, r, p) in enumerate(novel_findings):
    if p < 0.001:
        ax3.text(i, r + 0.02 if r > 0 else r - 0.02, '***',
                ha='center', va='bottom' if r > 0 else 'top', fontsize=14)

# Panel D: Significance bar plot
ax4 = axes[1, 1]
p_values = []
colors_d = []

for _, row in corr_df.iterrows():
    p_values.append(-np.log10(row['p']) if row['p'] > 0 else 10)

    if row['p'] < 0.001:
        colors_d.append('#d62728')  # Red
    elif row['p'] < 0.01:
        colors_d.append('#ff7f0e')  # Orange
    elif row['p'] < 0.05:
        colors_d.append('#2ca02c')  # Green
    else:
        colors_d.append('#7f7f7f')  # Gray

sorted_idx2 = np.argsort(p_values)[::-1]
gene_pairs_sorted2 = [gene_pairs[i] for i in sorted_idx2]
p_values_sorted = [p_values[i] for i in sorted_idx2]
colors_sorted2 = [colors_d[i] for i in sorted_idx2]

y_pos2 = np.arange(len(gene_pairs_sorted2))
ax4.barh(y_pos2, p_values_sorted, color=colors_sorted2, alpha=0.7)
ax4.set_yticks(y_pos2)
ax4.set_yticklabels(gene_pairs_sorted2, fontsize=9)
ax4.set_xlabel('-log10(P-value)', fontsize=11)
ax4.set_title('D. Statistical Significance', fontweight='bold', fontsize=12)
ax4.axvline(x=-np.log10(0.05), color='black', linestyle='--', alpha=0.5, linewidth=1)
ax4.text(-np.log10(0.05), len(gene_pairs_sorted2)-0.5, 'P=0.05', rotation=90,
         va='top', ha='right', fontsize=8, alpha=0.7)
ax4.grid(axis='x', alpha=0.3)
ax4.invert_yaxis()

plt.tight_layout()

# Save
output_file = Path("../outputs/tcga_full_cohort/TCGA_Full_Cohort_Analysis.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n[SUCCESS] Saved: {output_file}")
print(f"  All 4 panels now show data visualizations (no text panels)")

plt.close()
