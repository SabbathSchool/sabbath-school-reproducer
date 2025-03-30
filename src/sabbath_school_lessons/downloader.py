"""
GitHub Content Downloader for Sabbath School Lessons

This module handles downloading lesson content from the GitHub repository.
"""

import json
import requests
from urllib.parse import urljoin


class GitHubDownloader:
    """Downloads Sabbath School lesson content from GitHub repository."""
    
    def __init__(self, github_paths):
        """
        Initialize with GitHub paths
        
        Args:
            github_paths (dict): Dictionary with GitHub URLs
        """
        self.github_paths = github_paths
    
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
        
        # Download each lesson
        lessons = {}
        base_url = self.github_paths['base_url']
        
        for week_id in contents:
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