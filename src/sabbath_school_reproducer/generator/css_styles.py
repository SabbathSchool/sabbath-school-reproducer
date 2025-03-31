"""
CSS Styles for Sabbath School Lessons PDF

This module defines the CSS styles used in the generated PDF.
"""
from sabbath_school_reproducer.generator.css_editor import  CSSEditor
import re
import os
import yaml
from sabbath_school_reproducer.utils.language_utils import  LanguageConfig


CSS_TEMPLATE = """
/* Main styling for Sabbath School Lessons */
body {
    font-family: Georgia, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #3c1815;
    margin: 0;
    padding: 0;
    counter-reset: counter;
}

@page sectionbreak {
    counter-reset: counter;
}
.sectionbreak {
    page: sectionbreak;
    page-break-after: always;
    page-break-before: always;
    counter-reset: page 0;
}
.sectionbreaknone {
    counter-reset: page 0;
    counter-reset: page;
    counter-reset: counter;
    display:block;
}

@page {
    size: letter;
    margin: 0; /*0 for coverpages. Then set for the other sections separately*/
    /*margin: 0.75in;*/
}

@page :first {
    margin: 0;
    @bottom-center { content: ""; }
    @bottom-left { content: ""; }
    @bottom-right { content: ""; }
}

/* Frontmatter pages with counter explicitly reset to 1 */
@page frontmatter {
    margin: 0.75in;
    @bottom-center {
        content: counter(page, lower-roman);
        font-family: Georgia, serif;
        font-size: 12pt;
        color: #5a4130;
    }
    @bottom-left {
        content: "Quarter 2 2025"; /*Needs to be dynamically changed*/
        font-family: Georgia, serif;
        font-size: 10pt;
        color: #5a4130;
    }
    @bottom-right {
        content: "Topical Studies on the Message"; /*Needs to be dynamically changed*/
        font-family: Georgia, serif;
        font-size: 10pt;
        color: #5a4130;
    }
}

@page frontmatter:first {
    margin: 0;
    @bottom-center { content: ""; }
    @bottom-left { content: ""; }
    @bottom-right { content: ""; }
}

/* Mainmatter pages with counter explicitly reset to 1 */
@page mainmatter {
    margin: 0.75in;
    @bottom-center {
        content: counter(page);
        font-family: Georgia, serif;
        font-size: 12pt;
        color: #5a4130;
    }
    @bottom-left {
        content: "Quarter 2 2025";
        font-family: Georgia, serif;
        font-size: 10pt;
        color: #5a4130;
    }
    @bottom-right {
        content: "Topical Studies on the Message";
        font-family: Georgia, serif;
        font-size: 10pt;
        color: #5a4130;
    }
}

@page :last {
    margin: 0;
    @bottom-center { content: ""; }
    @bottom-left { content: ""; }
    @bottom-right { content: ""; }
}

/* Explicitly define counter reset points in the document flow */
.frontmatter-container {
    page: frontmatter;
    counter-reset: page 1;
}

.mainmatter-container {
    page: mainmatter;
    counter-reset: page 1;
}

/* Cover page styling - Full page with no margins */
.cover-page {
    position: relative;
    width: 100%;
    height: 100vh;
    page-break-after: always;
    margin: 0;
    padding: 0;
}

.cover-page svg {
    width: 100%;
    height: 100%;
    display: block;
}

/* Fix for blank page after cover */
.blank-page {
    height: 100vh;
    width: 100%;
    page-break-after: always;
}

/* Front matter styling */
.front-matter {
    page: frontmatter;
    counter-reset: page 1;
    margin-top: 2em;
}

.front-matter h1 {
    font-size: 24pt;
    text-align: center;
    margin-bottom: 1em;
    color: #7d2b2b;
}

.front-matter h2 {
    font-size: 18pt;
    margin-top: 1.5em;
    color: #5a4130;
}

.front-matter p {
    margin-bottom: 1em;
}

/* Table of Contents styling */
.toc-title {
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    margin: 20px 0;
    color: #3c1815;
}

.toc-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 2em;
}

.toc-table tr.header {
    font-weight: bold;
    border-bottom: 2px solid #8b4513;
}

.toc-table td {
    padding: 8px 5px;
    vertical-align: top;
}

.toc-table tr:not(.header) {
    border-bottom: 1px dotted #d4c7a5;
}

.toc-table a {
    color: #3c1815;
    text-decoration: none;
}

/* Lesson Header styling */
.lesson-header {
    background-color: #f5f1e6;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid #8b4513;
    position: relative;
    height: 100px;
}

.lesson-circle {
    position: absolute;
    top: 20px;
    left: 20px;
    width: 80px;
    height: 80px;
    background-color: #e0d5c0;
    border: 2px solid #8b4513;
    border-radius: 50%;
    text-align: center;
    line-height: 80px;
    font-size: 40px;
    font-weight: bold;
    color: #3c1815;
}

.lesson-title {
    position: absolute;
    top: 40px;
    left: 120px;
    font-size: 24pt;
    font-weight: bold;
    color: #3c1815;
}

.lesson-date {
    position: absolute;
    top: 20px;
    left: 120px;
    font-size: 12pt;
    font-style: italic;
    color: #5a4130;
}

.corner {
    position: absolute;
    width: 15px;
    height: 15px;
    background-color: #8b4513;
}

.top-left {
    top: 0;
    left: 0;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
}

.top-right {
    top: 0;
    right: 0;
    border-top-left-radius: 10px;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
}

.bottom-left {
    bottom: 0;
    left: 0;
    border-top-right-radius: 10px;
    border-top-left-radius: 10px;
    border-bottom-right-radius: 10px;
}

.bottom-right {
    bottom: 0;
    right: 0;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-left-radius: 10px;
}

.preliminary-note {
    font-style: italic;
    margin-bottom: 5px;
    padding: 10px 20px;
    background-color: #f9f7f1;
    border-left: 3px solid #8b4513;
    page-break-inside: avoid;
    page-break-before: avoid;
}

.questions-section {
    display:block;
    border: 1px solid #8b4513;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 12px;
    page-break-before: auto;
    page-break-inside: auto; /* Allow breaks within paragraphs */
    orphans: 1; /* Allow at least one question to appear with header */
    widows: 1; /* Allow at least one question at the bottom of a page */
}

.questions-section .question:first-of-type {
    page-break-before: avoid; /* Keep first question with header */
    page-break-inside: avoid; /* Keep first question intact */
    page-break-after: auto; /* Allow a page break after first question */
}

/* The clearfix shouldn't force breaks */
.clearfix {
    clear: both;
    page-break-before: auto;
    page-break-after: auto;
}

.questions-header {
    font-size: 14pt;
    font-weight: bold;
    margin-bottom: 10px;
    border-bottom: 1px solid #8b4513;
    padding-bottom: 5px;
}

.question {
    margin-bottom: 3px;
    position: relative;
    clear: both;
    page-break-inside: avoid;
}

.question-number {
    font-weight: bold;
    float: left;
    text-align: right;
    padding-right: 8px;
}

.question-number.one-digit {
    width: 20px;
}

.question-number.two-digit {
    width: 30px;
}

.question-text {
    margin-left: 30px; /* Minimum margin for one-digit numbers */
    text-align: left;
    position: relative;
    break-inside: auto;
    page-break-inside: auto;
}

/* For two-digit question numbers */
.two-digit + .question-text {
    margin-left: 40px; /* Increased margin for two-digit numbers */
}

.scripture-ref {
    float: right;
    color: #5a4130;
    font-style: italic;
    margin-left: 10px;
    text-align: right;
    page-break-before: avoid; /*keep with question*/
}

.scripture-ref p {
    margin: 0;  
    padding: 0; 
}

.answer {
    margin-top: 1px;
    color: #5a4130;
    clear: right; /* Ensure answer appears below the scripture reference */
}

.notes-section {
    background-color: #f9f7f1;
    border: 1px solid #8b4513;
    padding: 20px;
}

.notes-header {
    font-size: 16pt;
    font-weight: bold;
    margin-bottom: 15px;
    page-break-after: avoid;
}

.notes-content p:first-letter {
    font-variant: small-caps;
}

.notes-content p {
    text-indent: 1.5em;
    margin-bottom: 1em;
}

/* Keep first paragraph with header */
.notes-content p:first-child {
    page-break-before: avoid; /* Keep with header */
}

/* Allow breaks within other paragraphs */
.notes-content p {
    page-break-inside: auto; /* Allow breaks within paragraphs */
    orphans: 1; /* At least 1 lines at top of page */
    widows: 1; /* At least 1 lines at bottom of page */
    text-align: justify;
}

.clearfix {
    clear: both;
}

/* Back matter styling */
@page :last {
    margin: 0;
    @bottom-center { content: ""; }
    @bottom-left { content: ""; }
    @bottom-right { content: ""; }
}

/* Back cover styling */
.back-cover-page {
    position: relative;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100vh;
    margin: 0;
    padding: 0;
    page: :last;
}

@page :last {
    margin: 0;
    @bottom-center { content: ""; }
    @bottom-left { content: ""; }
    @bottom-right { content: ""; }
}
.back-cover-page svg {
    position: relative;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: block;
}

/* Table styling */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-family: Georgia, serif;
    font-size: 12pt;
}

table, th, td {
    border: 1px solid #8b4513;
}

thead {
    background-color: #f5f1e6;
}

th {
    color: #3c1815;
    font-weight: bold;
    text-align: left;
    padding: 8px 12px;
}

td {
    padding: 8px 12px;
    vertical-align: top;
}

tr:nth-child(even) {
    background-color: #f9f7f1;
}

/* Special styling for price tables */
table.price-table td:nth-child(2) {
    text-align: center;
    width: 80px;
}

/* Table caption styling */
table caption {
    font-style: italic;
    margin-bottom: 8px;
    color: #5a4130;
    text-align: left;
    caption-side: top;
}

.toc-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}

.toc-header, .toc-row {
    display: flex;
    margin-bottom: 5px;
}

.toc-header-cell, .toc-cell {
    padding: 5px;
    border: 1px solid #ddd;
    text-align: left;
    display: inline-block;
}

.toc-header-cell {
    font-weight: bold;
    background-color: #f4f4f4;
}

.toc-cell-number {
    width: 40px;
    text-align: center;
}

.toc-cell-title {
    flex: 1;
}

.toc-cell-date {
    width: 100px;
    text-align: center;
}

.toc-cell-page {
    width: 40px;
    text-align: right;
}

/* Style for the link */
.toc-link {
    display: block; /* Make the <a> tag a block element to cover the entire row */
    text-decoration: none; /* Remove underline */
    color: inherit; /* Inherit color from the row */
}

/* Highlight the row when hovered */
.toc-link:hover .toc-row {
    background-color: #f0f0f0;
}

/* Style the link inside the cells (optional) */
.toc-cell a {
    text-decoration: none;
    color: #007bff;
}

.toc-cell a:hover {
    text-decoration: underline;
}

.sectionbreaknone {
    page-break-after: always;
}

.additional-section {
    border: 1px solid #6a4e23; /* Darker border color for additional section */
    margin-bottom: 20px;
    padding: 20px;
    background-color: #f0e5d8; /* Lighter background color for differentiation */
    page-break-before: auto;
    border-radius: 8px;
}

/* Header styling for additional sections */
.additional-header {
    font-size: 18pt;
    font-weight: bold;
    color: #4b3b2f; /* Darker brown for the header text */
    margin-bottom: 10px;
    border-bottom: 3px solid #6a4e23; /* A stronger border below the header */
    padding-bottom: 5px;
    text-align: left;
    font-family: 'Georgia', serif; /* Different font family for header */
}

/* Content styling for the additional sections */
.additional-content {
    font-size: 12pt;
    line-height: 1.5;
    color: #4b3b2f; /* Darker brown text */
    text-align: justify; /* Justified text for a clean look */
    margin-top: 10px;
    font-family: 'Georgia', serif; /* Different font family for content */
}

/* Optional: First paragraph inside the additional content */
.additional-content p:first-child {
    margin-top: 0;
}

/* Style for hyperlinks in additional sections */
.additional-content a {
    color: #4b3b2f; /* Dark brown for links */
    text-decoration: underline;
}

.additional-content a:hover {
    color: #6a4e23; /* Change to a lighter brown when hovering */
    text-decoration: none;
}

/* Optional: Add specific spacing between paragraphs for clarity */
.additional-content p {
    margin-bottom: 1em;
}

/* Optional: Style for lists inside the additional section */
.additional-content ul,
.additional-content ol {
    margin-left: 1.5em;
    margin-bottom: 1em;
}

.additional-content li {
    margin-bottom: 0.5em;
}


@media print {
    .lesson-title {
        font-size: 20pt;
    }
}
"""

class CssUpdater:
    """Handles CSS style updates with dynamic content based on configuration."""
    
    @staticmethod
    def get_quarter_display(config):
        """
        Get the formatted quarter and year display
        
        Args:
            config (dict): Configuration dictionary
            
        Returns:
            str: Formatted quarter display
        """
        try:
            year = config['year']
            quarter = config['quarter']
            language_code = config.get('language', 'en')
            
            # Get the localized quarter name
            quarter_name = LanguageConfig.get_translation(
                language_code,
                f'quarter_names.{quarter.lower()}',
                f"Quarter {quarter[1] if quarter.startswith('q') or quarter.startswith('Q') else ''}"
            )
            
            # Format as "Quarter X YYYY" based on language
            return f"{quarter_name}, {year}"
        except (KeyError, ValueError):
            # Default if config is missing
            return "Quarter & Year"
    
    @staticmethod
    def load_color_theme(theme_path):
        """
        Load color theme from a YAML file
        
        Args:
            theme_path (str): Path to the color theme YAML file
            
        Returns:
            dict: Color theme dictionary or None if file not found
        """
        if not theme_path or not os.path.exists(theme_path):
            return None
            
        try:
            with open(theme_path, 'r') as file:
                return yaml.safe_load(file)
        except (yaml.YAMLError, IOError) as e:
            print(f"Error loading color theme: {e}")
            return None
    
    @staticmethod
    def apply_color_theme(css_template, color_theme):
        """
        Apply color theme to CSS template
        
        Args:
            css_template (str): Original CSS template string
            color_theme (dict): Color theme dictionary
            
        Returns:
            str: Updated CSS template with applied color theme
        """
        if not css_template or not color_theme:
            return css_template
            
        updated_css = css_template
        
        # Define color mappings from theme to CSS
        color_mappings = {
            # Text colors
            "#3c1815": color_theme["text"]["primary"],
            "#5a4130": color_theme["text"]["secondary"],
            "#7d2b2b": color_theme["text"]["accent"],
            "#007bff": color_theme["text"]["link"],
            
            # Background colors
            "#f9f7f1": color_theme["background"]["light"],
            "#f5f1e6": color_theme["background"]["medium"],
            "#e0d5c0": color_theme["background"]["dark"],
            "#f0e5d8": color_theme["background"]["additional"],
            "#f4f4f4": color_theme["background"]["tableHeader"],
            "#f0f0f0": color_theme["background"]["hover"],
            
            # Border colors
            "#8b4513": color_theme["border"]["primary"],
            "#d4c7a5": color_theme["border"]["secondary"],
            "#6a4e23": color_theme["border"]["additional"],
            "#ddd": color_theme["border"]["table"],
            
            # Accent colors
            "#4b3b2f": color_theme["accent"]["secondary"],
            "#696969": color_theme["accent"]["tertiary"],
            "#808080": color_theme["accent"]["quaternary"]
        }
        
        # Apply each color mapping
        for original_color, new_color in color_mappings.items():
            # Escape the hash character for regex
            original_color_escaped = original_color.replace('#', r'\#')
            updated_css = re.sub(
                original_color_escaped,
                new_color,
                updated_css
            )
        
        return updated_css
    
    @staticmethod
    def update_css_template(css_template, config, lesson_data=None):
        """
        Update CSS template with configuration data and color theme
        
        Args:
            css_template (str): Original CSS template string
            config (dict): Configuration dictionary
            lesson_data (dict, optional): Optional lesson data dictionary
            
        Returns:
            str: Updated CSS template string
        """
        if not css_template:
            return css_template
        
        try:
            # Get language code
            language_code = config.get('language', 'en')
            
            # Get quarter display for footer
            quarter_display = CssUpdater.get_quarter_display(config)
            
            # Get lesson title for footer
            reproduce = config.get("reproduce", {})
            year_orig = reproduce.get("year", 2025)  # Default to 2025 if 'year' is not found
            quarter_orig = reproduce.get("quarter", "q1") 
            
            # Get title from config or generate a default
            lesson_title = config.get("lesson_title", CSSEditor.get_lesson_title(year_orig, quarter_orig))

            # Update CSS footer content
            updated_css = css_template
            
            # Update quarter display in footers
            updated_css = re.sub(
                r'content: "Quarter \d+ \d+";',
                f'content: "{quarter_display}";',
                updated_css
            )
            
            # Update lesson title in footers
            updated_css = re.sub(
                r'content: "Topical Studies on the Message";',
                f'content: "{lesson_title}";',
                updated_css
            )
            
            # Apply color theme if specified
            color_theme_path = config.get("color_theme_path")
            if color_theme_path:
                color_theme = CssUpdater.load_color_theme(color_theme_path)
                if color_theme:
                    updated_css = CssUpdater.apply_color_theme(updated_css, color_theme)
            
            # Update language-specific labels
            if language_code != 'en':
                # Replace "NOTES" with translated version
                notes_label = LanguageConfig.get_translation(language_code, 'notes', 'NOTES')
                updated_css = re.sub(
                    r'\.notes-header.*?{[^}]*content:\s*["\']NOTES["\']',
                    f'.notes-header{{content: "{notes_label}"',
                    updated_css
                )
                
                # Replace "NOTE" with translated version
                note_label = LanguageConfig.get_translation(language_code, 'note', 'NOTE')
                updated_css = re.sub(
                    r'\.note-header.*?{[^}]*content:\s*["\']NOTE["\']',
                    f'.note-header{{content: "{note_label}"',
                    updated_css
                )
                
                # Replace "TABLE OF CONTENTS" with translated version
                toc_label = LanguageConfig.get_translation(language_code, 'table_of_contents', 'TABLE OF CONTENTS')
                updated_css = re.sub(
                    r'\.toc-title.*?{[^}]*content:\s*["\']TABLE OF CONTENTS["\']',
                    f'.toc-title{{content: "{toc_label}"',
                    updated_css
                )
            
            return updated_css
            
        except Exception as e:
            print(f"Error updating CSS template: {e}")
            return css_template