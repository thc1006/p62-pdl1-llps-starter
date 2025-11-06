#!/usr/bin/env python3
"""
Generate placeholder figure images for PDF submission using matplotlib
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

def create_placeholder_figure(filename, title, width=12, height=8):
    """Create a placeholder figure with title using matplotlib"""
    fig, ax = plt.subplots(1, 1, figsize=(width, height))

    # Remove axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Add border
    rect = patches.Rectangle((0.05, 0.05), 0.9, 0.9, linewidth=3,
                              edgecolor='#2c3e50', facecolor='white')
    ax.add_patch(rect)

    # Add title text (centered)
    ax.text(0.5, 0.55, title,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=28, fontweight='bold',
            color='#2c3e50',
            family='sans-serif')

    # Add subtitle
    subtitle = "[Figure placeholder - Replace with actual figure]"
    ax.text(0.5, 0.45, subtitle,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=18,
            color='#7f8c8d',
            family='sans-serif',
            style='italic')

    # Save with high DPI
    output_path = Path('outputs/figures') / filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    size_kb = output_path.stat().st_size // 1024
    print(f"Created: {output_path} ({size_kb} KB)")

def main():
    """Generate all placeholder figures"""
    figures = [
        ('Figure1_pipeline_flowchart.png', 'Figure 1: Analytical Pipeline'),
        ('Figure2_correlations.png', 'Figure 2: Gene Expression Correlations'),
        ('Figure3_immune_environment.png', 'Figure 3: Immune Microenvironment'),
        ('Figure4_survival_analysis.png', 'Figure 4: Survival Analysis'),
        ('FigureS1_study_design.png', 'Supplementary Figure S1: Study Design'),
        ('FigureS2_sample_characteristics.png', 'Supplementary Figure S2: Sample Characteristics'),
    ]

    print("Generating placeholder figures...")
    for filename, title in figures:
        # Adjust size for different figures
        if 'pipeline' in filename or 'study_design' in filename:
            create_placeholder_figure(filename, title, width=14, height=9)
        else:
            create_placeholder_figure(filename, title, width=12, height=8)

    print("\n✅ All placeholder figures created successfully!")
    print("\nFiles created in outputs/figures/:")
    for filename, _ in figures:
        path = Path('outputs/figures') / filename
        if path.exists():
            print(f"  - {filename} ({path.stat().st_size // 1024} KB)")

if __name__ == '__main__':
    main()
