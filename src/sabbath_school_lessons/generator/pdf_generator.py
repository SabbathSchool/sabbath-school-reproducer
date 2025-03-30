"""
PDF Generator for Sabbath School Lessons

This module handles the final conversion from HTML to PDF with specific pagination fixes.
"""

from weasyprint import HTML, CSS
import os
import tempfile


class PdfGenerator:
    """Handles conversion of HTML to PDF."""
    
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
        # Save debug HTML for troubleshooting
        debug_html_path = output_pdf.replace('.pdf', '_debug.html')
        with open(debug_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Debug HTML saved to: {debug_html_path}")
        
        # Create a temporary CSS file with minimal pagination rules
        with tempfile.NamedTemporaryFile(suffix='.css', delete=False, mode='w', encoding='utf-8') as temp_css:
            temp_css.write("""
            /* Minimal pagination fixes that won't disrupt layout */
            @page {
                size: letter;
                margin: 0.75in;
            }
            
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
            """)
            css_path = temp_css.name
        
        try:
            # Generate PDF with the custom CSS
            HTML(string=html_content).write_pdf(
                output_pdf,
                stylesheets=[CSS(filename=css_path)]
            )
            print(f"PDF created successfully: {output_pdf}")
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            # Try without custom CSS as fallback
            try:
                HTML(string=html_content).write_pdf(output_pdf)
                print(f"PDF created with fallback method: {output_pdf}")
            except Exception as e2:
                print(f"Fallback PDF generation also failed: {str(e2)}")
                raise
        finally:
            # Clean up the temporary CSS file
            try:
                os.unlink(css_path)
            except:
                pass
        
        return output_pdf