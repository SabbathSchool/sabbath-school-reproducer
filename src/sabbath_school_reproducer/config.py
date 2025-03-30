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
                
            # Handle reproduction config or set defaults
            if 'reproduce' not in config:
                config['reproduce'] = {}
                
            reproduce_config = config['reproduce']
            
            # Set reproduction defaults if not specified
            if not reproduce_config.get('year'):
                reproduce_config['year'] = 1905  # Default historical year
            if not reproduce_config.get('quarter'):
                reproduce_config['quarter'] = "q2"  # Default historical quarter
            if not reproduce_config.get('start_lesson'):
                reproduce_config['start_lesson'] = 1
            if not reproduce_config.get('stop_lesson'):
                reproduce_config['stop_lesson'] = None
                
            # Set default quarter start date if not provided
            if not reproduce_config.get('quarter_start_date'):
                # Calculate first day of target quarter
                year = config['year']
                quarter = config['quarter']
                quarter_month = ((int(quarter[1]) - 1) * 3) + 1  # q1->1, q2->4, q3->7, q4->10
                reproduce_config['quarter_start_date'] = f"{year}-{quarter_month:02d}-01"
                
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
            if year < 1880 or year > datetime.now().year + 1:  # Allow current year + 1
                raise ValueError(f"Year {year} is out of supported range")
        except ValueError:
            raise ValueError(f"Invalid year format: {config['year']}")
        
        # Validate quarter
        if config['quarter'] not in ['q1', 'q2', 'q3', 'q4']:
            raise ValueError(f"Quarter must be one of: q1, q2, q3, q4, not {config['quarter']}")
        
        # Validate language (simple check for now)
        if not isinstance(config['language'], str) or len(config['language']) < 2:
            raise ValueError(f"Invalid language code: {config['language']}")
        
        # Validate reproduction settings if present
        if 'reproduce' in config:
            reproduce = config['reproduce']
            
            # Validate reproduction year
            if 'year' in reproduce:
                try:
                    r_year = int(reproduce['year'])
                    if r_year < 1880 or r_year > datetime.now().year:
                        raise ValueError(f"Reproduction year {r_year} is out of supported range")
                except ValueError:
                    raise ValueError(f"Invalid reproduction year format: {reproduce['year']}")
            
            # Validate reproduction quarter
            if 'quarter' in reproduce and reproduce['quarter'] not in ['q1', 'q2', 'q3', 'q4']:
                raise ValueError(f"Reproduction quarter must be one of: q1, q2, q3, q4, not {reproduce['quarter']}")
            
            # Validate start_lesson if present
            if 'start_lesson' in reproduce:
                try:
                    start_lesson = int(reproduce['start_lesson'])
                    if start_lesson < 1:
                        raise ValueError(f"Start lesson must be at least 1, not {start_lesson}")
                except ValueError:
                    raise ValueError(f"Invalid start lesson format: {reproduce['start_lesson']}")
            
            # Validate stop_lesson if present and not None
            if 'stop_lesson' in reproduce and reproduce['stop_lesson'] is not None:
                try:
                    stop_lesson = int(reproduce['stop_lesson'])
                    if stop_lesson < 1:
                        raise ValueError(f"Stop lesson must be at least 1, not {stop_lesson}")
                    
                    # Check if stop_lesson is greater than or equal to start_lesson
                    if 'start_lesson' in reproduce and stop_lesson < reproduce['start_lesson']:
                        raise ValueError(f"Stop lesson ({stop_lesson}) must be greater than or equal to start lesson ({reproduce['start_lesson']})")
                except ValueError:
                    raise ValueError(f"Invalid stop lesson format: {reproduce['stop_lesson']}")
            
            # Validate quarter_start_date format if present
            if 'quarter_start_date' in reproduce:
                try:
                    # Check if the date string is in the correct format
                    datetime.strptime(reproduce['quarter_start_date'], '%Y-%m-%d')
                except ValueError:
                    raise ValueError(f"Invalid quarter start date format: {reproduce['quarter_start_date']}. Use YYYY-MM-DD format.")
        
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
        # Use reproduction settings if they exist, otherwise use main settings
        if 'reproduce' in self.config and self.config['reproduce'].get('year'):
            year = int(self.config['reproduce']['year'])
            quarter = self.config['reproduce']['quarter']
        else:
            year = int(self.config['year'])
            quarter = self.config['quarter']
        
        decade = f"{year // 10 * 10}s"
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