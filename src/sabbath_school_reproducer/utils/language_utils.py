"""
Language Utilities for Sabbath School Lesson Downloader

This module provides language-specific configuration and utilities.
"""

import os
import yaml
import re
from datetime import datetime

class LanguageConfig:
    """Configuration for language-specific processing."""
    
    # Language codes
    SUPPORTED_LANGUAGES = ['en', 'swa', 'luo']
    
    # Default translations as fallback
    DEFAULT_TRANSLATIONS = {
        'en': {
            'notes': 'NOTES',
            'note': 'NOTE',
            'questions': 'QUESTIONS',
            'answer_prefix': 'Ans.',
            'lesson': 'LESSON',
            'quarter_names': {
                'q1': 'FIRST QUARTER',
                'q2': 'SECOND QUARTER',
                'q3': 'THIRD QUARTER',
                'q4': 'FOURTH QUARTER'
            },
            'quarter_months': {
                'q1': 'January - March',
                'q2': 'April - June',
                'q3': 'July - September',
                'q4': 'October - December'
            },
            'table_of_contents': 'TABLE OF CONTENTS',
            'lesson_column': 'Lesson',
            'title_column': 'Title',
            'date_column': 'Date',
            'page_column': 'Page'
        }
    }
    
    # Cache for loaded language configurations
    _language_cache = {}
    
    @staticmethod
    def load_language_file(language_code, file_path=None):
        """
        Load a language configuration from a YAML file
        
        Args:
            language_code (str): Language code
            file_path (str, optional): Path to the language YAML file
            
        Returns:
            dict: Loaded language configuration, or default if not found
        """
        # Check if we already have this language in cache
        if language_code in LanguageConfig._language_cache:
            return LanguageConfig._language_cache[language_code]
        
        # Start with default translations if available
        translations = LanguageConfig.DEFAULT_TRANSLATIONS.get(language_code, LanguageConfig.DEFAULT_TRANSLATIONS['en']).copy()
        
        # If a file path is provided, try to load from file
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_translations = yaml.safe_load(f)
                
                # Deep merge the file translations with defaults
                if file_translations:
                    LanguageConfig._deep_merge(translations, file_translations)
                
                print(f"Loaded language configuration from: {file_path}")
            except Exception as e:
                print(f"Error loading language file {file_path}: {e}")
                print("Using default translations as fallback")
        
        # Cache the loaded translations
        LanguageConfig._language_cache[language_code] = translations
        
        return translations
    
    @staticmethod
    def _deep_merge(target, source):
        """Recursively merge source dictionary into target dictionary"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                LanguageConfig._deep_merge(target[key], value)
            else:
                target[key] = value
    
    @staticmethod
    def get_translation(language_code, key, default=None, config=None):
        """
        Get a translation for a key in the specified language
        
        Args:
            language_code (str): Language code
            key (str): Translation key
            default: Default value if key not found
            config (dict, optional): Configuration containing language_config_path
            
        Returns:
            str: Translated text
        """
        # Default to English if language not supported
        if language_code not in LanguageConfig.SUPPORTED_LANGUAGES:
            language_code = 'en'
        
        # Load language file if config provided
        file_path = None
        file_path = f"languages/{language_code}.yaml"
        # if config and 'language_config_path' in config:
        #     file_path = config['language_config_path']
        
        # Get translations
        translations = LanguageConfig.load_language_file(language_code, file_path)
        
        # Access nested keys like 'quarter_names.q1'
        if '.' in key:
            parts = key.split('.')
            current = translations
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return default
            return current
        
        # Direct key access
        return translations.get(key, default)
    
    @staticmethod
    def get_date_formats(language_code, config=None):
        """
        Get date formats for the specified language
        
        Args:
            language_code (str): Language code
            config (dict, optional): Configuration containing language_config_path
            
        Returns:
            list: List of date format regular expressions
        """
        # Load language file if config provided
        file_path = None
        if config and 'language_config_path' in config:
            file_path = config['language_config_path']
        
        # Get translations
        translations = LanguageConfig.load_language_file(language_code, file_path)
        
        # Return date formats if available
        if 'date_formats' in translations and isinstance(translations['date_formats'], list):
            return translations['date_formats']
        
        # Default fallback formats for English
        return [
            r'([A-Za-z]+ \d+, \d{4})',  # e.g., "May 20, 1905"
            r'(\d+ [A-Za-z]+, \d{4})',   # e.g., "20 May, 1905"
            r'(\d{1,2}/\d{1,2}/\d{4})'   # e.g., "5/20/1905"
        ]
    
    @staticmethod
    def get_month_names(language_code, config=None):
        """
        Get month names for the specified language
        
        Args:
            language_code (str): Language code
            config (dict, optional): Configuration containing language_config_path
            
        Returns:
            list: List of month names
        """
        # Load language file if config provided
        file_path = None
        if config and 'language_config_path' in config:
            file_path = config['language_config_path']
        
        # Get translations
        translations = LanguageConfig.load_language_file(language_code, file_path)
        
        # Return month names if available
        if 'month_names' in translations and isinstance(translations['month_names'], list):
            return translations['month_names']
        
        # Default fallback for English
        return [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
    
    @staticmethod
    def format_date(date_obj, language_code, config=None):
        """
        Format a date object for the specified language
        
        Args:
            date_obj (datetime): Date object
            language_code (str): Language code
            config (dict, optional): Configuration containing language_config_path
            
        Returns:
            str: Formatted date string
        """
        month_idx = date_obj.month - 1  # 0-based index
        month_name = LanguageConfig.get_month_names(language_code, config)[month_idx]
        
        # Load language file if config provided
        file_path = None
        if config and 'language_config_path' in config:
            file_path = config['language_config_path']
        
        # Get translations
        translations = LanguageConfig.load_language_file(language_code, file_path)
        
        # Get date format template if available
        template = '{month} {day}, {year}'  # Default English format
        if 'date_format_template' in translations:
            template = translations['date_format_template']
        
        # Format date using template
        return template.format(
            month=month_name,
            day=date_obj.day,
            year=date_obj.year
        )