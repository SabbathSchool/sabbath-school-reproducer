import markdown
import re
import os
import mimetypes
import base64

from sabbath_school_reproducer.generator.css_styles import CSS_TEMPLATE, CssUpdater
from sabbath_school_reproducer.generator.css_editor import  CSSEditor
from sabbath_school_reproducer.utils.language_utils import  LanguageConfig


class HtmlGenerator:
    """Generates HTML content for PDF generation with incremental approach."""
    
    @staticmethod
    def get_quarter_display(quarter, language_code='en'):
        """
        Get a formatted display for the quarter
        
        Args:
            quarter (str): Quarter code (e.g., q1, q2, q3, q4)
            language_code (str): Language code for translations
            
        Returns:
            str: Formatted quarter display
        """
        return LanguageConfig.get_translation(
            language_code, 
            f'quarter_names.{quarter.lower()}',
            "Quarter"
        )
    @staticmethod
    def read_file(filepath):
        """
        Read file content from the specified path
        
        Args:
            filepath (str): Path to file
            
        Returns:
            tuple: (content, mimetype) or (None, None) if error
        """
        # Check if the filepath is valid
        if not filepath:
            return None, None
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"Warning: File does not exist: {filepath}")
            return None, None
            
        try:
            # Get mimetype based on file extension
            mimetype, _ = mimetypes.guess_type(filepath)
            
            # Determine read mode based on file type
            if mimetype and mimetype.startswith('text/'):
                # Text files should be read as text
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read(), mimetype
            else:
                # Binary files should be read as binary
                with open(filepath, 'rb') as f:
                    return f.read(), mimetype
        except Exception as e:
            print(f"Warning: Could not read file from {filepath}: {e}")
            return None, None
    
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
            print(f"Warning: Could not read SVG from {filepath}: {e}")
            return None
    
    @staticmethod
    def is_svg_file(filepath):
        """
        Check if the file is an SVG by extension
        
        Args:
            filepath (str): Path to file
            
        Returns:
            bool: True if file is SVG, False otherwise
        """
        if not filepath:
            return False

        # Check if the file ends with .svg (case-insensitive)
        if filepath.lower().endswith('.svg'):
            return True

        # Otherwise, check the MIME type (just in case)
        _, mimetype = mimetypes.guess_type(filepath)
        print(filepath, mimetype)
        return mimetype == 'image/svg+xml'
    
    @staticmethod
    def get_image_dimensions(filepath):
        """
        Get image dimensions from file path
        Can be replaced with more sophisticated method using PIL/Pillow
        
        Args:
            filepath (str): Path to image file
            
        Returns:
            tuple: (width, height) or (800, 1000) as default
        """
        # Check if file exists
        if not filepath or not os.path.exists(filepath):
            print(f"Warning: Cannot get dimensions, file does not exist: {filepath}")
            return 800, 1000
            
        # This is a placeholder - ideally you would use PIL/Pillow to get actual dimensions
        # For now, return default dimensions
        return 800, 1000
    
    @staticmethod
    @staticmethod
    def get_base64_image(filepath):
        """
        Read an image file and convert it to a base64 data URI
        
        Args:
            filepath (str): Path to the image file
            
        Returns:
            str: Base64 data URI or None if error
        """
        # Handle invalid paths
        # abs_path = HtmlGenerator.get_absolute_path(filepath)
        abs_path = filepath
        if not abs_path or not os.path.exists(filepath):
            return None
        
        # Get the MIME type
        mime_type, _ = mimetypes.guess_type(abs_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        try:
            # Read and encode the file
            with open(abs_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
                return f"data:{mime_type};base64,{encoded}"
        except Exception as e:
            print(f"Error encoding image {abs_path}: {e}")
            return None
    
    @staticmethod
    def create_cover_page(front_cover_path=None, config=None):
        """
        Creates the cover page HTML using the image from file if provided
        
        Args:
            front_cover_path (str, optional): Path to front cover image
            config (dict, optional): Configuration dictionary
            
        Returns:
            str: HTML for cover page
        """
        # Set default values
        year = 2025
        quarter = "q1"
        lesson_title = ""
        
        # Get language code from config
        language_code = config.get('language', 'en') if config else 'en'
        
        # Use values from config if available
        if config:
            # Use the target year and quarter for display (not the source/reproduction year)
            year = config.get("year", 2025)
            quarter = config.get("quarter", "q1")

            reproduce = config.get("reproduce", {})
            year_orig = reproduce.get("year", 2025)  # Default to 2025 if 'year' is not found
            quarter_orig = reproduce.get("quarter", "q1") 
            
            # Get title from config or generate a default
            lesson_title = config.get("lesson_title", CSSEditor.get_lesson_title(year_orig, quarter_orig))
            
            # If we're in reproduction mode, add a note about the original source
            if config.get("reproduce", {}).get("year"):
                source_year = config["reproduce"]["year"]
                source_quarter = config["reproduce"]["quarter"]
                
                # Update title to indicate it's a reproduction
                if not config.get("title"):  # Only modify if no custom title is set
                    # Get translated word for "from" based on language
                    from_text = LanguageConfig.get_translation(language_code, 'from_text', 'from', config)
                    lesson_title = f"Sabbath School Lessons ({from_text} {source_year} {source_quarter.upper()})"
        
        # Format quarter display using translated name
        quarter_display = LanguageConfig.get_translation(
            language_code, 
            f'quarter_names.{quarter.lower()}', 
            HtmlGenerator.get_quarter_display(quarter, language_code),
            config
        )
        
        # Get quarter months for the specific language
        quarter_months = LanguageConfig.get_translation(
            language_code, 
            f'quarter_months.{quarter.lower()}', 
            f"Quarter {quarter[1]}", 
            config
        )
        
        # Check if a cover image is provided
        if front_cover_path:
            # Check if the file exists
            if not os.path.exists(front_cover_path):
                print(f"Warning: Front cover file does not exist: {front_cover_path}")
                # Will fall back to default cover
            else:
                # Check if the cover is an SVG
                if HtmlGenerator.is_svg_file(front_cover_path):
                    # Process SVG cover
                    svg_content = HtmlGenerator.read_svg_file(front_cover_path)
                    if svg_content:
                        return f"""
                        <div class="cover-page">
                            {svg_content}
                        </div>
                        """
                else:
                    # Process non-SVG cover (JPG, PNG, etc.)
                    # Get image dimensions (could be replaced with actual dimensions from PIL)
                    width, height = HtmlGenerator.get_image_dimensions(front_cover_path)
                    
                    use_base64  = True
                    if use_base64:
                        img_src = HtmlGenerator.get_base64_image(front_cover_path)
                    else:
                        img_src = HtmlGenerator.get_file_uri(front_cover_path)
                    
                    if img_src:
                        return f"""
                            <div class="full-page-image-container">
                                <img src="{img_src}" alt="Back Cover" class="full-page-image" 
                                    style="width: 100%; height: 100%; object-fit: fill; display: block; margin: 0 0;">
                            </div>
                        """
                    return ""
        
        # No valid cover provided, create a default SVG cover
        # Get translated text for the cover page
        sabbath_school_text = LanguageConfig.get_translation(language_code, 'sabbath_school', 'SABBATH SCHOOL', config)
        lessons_text = LanguageConfig.get_translation(language_code, 'lessons', 'LESSONS', config)
        
        # Use default fallback SVG with dynamic content
        svg_content = f"""
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" width="800" height="1000">
            <rect width="800" height="1000" fill="#ffffff"/>
            <rect x="30" y="30" width="740" height="940" stroke="#7d2b2b" stroke-width="3" fill="none"/>
            <text x="400" y="170" font-family="Georgia, serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#7d2b2b">{sabbath_school_text}</text>
            <text x="400" y="230" font-family="Georgia, serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#7d2b2b">{lessons_text}</text>
            <text x="400" y="730" font-family="Georgia, serif" font-size="36" font-weight="bold" text-anchor="middle" fill="#5a4130">{lesson_title}</text>
            <text x="400" y="790" font-family="Georgia, serif" font-size="24" text-anchor="middle" fill="#5a4130">{quarter_display}, {year}</text>
            <text x="400" y="830" font-family="Georgia, serif" font-size="18" text-anchor="middle" fill="#5a4130">{quarter_months} {year}</text>
        </svg>
        """
            
        # Add source attribution if this is a reproduction
        if config and config.get("reproduce", {}).get("year"):
            source_year = config["reproduce"]["year"]
            source_quarter = config["reproduce"]["quarter"].lower()
            
            # Get translated quarter name and adapted from text
            source_quarter_name = LanguageConfig.get_translation(
                language_code, 
                f'quarter_names.{source_quarter}', 
                HtmlGenerator.get_quarter_display(source_quarter, language_code),
                config
            )
            
            adapted_from = LanguageConfig.get_translation(language_code, 'adapted_from', 'Adapted from', config)
            
            # Add source attribution text to SVG
            svg_content = svg_content.replace('</svg>', f"""
            <text x="400" y="870" font-family="Georgia, serif" font-size="16" text-anchor="middle" font-style="italic" fill="#666666">
                {adapted_from} {source_quarter_name}, {source_year}
            </text>
            </svg>
            """)
    
        return f"""
        <div class="cover-page">
            {svg_content}
        </div>
        """

    @staticmethod
    def create_back_cover(back_cover_path=None):
        """
        Creates the back cover page HTML using the image from file if provided
        
        Args:
            back_cover_path (str, optional): Path to back cover image
            
        Returns:
            str: HTML for back cover
        """
        # Return empty string if no path provided
        if not back_cover_path:
            return ""
            
        # Check if the file exists
        if not os.path.exists(back_cover_path):
            print(f"Warning: Back cover file does not exist: {back_cover_path}")
            return ""
            
        # Check if the back cover is an SVG
        if HtmlGenerator.is_svg_file(back_cover_path):
            # Process SVG back cover
            svg_content = HtmlGenerator.read_svg_file(back_cover_path)
            if not svg_content:
                return ""
            
            return f"""
            <div class="back-cover-page">
                {svg_content}
            </div>
            """
        else:
            # Process non-SVG back cover (JPG, PNG, etc.)
            # Get image dimensions (could be replaced with actual dimensions from PIL)
            width, height = HtmlGenerator.get_image_dimensions(back_cover_path)
            
            # For non-SVG, use the file path directly in an img tag
            return f"""
            <div class="back-cover-page">
                <div class="full-page-image-container">
                    <img src="{back_cover_path}" alt="Back Cover" class="full-page-image" 
                         style="width: {width}px; height: {height}px; object-fit: contain; display: block; margin: 0 auto;">
                </div>
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
            extensions=['tables', 'extra']  # Enable table and extra extensions for better markdown support
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
    def create_lesson_html(lesson, language_code='en'):
        """
        Creates HTML for a single lesson with improved formatting for title and date
        
        Args:
            lesson (dict): Lesson dictionary
            language_code (str): Language code for translations
            
        Returns:
            str: HTML for lesson
        """
        # Determine title font size based on length
        title_font_size = "24px"  # Default
        title_top = '40px'
        if lesson.get('title'):
            if len(lesson.get('title', '')) <= 31:
                title_top = '45px'
            if len(lesson.get('title', '')) > 57:
                title_font_size = "18px"
        
        # Process preliminary note if present
        preliminary_html = ""
        if lesson.get('preliminary_note'):
            # Convert markdown to HTML with proper formatting
            preliminary_content = HtmlGenerator.convert_markdown_to_html(lesson['preliminary_note'])
            
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
                    preliminary_content = re.sub(pattern, '', preliminary_content, flags=re.MULTILINE)
            
            # If there's still content after removing dates, add it
            if preliminary_content.strip():
                preliminary_html = f"""
                <div class="preliminary-note">
                    {preliminary_content}
                </div>
                """
        
        # Process question sections with headers
        question_sections_html = ""
        
        # Group questions by section
        question_sections = {}
        
        # Get translations
        default_questions_header = LanguageConfig.get_translation(language_code, 'questions', 'QUESTIONS')
        
        # Create a default questions section if no headers are present
        if not lesson.get('question_headers'):
            question_sections[default_questions_header] = []
        
        # Group questions by their sections
        for question in lesson.get('questions', []):
            section = question.get('section', default_questions_header)
            if section not in question_sections:
                question_sections[section] = []
            question_sections[section].append(question)
        
        # Sort sections to ensure they're in the correct order if numbers are in section names
        section_names = sorted(question_sections.keys())
        
        # Get answer prefix translation
        answer_prefix = LanguageConfig.get_translation(language_code, 'answer_prefix', 'Ans.')
        
        # Process each section
        for section_name in section_names:
            section_questions = question_sections[section_name]
            section_questions_html = ""
            
            for i, question in enumerate(section_questions, 1):
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
                    answer_html = f'<div class="answer"><em>{answer_prefix} — {question["answer"]}</em></div>'
                
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
                section_questions_html += question_html
            
            # Create the section with the proper header
            question_sections_html += f"""
            <div class="questions-section">
                <div class="questions-header">{section_name}</div>
                {section_questions_html}
            </div>
            """
        
        # Process additional sections if present
        additional_sections_html = ""
        if lesson.get('additional_sections'):
            for section in lesson.get('additional_sections', []):
                section_title = section.get('title', 'ADDITIONAL')
                section_content = section.get('content', '')
                
                # Convert markdown to HTML with proper formatting
                section_content_html = HtmlGenerator.convert_markdown_to_html(section_content)
                
                additional_sections_html += f"""
                <div class="additional-section">
                    <div class="additional-header">{section_title}</div>
                    <div class="additional-content">
                        {section_content_html}
                    </div>
                </div>
                """
        
        # Process notes if present
        notes_html = ""
        if lesson.get('notes'):
            # Get translations for 'NOTES' and 'NOTE'
            notes_header = LanguageConfig.get_translation(language_code, 'notes', 'NOTES')
            note_header = LanguageConfig.get_translation(language_code, 'note', 'NOTE')
            
            # Convert markdown to HTML with proper formatting
            notes_content = HtmlGenerator.convert_markdown_to_html(HtmlGenerator.fix_markdown_lists(lesson['notes']))
            paragraphs = notes_content.split('</p>')
            non_empty_paragraphs = [p for p in paragraphs if p.strip()]
            
            # Use singular or plural form based on number of paragraphs
            header = note_header if len(non_empty_paragraphs) == 1 else notes_header

            notes_html = f"""
                <div class="notes-section">
                    <div class="notes-header">{header}</div>
                    <div class="notes-content">
                        {notes_content}
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
                    <div class="lesson-title" style="font-size: {title_font_size};top: {title_top}">{lesson.get('title', '')}</div>
                    <div class="lesson-date">{lesson.get('date', '')}</div>
                </div>
            </div>
            {preliminary_html}
            {question_sections_html}
            {additional_sections_html}
            {notes_html}
        </div>
        """

    @staticmethod
    def create_table_of_contents(lessons, language_code='en', config=None):
        """
        Creates the table of contents HTML with links to lessons
        
        Args:
            lessons (list): List of lesson dictionaries
            language_code (str): Language code for translations
            config (dict, optional): Configuration dictionary containing language_config_path
            
        Returns:
            str: HTML for table of contents
        """
        toc_rows = ""
        
        # Get translations
        table_title = LanguageConfig.get_translation(language_code, 'table_of_contents', 'TABLE OF CONTENTS', config)
        lesson_column = LanguageConfig.get_translation(language_code, 'lesson_column', 'Lesson', config)
        title_column = LanguageConfig.get_translation(language_code, 'title_column', 'Title', config)
        date_column = LanguageConfig.get_translation(language_code, 'date_column', 'Date', config)
        page_column = LanguageConfig.get_translation(language_code, 'page_column', 'Page', config)
        
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
        <div class="toc-title">{table_title}</div>
        <table class="toc-table">
            <tr class="header">
                <td style="width: 40px; padding: 5px;">{lesson_column}</td>
                <td style="padding: 5px;">{title_column}</td>
                <td style="width: 100px; padding: 5px;">{date_column}</td>
                <td style="width: 40px; padding: 5px; text-align: right;">{page_column}</td>
            </tr>
            {toc_rows}
        </table>
        <div class="sectionbreaknone"></div>
        """

    @staticmethod
    def fix_markdown_lists(markdown_content):
        """
        Fix markdown list rendering by indenting all non-numbered list item lines,
        but only if at least one numbered list item exists in the content.
        
        Args:
            markdown_content (str): Markdown content with or without numbered lists
                
        Returns:
            str: Fixed markdown content with proper indentation for list continuity
        """
        # Split the content into lines
        lines = markdown_content.split('\n')

        # If there's only one line, return the content as is
        if len(lines) == 1:
            return markdown_content
        
        # Check if there's at least one numbered list item
        has_numbered_list = any(re.match(r'^\s*(\d+)\.\s+', line) for line in lines)
        
        # Only indent non-numbered list lines if there's at least one numbered list item
        if has_numbered_list:
            lines = list(map(lambda line: "\t" + line if not re.match(r'^\s*(\d+)\.\s+', line) else line, lines))
        
        # Join the lines back together and return the modified content
        return '\n'.join(lines)


    @staticmethod
    def create_debug_html_with_css(content_parts, dynamic_css):
        """
        Creates HTML with current content parts and CSS
        
        Args:
            content_parts (list): List of HTML content parts
            dynamic_css (str): CSS content with modifications
            
        Returns:
            str: Complete HTML string
        """
        # HTML structure with placeholders
        html_structure = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Sabbath School Lessons</title>
    <!-- CSS_PLACEHOLDER -->
</head>
<body>
    <!-- CONTENT_PLACEHOLDER -->
</body>
</html>"""
        
        # Join all content parts
        all_content = ''.join(content_parts)
        
        # Insert the content and CSS into the HTML structure
        complete_html = html_structure.replace("<!-- CSS_PLACEHOLDER -->", f"<style>{dynamic_css}</style>")
        complete_html = complete_html.replace("<!-- CONTENT_PLACEHOLDER -->", all_content)
        
        return complete_html
    
    @staticmethod
    def add_section(content_parts, dynamic_css, state, section_name, section_html, 
                    start_on_odd=True, reset_counter=False):
        """
        Adds a section to the document, ensuring it starts on the correct page
        
        Args:
            content_parts (list): List of HTML content parts
            dynamic_css (str): CSS content with modifications
            state (dict): Current state tracking page numbers, etc.
            section_name (str): Name of the section for comments
            section_html (str): HTML content for the section
            start_on_odd (bool): Whether section should start on odd-numbered page
            reset_counter (bool): Whether to reset page counter for this section
            
        Returns:
            tuple: (updated content_parts, updated dynamic_css, updated state)
        """
        absolute_page_number = state.get('absolute_page_number', 1)
        
        # Check if we need to add a blank page to start on correct page type
        if start_on_odd and absolute_page_number % 2 == 0:  # Need odd page but on even
            # Add a blank page
            content_parts.append('<div class="blank-page" style="page-break-after: always; height: 100vh;"></div>')
            
            # Add comment for debugging
            content_parts.append(f'<!-- Added blank page to ensure {section_name} starts on odd page {absolute_page_number + 1} -->')
            
            absolute_page_number += 1
            state['absolute_page_number'] = absolute_page_number
        elif not start_on_odd and absolute_page_number % 2 == 1:  # Need even page but on odd
            # Add a blank page
            content_parts.append('<div class="blank-page" style="page-break-after: always; height: 100vh;"></div>')
            
            # Add comment for debugging
            content_parts.append(f'<!-- Added blank page to ensure {section_name} starts on even page {absolute_page_number + 1} -->')
            
            absolute_page_number += 1
            state['absolute_page_number'] = absolute_page_number
        
        # Add page-specific CSS rule if needed
        section_start_page = absolute_page_number
        if reset_counter:
            dynamic_css += f"""
/* {section_name} starts on page {section_start_page} */
@page :nth({section_start_page}) {{
    counter-reset: page 1;  /* Reset page counter for {section_name} */
}}
"""
        else:
            dynamic_css += f"""
/* {section_name} starts on page {section_start_page} */
@page :nth({section_start_page}) {{
    /* {section_name} specific styling can go here */
}}
"""
        
        # Add the section content
        content_parts.append(section_html)
        
        # Add comment for debugging
        content_parts.append(f'<!-- {section_name}: starts at page {absolute_page_number} -->')
        
        # Estimate how many pages this section will add
        # This is a simplistic estimate - for accurate counts, we'd need to render the HTML
        estimated_pages = section_html.count('page-break-after: always') + 1
        
        # Update the absolute page number
        absolute_page_number += estimated_pages
        state['absolute_page_number'] = absolute_page_number
        
        # Add comment about section page count
        content_parts.append(f'<!-- {section_name}: estimated {estimated_pages} pages -->')
        
        return content_parts, dynamic_css, state
    
    @staticmethod
    def generate_html(content_data, front_cover_svg_path=None, back_cover_svg_path=None, config=None):
        """
        Generate complete HTML document from content data with incremental approach
        
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
        
        # Get language code from config
        language_code = config.get('language', 'en') if config else 'en'
        
        # Initialize state tracking
        state = {
            'absolute_page_number': 1
        }
        
        # Initialize content parts and CSS
        content_parts = []
        dynamic_css = CSS_TEMPLATE
        
        # Update CSS with configuration if available
        if config:
            dynamic_css = CssUpdater.update_css_template(dynamic_css, config, content_data)
        # Replace first page selector with nth-child selector for more control
        dynamic_css = dynamic_css.replace("@page :first {", "@page :nth(1) {")
        
        # 1. Add cover page - pass the config to the cover page creation
        cover_html = HtmlGenerator.create_cover_page(front_cover_svg_path, config)
        content_parts, dynamic_css, state = HtmlGenerator.add_section(
            content_parts, dynamic_css, state,
            "Cover page", cover_html,
            start_on_odd=True, reset_counter=False
        )
        
        # 2. Add front matter if present
        if frontmatter:
            frontmatter_html = f'<div class="frontmatter-container">{HtmlGenerator.create_frontmatter_html(frontmatter)}</div>'
            content_parts, dynamic_css, state = HtmlGenerator.add_section(
                content_parts, dynamic_css, state,
                "Front matter", frontmatter_html,
                start_on_odd=True, reset_counter=True
            )
        
        # 3. Add table of contents - pass language_code
        toc_html = f'<div class="frontmatter-container">{HtmlGenerator.create_table_of_contents(lessons, language_code)}</div>'
        content_parts, dynamic_css, state = HtmlGenerator.add_section(
            content_parts, dynamic_css, state,
            "Table of contents", toc_html,
            start_on_odd=True, reset_counter=False
        )
        
        # 4. Add main content (lessons)
        main_content_html = '<div class="mainmatter-container">'
        
        # Add each lesson - pass language_code
        for lesson in lessons:
            main_content_html += f'<div id="lesson-{lesson["number"]}">{HtmlGenerator.create_lesson_html(lesson, language_code)}</div>'
        
        # Add back matter if present
        if backmatter:
            main_content_html += HtmlGenerator.create_backmatter_html(backmatter)
            main_content_html += '<div style="page-break-after: always;"></div>'
        
        # Close main content container
        main_content_html += '</div>'
        
        content_parts, dynamic_css, state = HtmlGenerator.add_section(
            content_parts, dynamic_css, state,
            "Main content", main_content_html,
            start_on_odd=True, reset_counter=True
        )
        
        # 5. Add blank pages to ensure total is divisible by 4
        total_pages = state['absolute_page_number'] - 1
        remainder = total_pages % 4
        if remainder != 0:
            blank_pages_needed = 4 - remainder
            blank_html = ""
            for i in range(blank_pages_needed):
                blank_html += '<div class="blank-page" style="page-break-after: always; height: 100vh;"></div>'
            
            content_parts, dynamic_css, state = HtmlGenerator.add_section(
                content_parts, dynamic_css, state,
                "Padding blank pages", blank_html,
                start_on_odd=False, reset_counter=False
            )
        
        # 6. Add back cover if provided
        if back_cover_svg_path:
            back_cover_html = HtmlGenerator.create_back_cover(back_cover_svg_path)
            content_parts, dynamic_css, state = HtmlGenerator.add_section(
                content_parts, dynamic_css, state,
                "Back cover", back_cover_html,
                start_on_odd=False, reset_counter=False
            )
        
        # Generate the complete HTML document
        return HtmlGenerator.create_debug_html_with_css(content_parts, dynamic_css)