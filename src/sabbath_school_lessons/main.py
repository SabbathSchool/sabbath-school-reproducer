#!/usr/bin/env python3
"""
Sabbath School Lesson Downloader and Generator

This script downloads lesson content from GitHub and generates a PDF.

Usage:
python3 main.py config.yaml [--debug] [--debug-html-only]
"""

import sys
import os
import argparse
import logging
from .config import Config
from .downloader import GitHubDownloader
from .aggregator import ContentAggregator
from .processor import MarkdownProcessor
from .generator.html_generator import HtmlGenerator
from .generator.pdf_generator import PdfGenerator
from .generator.svg_updater import SvgUpdater
from .utils.debug_tools import DebugTools


def main():
    """
    Main function that orchestrates the entire process
    """
    parser = argparse.ArgumentParser(description='Download and process Sabbath School lessons')
    parser.add_argument('config_file', nargs='?', help='Path to YAML configuration file')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode with verbose logging')
    parser.add_argument('--debug-html-only', action='store_true', help='Only generate debug HTML without PDF')
    parser.add_argument('--generate-config', action='store_true', help='Generate a sample config file and exit')
    parser.add_argument('--quiet-deps', action='store_true', help='Silence debug messages from dependencies')
    
    args = parser.parse_args()
    
    # Handle generate-config option
    if args.generate_config:
        from .bin.generate_config import generate_template_config
        config_path = generate_template_config()
        print(f"Sample configuration file generated at: {config_path}")
        return 0

    # Check if config file is provided when not generating a config
    if not args.config_file:
        parser.print_help()
        print("\nError: Config file is required unless using --generate-config")
        return 1
    
    # Configure logging based on debug flag
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    if args.quiet_deps:
        logging.getLogger('fontTools').setLevel(logging.WARNING)
        logging.getLogger('weasyprint').setLevel(logging.WARNING)
        logging.getLogger('fontTools.subset').setLevel(logging.WARNING)
        logging.getLogger('fontTools.ttLib.ttFont').setLevel(logging.WARNING)
        logging.getLogger('fontTools.subset.timer').setLevel(logging.WARNING)
    
    
    try:
        # Load configuration
        print(f"Loading configuration from {args.config_file}...")
        config = Config(args.config_file)
        
        # Generate GitHub paths
        github_paths = config.get_github_paths()
        print(f"Processing year {config['year']}, quarter {config['quarter']}, language {config['language']}")
        
        # Download lesson data
        print("Downloading lesson content from GitHub...")
        downloader = GitHubDownloader(github_paths)
        lesson_data = downloader.download_lesson_data()
        
        # Combine into a single markdown file
        print("Combining lesson content...")
        markdown_path = ContentAggregator.combine_lesson_content(lesson_data, config['input_file'])
        
        # Generate debug HTML if requested
        if args.debug_html_only:
            debug_html_path = config['output_file'].replace('.pdf', '_debug.html')
            debug_html_path = DebugTools.generate_debug_html(markdown_path, debug_html_path)
            print(f"Debug HTML created at: {debug_html_path}")
            return 0
        
        # Process the markdown file to extract structured content
        print("Processing markdown content...")
        content_data = MarkdownProcessor.process_markdown_file(markdown_path)
        
        # Update SVG files with dynamic content if available
        front_cover_path = config.get('front_cover_svg')
        back_cover_path = config.get('back_cover_svg')
        
        if front_cover_path:
            updated_front_cover = SvgUpdater.update_svg_with_config(front_cover_path, config, lesson_data, is_temporary=True)
            if updated_front_cover:
                front_cover_path = updated_front_cover
                print(f"Updated front cover SVG with dynamic content")
        
        if back_cover_path:
            updated_back_cover = SvgUpdater.update_svg_with_config(back_cover_path, config, lesson_data, is_temporary=True)
            if updated_back_cover:
                back_cover_path = updated_back_cover
                print(f"Updated back cover SVG with dynamic content")
        
        # Generate HTML
        print("Generating HTML...")
        html_content = HtmlGenerator.generate_html(
            content_data,
            front_cover_svg_path=front_cover_path,
            back_cover_svg_path=back_cover_path,
            config=config
        )
        print("Done Generating HTML...")
        
        # Save debug HTML
        debug_html_path = config['output_file'].replace('.pdf', '_debug.html')
        with open(debug_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Debug HTML saved to: {debug_html_path}")
        
        # Generate PDF
        print("Generating PDF...")
        PdfGenerator.generate_pdf(html_content, config['output_file'], config)
        print(f"PDF generation complete: {config['output_file']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())