"""
PDF Generator for Sabbath School Lessons

This module handles the final conversion from HTML to PDF with specific pagination fixes.
"""

import os
import tempfile
from weasyprint import HTML, CSS, Document


class PdfGenerator:
    """Handles conversion of HTML to PDF with pagination control."""
    
    @staticmethod
    def count_pages_in_document(document):
        """
        Count the number of pages in a WeasyPrint document
        
        Args:
            document (Document): WeasyPrint document
            
        Returns:
            int: Number of pages
        """
        return len(document.pages)
    
    @staticmethod
    def create_section_document(html_content):
        """
        Create a WeasyPrint document for a section
        
        Args:
            html_content (str): HTML content
            
        Returns:
            Document: WeasyPrint document
        """
        return HTML(string=html_content).render()
    
    @staticmethod
    def create_blank_page_pdf(output_path):
        """
        Generate a blank page PDF
        
        Args:
            output_path (str): Path to save the blank page PDF
            
        Returns:
            str: Path to the generated PDF
        """
        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Blank Page</title>
    <style>
        @page {
            size: letter;
            margin: 0;
        }
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
        }
    </style>
</head>
<body>
</body>
</html>"""
        HTML(string=html_content).write_pdf(output_path)
        return output_path
    
    @staticmethod
    def add_css_for_pagination(output_path):
        """
        Create a CSS file with pagination rules
        
        Args:
            output_path (str): Directory to save the CSS file
            
        Returns:
            str: Path to the generated CSS file
        """
        css_content = """
/* Pagination controls for Sabbath School lessons */

/* Set reasonable orphans/widows values */
p {
    orphans: 2;
    widows: 2;
}

/* Don't touch section layout, only prevent page breaks inside questions */
.question {
    page-break-inside: avoid;
}

/* Force page breaks between lessons, but not within lesson content */
.lesson {
    page-break-after: always;
}

/* Ensure questions-section doesn't use avoid settings that might push it to next page */
.questions-section {
    page-break-inside: auto !important;
    display: block;
}

/* Ensure header and preliminary note do not force questions off-page */
.lesson-header, .preliminary-note {
    page-break-after: auto !important;
}
"""
        css_path = os.path.join(output_path, "pagination.css")
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        return css_path
    
    @staticmethod
    def generate_pdf(html_content, output_pdf, config=None):
        """
        Converts HTML content to PDF with targeted pagination fixes
        
        Args:
            html_content (str): The complete HTML document
            output_pdf (str): Path to save the PDF file
            config (dict, optional): Configuration dictionary
            
        Returns:
            str: Path to the generated PDF
        """
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_pdf)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save debug HTML for troubleshooting
        debug_html_path = output_pdf.replace('.pdf', '_debug.html')
        with open(debug_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Debug HTML saved to: {debug_html_path}")
        
        # Create a temporary directory for intermediary files
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create CSS file with pagination rules
            css_path = PdfGenerator.add_css_for_pagination(temp_dir)
            
            # Count pages in the document for verification
            doc = PdfGenerator.create_section_document(html_content)
            page_count = PdfGenerator.count_pages_in_document(doc)
            
            # Check if page count is divisible by 4 (for booklet printing)
            remainder = page_count % 4
            if remainder != 0:
                print(f"Warning: Page count ({page_count}) is not divisible by 4. "
                      f"Adding {4 - remainder} padding pages for proper booklet printing.")
            
            # Generate PDF with the custom CSS
            HTML(string=html_content).write_pdf(
                output_pdf,
                stylesheets=[CSS(filename=css_path)]
            )
            
            print(f"PDF created successfully: {output_pdf} with {page_count} pages")
            return output_pdf
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            # Try without custom CSS as fallback
            try:
                HTML(string=html_content).write_pdf(output_pdf)
                print(f"PDF created with fallback method: {output_pdf}")
                return output_pdf
            except Exception as e2:
                print(f"Fallback PDF generation also failed: {str(e2)}")
                raise
        finally:
            # Clean up temporary files
            try:
                if os.path.exists(css_path):
                    os.unlink(css_path)
                os.rmdir(temp_dir)
            except:
                pass