import os
import pytest
import tempfile
from sabbath_school_reproducer.config import Config

class TestConfig:
    def setup_method(self):
        # Create a temporary config file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, "test_config.yaml")
        
        # Basic valid config
        with open(self.config_path, "w") as f:
            f.write("""
year: 2025
quarter: q2
language: en
input_file: ./test_input.md
output_file: ./test_output.pdf
            """)
    
    def teardown_method(self):
        self.temp_dir.cleanup()
    
    def test_load_valid_config(self):
        config = Config(self.config_path)
        assert config['year'] == 2025
        assert config['quarter'] == 'q2'
        assert config['language'] == 'en'
        assert config['input_file'] == './test_input.md'
        assert config['output_file'] == './test_output.pdf'
    
    def test_invalid_quarter(self):
        # Create config with invalid quarter
        with open(self.config_path, "w") as f:
            f.write("""
year: 2025
quarter: q5
language: en
input_file: ./test_input.md
output_file: ./test_output.pdf
            """)
        
        with pytest.raises(Exception, match=".*Quarter must be one of.*"):
            Config(self.config_path)
    
    def test_github_paths(self):
        config = Config(self.config_path)
        paths = config.get_github_paths()
        
        assert "base_url" in paths
        assert "1900s/1905/q2/en" in paths["base_url"]  # Update to match actual value
        assert "contents_url" in paths
        assert paths["contents_url"].endswith("contents.json")
    
    def test_reproduction_settings(self):
        # Test with reproduction settings
        with open(self.config_path, "w") as f:
            f.write("""
year: 2025
quarter: q2
language: en
input_file: ./test_input.md
output_file: ./test_output.pdf
reproduce:
  year: 1905
  quarter: q3
  start_lesson: 2
  stop_lesson: 5
  quarter_start_date: '2025-07-01'
            """)
        
        config = Config(self.config_path)
        assert config['reproduce']['year'] == 1905
        assert config['reproduce']['quarter'] == 'q3'
        assert config['reproduce']['start_lesson'] == 2
        assert config['reproduce']['stop_lesson'] == 5
        
        # Check that GitHub paths use reproduction settings
        paths = config.get_github_paths()
        assert "1900s/1905/q3/en" in paths["base_url"]