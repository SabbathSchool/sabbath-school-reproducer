"""
CSS Styles for Sabbath School Lessons PDF

This module defines the CSS styles used in the generated PDF.
"""

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
}

.questions-section {
    border: 1px solid #8b4513;
    padding: 20px;
    margin-bottom: 20px;
    display: block;
}

.questions-header {
    font-size: 14pt;
    font-weight: bold;
    margin-bottom: 10px;
    border-bottom: 1px solid #8b4513;
    padding-bottom: 5px;
}

.question {
    margin-bottom: 5px;
    position: relative;
    clear: both;
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
            quarter = config['quarter'].upper()
            
            # Format as "Quarter X YYYY"
            quarter_num = quarter[1] if quarter.startswith('Q') and len(quarter) >= 2 else ''
            return f"Quarter {quarter_num} {year}"
        except (KeyError, ValueError):
            # Default if config is missing
            return "Quarter & Year"
    
    @staticmethod
    def update_css_template(css_template, config, lesson_data=None):
        """
        Update CSS template with configuration data
        
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
            import re
            
            # Get quarter display for footer
            quarter_display = CssUpdater.get_quarter_display(config)
            
            # Get lesson title for footer
            lesson_title = "Sabbath School Lessons"
            if 'title' in config:
                lesson_title = config['title']
            elif lesson_data and 'front_matter' in lesson_data:
                title_match = re.search(r'(?:^|\n)#\s+(.*?)(?:\n|$)', lesson_data['front_matter'])
                if title_match:
                    lesson_title = title_match.group(1).strip()
            
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
            
            return updated_css
            
        except Exception as e:
            print(f"Error updating CSS template: {e}")
            return css_template