#!/usr/bin/env python3
"""
Generate professional academic-style PDF from markdown manuscript
Uses WeasyPrint for high-quality PDF generation with proper formatting
"""

import re
from weasyprint import HTML, CSS
from datetime import datetime

def extract_metadata(md_content):
    """Extract metadata from markdown frontmatter"""
    metadata = {}

    # Title
    title_match = re.search(r'title:\s*"(.+?)"', md_content, re.DOTALL)
    if title_match:
        metadata['title'] = title_match.group(1).replace('\n', ' ').strip()

    # Author
    author_match = re.search(r'name:\s*(.+?)$', md_content, re.MULTILINE)
    if author_match:
        metadata['author'] = author_match.group(1).strip()

    # Email
    email_match = re.search(r'email:\s*(.+?)$', md_content, re.MULTILINE)
    if email_match:
        metadata['email'] = email_match.group(1).strip()

    # Affiliation
    affil_match = re.search(r'affiliation:\s*(.+?)$', md_content, re.MULTILINE)
    if affil_match:
        metadata['affiliation'] = affil_match.group(1).strip()

    # Abstract
    abstract_match = re.search(r'abstract:\s*\|\s*\n(.*?)\n\n---', md_content, re.DOTALL)
    if abstract_match:
        abstract_text = abstract_match.group(1).strip()
        # Remove leading spaces from each line
        abstract_lines = [line.strip() for line in abstract_text.split('\n') if line.strip()]
        metadata['abstract'] = '\n\n'.join(abstract_lines)

    # Keywords
    keywords_match = re.search(r'\*\*Keywords:\*\*\s*(.+?)$', md_content, re.MULTILINE)
    if keywords_match:
        metadata['keywords'] = keywords_match.group(1).strip()

    return metadata

def extract_sections(md_content):
    """Extract main content sections"""
    # Remove frontmatter
    content = re.sub(r'^---.*?---', '', md_content, flags=re.DOTALL)

    # Remove abstract (already extracted)
    content = re.sub(r'abstract:.*?\n\n---', '', content, flags=re.DOTALL)

    # Split into sections by # headers
    sections = []
    current_section = None

    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            if current_section:
                sections.append(current_section)
            section_title = line.lstrip('#').strip()
            current_section = {
                'title': section_title,
                'content': [],
                'subsections': []
            }
        elif line.startswith('## ') and current_section:
            subsection_title = line.lstrip('#').strip()
            current_section['subsections'].append({
                'title': subsection_title,
                'content': []
            })
        elif current_section:
            if current_section['subsections']:
                current_section['subsections'][-1]['content'].append(line)
            else:
                current_section['content'].append(line)

    if current_section:
        sections.append(current_section)

    return sections

def markdown_to_html(text):
    """Convert markdown formatting to HTML"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*([^\*]+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    # Superscript (citations like [1])
    text = re.sub(r'\[(\d+)\]', r'<sup>[\1]</sup>', text)

    return text

def process_content(lines):
    """Process content lines into HTML"""
    html_parts = []
    in_list = False
    in_table = False
    current_para = []

    for line in lines:
        line = line.strip()

        if not line:
            if current_para:
                para_text = ' '.join(current_para)
                para_text = markdown_to_html(para_text)
                html_parts.append(f'<p>{para_text}</p>')
                current_para = []
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            continue

        # Table
        if line.startswith('|'):
            if not in_table:
                html_parts.append('<table>')
                in_table = True

            cells = [cell.strip() for cell in line.split('|')[1:-1]]

            # Check if header separator
            if all(re.match(r'^[-:]+$', cell) for cell in cells):
                continue

            # Determine if header row (first row)
            if in_table and len(html_parts) == 1:
                html_parts.append('<thead><tr>')
                for cell in cells:
                    html_parts.append(f'<th>{markdown_to_html(cell)}</th>')
                html_parts.append('</tr></thead><tbody>')
            else:
                html_parts.append('<tr>')
                for cell in cells:
                    html_parts.append(f'<td>{markdown_to_html(cell)}</td>')
                html_parts.append('</tr>')
            continue
        elif in_table:
            html_parts.append('</tbody></table>')
            in_table = False

        # Lists
        if line.startswith(('- ', '* ', '1. ', '2. ', '3. ', '4. ', '5. ')):
            if current_para:
                para_text = ' '.join(current_para)
                para_text = markdown_to_html(para_text)
                html_parts.append(f'<p>{para_text}</p>')
                current_para = []

            if not in_list:
                html_parts.append('<ul>')
                in_list = True

            list_text = re.sub(r'^[\-\*\d\.]\s+', '', line)
            list_text = markdown_to_html(list_text)
            html_parts.append(f'<li>{list_text}</li>')
            continue

        if in_list:
            html_parts.append('</ul>')
            in_list = False

        # Regular paragraph
        current_para.append(line)

    # Clean up remaining
    if current_para:
        para_text = ' '.join(current_para)
        para_text = markdown_to_html(para_text)
        html_parts.append(f'<p>{para_text}</p>')

    if in_list:
        html_parts.append('</ul>')

    if in_table:
        html_parts.append('</tbody></table>')

    return '\n'.join(html_parts)

def create_html(md_file):
    """Create professional HTML from markdown"""

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    metadata = extract_metadata(md_content)
    sections = extract_sections(md_content)

    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata.get('title', 'Manuscript')}</title>
    <style>
        @page {{
            size: letter;
            margin: 1in;
            @bottom-center {{
                content: counter(page);
                font-family: 'Times New Roman', Times, serif;
                font-size: 10pt;
            }}
        }}

        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #000;
            text-align: justify;
        }}

        .title-page {{
            text-align: center;
            margin-bottom: 2em;
            page-break-after: avoid;
        }}

        h1.title {{
            font-size: 18pt;
            font-weight: bold;
            margin: 0.5em 0 1em 0;
            line-height: 1.3;
            text-align: center;
        }}

        .author {{
            font-size: 14pt;
            margin: 0.5em 0;
        }}

        .affiliation {{
            font-size: 12pt;
            font-style: italic;
            margin: 0.3em 0;
        }}

        .email {{
            font-size: 11pt;
            margin: 0.3em 0;
        }}

        .date {{
            font-size: 11pt;
            margin: 1em 0;
            color: #666;
        }}

        .abstract-section {{
            margin: 2em 0;
            page-break-inside: avoid;
        }}

        .abstract-title {{
            font-size: 14pt;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1em;
        }}

        .abstract-content {{
            text-align: justify;
            margin: 0 2em;
        }}

        .keywords {{
            margin: 1em 2em;
            font-size: 11pt;
        }}

        h1 {{
            font-size: 16pt;
            font-weight: bold;
            margin: 1.5em 0 0.8em 0;
            page-break-after: avoid;
            border-bottom: 2px solid #000;
            padding-bottom: 0.3em;
        }}

        h2 {{
            font-size: 14pt;
            font-weight: bold;
            margin: 1.2em 0 0.6em 0;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 12pt;
            font-weight: bold;
            margin: 1em 0 0.5em 0;
            page-break-after: avoid;
        }}

        p {{
            margin: 0.8em 0;
            text-indent: 0;
        }}

        ul, ol {{
            margin: 0.8em 0;
            padding-left: 2em;
        }}

        li {{
            margin: 0.4em 0;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #000;
            padding: 8px;
            text-align: left;
        }}

        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}

        strong {{
            font-weight: bold;
        }}

        em {{
            font-style: italic;
        }}

        code {{
            font-family: 'Courier New', Courier, monospace;
            background-color: #f5f5f5;
            padding: 2px 4px;
            font-size: 11pt;
        }}

        sup {{
            font-size: 10pt;
            vertical-align: super;
        }}

        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        .page-break {{
            page-break-before: always;
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <h1 class="title">{metadata.get('title', '')}</h1>
        <div class="author">{metadata.get('author', '')}</div>
        <div class="affiliation">{metadata.get('affiliation', '')}</div>
        <div class="email">{metadata.get('email', '')}</div>
        <div class="date">{datetime.now().strftime('%B %d, %Y')}</div>
    </div>
"""

    # Abstract
    if 'abstract' in metadata:
        html += f"""
    <div class="abstract-section">
        <div class="abstract-title">ABSTRACT</div>
        <div class="abstract-content">
"""
        # Split abstract into paragraphs
        abstract_paragraphs = metadata['abstract'].split('\n\n')
        for para in abstract_paragraphs:
            if para.strip():
                para_html = markdown_to_html(para.strip())
                html += f"            <p>{para_html}</p>\n"

        if 'keywords' in metadata:
            keywords_html = markdown_to_html(metadata['keywords'])
            html += f"""            <p class="keywords"><strong>Keywords:</strong> {keywords_html}</p>\n"""

        html += """        </div>
    </div>

    <div class="page-break"></div>
"""

    # Main content
    for section in sections:
        if section['title'].lower() in ['acknowledgments', 'references',
                                          'supplementary materials']:
            html += '    <div class="page-break"></div>\n'

        html += f'    <h1>{section["title"]}</h1>\n'

        if section['content']:
            content_html = process_content(section['content'])
            html += f'    {content_html}\n'

        for subsection in section['subsections']:
            html += f'    <h2>{subsection["title"]}</h2>\n'
            subsection_html = process_content(subsection['content'])
            html += f'    {subsection_html}\n'

    html += """
</body>
</html>"""

    return html

def generate_pdf(md_file, output_pdf):
    """Generate professional PDF using WeasyPrint"""

    print("Converting markdown to HTML...")
    html_content = create_html(md_file)

    # Save HTML for debugging
    html_file = output_pdf.replace('.pdf', '.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML saved: {html_file}")

    print("Generating PDF...")
    HTML(string=html_content).write_pdf(output_pdf)

    print(f"✅ Professional PDF generated: {output_pdf}")

if __name__ == "__main__":
    md_file = "biorxiv_manuscript.md"
    output_pdf = "biorxiv_manuscript_professional.pdf"

    generate_pdf(md_file, output_pdf)
