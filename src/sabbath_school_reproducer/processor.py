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
                # Store original date for reference if needed
                if lesson.get('date'):
                    lesson['original_date'] = lesson['date']
                
                # Set the new lesson number (1-based)
                new_lesson_number = i + 1
                lesson['number'] = str(new_lesson_number)
                
                # Calculate new date (one week apart)
                lesson_date = quarter_start + timedelta(days=7 * i)
                
                # Format the date in the expected format (e.g., "April 1, 2025")
                new_date = lesson_date.strftime('%B %d, %Y')
                lesson['date'] = new_date
                
                # No need to clean preliminary note here as we've already handled
                # date extraction during initial parsing
            
            return lessons
                
        except Exception as e:
            print(f"Warning: Error adjusting lesson dates: {e}")
            return lessons  # Return original lessons if date adjustment fails
    
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
    def extract_and_remove_date(markdown_text):
        """
        Extract date from markdown and return the text with the date removed
        
        Args:
            markdown_text (str): The markdown text to process
            
        Returns:
            tuple: (extracted_date, cleaned_text)
        """
        # Common date formats in lessons
        date_patterns = [
            r'([A-Za-z]+ \d+, \d{4})',  # e.g., "May 20, 1905"
            r'(\d+ [A-Za-z]+, \d{4})',   # e.g., "20 May, 1905"
            r'(\d{1,2}/\d{1,2}/\d{4})'   # e.g., "5/20/1905"
        ]
        
        extracted_date = ""
        cleaned_text = markdown_text
        
        # Try to find and extract a date
        for pattern in date_patterns:
            date_match = re.search(pattern, markdown_text)
            if date_match:
                extracted_date = date_match.group(1)
                # Only remove the date if it appears on its own line
                date_line_pattern = r'(?m)^(\s*' + re.escape(extracted_date) + r'\s*)$'
                date_line_match = re.search(date_line_pattern, markdown_text)
                if date_line_match:
                    # Remove only the line containing just the date
                    cleaned_text = re.sub(date_line_pattern, '', markdown_text)
                    # Clean up any resulting double newlines
                    cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)
                break
        
        return extracted_date, cleaned_text.strip()
    
    @staticmethod
    def parse_lessons(markdown_content):
        """
        Parse the markdown content to extract lessons using a line-by-line approach
        
        Args:
            markdown_content (str): Markdown content containing lessons
            
        Returns:
            list: List of lesson dictionaries
        """
        # Split the content by lesson headers
        lesson_blocks = re.split(r'(?=^#\s*LESSON\s+\d+|^#\s*Lesson\s+\d+)', markdown_content, flags=re.MULTILINE)
        
        # Remove any empty blocks
        lesson_blocks = [block.strip() for block in lesson_blocks if block.strip()]
        
        lessons = []
        
        for block in lesson_blocks:
            lines = block.split('\n')
            
            # Initialize lesson structure
            lesson = {
                'number': '',
                'date': '',
                'title': '',
                'preliminary_note': '',
                'questions': [],
                'question_headers': [],
                'notes': '',
                'additional_sections': []
            }
            
            # Process the lesson header (first line)
            if lines and (lines[0].startswith('# LESSON') or lines[0].startswith('# Lesson')):
                header_line = lines[0]
                
                # Extract lesson number
                number_match = re.search(r'#\s*(?:LESSON|Lesson)\s+(\d+)', header_line)
                if number_match:
                    lesson['number'] = number_match.group(1)
                
                # Check for date in em-dash format
                em_dash_date_match = re.search(r'[—–-]\s*([A-Za-z]+ \d+, \d{4})', header_line)
                if em_dash_date_match:
                    lesson['date'] = em_dash_date_match.group(1)
                else:
                    # Check for title after dash
                    title_match = re.search(r'[-–—]\s*(.*?)$', header_line)
                    if title_match:
                        lesson['title'] = title_match.group(1).strip()
            
            # Process the rest of the lines
            line_index = 1  # Start from the second line
            preliminary_lines = []
            current_section = None
            current_question_section = None
            question_list = []
            
            # Flag to track if we've seen any section after questions
            seen_non_question_section = False
            
            # Look for the title in level 2 headers
            if not lesson['title'] and line_index < len(lines):
                for i in range(line_index, min(line_index + 10, len(lines))):
                    if i < len(lines) and re.match(r'^##\s+', lines[i]):
                        title_match = re.search(r'^##\s+(.*?)$', lines[i])
                        if title_match:
                            lesson['title'] = title_match.group(1).strip()
                            line_index = i + 1
                            break
            
            # Look for date on its own line
            if not lesson['date'] and line_index < len(lines):
                for i in range(line_index, min(line_index + 5, len(lines))):
                    if i < len(lines):
                        date_match = re.search(r'^([A-Za-z]+ \d+, \d{4})$', lines[i].strip())
                        if date_match:
                            lesson['date'] = date_match.group(1)
                            line_index = i + 1
                            break
                        
                        # Also check for italicized date
                        italics_date_match = re.search(r'^\*([A-Za-z]+ \d+, \d{4})\*$', lines[i].strip())
                        if italics_date_match:
                            lesson['date'] = italics_date_match.group(1)
                            line_index = i + 1
                            break
            
            # Find where content actually starts
            while line_index < len(lines) and not lines[line_index].strip():
                line_index += 1
            
            # Collect preliminary content - but we need to look ahead to see if it's followed by questions
            has_preliminary = False
            preliminary_start_index = line_index
            preliminary_end_index = line_index
            
            # Scan ahead to find patterns
            for i in range(line_index, len(lines)):
                line = lines[i]
                
                # If we find a numbered list, this is likely where questions start
                if re.match(r'^\s*\d+\.\s+', line):
                    # If there was content between line_index and i, it's preliminary
                    if i > line_index:
                        # Check if the line right before this is a section header
                        prev_line = ""
                        for j in range(i-1, max(0, i-5), -1):
                            if j >= 0 and lines[j].strip():
                                prev_line = lines[j]
                                break
                        if not re.match(r'^#{2,3}\s+', prev_line):
                            # Only collect as preliminary if it's not immediately after a header
                            has_preliminary = True
                            preliminary_end_index = i
                    break
                
                # If we find a section header followed by numbered list, it's not preliminary
                if re.match(r'^#{2,3}\s+', line):
                    # Look ahead to see if this section contains numbered lists
                    for j in range(i+1, min(i+5, len(lines))):
                        if j < len(lines) and re.match(r'^\s*\d+\.\s+', lines[j]):
                            # This is a question section header, not preliminary
                            has_preliminary = False
                            preliminary_end_index = i
                            break
            
            # Collect the preliminary content if we found some
            if has_preliminary:
                for i in range(preliminary_start_index, preliminary_end_index):
                    preliminary_lines.append(lines[i])
                line_index = preliminary_end_index
            
            # Save preliminary matter
            lesson['preliminary_note'] = '\n'.join(preliminary_lines).strip()
            
            # Process sections (questions, notes, and additional)
            section_buffer = []
            current_question_text = ""
            in_question = False
            
            while line_index < len(lines):
                line = lines[line_index]
                
                # Check if this line is a section header
                header_match = re.match(r'^#{2,3}\s+(.*?)$', line)
                
                if header_match:
                    # If we were collecting a question, save it
                    if in_question and current_question_text and not seen_non_question_section:
                        question_obj = MarkdownProcessor._parse_question(current_question_text, current_question_section or "QUESTIONS")
                        question_list.append(question_obj)
                        current_question_text = ""
                        in_question = False
                    
                    # Save the previous section if we have one
                    if current_section:
                        if current_section.upper() == 'NOTES':
                            lesson['notes'] = '\n'.join(section_buffer).strip()
                        elif current_section != 'questions':
                            # This is an additional section
                            lesson['additional_sections'].append({
                                'title': current_section,
                                'content': '\n'.join(section_buffer).strip()
                            })
                            # Once we've seen an additional section, no more questions
                            seen_non_question_section = True
                        
                        # Clear the buffer for the new section
                        section_buffer = []
                    
                    header_text = header_match.group(1).strip()
                    
                    # Look ahead to see if the next section is questions (has numbered list)
                    is_question_section = False
                    if not seen_non_question_section:  # Only check for question sections if we haven't seen non-question sections
                        for i in range(line_index + 1, min(line_index + 5, len(lines))):
                            if i < len(lines):
                                numbered_list_match = re.match(r'^\s*\d+\.\s+', lines[i])
                                if numbered_list_match:
                                    is_question_section = True
                                    break
                                elif lines[i].strip() and not re.match(r'^\s*$', lines[i]):
                                    # If we encounter non-empty, non-numbered list content, it's not a question section
                                    break
                    
                    # Determine the type of the new section
                    if re.search(r'^notes$', header_text, re.IGNORECASE):
                        current_section = 'NOTES'
                        current_question_section = None
                        seen_non_question_section = True
                    elif (is_question_section or re.search(r'^questions$', header_text, re.IGNORECASE)) and not seen_non_question_section:
                        # This is a questions section (only if we haven't seen non-question sections yet)
                        current_section = 'questions'
                        
                        # Track the question section header
                        current_question_section = header_text
                        if current_question_section not in lesson['question_headers']:
                            lesson['question_headers'].append(current_question_section)
                    else:
                        # This is an additional section
                        current_section = header_text
                        current_question_section = None
                        seen_non_question_section = True
                
                elif re.match(r'^\s*\d+\.\s+', line):
                    # This is a numbered list item, which could be a question or a note
                    
                    # If this is immediately after the NOTES header, it's a note
                    if current_section and current_section.upper() == 'NOTES':
                        section_buffer.append(line)
                    elif not seen_non_question_section:
                        # This is a question (only if we haven't seen non-question sections yet)
                        
                        # If we were collecting a question, save it
                        if in_question and current_question_text:
                            question_obj = MarkdownProcessor._parse_question(current_question_text, current_question_section or "QUESTIONS")
                            question_list.append(question_obj)
                        
                        # Start collecting a new question
                        in_question = True
                        current_question_text = line
                        
                        # If this is the first question and we don't have a section yet, use default
                        if not current_section or current_section != 'questions':
                            current_section = 'questions'
                            if "QUESTIONS" not in lesson['question_headers']:
                                current_question_section = "QUESTIONS"
                                lesson['question_headers'].append(current_question_section)
                    else:
                        # This is numbered content in another section
                        section_buffer.append(line)
                
                elif in_question and not seen_non_question_section:
                    # Continue collecting the current question
                    current_question_text += '\n' + line
                
                elif current_section:
                    # Collecting content for the current section
                    section_buffer.append(line)
                
                line_index += 1
            
            # Save any final question
            if in_question and current_question_text and not seen_non_question_section:
                question_obj = MarkdownProcessor._parse_question(current_question_text, current_question_section or "QUESTIONS")
                question_list.append(question_obj)
            
            # Save the final section if there is one
            if current_section:
                if current_section.upper() == 'NOTES':
                    lesson['notes'] = '\n'.join(section_buffer).strip()
                elif current_section != 'questions':
                    # This is an additional section
                    lesson['additional_sections'].append({
                        'title': current_section,
                        'content': '\n'.join(section_buffer).strip()
                    })
            
            # Add all questions to the lesson
            lesson['questions'] = question_list
            
            # Add the lesson to the list
            lessons.append(lesson)
        
        return lessons
    
    @staticmethod
    def _parse_question(question_text, section_name=None):
        """
        Parse a question text into question and answer parts
        
        Args:
            question_text (str): The full text of the question
            section_name (str, optional): The section this question belongs to
            
        Returns:
            dict: A dictionary with 'text', 'answer', and 'section' keys
        """
        # Remove the question number
        num_match = re.match(r'^\s*\d+\.\s+', question_text)
        if num_match:
            question_text = question_text[num_match.end():].strip()
        
        # Handle answer separator formats:
        # Format 1: Question? — Answer
        # Format 2: Question? Answer
        question_part = question_text
        answer_part = ""
        
        if '?' in question_text:
            # Split at the last question mark
            last_q_idx = question_text.rfind('?')
            question_part = question_text[:last_q_idx+1]
            answer_part = question_text[last_q_idx+1:].strip()
            
            # Check if answer starts with an em-dash
            if answer_part.startswith('—') or answer_part.startswith('-') or answer_part.startswith('–'):
                answer_part = answer_part[1:].strip()
        
        return {
            'text': question_part,
            'answer': answer_part,
            'section': section_name
        }
    
    @staticmethod
    def parse_questions_from_markdown(markdown_content):
        """
        Parse questions from markdown content.
        
        Args:
            markdown_content (str): Markdown content containing questions
            
        Returns:
            list: List of question dictionaries
        """
        question_list = []
        lines = markdown_content.split('\n')
        
        current_question_text = ""
        in_question = False
        
        for line in lines:
            # Check if this is a new question
            num_match = re.match(r'^\s*\d+\.\s+', line)
            
            if num_match:
                # If we were collecting a question, save it
                if in_question and current_question_text:
                    question_obj = MarkdownProcessor._parse_question(current_question_text)
                    question_list.append(question_obj)
                
                # Start collecting a new question
                in_question = True
                current_question_text = line
            
            elif in_question:
                # Continue collecting the current question
                current_question_text += '\n' + line
        
        # Save any final question
        if in_question and current_question_text:
            question_obj = MarkdownProcessor._parse_question(current_question_text)
            question_list.append(question_obj)
        
        return question_list
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