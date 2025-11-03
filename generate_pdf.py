#!/usr/bin/env python3
"""
Generate professional PDF from Markdown manuscript for bioRxiv submission
"""

import markdown2
from weasyprint import HTML, CSS
from pathlib import Path

# Define custom CSS for professional academic paper formatting
CSS_STYLE = """
@page {
    size: A4;
    margin: 2.5cm 2cm 2cm 2cm;
    @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", serif;
        font-size: 10pt;
    }
}

body {
    font-family: "Times New Roman", serif;
    font-size: 12pt;
    line-height: 1.5;
    text-align: justify;
    color: #000;
    max-width: 100%;
}

h1 {
    font-size: 18pt;
    font-weight: bold;
    text-align: center;
    margin-top: 0;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}

h2 {
    font-size: 14pt;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}

h3 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 1em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}

h4 {
    font-size: 12pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 0.8em;
    margin-bottom: 0.4em;
    page-break-after: avoid;
}

p {
    margin: 0 0 0.5em 0;
    text-indent: 0;
}

/* Authors and affiliations */
h2:first-of-type + p {
    text-align: center;
    font-style: italic;
    margin-bottom: 2em;
}

/* Abstract section */
strong {
    font-weight: bold;
}

em {
    font-style: italic;
}

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

th {
    background-color: #f0f0f0;
    font-weight: bold;
    text-align: left;
    padding: 8px;
    border: 1px solid #ddd;
}

td {
    padding: 6px 8px;
    border: 1px solid #ddd;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

/* Lists */
ul, ol {
    margin: 0.5em 0;
    padding-left: 2em;
}

li {
    margin: 0.3em 0;
}

/* Code and pre-formatted text */
code {
    font-family: "Courier New", monospace;
    font-size: 10pt;
    background-color: #f5f5f5;
    padding: 2px 4px;
}

pre {
    font-family: "Courier New", monospace;
    font-size: 10pt;
    background-color: #f5f5f5;
    padding: 10px;
    border: 1px solid #ddd;
    overflow-x: auto;
    page-break-inside: avoid;
}

/* Horizontal rules */
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 1.5em 0;
}

/* Superscripts and subscripts */
sup {
    vertical-align: super;
    font-size: 0.75em;
}

sub {
    vertical-align: sub;
    font-size: 0.75em;
}

/* Links */
a {
    color: #0066cc;
    text-decoration: underline;
}

/* Block quotes */
blockquote {
    margin: 1em 2em;
    padding: 0.5em 1em;
    border-left: 3px solid #ddd;
    font-style: italic;
    background-color: #f9f9f9;
}

/* Section spacing */
.page-break {
    page-break-before: always;
}

/* Figure legends and tables */
h2:contains("Figure"), h2:contains("Table") {
    margin-top: 2em;
    page-break-before: always;
}

/* References */
h2:contains("References") + ol {
    font-size: 10pt;
}

/* Keywords */
h2:contains("Keywords") + p {
    font-style: italic;
}
"""

def convert_markdown_to_pdf(input_md: str, output_pdf: str):
    """
    Convert Markdown manuscript to professional PDF

    Args:
        input_md: Path to input Markdown file
        output_pdf: Path to output PDF file
    """
    print(f"📄 Reading manuscript from: {input_md}")

    # Read Markdown content
    with open(input_md, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    print("🔄 Converting Markdown to HTML...")

    # Convert Markdown to HTML with extras
    html_content = markdown2.markdown(
        markdown_content,
        extras=[
            'tables',           # Support tables
            'fenced-code-blocks',  # Support ```code``` blocks
            'footnotes',        # Support footnotes
            'header-ids',       # Generate IDs for headers
            'strike',           # Support ~~strikethrough~~
            'task_list',        # Support task lists
            'cuddled-lists',    # Better list handling
        ]
    )

    # Wrap HTML content with proper structure
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PD-L1 Regulation by LLPS-Associated Proteins</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    print("📝 Applying professional formatting...")

    # Create CSS object
    css = CSS(string=CSS_STYLE)

    print("🖨️  Generating PDF with WeasyPrint...")

    # Generate PDF
    HTML(string=full_html).write_pdf(
        output_pdf,
        stylesheets=[css],
        optimize_size=('fonts', 'images')
    )

    # Get file size
    file_size = Path(output_pdf).stat().st_size / (1024 * 1024)  # MB

    print(f"✅ PDF generated successfully!")
    print(f"📊 Output file: {output_pdf}")
    print(f"📦 File size: {file_size:.2f} MB")
    print()
    print("🎉 Your manuscript is ready for bioRxiv submission!")
    print()
    print("📋 Next steps:")
    print("  1. Review the PDF to ensure proper formatting")
    print("  2. Add author information (names, affiliations, email)")
    print("  3. Replace placeholder text with actual data")
    print("  4. Add any missing figures/tables")
    print("  5. Upload to bioRxiv at https://www.biorxiv.org/submit-a-manuscript")

if __name__ == "__main__":
    # Set paths
    input_markdown = "/home/thc1006/dev/p62-pdl1-llps-starter/MANUSCRIPT_bioRxiv.md"
    output_pdf_file = "/home/thc1006/dev/p62-pdl1-llps-starter/MANUSCRIPT_bioRxiv_SUBMISSION.pdf"

    # Generate PDF
    try:
        convert_markdown_to_pdf(input_markdown, output_pdf_file)
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        print("\nTroubleshooting tips:")
        print("  - Ensure all dependencies are installed")
        print("  - Check that the Markdown file exists")
        print("  - Verify write permissions for output directory")
        import traceback
        traceback.print_exc()
