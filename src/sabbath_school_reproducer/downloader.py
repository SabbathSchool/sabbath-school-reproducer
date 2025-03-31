"""
GitHub Content Downloader for Sabbath School Lessons

This module handles downloading lesson content from the GitHub repository.
"""

import json
import requests
from urllib.parse import urljoin
import re


class GitHubDownloader:
    """Downloads Sabbath School lesson content from GitHub repository."""
    
    def __init__(self, github_paths, config=None):
        """
        Initialize with GitHub paths
        
        Args:
            github_paths (dict): Dictionary with GitHub URLs
            config (Config, optional): Configuration object for reproduction settings
        """
        self.github_paths = github_paths
        self.config = config
    
    def download_json(self, url):
        """
        Download and parse JSON from a URL
        
        Args:
            url (str): URL to download JSON from
            
        Returns:
            dict: Parsed JSON, or None if download failed
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error downloading JSON from {url}: {e}")
            return None
        except json.JSONDecodeError:
            print(f"Error parsing JSON from {url}")
            return None

    def download_markdown(self, url):
        """
        Download markdown content from a URL
        
        Args:
            url (str): URL to download markdown from
            
        Returns:
            str: Markdown content, or empty string if download failed
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error downloading markdown from {url}: {e}")
            return ""

    def download_lesson_data(self):
        """
        Download all lesson data from GitHub repository
                
        Returns:
            dict: Dictionary containing all downloaded content
            
        Raises:
            Exception: If download of contents.json fails
        """
        # Download contents.json first
        contents = self.download_json(self.github_paths['contents_url'])
        if not contents:
            raise Exception(f"Failed to download lesson contents from {self.github_paths['contents_url']}")
        
        # Download front matter
        front_matter = self.download_markdown(self.github_paths['front_matter_url'])
        
        # Download back matter
        back_matter = self.download_markdown(self.github_paths['back_matter_url'])
        
        # Get reproduction settings if available
        start_lesson = 1
        stop_lesson = float('inf')  # Default to all lessons
        
        if self.config and 'reproduce' in self.config.config:
            reproduce = self.config.config['reproduce']
            if 'start_lesson' in reproduce and reproduce['start_lesson']:
                start_lesson = int(reproduce['start_lesson'])
            
            if 'stop_lesson' in reproduce and reproduce['stop_lesson'] is not None:
                stop_lesson = int(reproduce['stop_lesson'])
        
        # Download each lesson
        lessons = {}
        base_url = self.github_paths['base_url']
        
        # Filter and sort week IDs
        filtered_week_ids = []
        for week_id in contents:
            # Extract lesson number from week_id (e.g., "week-01" -> 1)
            lesson_num_match = re.search(r'week-(\d+)', week_id)
            if lesson_num_match:
                lesson_num = int(lesson_num_match.group(1))
                if start_lesson <= lesson_num <= stop_lesson:
                    filtered_week_ids.append(week_id)
        
        # Sort the filtered week IDs
        filtered_week_ids.sort()
        
        for week_id in filtered_week_ids:
            week_url = urljoin(base_url + "/", f"{week_id}.md")
            week_content = self.download_markdown(week_url)
            
            if week_content:
                # Store with metadata from contents.json
                lessons[week_id] = {
                    'content': week_content,
                    'title': contents[week_id].get('title', ''),
                    'date': contents[week_id].get('date', '')
                }
                print(f"Downloaded {week_id}: {contents[week_id].get('title', '')}")
            else:
                print(f"Failed to download {week_id}")
        
        return {
            'contents': contents,
            'front_matter': front_matter,
            'back_matter': back_matter,
            'lessons': lessons
        }
    
    @staticmethod
    def get_lesson_range_filename(config):
        """
        Generate a filename that includes the lesson range information
        
        Args:
            config (Config): Configuration object
            
        Returns:
            str: Filename with lesson range information
        """
        year = config['year']
        quarter = config['quarter']
        language = config['language']
        
        # Get lesson range from reproduction settings
        start_lesson = 1
        stop_lesson = "null"
        
        if 'reproduce' in config.config:
            reproduce = config.config['reproduce']
            if 'start_lesson' in reproduce and reproduce['start_lesson']:
                start_lesson = reproduce['start_lesson']
            
            if 'stop_lesson' in reproduce and reproduce['stop_lesson'] is not None:
                stop_lesson = reproduce['stop_lesson']
        
        # Create filename with lesson range
        return f"combined_lessons_{year}_{quarter}_{language}_{start_lesson}_{stop_lesson}.md"

    @staticmethod
    def check_existing_file(filename, force_overwrite=False):
        """
        Check if the file already exists and prompt for overwrite
        
        Args:
            filename (str): Path to the file
            force_overwrite (bool): Whether to force overwrite without prompting
            
        Returns:
            bool: True if should proceed with download, False otherwise
        """
        import os
        
        if not os.path.exists(filename):
            return True  # File doesn't exist, proceed with download
        
        if force_overwrite:
            print(f"File {filename} exists, will overwrite (force mode)")
            return True
        
        # Prompt user for confirmation
        response = input(f"File {filename} already exists. Overwrite? (y/n): ")
        return response.lower() in ['y', 'yes']