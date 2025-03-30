import json
import pytest
from unittest.mock import patch, MagicMock
from sabbath_school_reproducer.downloader import GitHubDownloader

class TestDownloader:
    def setup_method(self):
        self.github_paths = {
            'base_url': 'https://github.com/test/1905/q2/en',
            'contents_url': 'https://github.com/test/1905/q2/en/contents.json',
            'front_matter_url': 'https://github.com/test/1905/q2/en/front-matter.md',
            'back_matter_url': 'https://github.com/test/1905/q2/en/back-matter.md'
        }
        
        # Mock config for reproduction settings
        self.mock_config = MagicMock()
        self.mock_config.config = {
            'reproduce': {
                'start_lesson': 1,
                'stop_lesson': 2
            }
        }
    
    @patch('sabbath_school_reproducer.downloader.requests.get')
    def test_download_json(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'test': 'data'}
        mock_get.return_value = mock_response
        
        downloader = GitHubDownloader(self.github_paths)
        result = downloader.download_json('https://test.url')
        
        assert result == {'test': 'data'}
        mock_get.assert_called_once_with('https://test.url')
    
    @patch('sabbath_school_reproducer.downloader.requests.get')
    def test_download_markdown(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "# Test Markdown"
        mock_get.return_value = mock_response
        
        downloader = GitHubDownloader(self.github_paths)
        result = downloader.download_markdown('https://test.url')
        
        assert result == "# Test Markdown"
        mock_get.assert_called_once_with('https://test.url')
    
    @patch('sabbath_school_reproducer.downloader.GitHubDownloader.download_json')
    @patch('sabbath_school_reproducer.downloader.GitHubDownloader.download_markdown')
    def test_download_lesson_data(self, mock_download_markdown, mock_download_json):
        # Setup mock responses
        mock_download_json.return_value = {
            'week-01': {'title': 'Lesson 1', 'date': '2025-04-01'},
            'week-02': {'title': 'Lesson 2', 'date': '2025-04-08'},
            'week-03': {'title': 'Lesson 3', 'date': '2025-04-15'}
        }
        
        mock_download_markdown.side_effect = [
            "# Front Matter",  # front-matter.md
            "# Back Matter",   # back-matter.md
            "# Lesson 1",      # week-01.md
            "# Lesson 2"       # week-02.md
        ]
        
        downloader = GitHubDownloader(self.github_paths, self.mock_config)
        result = downloader.download_lesson_data()
        
        assert 'contents' in result
        assert 'front_matter' in result
        assert 'back_matter' in result
        assert 'lessons' in result
        
        # Check that only weeks 1-2 are included due to stop_lesson=2
        assert len(result['lessons']) == 2
        assert 'week-01' in result['lessons']
        assert 'week-02' in result['lessons']
        assert 'week-03' not in result['lessons']
        
        # Check content
        assert result['front_matter'] == "# Front Matter"
        assert result['back_matter'] == "# Back Matter"
        assert result['lessons']['week-01']['content'] == "# Lesson 1"