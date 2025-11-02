#!/usr/bin/env python3
"""
Generate optimized academic PDF with better spacing and layout
Reduced whitespace, improved readability, better figure placement
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
    # Scientific notation with Unicode superscripts - convert to readable format
    # e.g., "9.3×10⁻⁶" → "9.3×10^-6" or better HTML representation
    text = re.sub(r'(\d+\.?\d*)\s*[×x]\s*10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)', convert_scientific_notation, text)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*([^\*\n]+?)\*', r'<i>\1</i>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<font name="Courier" size="9">\1</font>', text)
    # Remove links (keep text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # Citations - use proper superscript
    text = re.sub(r'\[\^(\d+)\]', r'<super>[\1]</super>', text)

    return text

def convert_scientific_notation(match):
    """Convert Unicode superscript scientific notation to HTML"""
    base = match.group(1)
    superscript = match.group(2)

    # Map Unicode superscripts to regular numbers
    superscript_map = {
        '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
        '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
        '⁻': '-'
    }

    # Convert Unicode superscript to regular string
    exponent = ''.join(superscript_map.get(c, c) for c in superscript)

    # Return HTML with proper superscript
    return f'{base}×10<super>{exponent}</super>'

def find_figure_files():
    """Find available figure files"""
    figures = {}

    figure_map = {
        'fig1': [
            '../outputs/figures/Figure2_TCGA_Correlation.png',
            'outputs/figures/Figure2_TCGA_Correlation.png',
        ],
        'fig2': [
            '../outputs/tcga_full_cohort/TCGA_Full_Cohort_Analysis.png',
            'outputs/tcga_full_cohort/TCGA_Full_Cohort_Analysis.png',
        ],
        'fig3': [
            '../outputs/survival_analysis_v2/Figure3_multivariate_cox.png',
            'outputs/survival_analysis_v2/Figure3_multivariate_cox.png',
            '../outputs/survival_analysis/kaplan_meier_curves.png',
            'outputs/survival_analysis/kaplan_meier_curves.png',
        ],
        'figS2': [
            '../outputs/partial_correlation/Figure_S2_partial_correlation.png',
            'outputs/partial_correlation/Figure_S2_partial_correlation.png',
        ],
        'fig4': [
            '../outputs/cptac_validation/Figure4_cptac_validation.png',
            'outputs/cptac_validation/Figure4_cptac_validation.png',
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
    """Create optimized paragraph styles with tighter spacing"""
    styles = getSampleStyleSheet()

    # Title - slightly smaller, tighter spacing
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=15,
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=16,
        fontName='Times-Bold'
    ))

    # Author info - more compact
    styles.add(ParagraphStyle(
        name='Author',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Times-Roman'
    ))

    # Abstract - tighter leading
    styles.add(ParagraphStyle(
        name='AbstractBody',
        parent=styles['BodyText'],
        fontSize=10.5,
        alignment=TA_JUSTIFY,
        leftIndent=36,
        rightIndent=36,
        spaceAfter=8,
        leading=13,
        fontName='Times-Roman'
    ))

    # Body text - optimized spacing
    styles.add(ParagraphStyle(
        name='Body',
        parent=styles['BodyText'],
        fontSize=10.5,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=13,
        fontName='Times-Roman'
    ))

    # H1 - reduced spacing
    styles.add(ParagraphStyle(
        name='H1',
        parent=styles['Heading1'],
        fontSize=13,
        fontName='Times-Bold',
        spaceAfter=8,
        spaceBefore=14,
        textColor=colors.black,
        keepWithNext=True
    ))

    # H2 - tighter spacing
    styles.add(ParagraphStyle(
        name='H2',
        parent=styles['Heading2'],
        fontSize=11.5,
        fontName='Times-Bold',
        spaceAfter=6,
        spaceBefore=10,
        keepWithNext=True
    ))

    # Caption - compact
    styles.add(ParagraphStyle(
        name='Caption',
        parent=styles['Normal'],
        fontSize=9.5,
        alignment=TA_JUSTIFY,
        fontName='Times-Italic',
        spaceAfter=8,
        leading=11
    ))

    return styles

def add_figure(story, fig_path, caption, styles, figure_num, max_height=4.5):
    """Add figure with caption - adaptive sizing"""
    if os.path.exists(fig_path):
        # Adaptive figure sizing - smaller max height to fit more content per page
        img = Image(fig_path, width=6*inch, height=max_height*inch, kind='proportional')

        # Compact caption
        caption_text = f"<b>Figure {figure_num}.</b> {caption}"
        caption_para = Paragraph(caption_text, styles['Caption'])

        # Keep figure and caption together with minimal spacing
        story.append(KeepTogether([img, Spacer(1, 0.05*inch), caption_para]))
        story.append(Spacer(1, 0.15*inch))
        return True
    return False

def create_pdf(md_file, output_pdf):
    """Create optimized PDF with better spacing"""

    print("="*60)
    print("Generating Optimized Academic PDF")
    print("="*60)

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    metadata, content = extract_frontmatter(md_content)
    figures = find_figure_files()

    print(f"\nFound {len(figures)} figures to embed")

    # PDF setup with slightly smaller margins
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        rightMargin=65,
        leftMargin=65,
        topMargin=65,
        bottomMargin=65
    )

    story = []
    styles = create_styles()

    # Title page - compact
    story.append(Paragraph(metadata.get('title', 'Manuscript'), styles['CustomTitle']))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(metadata.get('author', ''), styles['Author']))
    story.append(Paragraph(metadata.get('affiliation', ''), styles['Author']))
    story.append(Paragraph(metadata.get('email', ''), styles['Author']))
    story.append(Paragraph(datetime.now().strftime('%B %d, %Y'), styles['Author']))
    story.append(Spacer(1, 0.3*inch))

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
    in_results = False

    for i, line in enumerate(lines):
        line = line.strip()

        # Skip empty lines but don't add excessive spacing
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

            # Add page break only before Discussion and References
            if title in ['Discussion', 'References']:
                story.append(PageBreak())

            story.append(Paragraph(title, styles['H1']))

            # Track Results section
            if title == 'Results':
                in_results = True
                story.append(Spacer(1, 0.1*inch))

            continue

        elif line.startswith('## '):
            if current_para:
                story.append(Paragraph(md_to_html(' '.join(current_para)), styles['Body']))
                current_para = []

            title = line.lstrip('#').strip()

            # Insert figures after specific subsections
            if in_results:
                # After "Expression Correlations" subsection
                if 'Expression Correlations' in title or 'Correlations Among' in title:
                    story.append(Paragraph(title, styles['H2']))

                    # Add Figure 1 (correlation heatmap) - smaller
                    if 'fig1' in figures:
                        if add_figure(
                            story, figures['fig1'],
                            "Expression correlations among PD-L1 regulatory proteins across 1,300 tumor samples. ***P<0.001.",
                            styles, figure_counter, max_height=3.5
                        ):
                            figure_counter += 1

                    # Add Figure 2 (4-panel) - moderate size
                    if 'fig2' in figures:
                        if add_figure(
                            story, figures['fig2'],
                            "TCGA comprehensive analysis. (A) SQSTM1 vs CD274 scatter plot. (B) Correlation heatmap. (C) Expression distributions. (D) Summary statistics.",
                            styles, figure_counter, max_height=4.2
                        ):
                            figure_counter += 1
                    continue

                # After "Partial Correlation" subsection
                elif 'Partial Correlation' in title:
                    story.append(Paragraph(title, styles['H2']))

                    if 'figS2' in figures:
                        if add_figure(
                            story, figures['figS2'],
                            "Partial correlation analysis controlling for confounding factors. Six-panel analysis showing simple vs. partial correlations.",
                            styles, f"S{figure_counter}", max_height=4.5
                        ):
                            figure_counter += 1
                    continue

                # After "Multivariate Cox" subsection
                elif 'Multivariate Cox' in title or 'Survival Analysis' in title:
                    story.append(Paragraph(title, styles['H2']))

                    if 'fig3' in figures:
                        if add_figure(
                            story, figures['fig3'],
                            "Multivariate Cox survival analysis adjusting for clinical covariates. Four-panel Kaplan-Meier curves with forest plot.",
                            styles, figure_counter, max_height=4.2
                        ):
                            figure_counter += 1
                    continue

                # After "Protein-Level Validation" subsection
                elif 'Protein' in title and 'Validation' in title:
                    story.append(Paragraph(title, styles['H2']))

                    if 'fig4' in figures:
                        if add_figure(
                            story, figures['fig4'],
                            "CPTAC protein-level validation. Six-panel analysis showing mRNA vs protein correlation concordance.",
                            styles, figure_counter, max_height=4.5
                        ):
                            figure_counter += 1
                    continue

            story.append(Paragraph(title, styles['H2']))
            continue

        # Lists - more compact
        if line.startswith(('- ', '* ', '1. ', '2. ', '3. ', '4. ', '5. ', '6. ')):
            if current_para:
                story.append(Paragraph(md_to_html(' '.join(current_para)), styles['Body']))
                current_para = []

            list_text = re.sub(r'^[\-\*\d\.]\s+', '• ', line)
            story.append(Paragraph(md_to_html(list_text), styles['Body']))
            continue

        # Skip metadata lines
        if line.startswith('**Word Count:**') or line.startswith('**Figures:**') or line.startswith('**Tables:**'):
            continue

        current_para.append(line)

    # Final paragraph
    if current_para:
        para_text = ' '.join(current_para)
        if not (para_text.startswith('**Word Count:') or
                para_text.startswith('**Figures:') or
                para_text.startswith('**Tables:')):
            story.append(Paragraph(md_to_html(para_text), styles['Body']))

    # Build PDF
    print("\nBuilding optimized PDF...")
    doc.build(story)

    print("="*60)
    print(f"SUCCESS! Optimized PDF: {output_pdf}")
    print("="*60)
    print("\nOptimizations Applied:")
    print("  [OK] Reduced line spacing (15→13pt)")
    print("  [OK] Tighter paragraph spacing (12→8pt)")
    print("  [OK] Smaller margins (72→65pt)")
    print("  [OK] Adaptive figure sizing")
    print("  [OK] Minimal figure-caption gap")
    print(f"  [OK] {figure_counter-1} figures embedded")
    print("\nResult: Better page utilization, improved readability")
    print("="*60)

if __name__ == "__main__":
    create_pdf("biorxiv_clean.md", "biorxiv_OPTIMIZED.pdf")
