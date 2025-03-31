import markdown
import re
import os
import json
import requests
from sabbath_school_reproducer.generator.css_styles import CSS_TEMPLATE, CssUpdater


class HtmlGenerator:
    """Generates HTML content for PDF generation with incremental approach."""
    
    @staticmethod
    def get_lesson_title(year, quarter):
        """
        Get the lesson title from the lessons.json file
        
        Args:
            year (int): Year of the lesson
            quarter (str): Quarter of the lesson (e.g., q1, q2, q3, q4)
            
        Returns:
            str: Lesson title or default title if not found
        """
        try:
            # Download the lessons.json file
            response = requests.get("https://raw.githubusercontent.com/SabbathSchool/lessons/refs/heads/master/lessons.json")
            response.raise_for_status()
            
            # Parse the JSON data
            lessons_data = response.json()
            
            # Normalize the quarter format (q1 -> Q1)
            normalized_quarter = quarter.upper()
            
            # Find the lesson matching the year and quarter
            for lesson in lessons_data.get("lessons", []):
                # Safely convert both year values to strings
                lesson_year_str = str(lesson["year"])
                year_str = str(year)
                                
                if lesson_year_str == year_str and normalized_quarter in lesson["quarter"]:
                    return lesson["title"]
            
            # If no match found, return a default title
            return "Sabbath School Lessons"
        except Exception as e:
            print(f"Warning: Failed to get lesson title: {e}")
            return "Sabbath School Lessons"
    
    @staticmethod
    def get_quarter_display(quarter):
        """
        Get a formatted display for the quarter
        
        Args:
            quarter (str): Quarter code (e.g., q1, q2, q3, q4)
            
        Returns:
            str: Formatted quarter display (e.g., First Quarter)
        """
        quarter_map = {
            "q1": "First Quarter",
            "Q1": "First Quarter",
            "q2": "Second Quarter",
            "Q2": "Second Quarter",
            "q3": "Third Quarter", 
            "Q3": "Third Quarter",
            "q4": "Fourth Quarter",
            "Q4": "Fourth Quarter"
        }
        return quarter_map.get(quarter, "Quarter")
    
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
    def create_cover_page(front_cover_svg_path=None, config=None):
        """
        Creates the cover page HTML using the SVG from file if provided
        
        Args:
            front_cover_svg_path (str, optional): Path to front cover SVG
            config (dict, optional): Configuration dictionary
            
        Returns:
            str: HTML for cover page
        """
        svg_content = ""
                
        # Set default values
        year = 2025
        quarter = "q1"
        lesson_title = ""
        
        # Use values from config if available
        if config:
            # Use the target year and quarter for display (not the source/reproduction year)
            year = config.get("year", 2025)
            quarter = config.get("quarter", "q1")


            reproduce = config.get("reproduce", {})
            year_orig = reproduce.get("year", 2025)  # Default to 2025 if 'year' is not found
            quarter_orig = reproduce.get("quarter", "q1") 
            
            # Get title from config or generate a default
            lesson_title = config.get("lesson_title", HtmlGenerator.get_lesson_title(year_orig, quarter_orig))
            
            # If we're in reproduction mode, add a note about the original source
            if config.get("reproduce", {}).get("year"):
                source_year = config["reproduce"]["year"]
                source_quarter = config["reproduce"]["quarter"]
                
                # Update title to indicate it's a reproduction
                if not config.get("title"):  # Only modify if no custom title is set
                    lesson_title = f"Sabbath School Lessons (from {source_year} {source_quarter.upper()})"
        
        # Format quarter display
        quarter_display = HtmlGenerator.get_quarter_display(quarter)
        
        # If a path is provided, try to read the SVG from file
        if front_cover_svg_path:
            svg_content = HtmlGenerator.read_svg_file(front_cover_svg_path)
            if not svg_content:
                print(f"Warning: Could not read SVG from {front_cover_svg_path}")
                # We'll fall back to the default SVG
        
        if not svg_content:
            # Use default fallback SVG with dynamic content
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" width="800" height="1000">
                <rect width="800" height="1000" fill="#ffffff"/>
                <rect x="30" y="30" width="740" height="940" stroke="#7d2b2b" stroke-width="3" fill="none"/>
                <text x="400" y="170" font-family="Georgia, serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#7d2b2b">SABBATH SCHOOL</text>
                <text x="400" y="230" font-family="Georgia, serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#7d2b2b">LESSONS</text>
                <text x="400" y="730" font-family="Georgia, serif" font-size="36" font-weight="bold" text-anchor="middle" fill="#5a4130">{lesson_title}</text>
                <text x="400" y="800" font-family="Georgia, serif" font-size="20" text-anchor="middle" fill="#5a4130">{quarter_display}, {year}</text>
            </svg>
            """
            
            # Add source attribution if this is a reproduction
            if config and config.get("reproduce", {}).get("year"):
                source_year = config["reproduce"]["year"]
                source_quarter = config["reproduce"]["quarter"].upper()
                source_quarter_name = HtmlGenerator.get_quarter_display(source_quarter)
                
                # Add source attribution text to SVG
                svg_content = svg_content.replace('</svg>', f"""
                <text x="400" y="850" font-family="Georgia, serif" font-size="16" text-anchor="middle" font-style="italic" fill="#666666">
                    Adapted from {source_quarter_name}, {source_year}
                </text>
                </svg>
                """)
        
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
        
        # Create a default "QUESTIONS" section if no headers are present
        if not lesson.get('question_headers'):
            question_sections["QUESTIONS"] = []
        
        # Group questions by their sections
        for question in lesson.get('questions', []):
            section = question.get('section', 'QUESTIONS')
            if section not in question_sections:
                question_sections[section] = []
            question_sections[section].append(question)
        
        # Sort sections to ensure they're in the correct order if numbers are in section names
        section_names = sorted(question_sections.keys())
        
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
            # Convert markdown to HTML with proper formatting
            notes_content = HtmlGenerator.convert_markdown_to_html(HtmlGenerator.fix_markdown_lists(lesson['notes']))
            paragraphs = notes_content.split('</p>')
            non_empty_paragraphs = [p for p in paragraphs if p.strip()]
            header = "NOTE" if len(non_empty_paragraphs) == 1 else "NOTES"

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
    def fix_markdown_lists(markdown_content):
        """
        Fix markdown list rendering by indenting all non-numbered list item lines.
        This ensures that multi-paragraph list items are correctly rendered as part
        of the same list item rather than causing the list to restart numbering.
        
        Args:
            markdown_content (str): Markdown content with numbered lists
                
        Returns:
            str: Fixed markdown content with proper indentation for list continuity
        """
        # Split the content into lines
        lines = markdown_content.split('\n')

        # If there's only one line, return the content as is
        if len(lines) == 1:
            return markdown_content
        
        # Otherwise, indent non-numbered list lines with a tab
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
        # # Always add a blank page after cover for simplicity
        # content_parts.append('<div class="blank-page" style="page-break-after: always; height: 100vh;"></div>')
        # content_parts.append('<!-- Blank page after cover -->')
        # state['absolute_page_number'] += 1
        
        # 2. Add front matter if present
        if frontmatter:
            frontmatter_html = f'<div class="frontmatter-container">{HtmlGenerator.create_frontmatter_html(frontmatter)}</div>'
            content_parts, dynamic_css, state = HtmlGenerator.add_section(
                content_parts, dynamic_css, state,
                "Front matter", frontmatter_html,
                start_on_odd=True, reset_counter=True
            )
        
        # 3. Add table of contents
        toc_html = f'<div class="frontmatter-container">{HtmlGenerator.create_table_of_contents(lessons)}</div>'
        content_parts, dynamic_css, state = HtmlGenerator.add_section(
            content_parts, dynamic_css, state,
            "Table of contents", toc_html,
            start_on_odd=True, reset_counter=False
        )
        
        # 4. Add main content (lessons)
        main_content_html = '<div class="mainmatter-container">'
        
        # Add each lesson
        for lesson in lessons:
            main_content_html += f'<div id="lesson-{lesson["number"]}">{HtmlGenerator.create_lesson_html(lesson)}</div>'
            # main_content_html += '<div style="page-break-after: always;"></div>'
        
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