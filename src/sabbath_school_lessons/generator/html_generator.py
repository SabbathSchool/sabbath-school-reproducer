"""
HTML Generator for Sabbath School Lessons

This module generates HTML content for the PDF conversion.
"""

import markdown
import re
from .css_styles import CSS_TEMPLATE


class HtmlGenerator:
    """Generates HTML content for PDF generation."""
    
    @staticmethod
    def read_svg_file(filepath):
        """
        Read SVG file content from the specified path
        
        Args:
            filepath (str): Path to SVG file
            
        Returns:
            str or None: SVG content or None if error
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading SVG file {filepath}: {e}")
            return None
    
    @staticmethod
    def create_cover_page(front_cover_svg_path=None):
        """
        Creates the cover page HTML using the SVG from file if provided
        
        Args:
            front_cover_svg_path (str, optional): Path to front cover SVG
            
        Returns:
            str: HTML for cover page
        """
        svg_content = ""
        
        # If a path is provided, try to read the SVG from file
        if front_cover_svg_path:
            svg_content = HtmlGenerator.read_svg_file(front_cover_svg_path)
            if not svg_content:
                print(f"Warning: Could not read SVG from {front_cover_svg_path}")
                return ""
        
        if not svg_content:
            # Use default fallback SVG (simplified version)
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" width="800" height="1000">
                <rect width="800" height="1000" fill="#ffffff"/>
                <rect x="30" y="30" width="740" height="940" stroke="#7d2b2b" stroke-width="3" fill="none"/>
                <text x="400" y="170" font-family="Georgia, serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#7d2b2b">SABBATH SCHOOL</text>
                <text x="400" y="230" font-family="Georgia, serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#7d2b2b">LESSONS</text>
                <text x="400" y="500" font-family="Georgia, serif" font-size="28" text-anchor="middle" fill="#5a4130">Quarter X, YYYY</text>
            </svg>
            """
        
        return f"""
        <div class="cover-page">
            {svg_content}
        </div>
        """
    
    @staticmethod
    def create_back_cover(back_cover_svg_path=None):
        """
        Creates the back cover page HTML using the SVG from file if provided
        
        Args:
            back_cover_svg_path (str, optional): Path to back cover SVG
            
        Returns:
            str: HTML for back cover
        """
        if not back_cover_svg_path:
            return ""
            
        svg_content = HtmlGenerator.read_svg_file(back_cover_svg_path)
        if not svg_content:
            return ""
        
        return f"""
        <div class="back-cover-page">
            {svg_content}
        </div>
        """
    
    @staticmethod
    def convert_markdown_to_html(markdown_content):
        """
        Convert markdown to HTML with table support
        
        Args:
            markdown_content (str): Markdown content
            
        Returns:
            str: HTML content
        """
        return markdown.markdown(
            markdown_content,
            extensions=['tables']  # Enable table extension
        )
    
    @staticmethod
    def create_frontmatter_html(frontmatter_content):
        """
        Creates HTML for the front matter section with table support
        
        Args:
            frontmatter_content (str): Front matter markdown content
            
        Returns:
            str: HTML for front matter
        """
        if not frontmatter_content:
            return ""
        
        # Convert markdown to HTML with table support
        html_content = HtmlGenerator.convert_markdown_to_html(frontmatter_content)
        
        # Wrap in appropriate container
        return f"""
        <div class="front-matter">
            {html_content}
            <div style="page-break-after: always;"></div>
        </div>
        """
    
    @staticmethod
    def create_backmatter_html(backmatter_content):
        """
        Creates HTML for the back matter section with table support
        
        Args:
            backmatter_content (str): Back matter markdown content
            
        Returns:
            str: HTML for back matter
        """
        if not backmatter_content:
            return ""
        
        # Convert markdown to HTML with table support
        html_content = HtmlGenerator.convert_markdown_to_html(backmatter_content)
        
        # Wrap in appropriate container
        return f"""
        <div class="back-matter">
            {html_content}
        </div>
        """
    
    @staticmethod
    def create_table_of_contents(lessons):
        """
        Creates the table of contents HTML with links to lessons
        
        Args:
            lessons (list): List of lesson dictionaries
            
        Returns:
            str: HTML for table of contents
        """
        toc_rows = ""
        
        for lesson in lessons:
            # Only include items that have proper lesson structure
            if 'number' in lesson and 'title' in lesson and 'date' in lesson:
                toc_row = f"""
                <tr>
                    <td style="width: 40px; padding: 5px;">{lesson['number']}</td>
                    <td style=""><a href="#lesson-{lesson['number']}">{lesson['title']}</a></td>
                    <td style="">{lesson['date']}</td>
                    <td style="width: 40px; padding: 5px; text-align: right;">{lesson['number']}</td>
                </tr>
                """
                toc_rows += toc_row
        
        return f"""
        <div class="toc-title">TABLE OF CONTENTS</div>
        <table class="toc-table">
            <tr class="header">
                <td style="width: 40px; padding: 5px;">Lesson</td>
                <td style="padding: 5px;">Title</td>
                <td style="width: 100px; padding: 5px;">Date</td>
                <td style="width: 40px; padding: 5px; text-align: right;">Page</td>
            </tr>
            {toc_rows}
        </table>
        <div class="sectionbreaknone"></div>
        """
    
    @staticmethod
    def create_lesson_html(lesson):
        """
        Creates HTML for a single lesson with improved formatting for title and date
        
        Args:
            lesson (dict): Lesson dictionary
            
        Returns:
            str: HTML for lesson
        """
        # Process preliminary note if present
        preliminary_html = ""
        if lesson.get('preliminary_note'):
            cleaned_note = lesson['preliminary_note']
            
            # Remove any lines that match the lesson date
            if lesson.get('date'):
                # Create more flexible patterns to match the date in various formats
                date_only = lesson['date'].strip()
                date_patterns = [
                    re.escape(date_only),  # Exact match
                    re.escape(date_only) + r'\s*$',  # Date at end of line
                    r'^\s*' + re.escape(date_only),  # Date at beginning of line
                    r'^\s*' + re.escape(date_only) + r'\s*$'  # Date alone on a line
                ]
                
                # Apply each pattern to remove the date
                for pattern in date_patterns:
                    cleaned_note = re.sub(pattern, '', cleaned_note, flags=re.MULTILINE)
                
                # Remove any empty lines that might be left
                cleaned_note = re.sub(r'\n\s*\n+', '\n\n', cleaned_note)
                cleaned_note = cleaned_note.strip()
            
            # If there's still content after removing dates, format it
            if cleaned_note.strip():
                # Replace newlines with paragraph tags
                paragraphs = cleaned_note.split('\n\n')
                formatted_paragraphs = ''.join(f'<p>{p}</p>' for p in paragraphs if p.strip())
                
                preliminary_html = f"""
                <div class="preliminary-note">
                    {formatted_paragraphs}
                </div>
                """
        
        # Process questions with improved formatting
        questions_html = ""
        for i, question in enumerate(lesson.get('questions', []), 1):
            # Handle scripture reference with proper punctuation
            scripture_html = ""
            if question.get('scripture'):
                # Ensure the scripture reference ends with a period if it doesn't already
                scripture_with_period = question['scripture']
                if not scripture_with_period.endswith('.'):
                    scripture_with_period += '.'
                scripture_html = f'<span class="scripture-ref">{scripture_with_period}</span>'
            
            # Handle answer
            answer_html = ""
            if question.get('answer'):
                answer_html = f'<div class="answer"><em>Ans. — {question["answer"]}</em></div>'
            
            # Add padding for two-digit numbers
            num_class = "two-digit" if i >= 10 else "one-digit"
            
            # Make sure question text ends with proper punctuation
            question_text = question.get('text', '')
            if question_text and not re.search(r'[.?!]$', question_text):
                question_text += '.'
                
            question_html = f"""
            <div class="question">
                <span class="question-number {num_class}">{i}.</span>
                <div class="question-text">
                    {question_text} {scripture_html}
                    {answer_html}
                </div>
                <div class="clearfix"></div>
            </div>
            """
            questions_html += question_html
        
        # Process notes if present
        notes_html = ""
        if lesson.get('notes'):
            # Split notes by paragraphs and format them
            paragraphs = lesson['notes'].split('\n\n')
            formatted_paragraphs = ''.join(f'<p>{p}</p>' for p in paragraphs if p.strip())
            
            notes_html = f"""
            <div class="notes-section">
                <div class="notes-header">NOTES</div>
                <div class="notes-content">
                    {formatted_paragraphs}
                </div>
            </div>
            """
        
        # Combine all sections with updated header structure
        return f"""
        <div class="lesson">
            <div class="lesson-header">
                <div class="corner top-left"></div>
                <div class="corner top-right"></div>
                <div class="corner bottom-left"></div>
                <div class="corner bottom-right"></div>
                <div class="lesson-circle">{lesson.get('number', '')}</div>
                <div class="lesson-title-container">
                    <div class="lesson-title">{lesson.get('title', '')}</div>
                    <div class="lesson-date">{lesson.get('date', '')}</div>
                </div>
            </div>
            {preliminary_html}
            <div class="questions-section">
                <div class="questions-header">QUESTIONS</div>
                {questions_html}
            </div>
            {notes_html}
        </div>
        """
    
    @staticmethod
    def generate_html(content_data, front_cover_svg_path=None, back_cover_svg_path=None, config=None):
        """
        Generate complete HTML document from content data
        
        Args:
            content_data (dict): Dictionary with content data
            front_cover_svg_path (str, optional): Path to front cover SVG
            back_cover_svg_path (str, optional): Path to back cover SVG
            config (dict, optional): Configuration dictionary
            
        Returns:
            str: Complete HTML document
        """
        lessons = content_data['lessons']
        frontmatter = content_data['frontmatter']
        backmatter = content_data['backmatter']
        
        # Create HTML for the document
        html_parts = []
        
        # Start with HTML header
        html_parts.extend([
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '    <meta charset="utf-8">',
            '    <title>Sabbath School Lessons</title>',
            '    <style>',
            CSS_TEMPLATE,
            '    </style>',
            '</head>',
            '<body>'
        ])
        
        # Add cover page
        html_parts.append(HtmlGenerator.create_cover_page(front_cover_svg_path))
        
        # Add a blank page after cover (common in book printing)
        html_parts.append('<div class="blank-page"></div>')
        
        # Start frontmatter section with proper class for counter reset
        html_parts.append('<div class="frontmatter-container">')
        
        # Add front matter content
        if frontmatter:
            html_parts.append(HtmlGenerator.create_frontmatter_html(frontmatter))
        
        # Add table of contents
        html_parts.append(HtmlGenerator.create_table_of_contents(lessons))
        
        # End frontmatter section
        html_parts.append('</div>')
        
        # Start main content section with proper class for counter reset
        html_parts.append('<div class="mainmatter-container">')
        
        # Add each lesson
        for lesson in lessons:
            html_parts.append(f'<div id="lesson-{lesson["number"]}">')
            html_parts.append(HtmlGenerator.create_lesson_html(lesson))
            html_parts.append('</div>')
            html_parts.append('<div style="page-break-after: always;"></div>')
        
        # Add back matter if it exists - inside the mainmatter page section
        if backmatter:
            html_parts.append(HtmlGenerator.create_backmatter_html(backmatter))
            html_parts.append('<div style="page-break-after: always;"></div>')
        
        # End mainmatter section
        html_parts.append('</div>')
        
        # Add back cover
        if back_cover_svg_path:
            html_parts.append('<div style="page-break-before: always;"></div>')
            html_parts.append(HtmlGenerator.create_back_cover(back_cover_svg_path))
        
        # Close HTML tags
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return '\n'.join(html_parts)