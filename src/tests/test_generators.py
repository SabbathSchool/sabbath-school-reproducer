import os
import tempfile
import pytest
from sabbath_school_reproducer.generator.html_generator import HtmlGenerator
from sabbath_school_reproducer.generator.pdf_generator import PdfGenerator

class TestHtmlGenerator:
    def setup_method(self):
        # Test content data
        self.content_data = {
            'lessons': [
                {
                    'number': '1',
                    'title': 'Test Lesson',
                    'date': 'April 1, 2025',
                    'questions': [
                        {'text': 'Test question?', 'scripture': 'Gen. 1:1.', 'answer': ''}
                    ],
                    'notes': 'Test note.',
                    'preliminary_note': 'This is a test.'
                }
            ],
            'frontmatter': '# Front Matter\nTest front matter content.',
            'backmatter': '# Back Matter\nTest back matter content.',
            'metadata': {}
        }
        
        # Test config
        self.config = {
            'year': 2025,
            'quarter': 'q2',
            'title': 'Test Lessons',
            'subtitle': 'Q2 2025'
        }
    
    def test_create_cover_page(self):
        # Test with no SVG path
        cover_html = HtmlGenerator.create_cover_page(None, self.config)
        
        assert '<div class="cover-page">' in cover_html
        assert '<svg' in cover_html
        assert '2025' in cover_html
    
    def test_convert_markdown_to_html(self):
        markdown = "# Test Heading\n\nTest paragraph."
        html = HtmlGenerator.convert_markdown_to_html(markdown)
        
        assert '<h1>Test Heading</h1>' in html
        assert '<p>Test paragraph.</p>' in html
    
    def test_create_lesson_html(self):
        lesson = self.content_data['lessons'][0]
        lesson_html = HtmlGenerator.create_lesson_html(lesson)
        
        assert 'Test Lesson' in lesson_html
        assert 'April 1, 2025' in lesson_html
        assert 'Test question?' in lesson_html
        assert 'Gen. 1:1.' in lesson_html
        assert 'Test note.' in lesson_html
        assert 'This is a test.' in lesson_html
    
    def test_generate_html(self):
        html = HtmlGenerator.generate_html(self.content_data, None, None, self.config)
        
        assert '<!DOCTYPE html>' in html
        assert '<title>Sabbath School Lessons</title>' in html
        assert 'Test Lesson' in html
        assert 'Front Matter' in html
        assert 'Back Matter' in html

class TestPdfGenerator:
    def test_count_pages(self, monkeypatch):
        # Mock Document class
        class MockDoc:
            def __init__(self):
                self.pages = [1, 2, 3]  # 3 pages
        
        # Test the function
        page_count = PdfGenerator.count_pages_in_document(MockDoc())
        assert page_count == 3