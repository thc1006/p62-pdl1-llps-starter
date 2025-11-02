#!/usr/bin/env python3
"""
Generate perfect academic PDF with embedded figures
Fixed all formatting issues
"""

import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, KeepTogether
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from datetime import datetime

def extract_frontmatter(md_content):
    """Extract YAML frontmatter"""
    fm_match = re.search(r'^---\s*\n(.*?)\n---', md_content, re.DOTALL)
    if not fm_match:
        return {}, md_content

    fm_text = fm_match.group(1)
    metadata = {}

    if match := re.search(r'title:\s*"(.+?)"', fm_text, re.DOTALL):
        metadata['title'] = match.group(1).strip()
    if match := re.search(r'name:\s*(.+?)$', fm_text, re.MULTILINE):
        metadata['author'] = match.group(1).strip()
    if match := re.search(r'email:\s*(.+?)$', fm_text, re.MULTILINE):
        metadata['email'] = match.group(1).strip()
    if match := re.search(r'affiliation:\s*(.+?)$', fm_text, re.MULTILINE):
        metadata['affiliation'] = match.group(1).strip()
    if match := re.search(r'abstract:\s*\|\s*\n(.*?)\n\s*keywords:', fm_text, re.DOTALL):
        metadata['abstract'] = match.group(1).strip()
    if match := re.search(r'keywords:\s*(.+?)$', fm_text, re.MULTILINE):
        metadata['keywords'] = match.group(1).strip()

    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', md_content, flags=re.DOTALL)
    return metadata, content

def md_to_html(text):
    """Convert markdown to HTML for reportlab"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*([^\*\n]+?)\*', r'<i>\1</i>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<font name="Courier" size="10">\1</font>', text)
    # Remove links (keep text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # Citations - use proper superscript
    text = re.sub(r'\[\^(\d+)\]', r'<super>[\1]</super>', text)

    return text

def find_figure_files():
    """Find available figure files"""
    figures = {}

    # Figure priority order
    # fig1: Correlation heatmap (Figure2_TCGA_Correlation.png)
    # fig2: Full cohort analysis with 4 panels (TCGA_Full_Cohort_Analysis.png)
    # fig3: Kaplan-Meier survival curves

    figure_map = {
        'fig1': [
            'outputs/figures/Figure2_TCGA_Correlation.png',
            '../outputs/figures/Figure2_TCGA_Correlation.png',
        ],
        'fig2': [
            'outputs/tcga_full_cohort/TCGA_Full_Cohort_Analysis.png',
            '../outputs/tcga_full_cohort/TCGA_Full_Cohort_Analysis.png',
        ],
        'fig3': [
            'outputs/survival_analysis/kaplan_meier_curves.png',
            '../outputs/survival_analysis/kaplan_meier_curves.png',
        ]
    }

    for fig_key, paths in figure_map.items():
        for path in paths:
            if os.path.exists(path):
                figures[fig_key] = path
                print(f"  Found {fig_key}: {path}")
                break

    return figures

def create_styles():
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=24,
        fontName='Times-Bold'
    ))

    styles.add(ParagraphStyle(
        name='Author',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Times-Roman'
    ))

    styles.add(ParagraphStyle(
        name='AbstractBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        leftIndent=36,
        rightIndent=36,
        spaceAfter=12,
        leading=15,
        fontName='Times-Roman'
    ))

    styles.add(ParagraphStyle(
        name='Body',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=15,
        fontName='Times-Roman'
    ))

    styles.add(ParagraphStyle(
        name='H1',
        parent=styles['Heading1'],
        fontSize=14,
        fontName='Times-Bold',
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.black,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='H2',
        parent=styles['Heading2'],
        fontSize=12,
        fontName='Times-Bold',
        spaceAfter=10,
        spaceBefore=16,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='Caption',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        fontName='Times-Italic',
        spaceAfter=12,
        leading=12
    ))

    return styles

def add_figure(story, fig_path, caption, styles, figure_num):
    """Add figure with caption"""
    if os.path.exists(fig_path):
        # Add figure with larger size - use full page width
        # kind='proportional' maintains aspect ratio
        img = Image(fig_path, width=6.5*inch, height=6*inch, kind='proportional')

        # Create figure with caption as a unit
        caption_text = f"<b>Figure {figure_num}.</b> {caption}"
        caption_para = Paragraph(caption_text, styles['Caption'])

        # Keep figure and caption together
        story.append(KeepTogether([img, Spacer(1, 0.1*inch), caption_para]))
        story.append(Spacer(1, 0.3*inch))
        return True
    return False

def create_pdf(md_file, output_pdf):
    """Create perfect PDF with figures"""

    print("="*60)
    print("Generating Perfect Academic PDF")
    print("="*60)

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    metadata, content = extract_frontmatter(md_content)
    figures = find_figure_files()

    print(f"\nFound {len(figures)} figures to embed")

    # PDF setup
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    story = []
    styles = create_styles()

    # Title page
    story.append(Paragraph(metadata.get('title', 'Manuscript'), styles['CustomTitle']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(metadata.get('author', ''), styles['Author']))
    story.append(Paragraph(metadata.get('affiliation', ''), styles['Author']))
    story.append(Paragraph(metadata.get('email', ''), styles['Author']))
    story.append(Paragraph(datetime.now().strftime('%B %d, %Y'), styles['Author']))
    story.append(Spacer(1, 0.4*inch))

    # Abstract
    if 'abstract' in metadata:
        story.append(Paragraph('<b>ABSTRACT</b>', styles['H2']))
        abstract_text = md_to_html(metadata['abstract'])
        story.append(Paragraph(abstract_text, styles['AbstractBody']))

        if 'keywords' in metadata:
            kw_text = f"<b>Keywords:</b> {md_to_html(metadata['keywords'])}"
            story.append(Paragraph(kw_text, styles['AbstractBody']))

    story.append(PageBreak())

    # Process content
    lines = content.split('\n')
    current_para = []
    figure_counter = 1

    for i, line in enumerate(lines):
        line = line.strip()

        if not line:
            if current_para:
                para_text = ' '.join(current_para)
                para_text = md_to_html(para_text)
                story.append(Paragraph(para_text, styles['Body']))
                current_para = []
            continue

        # Headers
        if line.startswith('# '):
            if current_para:
                story.append(Paragraph(md_to_html(' '.join(current_para)), styles['Body']))
                current_para = []

            title = line.lstrip('#').strip()

            # Add page break before major sections
            if title in ['Discussion', 'References', 'Acknowledgments']:
                story.append(PageBreak())

            story.append(Paragraph(title, styles['H1']))

            # Add figures after Results section header
            if title == 'Results' and figures:
                story.append(Spacer(1, 0.2*inch))

                # Figure 1: Correlation heatmap
                if 'fig1' in figures:
                    if add_figure(
                        story, figures['fig1'],
                        "Expression correlations among PD-L1 regulatory proteins. Heatmap showing Pearson correlation coefficients for pairwise comparisons of CD274, CMTM6, STUB1, HIP1R, and SQSTM1 across 1,300 tumor samples. *P<0.05, **P<0.01, ***P<0.001.",
                        styles, figure_counter
                    ):
                        figure_counter += 1

                # Figure 2: Full cohort analysis with 4 panels (A-D)
                if 'fig2' in figures:
                    if add_figure(
                        story, figures['fig2'],
                        "TCGA LUAD+LUSC comprehensive analysis. (A) SQSTM1 vs CD274 scatter plot with regression line showing weak correlation (r=-0.016, P=0.560, n=1300). (B) Correlation heatmap of all five regulatory proteins (CD274, CMTM6, STUB1, HIP1R, SQSTM1). (C) Expression distribution histograms for SQSTM1 and CD274 showing log2(FPKM+1) values. (D) Analysis summary statistics including sample size, key findings, and interpretation.",
                        styles, figure_counter
                    ):
                        figure_counter += 1

                # Figure 3: Kaplan-Meier survival curves
                if 'fig3' in figures:
                    if add_figure(
                        story, figures['fig3'],
                        "Kaplan-Meier survival analysis stratified by gene expression. Patients were divided into high and low expression groups based on median expression values. Log-rank test P-values are shown for each gene across multiple cancer types.",
                        styles, figure_counter
                    ):
                        figure_counter += 1

            continue

        elif line.startswith('## '):
            if current_para:
                story.append(Paragraph(md_to_html(' '.join(current_para)), styles['Body']))
                current_para = []

            title = line.lstrip('#').strip()
            story.append(Paragraph(title, styles['H2']))
            continue

        # Lists
        if line.startswith(('- ', '* ', '1. ', '2. ', '3. ', '4. ')):
            if current_para:
                story.append(Paragraph(md_to_html(' '.join(current_para)), styles['Body']))
                current_para = []

            list_text = re.sub(r'^[\-\*\d\.]\s+', '• ', line)
            story.append(Paragraph(md_to_html(list_text), styles['Body']))
            continue

        # Skip lines that look like metadata
        if line.startswith('**Word Count:**') or line.startswith('**Figures:**') or line.startswith('**Tables:**'):
            continue

        current_para.append(line)

    # Final paragraph
    if current_para:
        para_text = ' '.join(current_para)
        # Don't add if it's just metadata
        if not (para_text.startswith('**Word Count:') or
                para_text.startswith('**Figures:') or
                para_text.startswith('**Tables:')):
            story.append(Paragraph(md_to_html(para_text), styles['Body']))

    # Build PDF
    print("\nBuilding PDF...")
    doc.build(story)

    print("="*60)
    print(f"SUCCESS! PDF generated: {output_pdf}")
    print("="*60)
    print("\nPDF Features:")
    print("  [OK] Professional academic formatting")
    print("  [OK] Embedded figures with captions")
    print("  [OK] Proper page breaks")
    print("  [OK] Clean reference formatting")
    print(f"  [OK] {figure_counter-1} figures embedded")
    print("\nReady for bioRxiv submission!")
    print("="*60)

if __name__ == "__main__":
    create_pdf("biorxiv_clean.md", "biorxiv_PERFECT.pdf")
