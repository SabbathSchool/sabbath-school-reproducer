import os
import tempfile
import pytest
from sabbath_school_reproducer.processor import MarkdownProcessor

class TestMarkdownProcessor:
    def setup_method(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_md_path = os.path.join(self.temp_dir.name, "test.md")
        
        # Create a test markdown file
        with open(self.test_md_path, "w") as f:
            f.write("""# File: front-matter.md
#------------------------------------------------------------------------------

# Sabbath School Lesson Quarterly
## First Quarter, 2025

# File: week-01.md
#------------------------------------------------------------------------------

# Lesson 1 - Nature of Man

January 1, 2025

## Questions

1. What is the nature of man? Gen. 1:26, 27.
2. How was man created? Gen. 2:7.

## Notes

1. God created man in His image.
2. Man was formed from dust.

# File: week-02.md
#------------------------------------------------------------------------------

# Lesson 2 - State of the Dead

January 8, 2025

## Questions

1. What happens at death? Eccl. 9:5, 6.
2. How does the Bible describe death? 1 Thess. 4:13.

## Notes

1. The dead know nothing.

# File: back-matter.md
#------------------------------------------------------------------------------

# Lesson Helps
* Here and Hereafter - a book about man's nature
""")
    
    def teardown_method(self):
        self.temp_dir.cleanup()
    
    def test_parse_file_sections(self):
        with open(self.test_md_path, "r") as f:
            content = f.read()
        
        lessons, front, back = MarkdownProcessor.parse_file_sections(content)
        
        assert "# Lesson 1 - Nature of Man" in lessons
        assert "# Lesson 2 - State of the Dead" in lessons
        assert "# Sabbath School Lesson Quarterly" in front
        assert "# Lesson Helps" in back
    
    def test_parse_questions(self):
        questions_text = """1. What is the nature of man? Gen. 1:26, 27.
2. How was man created? Gen. 2:7."""
        
        questions = MarkdownProcessor.parse_questions_from_markdown(questions_text)
        
        assert len(questions) == 2
        assert questions[0]['text'] == "What is the nature of man?"
        assert questions[0]['scripture'] == "Gen. 1:26, 27."
        assert questions[1]['text'] == "How was man created?"
        assert questions[1]['scripture'] == "Gen. 2:7."
    
    def test_extract_date(self):
        text = """# Lesson 1 - Title
        
January 1, 2025

Some other content."""
        
        date, cleaned = MarkdownProcessor.extract_and_remove_date(text)
        
        assert date == "January 1, 2025"
        assert "January 1, 2025" not in cleaned
        assert "# Lesson 1 - Title" in cleaned
        assert "Some other content" in cleaned
    
    def test_adjust_dates(self):
        lessons = [
            {'number': '1', 'date': 'January 1, 1905', 'title': 'Lesson 1'},
            {'number': '2', 'date': 'January 8, 1905', 'title': 'Lesson 2'}
        ]
        
        config = {
            'reproduce': {
                'quarter_start_date': '2025-04-01'
            }
        }
        
        updated = MarkdownProcessor.adjust_dates(lessons, config)
        
        assert updated[0]['date'] == 'April 01, 2025'
        assert updated[1]['date'] == 'April 08, 2025'
        assert updated[0]['original_date'] == 'January 1, 1905'