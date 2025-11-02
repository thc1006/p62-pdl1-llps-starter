#!/usr/bin/env python3
"""
Generate professional academic-style HTML that can be printed to PDF via browser
This produces the highest quality output
"""

import re
from datetime import datetime

def extract_metadata(md_content):
    """Extract metadata from markdown frontmatter"""
    metadata = {}

    title_match = re.search(r'title:\s*"(.+?)"', md_content, re.DOTALL)
    if title_match:
        metadata['title'] = title_match.group(1).replace('\n', ' ').strip()

    author_match = re.search(r'name:\s*(.+?)$', md_content, re.MULTILINE)
    if author_match:
        metadata['author'] = author_match.group(1).strip()

    email_match = re.search(r'email:\s*(.+?)$', md_content, re.MULTILINE)
    if email_match:
        metadata['email'] = email_match.group(1).strip()

    affil_match = re.search(r'affiliation:\s*(.+?)$', md_content, re.MULTILINE)
    if affil_match:
        metadata['affiliation'] = affil_match.group(1).strip()

    abstract_match = re.search(r'abstract:\s*\|\s*\n(.*?)\n\n---', md_content, re.DOTALL)
    if abstract_match:
        abstract_text = abstract_match.group(1).strip()
        abstract_lines = [line.strip() for line in abstract_text.split('\n') if line.strip()]
        metadata['abstract'] = abstract_lines

    keywords_match = re.search(r'\*\*Keywords:\*\*\s*(.+?)$', md_content, re.MULTILINE)
    if keywords_match:
        metadata['keywords'] = keywords_match.group(1).strip()

    return metadata

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
    # Citations
    text = re.sub(r'\[(\d+)\]', r'<sup>[\1]</sup>', text)
    return text

def extract_sections(md_content):
    """Extract main content sections"""
    content = re.sub(r'^---.*?---', '', md_content, flags=re.DOTALL)
    content = re.sub(r'abstract:.*?\n\n---', '', content, flags=re.DOTALL)

    sections = []
    current_section = None
    current_subsection = None

    for line in content.split('\n'):
        if line.startswith('# '):
            if current_section:
                sections.append(current_section)
            section_title = line.lstrip('#').strip()
            current_section = {
                'title': section_title,
                'level': 1,
                'content': []
            }
            current_subsection = None
        elif line.startswith('## ') and current_section:
            subsection_title = line.lstrip('#').strip()
            subsection = {
                'title': subsection_title,
                'level': 2,
                'content': []
            }
            current_section['content'].append(subsection)
            current_subsection = subsection
        elif line.startswith('### ') and current_subsection:
            subsubsection_title = line.lstrip('#').strip()
            subsubsection = {
                'title': subsubsection_title,
                'level': 3,
                'content': []
            }
            current_subsection['content'].append(subsubsection)
        elif current_section:
            if current_subsection:
                current_subsection['content'].append(line)
            else:
                current_section['content'].append(line)

    if current_section:
        sections.append(current_section)

    return sections

def process_content_lines(lines):
    """Process content lines into HTML"""
    html_parts = []
    in_list = False
    in_table = False
    current_para = []
    table_rows = []

    for line in lines:
        if isinstance(line, dict):  # Nested section
            if current_para:
                para_text = ' '.join(current_para)
                html_parts.append(f'<p>{markdown_to_html(para_text)}</p>')
                current_para = []
            if line['level'] == 2:
                html_parts.append(f'<h2>{line["title"]}</h2>')
            else:
                html_parts.append(f'<h3>{line["title"]}</h3>')
            html_parts.extend(process_content_lines(line['content']))
            continue

        line = line.strip()

        if not line:
            if current_para:
                para_text = ' '.join(current_para)
                html_parts.append(f'<p>{markdown_to_html(para_text)}</p>')
                current_para = []
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            if in_table and table_rows:
                html_parts.append('<table>')
                for row in table_rows:
                    html_parts.append(row)
                html_parts.append('</table>')
                table_rows = []
                in_table = False
            continue

        # Table
        if line.startswith('|'):
            if current_para:
                para_text = ' '.join(current_para)
                html_parts.append(f'<p>{markdown_to_html(para_text)}</p>')
                current_para = []

            cells = [cell.strip() for cell in line.split('|')[1:-1]]

            if all(re.match(r'^[-:]+$', cell) for cell in cells):
                continue

            if not in_table:
                in_table = True
                table_rows.append('<thead><tr>')
                for cell in cells:
                    table_rows.append(f'<th>{markdown_to_html(cell)}</th>')
                table_rows.append('</tr></thead><tbody>')
            else:
                table_rows.append('<tr>')
                for cell in cells:
                    table_rows.append(f'<td>{markdown_to_html(cell)}</td>')
                table_rows.append('</tr>')
            continue

        # Lists
        if line.startswith(('- ', '* ', '1. ', '2. ', '3. ', '4. ')):
            if current_para:
                para_text = ' '.join(current_para)
                html_parts.append(f'<p>{markdown_to_html(para_text)}</p>')
                current_para = []

            if not in_list:
                html_parts.append('<ul>')
                in_list = True

            list_text = re.sub(r'^[\-\*\d\.]\s+', '', line)
            html_parts.append(f'<li>{markdown_to_html(list_text)}</li>')
            continue

        if in_list:
            html_parts.append('</ul>')
            in_list = False

        current_para.append(line)

    # Clean up
    if current_para:
        para_text = ' '.join(current_para)
        html_parts.append(f'<p>{markdown_to_html(para_text)}</p>')
    if in_list:
        html_parts.append('</ul>')
    if in_table and table_rows:
        html_parts.append('<table>')
        for row in table_rows:
            html_parts.append(row)
        html_parts.append('</tbody></table>')

    return html_parts

def create_professional_html(md_file, output_html):
    """Create professional HTML for printing to PDF"""

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    metadata = extract_metadata(md_content)
    sections = extract_sections(md_content)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + metadata.get('title', 'Manuscript') + """</title>
    <style>
        @page {
            size: letter;
            margin: 1in;
        }

        @media print {
            body {
                margin: 0;
                padding: 0;
            }
            .page-break {
                page-break-before: always;
            }
            h1, h2, h3 {
                page-break-after: avoid;
            }
            p, table {
                orphans: 3;
                widows: 3;
            }
        }

        body {
            font-family: 'Times New Roman', Times, serif;
            font-size: 12pt;
            line-height: 1.8;
            color: #000;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 1in;
            background: #fff;
        }

        .title-section {
            text-align: center;
            margin-bottom: 3em;
        }

        .manuscript-title {
            font-size: 20pt;
            font-weight: bold;
            margin: 1em 0;
            line-height: 1.4;
        }

        .author {
            font-size: 14pt;
            margin: 0.8em 0 0.3em 0;
        }

        .affiliation {
            font-size: 12pt;
            font-style: italic;
            margin: 0.3em 0;
        }

        .email {
            font-size: 11pt;
            color: #0066cc;
            margin: 0.3em 0;
        }

        .date {
            font-size: 11pt;
            margin: 1em 0;
            color: #333;
        }

        .abstract-box {
            margin: 2em 0 3em 0;
            padding: 1.5em;
            border: 1px solid #ccc;
            background: #f9f9f9;
        }

        .abstract-heading {
            font-size: 14pt;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1em;
        }

        .abstract-content p {
            text-align: justify;
            margin: 1em 0;
        }

        .keywords {
            margin-top: 1.5em;
            font-size: 11pt;
        }

        h1 {
            font-size: 16pt;
            font-weight: bold;
            margin: 2em 0 1em 0;
            border-bottom: 2px solid #000;
            padding-bottom: 0.3em;
        }

        h2 {
            font-size: 14pt;
            font-weight: bold;
            margin: 1.5em 0 0.8em 0;
        }

        h3 {
            font-size: 13pt;
            font-weight: bold;
            margin: 1.2em 0 0.6em 0;
            font-style: italic;
        }

        p {
            margin: 1em 0;
            text-align: justify;
            text-indent: 0;
        }

        ul {
            margin: 1em 0;
            padding-left: 2.5em;
        }

        li {
            margin: 0.5em 0;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            font-size: 11pt;
        }

        th, td {
            border: 1px solid #333;
            padding: 10px;
            text-align: left;
        }

        th {
            background-color: #e8e8e8;
            font-weight: bold;
        }

        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }

        code {
            font-family: 'Courier New', Courier, monospace;
            background-color: #f0f0f0;
            padding: 2px 5px;
            font-size: 11pt;
            border-radius: 3px;
        }

        sup {
            font-size: 9pt;
            vertical-align: super;
        }

        a {
            color: #0066cc;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .page-break {
            page-break-before: always;
        }

        @media screen {
            body {
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                margin: 20px auto;
            }
        }
    </style>
</head>
<body>
    <div class="title-section">
        <div class="manuscript-title">""" + metadata.get('title', '') + """</div>
        <div class="author">""" + metadata.get('author', '') + """</div>
        <div class="affiliation">""" + metadata.get('affiliation', '') + """</div>
        <div class="email">""" + metadata.get('email', '') + """</div>
        <div class="date">""" + datetime.now().strftime('%B %d, %Y') + """</div>
    </div>

    <div class="abstract-box">
        <div class="abstract-heading">ABSTRACT</div>
        <div class="abstract-content">
"""

    # Abstract paragraphs
    if 'abstract' in metadata:
        for para in metadata['abstract']:
            if para.strip():
                html += f"            <p>{markdown_to_html(para)}</p>\n"

        if 'keywords' in metadata:
            html += f"""            <p class="keywords"><strong>Keywords:</strong> {markdown_to_html(metadata['keywords'])}</p>\n"""

    html += """        </div>
    </div>

    <div class="page-break"></div>

"""

    # Main sections
    for section in sections:
        if section['title'].lower() in ['acknowledgments', 'references', 'supplementary materials']:
            html += '    <div class="page-break"></div>\n'

        html += f'    <h1>{section["title"]}</h1>\n'

        content_html = process_content_lines(section['content'])
        for line in content_html:
            html += f'    {line}\n'

    html += """
</body>
</html>"""

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[SUCCESS] Professional HTML generated: {output_html}")
    print("\n[INSTRUCTIONS] To convert to PDF:")
    print("   1. Open the HTML file in Chrome or Edge browser")
    print("   2. Press Ctrl+P (or Cmd+P on Mac)")
    print("   3. Select 'Save as PDF' as destination")
    print("   4. Set margins to 'Default'")
    print("   5. Enable 'Background graphics'")
    print("   6. Click 'Save'")
    print("\n   This will produce a professional, publication-ready PDF!")

if __name__ == "__main__":
    md_file = "biorxiv_manuscript.md"
    output_html = "biorxiv_manuscript_professional.html"

    create_professional_html(md_file, output_html)
