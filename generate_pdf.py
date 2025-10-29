import os
import markdown
from pathlib import Path
from weasyprint import HTML

# Get absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
md_file = os.path.join(current_dir, 'PROJECT_SUMMARY.md')
pdf_file = os.path.join(current_dir, 'Project_Summary.pdf')

try:
    print(f"Looking for markdown file at: {md_file}")
    
    # Read the markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    print("Successfully loaded the markdown content")

    # Convert markdown to HTML with custom CSS
    html_content = f"""
    <html>
    <head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
        }}
        h1, h2, h3 {{ 
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        code {{ 
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 4px;
            font-family: 'Consolas', monospace;
        }}
        pre {{ 
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        ul, ol {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 5px;
        }}
    </style>
    </head>
    <body>
    {markdown.markdown(markdown_content, extensions=['extra', 'codehilite'])}
    </body>
    </html>
    """

    print(f"Creating PDF at: {pdf_file}")
    # Convert HTML to PDF
    HTML(string=html_content).write_pdf(pdf_file)
    print(f"PDF created successfully at: {pdf_file}")
    
    # Verify the file exists
    if os.path.exists(pdf_file):
        print(f"Verified: PDF file exists at {pdf_file}")
        print(f"File size: {os.path.getsize(pdf_file)} bytes")
    else:
        print("Warning: PDF file was not found after creation!")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Error details:", e.__class__.__name__)
    raise