#!/usr/bin/env python3
"""
Direct conversion of clean manuscript to professional PDF
"""

import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
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

    # Title
    if match := re.search(r'title:\s*"(.+?)"', fm_text, re.DOTALL):
        metadata['title'] = match.group(1).strip()

    # Author
    if match := re.search(r'name:\s*(.+?)$', fm_text, re.MULTILINE):
        metadata['author'] = match.group(1).strip()

    # Email
    if match := re.search(r'email:\s*(.+?)$', fm_text, re.MULTILINE):
        metadata['email'] = match.group(1).strip()

    # Affiliation
    if match := re.search(r'affiliation:\s*(.+?)$', fm_text, re.MULTILINE):
        metadata['affiliation'] = match.group(1).strip()

    # Abstract
    if match := re.search(r'abstract:\s*\|\s*\n(.*?)\nkeywords:', fm_text, re.DOTALL):
        metadata['abstract'] = match.group(1).strip()

    # Keywords
    if match := re.search(r'keywords:\s*(.+?)$', fm_text, re.MULTILINE):
        metadata['keywords'] = match.group(1).strip()

    # Remove frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', md_content, flags=re.DOTALL)

    return metadata, content

def md_to_reportlab(text):
    """Convert markdown to reportlab-compatible text"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*([^\*\n]+?)\*', r'<i>\1</i>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text)
    # Remove markdown links (keep text only)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # Citations
    text = re.sub(r'\[\^(\d+)\]', r'<super>[\1]</super>', text)

    return text

def create_pdf(md_file, output_pdf):
    """Create professional PDF"""

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    metadata, content = extract_frontmatter(md_content)

    # PDF setup
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )

    author_style = ParagraphStyle(
        'Author',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    abstract_style = ParagraphStyle(
        'Abstract',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        leftIndent=36,
        rightIndent=36,
        spaceAfter=12,
        leading=14
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontSize=14,
        fontName='Helvetica-Bold',
        spaceAfter=12,
        spaceBefore=18,
        textColor=colors.HexColor('#000000'),
        borderWidth=1,
        borderPadding=4,
        borderColor=colors.HexColor('#000000'),
        borderRadius=None
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=12,
        fontName='Helvetica-Bold',
        spaceAfter=10,
        spaceBefore=14
    )

    # Title page
    story.append(Paragraph(metadata.get('title', 'Manuscript'), title_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph(metadata.get('author', ''), author_style))
    story.append(Paragraph(metadata.get('affiliation', ''), author_style))
    story.append(Paragraph(metadata.get('email', ''), author_style))
    story.append(Paragraph(datetime.now().strftime('%B %d, %Y'), author_style))

    story.append(Spacer(1, 0.4*inch))

    # Abstract
    if 'abstract' in metadata:
        story.append(Paragraph('<b>ABSTRACT</b>', h2_style))
        abstract_text = md_to_reportlab(metadata['abstract'])
        story.append(Paragraph(abstract_text, abstract_style))

        if 'keywords' in metadata:
            keywords_text = f"<b>Keywords:</b> {md_to_reportlab(metadata['keywords'])}"
            story.append(Paragraph(keywords_text, abstract_style))

    story.append(PageBreak())

    # Process content
    lines = content.split('\n')
    current_para = []

    for line in lines:
        line = line.strip()

        if not line:
            if current_para:
                para_text = ' '.join(current_para)
                para_text = md_to_reportlab(para_text)
                story.append(Paragraph(para_text, body_style))
                current_para = []
            continue

        # Headers
        if line.startswith('# '):
            if current_para:
                para_text = ' '.join(current_para)
                story.append(Paragraph(md_to_reportlab(para_text), body_style))
                current_para = []

            title = line.lstrip('#').strip()
            story.append(Paragraph(title, h1_style))
            continue

        elif line.startswith('## '):
            if current_para:
                para_text = ' '.join(current_para)
                story.append(Paragraph(md_to_reportlab(para_text), body_style))
                current_para = []

            title = line.lstrip('#').strip()
            story.append(Paragraph(title, h2_style))
            continue

        # Lists
        if line.startswith(('- ', '* ', '1. ')):
            if current_para:
                para_text = ' '.join(current_para)
                story.append(Paragraph(md_to_reportlab(para_text), body_style))
                current_para = []

            list_text = re.sub(r'^[\-\*\d\.]\s+', '• ', line)
            story.append(Paragraph(md_to_reportlab(list_text), body_style))
            continue

        current_para.append(line)

    # Final paragraph
    if current_para:
        para_text = ' '.join(current_para)
        story.append(Paragraph(md_to_reportlab(para_text), body_style))

    # Build PDF
    print("Generating professional PDF...")
    doc.build(story)
    print(f"[SUCCESS] PDF generated: {output_pdf}")

if __name__ == "__main__":
    create_pdf("biorxiv_clean.md", "biorxiv_FINAL.pdf")
