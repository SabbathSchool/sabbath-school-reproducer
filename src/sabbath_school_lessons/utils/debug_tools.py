"""
Debug Tools for Sabbath School Lesson Downloader

This module provides tools to parse and debug the combined markdown file.
"""

import os
import re
import markdown
from bs4 import BeautifulSoup


class DebugTools:
    """Tools for debugging and inspecting markdown content."""
    
    @staticmethod
    def parse_file_sections(markdown_path):
        """
        Parse the combined markdown file into its component file sections
        
        Args:
            markdown_path (str): Path to the combined markdown file
            
        Returns:
            dict: Dictionary mapping file names to content
        """
        try:
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all file sections
            file_sections = re.findall(r'# File: ([^\n]+)[\r\n]+#-+[\r\n]+(.*?)(?=# File:|$)', content, re.DOTALL)
            
            result = {}
            for filename, section_content in file_sections:
                filename = filename.strip()
                result[filename] = section_content.strip()
            
            return result
        except Exception as e:
            print(f"Error parsing file: {e}")
            return {}

    @staticmethod
    def extract_section(markdown_path, section_name):
        """
        Extract a specific section from the combined markdown file
        
        Args:
            markdown_path (str): Path to the combined markdown file
            section_name (str): Name of the section to extract (e.g., 'front-matter.md')
            
        Returns:
            str or None: Content of the specified section, or None if not found
        """
        sections = DebugTools.parse_file_sections(markdown_path)
        
        # Try exact match first
        if section_name in sections:
            return sections[section_name]
        
        # Try partial match
        for filename in sections:
            if section_name in filename:
                return sections[filename]
        
        return None

    @staticmethod
    def generate_debug_html(markdown_path, output_path=None):
        """
        Generate a more sophisticated debug HTML from the combined markdown file
        
        Args:
            markdown_path (str): Path to the combined markdown file
            output_path (str, optional): Path to save the HTML file
            
        Returns:
            str: Path to the generated HTML file
        """
        if not output_path:
            output_path = markdown_path.replace('.md', '_debug.html')
        
        sections = DebugTools.parse_file_sections(markdown_path)
        
        # Generate HTML with collapsible sections
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '    <meta charset="utf-8">',
            '    <title>Debug View - ' + os.path.basename(markdown_path) + '</title>',
            '    <style>',
            '        body { font-family: Georgia, serif; margin: 2em; line-height: 1.5; }',
            '        .section { border: 1px solid #ddd; margin: 1em 0; border-radius: 4px; overflow: hidden; }',
            '        .section-header { background-color: #f5f1e6; padding: 0.8em; font-weight: bold; cursor: pointer; user-select: none; }',
            '        .section-header:hover { background-color: #ebe5d6; }',
            '        .section-content { padding: 1em; display: none; border-top: 1px solid #ddd; overflow-x: auto; }',
            '        .section-content.open { display: block; }',
            '        .section-content pre { margin: 0; white-space: pre-wrap; }',
            '        .section-content.html-preview { background-color: #f9f9f9; }',
            '        .tabs { display: flex; background-color: #f5f5f5; border-bottom: 1px solid #ddd; }',
            '        .tab { padding: 0.5em 1em; cursor: pointer; border-right: 1px solid #ddd; }',
            '        .tab.active { background-color: #fff; border-bottom: 2px solid #7d2b2b; }',
            '        h1, h2, h3 { color: #7d2b2b; }',
            '        .summary { background-color: #f9f7f1; padding: 1em; border-left: 3px solid #7d2b2b; margin-bottom: 1em; }',
            '    </style>',
            '</head>',
            '<body>',
            '    <h1>Debug View for Sabbath School Lessons</h1>',
            '    <p>This page shows the content of each file section from the combined markdown file.</p>',
            '    <div class="summary">',
            f'    <p><strong>Filename:</strong> {os.path.basename(markdown_path)}</p>',
            f'    <p><strong>Total sections:</strong> {len(sections)}</p>',
            '    </div>'
        ]
        
        # Add collapsible sections
        for filename, content in sections.items():
            # Convert markdown to HTML for preview
            html_preview = markdown.markdown(content)
            
            section_html = f"""
        <div class="section">
            <div class="section-header" onclick="toggleSection(this.parentNode)">
                {filename}
            </div>
            <div class="tabs">
                <div class="tab active" onclick="switchTab(this, 'raw')">Raw Markdown</div>
                <div class="tab" onclick="switchTab(this, 'html')">HTML Preview</div>
            </div>
            <div class="section-content raw open">
                <pre>{content}</pre>
            </div>
            <div class="section-content html-preview html">
                {html_preview}
            </div>
        </div>
            """
            html_parts.append(section_html)
        
        # Add JavaScript for interaction
        html_parts.extend([
            '    <script>',
            '        function toggleSection(section) {',
            '            const content = section.querySelector(".section-content.open");',
            '            if (content) {',
            '                content.classList.toggle("open");',
            '            }',
            '        }',
            '        function switchTab(tab, type) {',
            '            const section = tab.closest(".section");',
            '            const tabs = section.querySelectorAll(".tab");',
            '            const contents = section.querySelectorAll(".section-content");',
            '            ',
            '            // Deactivate all tabs and hide all contents',
            '            tabs.forEach(t => t.classList.remove("active"));',
            '            contents.forEach(c => c.classList.remove("open"));',
            '            ',
            '            // Activate selected tab and show corresponding content',
            '            tab.classList.add("active");',
            '            section.querySelector(`.section-content.${type}`).classList.add("open");',
            '        }',
            '    </script>',
            '</body>',
            '</html>'
        ])
        
        # Write HTML to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_parts))
        
        return output_path