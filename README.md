# Sabbath School Lesson Downloader and PDF Generator

This project downloads Sabbath School lessons from the GitHub repository and generates a beautifully formatted PDF.

## Features

- YAML-based configuration for easy customization
- Automatic downloading of lesson content from GitHub
- Combines multiple files into a properly formatted markdown document
- Generates a professionally formatted PDF
- Support for custom cover SVGs

## Requirements

- Python 3.6+
- Dependencies: `pyyaml`, `requests`, `markdown`, `weasyprint`, `beautifulsoup4`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/SabbathSchool/sabbath-school-reproducer.git
cd sabbath-school-reproducer
```

2. Install dependencies:
```bash
pip install -e .
```

## Usage

1. Create or modify a configuration YAML file:
```yaml
year: 2025
quarter: q2
language: en
input_file: ./combined_lessons.md
output_file: ./output/sabbath_school_lessons_2025_q2.pdf
front_cover_svg: ./assets/front_cover.svg
back_cover_svg: ./assets/back_cover.svg
```

2. Run the script:
```bash
python main.py config.yaml
```

Or with debugging options:
```bash
python main.py config.yaml --debug            # Enable verbose logging
python main.py config.yaml --debug-html-only  # Only generate debug HTML without PDF
```

You can also use the shell script:
```bash
./bin/run.sh config.yaml
./bin/run.sh config.yaml --debug
./bin/run.sh config.yaml --debug-html-only
```

## Project Structure

- `main.py` - Main script entry point
- `config.py` - YAML configuration module
- `downloader.py` - Handles downloading content from GitHub
- `aggregator.py` - Combines downloaded content
- `processor.py` - Processes markdown content into structured data
- `generator/` - Package for PDF generation
  - `html_generator.py` - Generates HTML from structured data
  - `pdf_generator.py` - Converts HTML to PDF
  - `css_styles.py` - CSS styles for the PDF
  - `svg_updater.py` - Updates SVG covers with dynamic content
- `utils/` - Utility modules
  - `debug_tools.py` - Tools for debugging and inspecting content
- `bin/` - Command-line scripts
  - `run.sh` - Runner script
  - `generate_config.py` - Config generator

## Configuration Options

- `year` - Year of the lessons (e.g., 2025)
- `quarter` - Quarter (q1, q2, q3, or q4)
- `language` - Language code (e.g., en, es)
- `input_file` - Path to save the combined markdown file
- `output_file` - Path to save the generated PDF
- `front_cover_svg` - Path to front cover SVG (optional)
- `back_cover_svg` - Path to back cover SVG (optional)
- `title` - Title for the lesson quarterly (optional)
- `subtitle` - Subtitle for the lesson quarterly (optional)
- `publisher` - Publisher name (optional)

## GitHub Repository Structure

This script relies on the SabbathSchool/lessons GitHub repository structure:

```
/DECADE/YEAR/QUARTER/LANGUAGE/
  - contents.json
  - front-matter.md
  - back-matter.md
  - week-01.md
  - week-02.md
  - ...
```

Where:
- DECADE is formatted as, e.g., "1880s"
- YEAR is the full year, e.g., "2025"
- QUARTER is q1, q2, q3, or q4
- LANGUAGE is the language code, e.g., "en"

## Debugging Tools

The project includes several debugging tools to help troubleshoot issues:

1. **Debug HTML Generator**:
   ```bash
   python main.py config.yaml --debug-html-only
   ```
   This generates an interactive HTML file that shows each section of the combined markdown file with tabs for raw markdown and HTML preview.

2. **Section Extractor**:
   ```python
   from utils.debug_tools import DebugTools
   content = DebugTools.extract_section("combined_lessons.md", "front-matter.md")
   ```
   This extracts a specific section from the combined markdown file for closer inspection.

3. **Verbose Logging**:
   ```bash
   python main.py config.yaml --debug
   ```
   This enables detailed logging output during the download and processing steps.

## License

This project is licensed under the MIT License - see the LICENSE file for details.