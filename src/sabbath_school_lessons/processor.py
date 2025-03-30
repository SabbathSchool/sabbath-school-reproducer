"""
Markdown Processor for Sabbath School Lessons

This module processes markdown files, extracting lesson content, front matter, and back matter.
"""

import re
import markdown
from bs4 import BeautifulSoup


class MarkdownProcessor:
    """Processes markdown files to extract structured content."""
    
    @staticmethod
    def adjust_dates(lessons, config):
        """
        Adjust lesson dates based on the quarter_start_date in config
        
        Args:
            lessons (list): List of lesson dictionaries
            config (dict): Configuration dictionary with reproduction settings
            
        Returns:
            list: Updated list of lesson dictionaries with adjusted dates
        """
        if not config or 'reproduce' not in config or not config['reproduce'].get('quarter_start_date'):
            return lessons  # No date adjustment needed
        
        try:
            # Parse the quarter start date
            from datetime import datetime, timedelta
            quarter_start = datetime.strptime(config['reproduce']['quarter_start_date'], '%Y-%m-%d')
            
            # Set new lesson numbers if needed
            start_lesson = config['reproduce'].get('start_lesson', 1)
            
            # Sort lessons by their original number
            lessons.sort(key=lambda l: int(l.get('number', 0)))
            
            # Apply new dates and lesson numbers
            for i, lesson in enumerate(lessons):
                # Set the new lesson number (1-based)
                new_lesson_number = i + 1
                lesson['number'] = str(new_lesson_number)
                
                # Calculate new date (one week apart)
                lesson_date = quarter_start + timedelta(days=7 * i)
                
                # Format the date in the expected format (e.g., "April 1, 2025")
                new_date = lesson_date.strftime('%B %d, %Y')
                lesson['date'] = new_date
            
            return lessons
            
        except Exception as e:
            print(f"Warning: Error adjusting lesson dates: {e}")
            return lessons  # Return original lessons if date adjustment fails
    
    @staticmethod
    def parse_questions_from_markdown(questions_text):
        """
        Parse questions directly from markdown text
        
        Args:
            questions_text (str): Markdown text containing questions
            
        Returns:
            list: List of question dictionaries with text, scripture, and answer
        """
        # [Existing implementation remains the same]
        questions = []
        
        # Split by question numbers (1., 2., etc.)
        question_blocks = re.split(r'(?m)^\s*(\d+\.)\s+', questions_text.strip())
        
        # The first element will be empty if the text starts with a numbered list
        if question_blocks and not question_blocks[0].strip():
            question_blocks.pop(0)
        
        # Process question blocks in pairs (number, content)
        for i in range(0, len(question_blocks), 2):
            if i + 1 >= len(question_blocks):
                break
                
            question_content = question_blocks[i + 1].strip()
            
            # Extract scripture reference - everything after the last question mark
            question_parts = question_content.split('?')
            scripture_ref = ""
            
            if len(question_parts) > 1:
                # The last part after the question mark contains the scripture reference
                scripture_part = question_parts[-1].strip()
                scripture_ref = scripture_part
                
                # Remove scripture reference from question text
                question_content = '?'.join(question_parts[:-1]) + '?'
            
            # Extract answer if present
            ans_match = re.search(r'Ans\.\s*—\s*(.*?)$', question_content, re.DOTALL)
            answer = ""
            if ans_match:
                answer = ans_match.group(1).strip()
                question_content = question_content[:ans_match.start()].strip()
            
            # Clean up question text
            question_text = question_content.strip()
            
            # Add the parsed question
            questions.append({
                'text': question_text,
                'scripture': scripture_ref,
                'answer': answer
            })
        
        return questions
    
    @staticmethod
    def parse_file_sections(content):
        """
        Extract content from different file sections marked with special headers
        
        Args:
            content (str): Combined markdown file content
            
        Returns:
            tuple: (lessons_content, frontmatter_content, backmatter_content)
        """
        # [Existing implementation remains the same]
        # Find all file sections
        file_sections = re.findall(r'# File: ([^\n]+)[\r\n]+#-+[\r\n]+(.*?)(?=# File:|$)', content, re.DOTALL)
        
        frontmatter_content = ""
        backmatter_content = ""
        lessons_content = ""
        
        for filename, section_content in file_sections:
            filename = filename.strip().lower()
            
            if 'front-matter' in filename:
                frontmatter_content = section_content.strip()
            elif 'back-matter' in filename:
                backmatter_content = section_content.strip()
            elif 'week-' in filename or 'lesson-' in filename:
                lessons_content += section_content + "\n\n"
        
        return lessons_content, frontmatter_content, backmatter_content
    
    @staticmethod
    def parse_lessons(markdown_content):
        """
        Parse the markdown content to extract lessons
        
        Args:
            markdown_content (str): Markdown content containing lessons
            
        Returns:
            list: List of lesson dictionaries
        """
        # [Existing implementation remains the same]
        # Convert markdown to HTML for structure analysis
        html_content = markdown.markdown(markdown_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract lessons
        lessons = []
        current_lesson = None
        
        for heading in soup.find_all(['h1']):
            if "LESSON" in heading.get_text().upper():
                # Save previous lesson if exists
                if current_lesson:
                    lessons.append(current_lesson)
                
                # Parse lesson header
                header_text = heading.get_text()
                lesson_match = re.search(r'LESSON (\d+)', header_text, re.IGNORECASE)
                title_match = re.search(r'- ([^\n]+)', header_text)
                
                lesson_number = lesson_match.group(1) if lesson_match else ""
                lesson_title = title_match.group(1).strip() if title_match else ""
                
                # Start new lesson
                current_lesson = {
                    'number': lesson_number,
                    'date': "",
                    'title': lesson_title,
                    'preliminary_note': "",
                    'questions': [],
                    'notes': ''
                }
                
                # Find the original markdown content for this lesson
                lesson_start_pattern = re.escape(f"# Lesson {lesson_number}")
                lesson_start_match = re.search(lesson_start_pattern, markdown_content, re.IGNORECASE)
                
                if lesson_start_match:
                    lesson_start = lesson_start_match.start()
                    
                    # Find the start of the next lesson or the end of content
                    next_lesson_match = re.search(r'# Lesson \d+', markdown_content[lesson_start + 1:], re.IGNORECASE)
                    if next_lesson_match:
                        lesson_end = lesson_start + 1 + next_lesson_match.start()
                    else:
                        lesson_end = len(markdown_content)
                    
                    lesson_markdown = markdown_content[lesson_start:lesson_end]
                    
                    # Extract date from markdown
                    date_match = re.search(r'([A-Za-z]+ \d+, \d{4})', lesson_markdown)
                    if date_match:
                        current_lesson['date'] = date_match.group(1)
                    
                    # Extract questions section from markdown
                    questions_match = re.search(r'## Questions\s+(.*?)(?=##|$)', lesson_markdown, re.DOTALL)
                    if questions_match:
                        questions_text = questions_match.group(1).strip()
                        current_lesson['questions'] = MarkdownProcessor.parse_questions_from_markdown(questions_text)
                    
                    # Extract preliminary note
                    preliminary_match = re.search(r'(?<=\n\n)(.*?)(?=## Questions)', lesson_markdown, re.DOTALL)
                    if preliminary_match:
                        current_lesson['preliminary_note'] = preliminary_match.group(1).strip()
                    
                    # Extract notes section
                    notes_match = re.search(r'## Notes\s+(.*?)(?=##|$)', lesson_markdown, re.DOTALL)
                    if notes_match:
                        current_lesson['notes'] = notes_match.group(1).strip()
        
        # Add the last lesson
        if current_lesson:
            lessons.append(current_lesson)
        
        return lessons
    
    @staticmethod
    def process_markdown_file(markdown_file, config=None):
        """
        Process the markdown file to extract content
        
        Args:
            markdown_file (str): Path to the markdown file
            config (dict, optional): Configuration dictionary for reproduction
            
        Returns:
            dict: Dictionary with extracted content
        """
        # Read the markdown file
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract file sections first
        lessons_content, frontmatter_content, backmatter_content = MarkdownProcessor.parse_file_sections(content)
        
        # Parse lessons from the lessons content
        lessons = MarkdownProcessor.parse_lessons(lessons_content)
        
        # Apply date adjustments if reproduction settings exist
        if config and 'reproduce' in config:
            lessons = MarkdownProcessor.adjust_dates(lessons, config)
        
        # Log debugging information
        print(f"Found {len(lessons)} lessons")
        for lesson in lessons:
            print(f"Lesson {lesson['number']}: {lesson['title']} ({lesson['date']})")
            print(f"Questions: {len(lesson['questions'])}")
            print(f"Notes: {'Yes' if lesson['notes'] else 'No'}")
            print(f"Preliminary: {'Yes' if lesson['preliminary_note'] else 'No'}")
        
        # Log frontmatter and backmatter status
        print(f"Frontmatter present: {'Yes' if frontmatter_content else 'No'}")
        print(f"Backmatter present: {'Yes' if backmatter_content else 'No'}")
        
        return {
            'lessons': lessons,
            'metadata': {},
            'frontmatter': frontmatter_content,
            'backmatter': backmatter_content
        }