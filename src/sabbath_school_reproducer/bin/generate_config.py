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
    yaml_output += f"output_file: ./output/sabbath_school_lesson_{year}_{quarter}_en.pdf\n"
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
    
    # Generate the configuration file (won't overwrite existing files)
    generate_template_config(output_path)
    
    # Always ensure we have the default theme
    generate_default_theme()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())