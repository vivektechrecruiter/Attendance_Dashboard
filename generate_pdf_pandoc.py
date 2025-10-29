import os
import pypandoc

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(current_dir, 'PROJECT_SUMMARY.md')
    pdf_file = os.path.join(current_dir, 'Project_Summary.pdf')
    
    print(f"Converting markdown file from: {md_file}")
    print(f"Output PDF will be at: {pdf_file}")
    
    # Convert markdown to PDF
    output = pypandoc.convert_file(
        md_file,
        'pdf',
        outputfile=pdf_file,
        extra_args=[
            '--pdf-engine=xelatex',
            '-V', 'geometry:margin=1in',
            '-V', 'mainfont:Arial',
            '-V', 'monofont:Consolas',
            '--toc',
            '--highlight-style=tango'
        ]
    )
    
    if os.path.exists(pdf_file):
        print(f"Success! PDF created at: {pdf_file}")
        print(f"File size: {os.path.getsize(pdf_file)} bytes")
    else:
        print("Error: PDF file was not created")
        
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("\nTroubleshooting steps:")
    print("1. Install Pandoc from: https://pandoc.org/installing.html")
    print("2. Install MiKTeX from: https://miktex.org/download")
    print("3. Ensure both are added to system PATH")
    raise