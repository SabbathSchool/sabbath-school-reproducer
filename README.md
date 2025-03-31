# 📚 Sabbath School Lessons Reproducer

A tool to download, format, and reproduce Sabbath School lessons from historical archives for modern use.

[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://sabbathschool.github.io/sabbath-school-reproducer/)
[![PyPI version](https://img.shields.io/pypi/v/sabbath-school-reproducer.svg)](https://pypi.org/project/sabbath-school-reproducer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 📝 YAML-based configuration for easy customization
- 🔄 Automatic downloading of lesson content from GitHub repositories
- 🕰️ Reproduction mode for adapting historical lessons to current dates
- 📑 Professionally formatted PDF generation with customizable styling
- 🎨 Support for custom cover designs
- 🌐 Comprehensive multi-language support (English, Swahili, Luo) with user-modifiable translations

## 🔧 Requirements

- Python 3.6+
- Dependencies: `pyyaml`, `requests`, `markdown`, `weasyprint`, `beautifulsoup4`

## 💻 Installation

### From PyPI

```bash
pip install sabbath-school-reproducer
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/sabbathschool/sabbath-school-reproducer.git
cd sabbath-school-reproducer
```

2. Install the package:
```bash
pip install -e .
```

## 🚀 Quick Start

1. Initialize with default templates and configuration:
```bash
sabbath-school-reproducer init
```

2. Edit the generated `config.yaml` file with your desired settings

3. Run the tool with your configuration:
```bash
sabbath-school-reproducer run config.yaml
```

## 📖 Usage

```
sabbath-school-reproducer [-h] {init,run} ...

Download and process Sabbath School lessons

options:
  -h, --help     show this help message and exit

Commands:
  {init,run}
    init         Initialize the environment with default settings
    run          Run a lesson configuration
```

### 🔰 Init Command

Generate template files and default configuration:

```bash
sabbath-school-reproducer init
```

This will create:
- A default `config.yaml` file
- Language files for all supported languages in the `languages` directory
- A color theme file in the `themes` directory

### ▶️ Run Command

Process a configuration file and generate PDF:

```bash
sabbath-school-reproducer run config.yaml [options]
```

Options:
- `--debug` - Enable debug mode with verbose logging
- `--debug-html-only` - Only generate debug HTML without PDF
- `--quiet-deps` - Silence debug messages from dependencies
- `-y, --yes` - Answer yes to all prompts (force overwrite)

## ⚙️ Configuration Options

Create a YAML configuration file with the following options:

```yaml
# Target output options
year: 2025              # Year for generated lessons
quarter: q2             # Quarter (q1, q2, q3, q4)
language: en            # Language code (en, sw, luo)

# File paths
input_file: ./combined_lessons_2025_q2_en_1_null.md   # Path for intermediate markdown file
output_file: ./output/sabbath_school_lesson_2025_q2_en.pdf  # Final PDF path

# Optional cover SVG files
front_cover_svg: ./assets/front_cover.svg   # Custom front cover
back_cover_svg: ./assets/back_cover.svg     # Custom back cover

# Color theme
color_theme_path: ./themes/burgundy.yaml    # Custom color theme

# Language configuration
language_config_path: ./languages/en.yaml   # Language-specific translations

# Reproduction options
reproduce:
  # Original content to adapt
  year: 1905            # Historical year to source from
  quarter: q2           # Historical quarter to source from
  
  # Lesson selection
  start_lesson: 1       # First lesson to include (starting from 1)
  stop_lesson: 13       # Last lesson to include (or null for all)
  
  # New date assignment
  quarter_start_date: 2025-04-01  # First lesson date (YYYY-MM-DD)

# PDF metadata
title: Sabbath School Lessons      # Title for the lesson quarterly
subtitle: Quarter 2, 2025          # Subtitle
publisher: Gospel Sounders         # Publisher name
```

## 🔄 Reproduction Mode

The reproduction feature allows you to adapt historical Sabbath School lessons for modern use:

1. Source lessons from a specific historical year and quarter
2. Start from any lesson number (e.g., lesson 5)
3. Set a limit for the number of lessons to include
4. Apply modern dates starting from a specified date
5. Generate a PDF that uses current dates while attributing the source material

Example reproduction configuration:
```yaml
reproduce:
  year: 1888            # Source from 1888
  quarter: q3           # Third quarter
  start_lesson: 3       # Start from lesson 3
  stop_lesson: 10       # Include up to lesson 10
  quarter_start_date: 2025-04-01  # Use dates starting April 1, 2025
```

## 🌐 Multi-language Support

The tool provides comprehensive support for multiple languages:

### Supported Languages

- English (en)
- Swahili (sw)
- Luo (luo)

### Language Configuration

The language configuration files are generated in the `languages` directory when you run the `init` command. You can customize translations by editing these files:

```yaml
# Language configuration for sw (Swahili)
# This file contains language-specific translations

# Basic terms
notes: 'MAELEZO'  # Used for section headers and headings
note: 'ELEZO'     # Used for single-note sections
questions: 'MASWALI'  # Questions section header
answer_prefix: 'Jibu'  # Prefix for answers in questions
lesson: 'SOMO'  # Used for lesson titles

# Cover page terms
sabbath_school: 'SHULE YA SABATO'  # Main title on cover page
lessons: 'MASOMO'  # Secondary title on cover page
adapted_from: 'Imetoholewa kutoka'  # Text used in "Adapted from X" on cover
from_text: 'kutoka'  # Text used in "from X" in titles

# Quarter names (used in headings and footers)
quarter_names:
  q1: 'ROBO YA KWANZA'
  q2: 'ROBO YA PILI'
  q3: 'ROBO YA TATU'
  q4: 'ROBO YA NNE'

# Quarter month ranges (used in cover pages)
quarter_months:
  q1: 'Januari - Machi'
  q2: 'Aprili - Juni'
  q3: 'Julai - Septemba'
  q4: 'Oktoba - Desemba'

# Table of contents translations
table_of_contents: 'YALIYOMO'
lesson_column: 'Somo'
title_column: 'Kichwa'
date_column: 'Tarehe'
page_column: 'Ukurasa'

# Month names for date formatting
month_names:
  - 'Januari'
  - 'Februari'
  # ... other months

# Date format template
date_format_template: '{day} {month}, {year}'
```

### Using Different Languages

To generate lessons in a specific language:

1. Set the `language` field in your config.yaml file (e.g., `language: sw` for Swahili)
2. Ensure the corresponding language file exists (e.g., `languages/sw.yaml`)
3. Run the tool with your configuration

The tool will automatically:
- Use the correct language when downloading lessons
- Apply language-specific formatting to dates
- Use translated text for all UI elements and headers
- Format the cover page with proper translations

## 🔍 Advanced Usage

### 🐞 Debug Mode

Run with debug output for more detailed information:
```bash
sabbath-school-reproducer run config.yaml --debug
```

### 🌐 Debug HTML Only

Generate only the debug HTML without PDF generation:
```bash
sabbath-school-reproducer run config.yaml --debug-html-only
```

### ⚡ Force Overwrite

Skip confirmation prompts when overwriting existing files:
```bash
sabbath-school-reproducer run config.yaml -y
```

### 🎨 Custom CSS

You can customize the PDF styling by modifying the CSS in your project:
```python
# In css_styles.py
CSS_TEMPLATE = """
/* Your custom CSS here */
"""
```

## 📚 Documentation

The project documentation is available at [https://sabbathschool.github.io/sabbath-school-reproducer/](https://sabbathschool.github.io/sabbath-school-reproducer/).

To build the documentation locally:

```bash
# Navigate to docs directory
cd docs

# Build the documentation
make html

# View the documentation
# Open docs/_build/html/index.html in your browser
```

## 👨‍💻 Development

### 🔢 Version Control

The project includes an automated version checker that increments the version number when building:

```bash
./build.sh
```

### 🧪 Testing

Run tests with:

```bash
pytest tests/
```

### 📦 Building and Publishing

To build the package:

```bash
# Clean and build
./build.sh
```

To upload to PyPI:

```bash
# Upload to PyPI
./upload.sh
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Steps to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.