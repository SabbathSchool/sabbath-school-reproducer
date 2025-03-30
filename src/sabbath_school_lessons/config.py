"""
Configuration Module for Sabbath School Lessons

This module handles loading and validating configuration from a YAML file.
"""

import os
import yaml
from datetime import datetime


class Config:
    """Handles configuration loading and validation for Sabbath School lessons."""
    
    def __init__(self, config_path):
        """
        Initialize with a path to a config file
        
        Args:
            config_path (str): Path to YAML config file
        """
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """
        Load configuration from YAML file
        
        Returns:
            dict: Validated configuration dictionary
            
        Raises:
            Exception: If config loading or validation fails
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Handle optional fields with defaults
            if 'front_cover_svg' not in config:
                config['front_cover_svg'] = None
            if 'back_cover_svg' not in config:
                config['back_cover_svg'] = None
                
            return self.validate_config(config)
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")
    
    def validate_config(self, config):
        """
        Validates the configuration data
        
        Args:
            config (dict): Configuration dictionary
            
        Returns:
            dict: Validated configuration dictionary
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = ['year', 'quarter', 'language', 'input_file', 'output_file']
        
        # Check required fields
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field in configuration: {field}")
        
        # Validate year
        try:
            year = int(config['year'])
            if year < 1880 or year > datetime.now().year:
                raise ValueError(f"Year {year} is out of supported range")
        except ValueError:
            raise ValueError(f"Invalid year format: {config['year']}")
        
        # Validate quarter
        if config['quarter'] not in ['q1', 'q2', 'q3', 'q4']:
            raise ValueError(f"Quarter must be one of: q1, q2, q3, q4, not {config['quarter']}")
        
        # Validate language (simple check for now)
        if not isinstance(config['language'], str) or len(config['language']) < 2:
            raise ValueError(f"Invalid language code: {config['language']}")
        
        # Check if output directory exists, create if not
        output_dir = os.path.dirname(config['output_file'])
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        return config
    
    def get_github_paths(self):
        """
        Generate GitHub repository paths based on configuration
        
        Returns:
            dict: Dictionary with GitHub paths
        """
        year = int(self.config['year'])
        decade = f"{year // 10 * 10}s"
        quarter = self.config['quarter']
        lang = self.config['language']
        
        base_url = f"https://raw.githubusercontent.com/SabbathSchool/lessons/refs/heads/master/{decade}/{year}/{quarter}/{lang}"
        contents_url = f"{base_url}/contents.json"
        front_matter_url = f"{base_url}/front-matter.md"
        back_matter_url = f"{base_url}/back-matter.md"
        
        return {
            'base_url': base_url,
            'contents_url': contents_url,
            'front_matter_url': front_matter_url,
            'back_matter_url': back_matter_url
        }
    
    def __getitem__(self, key):
        """Allow dictionary-like access to config values"""
        return self.config[key]
    
    def get(self, key, default=None):
        """Get a config value with a default"""
        return self.config.get(key, default)