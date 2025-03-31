import requests

class CSSEditor:
    """Generates HTML content for PDF generation with incremental approach."""
    
    @staticmethod
    def get_lesson_title(year, quarter):
        """
        Get the lesson title from the lessons.json file
        
        Args:
            year (int): Year of the lesson
            quarter (str): Quarter of the lesson (e.g., q1, q2, q3, q4)
            
        Returns:
            str: Lesson title or default title if not found
        """
        try:
            # Download the lessons.json file
            response = requests.get("https://raw.githubusercontent.com/SabbathSchool/lessons/refs/heads/master/lessons.json")
            response.raise_for_status()
            
            # Parse the JSON data
            lessons_data = response.json()
            
            # Normalize the quarter format (q1 -> Q1)
            normalized_quarter = quarter.upper()
            
            # Find the lesson matching the year and quarter
            for lesson in lessons_data.get("lessons", []):
                # Safely convert both year values to strings
                lesson_year_str = str(lesson["year"])
                year_str = str(year)
                                
                if lesson_year_str == year_str and normalized_quarter in lesson["quarter"]:
                    return lesson["title"]
            
            # If no match found, return a default title
            return "Sabbath School Lessons"
        except Exception as e:
            print(f"Warning: Failed to get lesson title: {e}")
            return "Sabbath School Lessons"