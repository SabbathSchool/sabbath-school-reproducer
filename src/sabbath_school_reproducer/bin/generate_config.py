#!/usr/bin/env python3
"""
Configuration Template Generator

This script generates a template YAML configuration file.

Usage:
python3 generate_config.py [output_file]
"""

import sys
import os
import yaml
from datetime import datetime

def generate_template_config(output_path="config.yaml"):
    """
    Generate a template configuration file with default values
    
    Args:
        output_path (str): Path to save the configuration file
        
    Returns:
        str: Path to the generated configuration file
    """
    # Get current year and determine current quarter
    now = datetime.now()
    year = now.year
    quarter = f"q{(now.month - 1) // 3 + 1}"
    
    # Calculate default start date (first day of current quarter)
    quarter_month = ((int(quarter[1]) - 1) * 3) + 1  # q1->1, q2->4, q3->7, q4->10
    start_date = f"{year}-{quarter_month:02d}-01"  # Format: YYYY-MM-DD
    
    # Create a template configuration
    config = {
        "year": year,
        "quarter": quarter,
        "language": "en",
        "input_file": f"./combined_lessons_{year}_{quarter}_en.md",
        "output_file": f"./output/sabbath_school_lesson_{year}_{quarter}_en.pdf",
        "front_cover_svg": "./assets/front_cover.svg",
        "back_cover_svg": "./assets/back_cover.svg",
        "reproduce": {
            "year": 1905,  # Default historical year
            "quarter": "q2",  # Default historical quarter
            "start_lesson": 1,  # First lesson to include
            "stop_lesson": None,  # Last lesson to include, None for all
            "quarter_start_date": start_date,  # First day of the quarter in format YYYY-MM-DD
        },
        "title": "Sabbath School Lessons",
        "subtitle": f"Quarter {quarter[1]}, {year}",
        "publisher": "Gospel Sounders"
    }

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
    yaml_output += "# Path to the input markdown file containing the lessons\n"
    yaml_output += f"input_file: ./combined_lessons_{year}_{quarter}_en.md\n"
    yaml_output += "# Path to the output PDF file for the lessons\n"
    yaml_output += f"output_file: ./output/sabbath_school_lesson_{year}_{quarter}_en.pdf\n"
    yaml_output += "# Path to the front cover SVG file\n"
    yaml_output += "front_cover_svg: ./assets/front_cover.svg\n"
    yaml_output += "# Path to the back cover SVG file\n"
    yaml_output += "back_cover_svg: ./assets/back_cover.svg\n"

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
    generate_template_config(output_path)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
