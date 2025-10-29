import markdown
import pdfkit
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
            body {{ 
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
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
    
    # Create a temporary HTML file
    temp_html = 'temp_summary.html'
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_with_style)
    
    # Convert HTML to PDF
    pdfkit.from_file(temp_html, output_file)
    
    # Clean up temporary file
    os.remove(temp_html)
    print(f"PDF created successfully: {output_file}")

if __name__ == "__main__":
    input_file = "PROJECT_SUMMARY.md"
    output_file = "Project_Summary.pdf"
    convert_md_to_pdf(input_file, output_file)