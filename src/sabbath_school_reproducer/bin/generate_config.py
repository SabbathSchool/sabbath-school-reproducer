#!/usr/bin/env python3
"""
Configuration Template Generator

This script generates a template YAML configuration file and color theme.

Usage:
python3 generate_config.py [output_file]
"""

import sys
import os
import yaml
from datetime import datetime

def generate_default_theme(theme_directory="themes"):
    """
    Generate a default burgundy color theme and save it to the themes directory
    
    Args:
        theme_directory (str): Directory to save the theme file
        
    Returns:
        str: Path to the generated theme file
    """
    # Create themes directory if it doesn't exist
    os.makedirs(theme_directory, exist_ok=True)
    
    # Define the theme file path
    theme_path = os.path.join(theme_directory, "burgundy.yaml")
    
    # Skip if the theme file already exists
    if os.path.exists(theme_path):
        print(f"Theme file already exists at: {theme_path}")
        return theme_path
    
    # Create the default burgundy theme content with detailed comments
    theme_content = """# Burgundy Theme for Sabbath School Lessons PDF
# This default theme uses warm, burgundy tones for a traditional look.

# Text colors
text:
  primary: '#3c1815'    # Main body text color (deep burgundy)
  secondary: '#5a4130'  # Secondary text, used in footers/headers (brown)
  accent: '#7d2b2b'     # Accent text color for headings (rich burgundy)
  link: '#007bff'       # Color for links (blue)

# Background colors
background:
  light: '#f9f7f1'        # Light background color (cream)
  medium: '#f5f1e6'       # Medium background color (light tan)
  dark: '#e0d5c0'         # Dark background color (tan)
  additional: '#f0e5d8'   # Additional section background (lighter tan)
  tableHeader: '#f4f4f4'  # Table header background (light grey)
  tableRowEven: '#f9f7f1' # Even row background in tables (cream)
  hover: '#f0f0f0'        # Hover state background (light grey)

# Border colors
border:
  primary: '#8b4513'     # Primary border color (saddle brown)
  secondary: '#d4c7a5'   # Secondary, lighter border (light tan)
  additional: '#6a4e23'  # Additional section border (darker brown)
  table: '#ddd'          # Table border color (light grey)

# Accent colors
accent:
  primary: '#7d2b2b'      # Primary accent color (rich burgundy)
  secondary: '#4b3b2f'    # Secondary accent color (dark brown)
  tertiary: '#696969'     # Tertiary accent color (dim grey)
  quaternary: '#808080'   # Quaternary accent color (grey)

# Special colors for specific elements
special:
  sun: '#FFD700'       # Sun color in illustrations (gold)
  lake: '#4682B4'      # Lake color in illustrations (steel blue)
  grass: '#228B22'     # Grass color in illustrations (forest green)
  tree: '#8B4513'      # Tree color in illustrations (saddle brown)
"""
    
    # Write the theme to file
    with open(theme_path, 'w', encoding='utf-8') as f:
        f.write(theme_content)
    
    print(f"Default burgundy theme generated at: {theme_path}")
    return theme_path


def generate_language_template(language_code='en', output_directory='languages'):
    """
    Generate a language configuration template file for the specified language
    
    Args:
        language_code (str): Language code (e.g., 'en', 'sw', 'luo')
        output_directory (str): Directory to save the language file
        
    Returns:
        str: Path to the generated language file
    """
    # Create languages directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Define the language file path
    language_path = os.path.join(output_directory, f"{language_code}.yaml")
    
    # Skip if the language file already exists
    if os.path.exists(language_path):
        print(f"Language file already exists at: {language_path}")
        return language_path
    
    # Define default translations based on language code
    translations = {}
    
    if language_code == 'en':
        translations = {
            'notes': 'NOTES',
            'note': 'NOTE',
            'questions': 'QUESTIONS',
            'answer_prefix': 'Ans.',
            'lesson': 'LESSON',
            'sabbath_school': 'SABBATH SCHOOL',
            'lessons': 'LESSONS',
            'adapted_from': 'Adapted from',
            'from_text': 'from',
            'quarter_names': {
                'q1': 'FIRST QUARTER',
                'q2': 'SECOND QUARTER',
                'q3': 'THIRD QUARTER',
                'q4': 'FOURTH QUARTER'
            },
            'quarter_months': {
                'q1': 'January - March',
                'q2': 'April - June',
                'q3': 'July - September',
                'q4': 'October - December'
            },
            'table_of_contents': 'TABLE OF CONTENTS',
            'lesson_column': 'Lesson',
            'title_column': 'Title',
            'date_column': 'Date',
            'page_column': 'Page'
        }
    elif language_code == 'sw':
        translations = {
            'notes': 'MAELEZO',
            'note': 'ELEZO',
            'questions': 'MASWALI',
            'answer_prefix': 'Jibu',
            'lesson': 'SOMO',
            'sabbath_school': 'SHULE YA SABATO',
            'lessons': 'MASOMO',
            'adapted_from': 'Imetoholewa kutoka',
            'from_text': 'kutoka',
            'quarter_names': {
                'q1': 'ROBO YA KWANZA',
                'q2': 'ROBO YA PILI',
                'q3': 'ROBO YA TATU',
                'q4': 'ROBO YA NNE'
            },
            'quarter_months': {
                'q1': 'Januari - Machi',
                'q2': 'Aprili - Juni',
                'q3': 'Julai - Septemba',
                'q4': 'Oktoba - Desemba'
            },
            'table_of_contents': 'YALIYOMO',
            'lesson_column': 'Somo',
            'title_column': 'Kichwa',
            'date_column': 'Tarehe',
            'page_column': 'Ukurasa'
        }
    elif language_code == 'luo':
        translations = {
            'notes': 'WECHE',
            'note': 'WACH',
            'questions': 'PENJO',
            'answer_prefix': 'Duoko',
            'lesson': 'PUONJ',
            'sabbath_school': 'SKUL MAR SABATO',
            'lessons': 'PUONJO',
            'adapted_from': 'Olos kuom',
            'from_text': 'kuom',
            'quarter_names': {
                'q1': 'NUT MOKWONGO MAR HIGA',
                'q2': 'NUT MAR ARIYO MAR HIGA',
                'q3': 'NUT MAR ADEK MAR HIGA',
                'q4': 'NUT MAR ANGʼWEN MAR HIGA'
            },
            'quarter_months': {
                'q1': 'Januari - Mach',
                'q2': 'April - Jun',
                'q3': 'July - September',
                'q4': 'October - December'
            },
            'table_of_contents': 'GIKO MAR PUONJ',
            'lesson_column': 'Puonj',
            'title_column': 'Wach Motelo',
            'date_column': 'Tarik',
            'page_column': 'Kama Ondike'
        }
    else:
        # For unsupported languages, use English as template
        translations = {
            'notes': 'NOTES',
            'note': 'NOTE',
            'questions': 'QUESTIONS',
            'answer_prefix': 'Ans.',
            'lesson': 'LESSON',
            'sabbath_school': 'SABBATH SCHOOL',
            'lessons': 'LESSONS',
            'adapted_from': 'Adapted from',
            'from_text': 'from',
            'quarter_names': {
                'q1': 'FIRST QUARTER',
                'q2': 'SECOND QUARTER',
                'q3': 'THIRD QUARTER',
                'q4': 'FOURTH QUARTER'
            },
            'quarter_months': {
                'q1': 'January - March',
                'q2': 'April - June',
                'q3': 'July - September',
                'q4': 'October - December'
            },
            'table_of_contents': 'TABLE OF CONTENTS',
            'lesson_column': 'Lesson',
            'title_column': 'Title',
            'date_column': 'Date',
            'page_column': 'Page'
        }
    
    # Add month names
    if language_code == 'en':
        translations['month_names'] = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
    elif language_code == 'sw':
        translations['month_names'] = [
            'Januari', 'Februari', 'Machi', 'Aprili', 'Mei', 'Juni',
            'Julai', 'Agosti', 'Septemba', 'Oktoba', 'Novemba', 'Desemba'
        ]
    elif language_code == 'luo':
        translations['month_names'] = [
            'Januari', 'Februari', 'Mach', 'April', 'May', 'Jun',
            'July', 'Agost', 'September', 'October', 'November', 'December'
        ]
    else:
        translations['month_names'] = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
    
    # Add date formats
    if language_code == 'en':
        translations['date_formats'] = [
            '([A-Za-z]+ \d+, \d{4})',  # e.g., "May 20, 1905"
            '(\d+ [A-Za-z]+, \d{4})',   # e.g., "20 May, 1905"
            '(\d{1,2}/\d{1,2}/\d{4})'   # e.g., "5/20/1905"
        ]
    elif language_code == 'sw':
        translations['date_formats'] = [
            '([A-Za-z]+ \d+, \d{4})',  # e.g., "Mei 20, 1905"
            '(\d+ [A-Za-z]+, \d{4})',   # e.g., "20 Mei, 1905"
            '(\d{1,2}/\d{1,2}/\d{4})'   # e.g., "20/5/1905"
        ]
    elif language_code == 'luo':
        translations['date_formats'] = [
            '([A-Za-z]+ \d+, \d{4})',  # e.g., "May 20, 1905"
            '(\d+ [A-Za-z]+, \d{4})',   # e.g., "20 May, 1905"
            '(\d{1,2}/\d{1,2}/\d{4})'   # e.g., "20/5/1905"
        ]
    else:
        translations['date_formats'] = [
            '([A-Za-z]+ \d+, \d{4})',  # e.g., "May 20, 1905"
            '(\d+ [A-Za-z]+, \d{4})',   # e.g., "20 May, 1905"
            '(\d{1,2}/\d{1,2}/\d{4})'   # e.g., "5/20/1905"
        ]
    
    # Add date format template
    translations['date_format_template'] = '{month} {day}, {year}' if language_code == 'en' else '{day} {month}, {year}'
    
    # Create the YAML content with comments
    yaml_content = f"""# Language configuration for {language_code}
# This file contains language-specific translations for Sabbath School Lesson Downloader

# Basic terms
notes: '{translations['notes']}'  # Used for section headers and headings
note: '{translations['note']}'    # Used for single-note sections
questions: '{translations['questions']}'  # Questions section header
answer_prefix: '{translations['answer_prefix']}'  # Prefix for answers in questions
lesson: '{translations['lesson']}'  # Used for lesson titles

# Cover page terms
sabbath_school: '{translations['sabbath_school']}'  # Main title on cover page
lessons: '{translations['lessons']}'  # Secondary title on cover page
adapted_from: '{translations['adapted_from']}'  # Text used in "Adapted from X" on cover
from_text: '{translations['from_text']}'  # Text used in "from X" in titles

# Quarter names (used in headings and footers)
quarter_names:
  q1: '{translations['quarter_names']['q1']}'
  q2: '{translations['quarter_names']['q2']}'
  q3: '{translations['quarter_names']['q3']}'
  q4: '{translations['quarter_names']['q4']}'

# Quarter month ranges (used in cover pages)
quarter_months:
  q1: '{translations['quarter_months']['q1']}'
  q2: '{translations['quarter_months']['q2']}'
  q3: '{translations['quarter_months']['q3']}'
  q4: '{translations['quarter_months']['q4']}'

# Table of contents translations
table_of_contents: '{translations['table_of_contents']}'
lesson_column: '{translations['lesson_column']}'
title_column: '{translations['title_column']}'
date_column: '{translations['date_column']}'
page_column: '{translations['page_column']}'

# Month names for date formatting
month_names:
"""

    # Add month names
    for month in translations['month_names']:
        yaml_content += f"  - '{month}'\n"
    
    # Add date formats
    yaml_content += """
# Date format regular expressions (used for extracting dates from content)
date_formats:
"""
    for format_regex in translations['date_formats']:
        yaml_content += f"  - '{format_regex}'\n"
    
    # Add date format template
    yaml_content += f"""
# Date format template for generating new dates
date_format_template: '{translations['date_format_template']}'
"""
    
    # Write the YAML content to file
    with open(language_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    print(f"Language template for '{language_code}' generated at: {language_path}")
    return language_path


def generate_template_config(output_path="config.yaml"):
    """
    Generate a template configuration file with default values
    
    Args:
        output_path (str): Path to save the configuration file
        
    Returns:
        str: Path to the generated configuration file
    """
    # Check if the config file already exists
    if os.path.exists(output_path):
        print(f"Configuration file already exists at: {output_path}")
        return output_path
    
    # Get current year and determine current quarter
    now = datetime.now()
    year = now.year
    quarter = f"q{(now.month - 1) // 3 + 1}"
    
    # Calculate default start date (first day of current quarter)
    quarter_month = ((int(quarter[1]) - 1) * 3) + 1  # q1->1, q2->4, q3->7, q4->10
    start_date = f"{year}-{quarter_month:02d}-01"  # Format: YYYY-MM-DD
    
    # Generate the default color theme and get its path
    theme_path = generate_default_theme()
    # Convert to relative path for config file
    rel_theme_path = os.path.relpath(theme_path, os.path.dirname(output_path))
    
    # Create a string for the YAML output with manual comments for fields
    yaml_output = "# Sabbath School Lesson Configuration\n\n"
    yaml_output += "# Year and quarter to download\n"
    yaml_output += "# The year of the lessons (e.g., 2025)\n"
    yaml_output += f"year: {year}\n"
    yaml_output += "# The quarter of the lessons (q1, q2, q3, q4)\n"
    yaml_output += f"quarter: {quarter}\n"
    yaml_output += "# The language of the lessons (e.g., 'en' for English)\n"
    yaml_output += f"language: en\n"

    yaml_output += "\n# File paths\n"
    yaml_output += "# Path to the output PDF file for the lessons\n"
    # yaml_output += f"output_file: ./output/sabbath_school_lesson_{year}_{quarter}_en.pdf\n"
    yaml_output += "# Path to the front cover SVG file\n"
    yaml_output += "front_cover_svg: ./assets/front_cover.svg\n"
    yaml_output += "# Path to the back cover SVG file\n"
    yaml_output += "back_cover_svg: ./assets/back_cover.svg\n"
    yaml_output += "# Path to the color theme YAML file\n"
    yaml_output += f"color_theme_path: {rel_theme_path}\n"

    yaml_output += "\n# Reproduction options\n"
    yaml_output += "# Historical year to adapt (e.g., 1905)\n"
    yaml_output += f"reproduce:\n"
    yaml_output += f"  year: 1905\n"
    yaml_output += "# Historical quarter to adapt (e.g., q2)\n"
    yaml_output += f"  quarter: q2\n"
    yaml_output += "# First lesson to include (default is 1)\n"
    yaml_output += f"  start_lesson: 1\n"
    yaml_output += "# Last lesson to include (None for all lessons)\n"
    yaml_output += f"  stop_lesson: null\n"
    yaml_output += "# The start date of the quarter (format: YYYY-MM-DD)\n"
    yaml_output += f"  quarter_start_date: '{start_date}'\n"

    yaml_output += "\n# PDF metadata\n"
    yaml_output += "# The title of the generated PDF\n"
    yaml_output += f"title: Sabbath School Lessons\n"
    yaml_output += "# The subtitle for the PDF (typically the quarter and year)\n"
    yaml_output += f"subtitle: Quarter {quarter[1]}, {year}\n"
    yaml_output += "# The publisher of the generated PDF\n"
    yaml_output += f"publisher: Gospel Sounders\n"

    yaml_output += "\n# Language settings\n"
    yaml_output += "# Path to the language configuration file\n"
    yaml_output += f"languages_dir: ./languages\n"
    yaml_output += "# lesson title: will use lesson title from english repo if this is not give"
    yaml_output += "lesson_title: lesson title"


    # Write the output to the specified file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(yaml_output)
    
    print(f"Template configuration generated at: {output_path}")
    return output_path

def main():
    """
    Main function
    
    Returns:
        int: Exit code
    """
    # Get output path from command line argument or use default
    output_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"

    os.makedirs("languages", exist_ok=True)
    for lang in ["en", "swa", "luo"]:
        generate_language_template(lang, "languages")
    
    # Generate the configuration file (won't overwrite existing files)
    generate_template_config(output_path)
    
    # Always ensure we have the default theme
    generate_default_theme()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())