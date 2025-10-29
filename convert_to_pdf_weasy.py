from weasyprint import HTML
import markdown
import os

def convert_md_to_pdf(input_file, output_file):
    # Read markdown content
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['extra', 'smarty']
    )
    
    # Add some CSS for better formatting
    html_with_style = f"""
    <html>
    <head>
        <style>
            @page {{ margin: 2.5cm; }}
            body {{ 
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }}
            h1, h2, h3 {{ color: #2c3e50; }}
            code {{ 
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 4px;
            }}
            pre {{ 
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    HTML(string=html_with_style).write_pdf(output_file)
    print(f"PDF created successfully: {output_file}")

if __name__ == "__main__":
    input_file = "PROJECT_SUMMARY.md"
    output_file = "Project_Summary.pdf"
    convert_md_to_pdf(input_file, output_file)