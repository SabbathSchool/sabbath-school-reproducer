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
    
    This function handles command-line arguments, loads configuration,
    downloads lesson content, and generates PDF output. It also supports
    reproduction mode for adapting historical lessons to new dates.
    """

    # Create the main parser
    parser = argparse.ArgumentParser(description='Download and process Sabbath School lessons')
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add 'init' subcommand
    init_parser = subparsers.add_parser('init', help='Initialize the environment with default settings')
    
    # Add 'run' subcommand for the main functionality
    run_parser = subparsers.add_parser('run', help='Run a lesson configuration')
    run_parser.add_argument('config_file', help='Path to YAML configuration file')
    run_parser.add_argument('--debug', action='store_true', help='Enable debug mode with verbose logging')
    run_parser.add_argument('--debug-html-only', action='store_true', help='Only generate debug HTML without PDF')
    run_parser.add_argument('--generate-config', action='store_true', help='Generate a sample config file and exit')
    run_parser.add_argument('--quiet-deps', action='store_true', help='Silence debug messages from dependencies')
    run_parser.add_argument('-y', '--yes', action='store_true', help='Answer yes to all prompts (force overwrite)')
    
    # Add shared arguments to the main parser for backward compatibility
    parser.add_argument('--debug', action='store_true', help='Enable debug mode with verbose logging')
    parser.add_argument('--debug-html-only', action='store_true', help='Only generate debug HTML without PDF')
    parser.add_argument('--generate-config', action='store_true', help='Generate a sample config file and exit')
    parser.add_argument('--quiet-deps', action='store_true', help='Silence debug messages from dependencies')
    parser.add_argument('-y', '--yes', action='store_true', help='Answer yes to all prompts (force overwrite)')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Handle generate-config option 
    if args.generate_config:
        from .bin.generate_config import generate_template_config, generate_default_theme, generate_language_template
        config_path = generate_template_config()
        generate_default_theme()
        os.makedirs("languages", exist_ok=True)
        for lang in ["en", "swa", "luo"]:
            generate_language_template(lang, "languages")
        print(f"Sample configuration file generated at: {config_path}")
        return 0
    
    # Handle init command
    if args.command == 'init':
        from .bin.generate_config import generate_template_config, generate_default_theme, generate_language_template
        config_path = generate_template_config()
        generate_default_theme()
        os.makedirs("languages", exist_ok=True)
        for lang in ["en", "swa", "luo"]:
            generate_language_template(lang, "languages")
        print(f"Sample configuration file generated at: {config_path}")
        return 0
    
    # Check if a valid command or config file is provided
    if args.command != 'run' and not hasattr(args, 'config_file'):
        parser.print_help()
        print("\nError: Either a command or config file is required")
        return 1
        
    # For backward compatibility, if no command is specified but a config file is given as positional arg
    if not args.command and len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        args.config_file = sys.argv[1]
        args.command = 'run'
    
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
        # Get config filename from args
        config_file = args.config_file if hasattr(args, 'config_file') else None
        
        if not config_file and args.command != 'run':
            parser.print_help()
            print("\nError: Config file is required when using the 'run' command")
            return 1
            
        print(f"Loading configuration from {config_file}...")
        config = Config(config_file)
        
        # Generate input filename with lesson range information
        range_filename = GitHubDownloader.get_lesson_range_filename(config)
        
        # Check if file path is absolute or relative
        if not os.path.isabs(range_filename):
            # Make sure the filename is in the same directory as the config file
            config_dir = os.path.dirname(args.config_file)
            range_filename = os.path.join(config_dir, range_filename)

        year = config.get("year")
        quarter = config.get("quarter")
        language = config.get("language")
        config.config['output_file'] = f"./output/sabbath_school_lesson_{year}_{quarter}_{language}.pdf"
        
        # Update config with the new filename
        config.config['input_file'] = range_filename
        
        # Print reproduction settings if configured
        if 'reproduce' in config.config and config.config['reproduce'].get('year'):
            reproduction_year = config.config['reproduce']['year']
            reproduction_quarter = config.config['reproduce']['quarter']
            target_year = config.config['year']
            target_quarter = config.config['quarter']
            
            print(f"Reproduction mode: Converting {reproduction_year} {reproduction_quarter} to {target_year} {target_quarter}")
            
            if config.config['reproduce'].get('start_lesson'):
                start_lesson = config.config['reproduce']['start_lesson']
                stop_lesson = config.config['reproduce'].get('stop_lesson', 'end')
                print(f"Lesson range: {start_lesson} to {stop_lesson}")
            
            if config.config['reproduce'].get('quarter_start_date'):
                print(f"New quarter start date: {config.config['reproduce']['quarter_start_date']}")
        
        # Generate GitHub paths
        github_paths = config.get_github_paths()
        print(f"Processing source: year {github_paths['base_url'].split('/')[-3]}, quarter {github_paths['base_url'].split('/')[-2]}, language {config['language']}")
        
        # Check if we should download the file
        should_download = GitHubDownloader.check_existing_file(range_filename, args.yes)
        
        if should_download:
            # Download lesson data
            print("Downloading lesson content from GitHub...")
            downloader = GitHubDownloader(github_paths, config)
            lesson_data = downloader.download_lesson_data()
            
            # Combine into a single markdown file
            print("Combining lesson content...")
            markdown_path = ContentAggregator.combine_lesson_content(lesson_data, range_filename)
        else:
            # Use existing file
            print(f"Using existing file: {range_filename}")
            markdown_path = range_filename
            with open(range_filename, 'r') as file:
                lesson_data = file.read()

        
        # Generate debug HTML if requested
        if args.debug_html_only:
            debug_html_path = config['output_file'].replace('.pdf', '_debug.html')
            debug_html_path = DebugTools.generate_debug_html(markdown_path, debug_html_path)
            print(f"Debug HTML created at: {debug_html_path}")
            return 0
        
        # Process the markdown file to extract structured content
        print("Processing markdown content...")
        content_data = MarkdownProcessor.process_markdown_file(markdown_path, config.config)
        
        # Update SVG files with dynamic content if available
        front_cover_path = config.get('front_cover_svg')
        back_cover_path = config.get('back_cover_svg')
        
        if front_cover_path:
            updated_front_cover = SvgUpdater.update_svg_with_config(front_cover_path, config.config, lesson_data, is_temporary=True)
            if updated_front_cover:
                front_cover_path = updated_front_cover
                print(f"Updated front cover SVG with dynamic content")
        
        if back_cover_path:
            updated_back_cover = SvgUpdater.update_svg_with_config(back_cover_path, config.config, lesson_data, is_temporary=True)
            if updated_back_cover:
                back_cover_path = updated_back_cover
                print(f"Updated back cover SVG with dynamic content")
        
        # Generate HTML
        print("Generating HTML...")
        html_content = HtmlGenerator.generate_html(
            content_data,
            front_cover_svg_path=front_cover_path,
            back_cover_svg_path=back_cover_path,
            config=config.config
        )
        
        # Save debug HTML
        debug_html_path = config['output_file'].replace('.pdf', '_debug.html')
        with open(debug_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Debug HTML saved to: {debug_html_path}")
        
        # Generate PDF
        print("Generating PDF...")
        PdfGenerator.generate_pdf(html_content, config['output_file'], config.config)
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