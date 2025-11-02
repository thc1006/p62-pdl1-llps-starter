#!/usr/bin/env python3
"""
Generate PDF from bioRxiv manuscript markdown file
Uses reportlab for PDF generation
"""

import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
import markdown2

def clean_markdown_frontmatter(text):
    """Remove YAML frontmatter from markdown"""
    # Remove frontmatter between --- markers
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    return text

def markdown_to_html(md_text):
    """Convert markdown to HTML"""
    # Clean frontmatter first
    md_text = clean_markdown_frontmatter(md_text)

    # Convert markdown to HTML
    html = markdown2.markdown(md_text, extras=['tables', 'fenced-code-blocks', 'header-ids'])
    return html

def html_to_reportlab_elements(html_content, styles):
    """Convert HTML to ReportLab flowable elements"""
    elements = []

    # Simple parsing - split by common HTML tags
    # This is a simplified version - real HTML parsing would be more complex

    # Remove HTML tags but keep text structure
    paragraphs = re.split(r'<(?:p|h[1-6]|li|td)>', html_content)

    for para in paragraphs:
        if not para.strip():
            continue

        # Remove closing tags
        text = re.sub(r'</[^>]+>', '', para)
        text = re.sub(r'<[^>]+>', '', text)  # Remove remaining tags
        text = text.strip()

        if not text:
            continue

        # Determine style based on content
        if text.startswith('#'):
            # Header
            level = len(re.match(r'^#+', text).group())
            text = text.lstrip('#').strip()
            if level == 1:
                elements.append(Paragraph(text, styles['Title']))
            elif level == 2:
                elements.append(Paragraph(text, styles['Heading1']))
            elif level == 3:
                elements.append(Paragraph(text, styles['Heading2']))
            else:
                elements.append(Paragraph(text, styles['Heading3']))
        else:
            # Regular paragraph
            elements.append(Paragraph(text, styles['Normal']))

        elements.append(Spacer(1, 0.1*inch))

    return elements

def create_pdf(md_file, output_pdf):
    """Create PDF from markdown file"""

    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract title and author from frontmatter
    title_match = re.search(r'title:\s*"(.+?)"', md_content)
    author_match = re.search(r'name:\s*(.+?)$', md_content, re.MULTILINE)
    email_match = re.search(r'email:\s*(.+?)$', md_content, re.MULTILINE)
    affil_match = re.search(r'affiliation:\s*(.+?)$', md_content, re.MULTILINE)

    title_text = title_match.group(1) if title_match else "Manuscript"
    author_text = author_match.group(1).strip() if author_match else ""
    email_text = email_match.group(1).strip() if email_match else ""
    affil_text = affil_match.group(1).strip() if affil_match else ""

    # Create PDF
    doc = SimpleDocTemplate(output_pdf, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    # Container for elements
    story = []

    # Styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='black',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    author_style = ParagraphStyle(
        'Author',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    abstract_title_style = ParagraphStyle(
        'AbstractTitle',
        parent=styles['Heading2'],
        fontSize=14,
        fontName='Helvetica-Bold',
        spaceAfter=12
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    )

    # Add title
    story.append(Paragraph(title_text, title_style))
    story.append(Spacer(1, 0.2*inch))

    # Add author info
    if author_text:
        story.append(Paragraph(author_text, author_style))
    if affil_text:
        story.append(Paragraph(affil_text, author_style))
    if email_text:
        story.append(Paragraph(email_text, author_style))

    story.append(Spacer(1, 0.3*inch))

    # Extract and add abstract
    abstract_match = re.search(r'abstract:\s*\|\s*\n(.*?)\n\n', md_content, re.DOTALL)
    if abstract_match:
        abstract_text = abstract_match.group(1).strip()
        # Remove markdown formatting
        abstract_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', abstract_text)
        abstract_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', abstract_text)

        story.append(Paragraph('<b>ABSTRACT</b>', abstract_title_style))

        # Split abstract into paragraphs
        for para in abstract_text.split('\n\n'):
            if para.strip():
                story.append(Paragraph(para.strip(), body_style))

    story.append(PageBreak())

    # Convert markdown to HTML (excluding frontmatter and abstract)
    # Remove frontmatter and abstract
    main_content = re.sub(r'^---.*?---', '', md_content, flags=re.DOTALL)
    main_content = re.sub(r'abstract:.*?\n\n', '', main_content, flags=re.DOTALL)

    # Convert markdown to simple text sections
    sections = re.split(r'\n# ', main_content)

    for section in sections[1:]:  # Skip first empty split
        if not section.strip():
            continue

        lines = section.split('\n')
        section_title = lines[0].strip()

        # Add section title
        story.append(Paragraph(section_title, styles['Heading1']))
        story.append(Spacer(1, 0.1*inch))

        # Process section content
        current_para = []

        for line in lines[1:]:
            line = line.strip()

            if not line:
                if current_para:
                    para_text = ' '.join(current_para)
                    # Simple markdown formatting
                    para_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', para_text)
                    para_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', para_text)
                    para_text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', para_text)

                    story.append(Paragraph(para_text, body_style))
                    current_para = []
                continue

            # Handle subsections
            if line.startswith('## '):
                if current_para:
                    para_text = ' '.join(current_para)
                    para_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', para_text)
                    story.append(Paragraph(para_text, body_style))
                    current_para = []

                subsection_title = line.lstrip('#').strip()
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(subsection_title, styles['Heading2']))
                story.append(Spacer(1, 0.05*inch))
                continue

            # Handle lists
            if line.startswith(('- ', '* ', '1. ', '2. ', '3. ')):
                if current_para:
                    para_text = ' '.join(current_para)
                    para_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', para_text)
                    story.append(Paragraph(para_text, body_style))
                    current_para = []

                list_item = re.sub(r'^[\-\*\d\.]\s+', '• ', line)
                list_item = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', list_item)
                story.append(Paragraph(list_item, body_style))
                continue

            current_para.append(line)

        # Handle remaining paragraph
        if current_para:
            para_text = ' '.join(current_para)
            para_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', para_text)
            para_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', para_text)
            story.append(Paragraph(para_text, body_style))

    # Build PDF
    doc.build(story)
    print(f"PDF generated successfully: {output_pdf}")

if __name__ == "__main__":
    md_file = "biorxiv_manuscript.md"
    output_pdf = "biorxiv_manuscript.pdf"

    create_pdf(md_file, output_pdf)
