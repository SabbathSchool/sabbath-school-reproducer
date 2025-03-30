"""
Dynamic SVG Updater for Sabbath School Lessons

This module updates SVG files with dynamic content based on configuration.
"""

import re
import os
import tempfile
from datetime import datetime


class SvgUpdater:
    """Updates SVG files with dynamic content based on configuration."""
    
    # Quarter mapping
    QUARTER_NAMES = {
        'q1': 'FIRST QUARTER',
        'q2': 'SECOND QUARTER',
        'q3': 'THIRD QUARTER',
        'q4': 'FOURTH QUARTER'
    }
    
    # Month ranges for quarters
    QUARTER_MONTHS = {
        'q1': 'January - March',
        'q2': 'April - June',
        'q3': 'July - September',
        'q4': 'October - December'
    }
    
    @staticmethod
    def get_quarter_title(config, lesson_data):
        """
        Get the quarter title from either config or lesson data
        
        Args:
            config (dict): Configuration dictionary
            lesson_data (dict): Lesson data dictionary
            
        Returns:
            str: Quarter title
        """
        # Try to get title from lesson data's front matter
        title = None
        if lesson_data and 'front_matter' in lesson_data:
            title_match = re.search(r'(?:^|\n)#\s+(.*?)(?:\n|$)', lesson_data['front_matter'])
            if title_match:
                title = title_match.group(1).strip()
        
        # If not found, use a default based on the first lesson title
        if not title and lesson_data and 'lessons' in lesson_data:
            first_lesson = None
            for week_id in sorted(lesson_data['lessons'].keys()):
                first_lesson = lesson_data['lessons'][week_id]
                break
                
            if first_lesson and 'title' in first_lesson:
                title = f"Topical Studies on {first_lesson['title']}"
        
        # If still not found, use default
        if not title:
            title = "Sabbath School Lessons"
        
        return title

    @staticmethod
    def update_svg_with_config(svg_path, config, lesson_data=None, is_temporary=False):
        """
        Update SVG file with configuration data
        
        Args:
            svg_path (str): Path to SVG file
            config (dict): Configuration dictionary
            lesson_data (dict, optional): Optional lesson data dictionary
            is_temporary (bool): Whether this is a temporary file
            
        Returns:
            str: Path to updated SVG file
        """
        return
        if not svg_path or not os.path.exists(svg_path):
            return None
            
        try:
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            
            # Get quarter information - use the target year/quarter for display
            year = config['year']
            quarter = config['quarter']
            quarter_name = SvgUpdater.QUARTER_NAMES.get(quarter, 'QUARTER')
            month_range = SvgUpdater.QUARTER_MONTHS.get(quarter, '')
            
            # Get title
            title = SvgUpdater.get_quarter_title(config, lesson_data)
            
            # Check if this is a reproduction
            is_reproduction = 'reproduce' in config and config['reproduce'].get('year')
            
            # If reproduction, append source info to title
            if is_reproduction:
                source_year = config['reproduce']['year']
                source_quarter = config['reproduce']['quarter']
                source_quarter_name = SvgUpdater.QUARTER_NAMES.get(source_quarter, 'QUARTER')
                
                # Only append if not already customized
                if not config.get("title"):
                    title += f" (from {source_year} {source_quarter_name})"
            
            # Replace relevant text in SVG
            # Update quarter info
            svg_content = re.sub(
                r'<text[^>]*>\s*(?:FIRST|SECOND|THIRD|FOURTH)\s+QUARTER,\s*\d{4}\s*</text>',
                f'<text x="400" y="810" font-family="Georgia, serif" font-size="22" font-weight="bold" text-anchor="middle" fill="#7d2b2b">{quarter_name}, {year}</text>',
                svg_content
            )
            
            # Update month range
            svg_content = re.sub(
                r'<text[^>]*>\s*(?:January|April|July|October)\s+-\s+(?:March|June|September|December)\s+\d{4}\s*</text>',
                f'<text x="400" y="840" font-family="Georgia, serif" font-size="18" text-anchor="middle" fill="#7d2b2b">{month_range} {year}</text>',
                svg_content
            )
            
            # Update title if it exists in SVG
            if title:
                # For "TOPICAL STUDIES" or similar main title lines
                svg_content = re.sub(
                    r'<text[^>]*>TOPICAL STUDIES</text>',
                    f'<text x="400" y="170" font-family="Georgia, serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#7d2b2b">{title.upper()}</text>',
                    svg_content
                )
                
                # For "ON THE MESSAGE" or similar subtitle lines
                # Only if title is longer than one line, split it
                title_parts = title.split(' ', 3)
                if len(title_parts) > 3:
                    first_line = ' '.join(title_parts[:3])
                    second_line = ' '.join(title_parts[3:])
                    
                    # Replace first line
                    svg_content = re.sub(
                        r'<text[^>]*>TOPICAL STUDIES</text>',
                        f'<text x="400" y="170" font-family="Georgia, serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#7d2b2b">{first_line.upper()}</text>',
                        svg_content
                    )
                    
                    # Replace second line
                    svg_content = re.sub(
                        r'<text[^>]*>ON THE MESSAGE</text>',
                        f'<text x="400" y="230" font-family="Georgia, serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#7d2b2b">{second_line.upper()}</text>',
                        svg_content
                    )
            
            # Add source attribution if this is a reproduction
            if is_reproduction:
                source_year = config['reproduce']['year']
                source_quarter = config['reproduce']['quarter']
                source_quarter_name = SvgUpdater.QUARTER_NAMES.get(source_quarter, 'QUARTER')
                
                # Check if there's already a source attribution
                attribution_pattern = r'<text[^>]*>\s*Adapted from.*\s*</text>'
                attribution_text = f'<text x="400" y="870" font-family="Georgia, serif" font-size="16" text-anchor="middle" font-style="italic" fill="#666666">Adapted from {source_quarter_name}, {source_year}</text>'
                
                if re.search(attribution_pattern, svg_content):
                    # Replace existing attribution
                    svg_content = re.sub(attribution_pattern, attribution_text, svg_content)
                else:
                    # Add new attribution before closing svg tag
                    svg_content = svg_content.replace('</svg>', f'{attribution_text}\n</svg>')
            
            # Write to a new file if temporary, otherwise update in place
            if is_temporary:
                temp_svg = tempfile.NamedTemporaryFile(suffix='.svg', delete=False)
                temp_svg_path = temp_svg.name
                with open(temp_svg_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                return temp_svg_path
            else:
                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                return svg_path
                
        except Exception as e:
            print(f"Error updating SVG {svg_path}: {e}")
            return None