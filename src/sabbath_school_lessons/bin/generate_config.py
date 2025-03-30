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
    year = 1905# now.year
    quarter = "q2" #f"q{(now.month - 1) // 3 + 1}"
    
    # Create a template configuration
    config = {
        "# Sabbath School Lesson Configuration": "",
        
        "# Year and quarter to download": "",
        "year": year,
        "quarter": quarter,
        "language": "en",
        
        "# File paths": "",
        "input_file": f"./combined_lessons_{year}_{quarter}.md",
        "output_file": f"./output/sabbath_school_lessons_{year}_{quarter}.pdf",
        
        "# Optional cover SVG files": "",
        "front_cover_svg": "./assets/front_cover.svg",
        "back_cover_svg": "./assets/back_cover.svg",
        
        "# PDF metadata": "",
        "title": "Sabbath School Lessons",
        "subtitle": f"Quarter {quarter[1]}, {year}",
        "publisher": "Gospel Sounders"
    }
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
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