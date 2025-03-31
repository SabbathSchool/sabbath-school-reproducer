#!/usr/bin/env python3
"""
Test script for the Sabbath School lesson parser

This script tests the parse_lessons and parse_questions_from_markdown functions
with different lesson formats to ensure they work correctly.
"""

import unittest
import re
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the functions to be tested
from sabbath_school_reproducer.processor import MarkdownProcessor

class TestLessonParser(unittest.TestCase):
    """Test cases for the lesson parser."""

    def test_modern_format_with_dash(self):
        """Test parsing a modern format lesson with a dash in the title."""
        content = """
# LESSON 1 - BIRTH OF CHRIST

*January 7, 1899*

**Nazareth and Bethlehem, B.C. 5**
*(Matt. 1:1-25; Luke 1:26-35; 2:1-7)*

1. How is Christ introduced to the student of the New Testament? Matt. 1:1. *See note 1.*

2. How did the birth of Christ come about? Isa. 7:14. Verse 18.

3. Who had previously visited Mary? Luke 1:26, 27.

16. What humble resting-place was assigned to Jesus? Verse 7. Why was this?

## READING

"Desire of Ages," pp. 43, 44.

## NOTES

1. Inasmuch as Christ was to be manifested to the world as the "promised Seed" of Abraham...
"""
        lessons = MarkdownProcessor.parse_lessons(content)
        
        # Check that we parsed one lesson
        self.assertEqual(len(lessons), 1)
        
        # Check lesson details
        lesson = lessons[0]
        self.assertEqual(lesson['number'], '1')
        self.assertEqual(lesson['title'], 'BIRTH OF CHRIST')
        self.assertEqual(lesson['date'], 'January 7, 1899')
        self.assertEqual(lesson['location'], 'Nazareth and Bethlehem, B.C. 5')
        self.assertEqual(lesson['references'], 'Matt. 1:1-25; Luke 1:26-35; 2:1-7')
        
        # Check questions
        self.assertEqual(len(lesson['questions']), 4)
        self.assertIn('See note 1', lesson['questions'][0].get('scripture', ''))
        
        # Check additional sections
        self.assertEqual(len(lesson['additional_sections']), 1)
        self.assertEqual(lesson['additional_sections'][0]['title'], 'READING')
        self.assertIn('Desire of Ages', lesson['additional_sections'][0]['content'])
        
        # Check notes
        self.assertTrue(lesson['notes'])
        self.assertIn('Inasmuch as Christ', lesson['notes'])

    def test_older_format_with_em_dash(self):
        """Test parsing an older format lesson with em dash and section headers."""
        content = """
# LESSON 2 — January 12, 1895

## THE WORLDLY SANCTUARY

### INSTRUCTION FOR BUILDING

1. Who gave instruction for building the sanctuary? Ex. 25:1, 8.
2. To whom was this instruction given?
3. Where and at what time was it given? Ex. 24:12-18.
4. What kind of offerings were to be brought for the sanctuary? Ex. 25:2. Note 1.
5. Of what were the offerings to consist? Verses 3-7.

### MATERIALS FOR BUILDING

11. Of what were the sides composed? Ex. 26:15. Note 2.
12. Of what length and width were these boards? Verse 16. Note 3.
13. How many boards were there to be on the north and south sides of the tabernacle? Verses 18, 20.

## NOTES

1. There is an important lesson for us in the instruction which the Lord gave His people...
"""
        lessons = MarkdownProcessor.parse_lessons(content)
        
        # Check that we parsed one lesson
        self.assertEqual(len(lessons), 1)
        
        # Check lesson details
        lesson = lessons[0]
        self.assertEqual(lesson['number'], '2')
        self.assertEqual(lesson['title'], 'THE WORLDLY SANCTUARY')
        self.assertEqual(lesson['date'], 'January 12, 1895')
        
        # Check questions
        self.assertEqual(len(lesson['questions']), 8)
        
        # Check question section headers
        self.assertEqual(len(lesson['question_headers']), 2)
        self.assertEqual(lesson['question_headers'][0], 'INSTRUCTION FOR BUILDING')
        self.assertEqual(lesson['question_headers'][1], 'MATERIALS FOR BUILDING')
        
        # Check first question from first section
        self.assertIn('Ex. 25:1, 8', lesson['questions'][0].get('text', ''))
        self.assertEqual(lesson['questions'][0].get('section'), 'INSTRUCTION FOR BUILDING')
        
        # Check first question from second section
        self.assertIn('Ex. 26:15', lesson['questions'][5].get('text', ''))
        self.assertEqual(lesson['questions'][5].get('section'), 'MATERIALS FOR BUILDING')
        
        # Check notes
        self.assertTrue(lesson['notes'])
        self.assertIn('important lesson', lesson['notes'])

    def test_wise_men_visit_format(self):
        """Test parsing the Wise Men lesson format."""
        content = """
# LESSON 3 - VISIT OF THE WISE MEN, AND THE FLIGHT INTO EGYPT

*January 21, 1899*

**Bethlehem and Jerusalem, B.C. 4**
*(Matt. 2:1-18)*

1. Who came from the East to Jerusalem, shortly after the birth of Christ? Matt. 2:1. *See note 1.*

2. For whom did they inquire? and why? Verse 2.

3. What effect did their inquiry have upon the king and people? Verse 3.

4. In their trouble, what step was taken by the king? Verse 4. *See note 2.*

5. What did the king learn from the priests and scribes? Verse 5.

6. What reason did the priests give for this statement? *See note 3.* Verses 5, 6.

19. In carrying out this decree, what scripture was fulfilled? Verses 17, 18.

## READING

"Desire of Ages," pp. 59-65.

## NOTES

1. "The epithet by which Matthew describes to us these Eastern strangers is not so vague and indefinite as it seems in our translation. He calls them Magi from the East. The birthplace and natural home of the magian worship was in Persia. And there the Magi had a place and power such as the
"""
        lessons = MarkdownProcessor.parse_lessons(content)
        
        # Check that we parsed one lesson
        self.assertEqual(len(lessons), 1)
        
        # Check lesson details
        lesson = lessons[0]
        self.assertEqual(lesson['number'], '3')
        self.assertEqual(lesson['title'], 'VISIT OF THE WISE MEN, AND THE FLIGHT INTO EGYPT')
        self.assertEqual(lesson['date'], 'January 21, 1899')
        self.assertEqual(lesson['location'], 'Bethlehem and Jerusalem, B.C. 4')
        self.assertEqual(lesson['references'], 'Matt. 2:1-18')
        
        # Check questions
        self.assertEqual(len(lesson['questions']), 7)
        self.assertIn('See note 1', lesson['questions'][0].get('scripture', ''))
        self.assertIn('See note 2', lesson['questions'][3].get('scripture', ''))
        self.assertIn('See note 3', lesson['questions'][5].get('scripture', ''))
        
        # Check additional sections
        self.assertEqual(len(lesson['additional_sections']), 1)
        self.assertEqual(lesson['additional_sections'][0]['title'], 'READING')
        self.assertIn('Desire of Ages', lesson['additional_sections'][0]['content'])
        
        # Check notes
        self.assertTrue(lesson['notes'])
        self.assertIn('epithet', lesson['notes'])

    def test_nature_of_man_format(self):
        """Test parsing the Nature of Man lesson format."""
        content = """
# Lesson 1 - Nature of Man

April 1, 1905

## Questions

1. In whose image was man created? Gen. 1:26, 27.
2. How was man created? What was given him? Gen. 2:7.
3. Was this "breath of life" limited to man alone? Gen. 7:21, 22; Eccl. 3:19.
4. To what was man given free access? Gen. 2:16, 17.
16. In the immortal state, to what will man again have free access? Rev. 2:7; 22:14.

## Notes

1. God did not purpose to perpetuate sin throughout eternity, therefore when man sinned he was shut away from the tree of life. None of the human family has ever passed this cherubim and flaming sword sent to guard the way to the tree of life, so there is not an immortal sinner on earth.

4. The mission of Christ to this earth was to bring life to man, who, by reason of transgression, had been shut away from the tree of life. He offers to become a tree of life to all who will believe. Nothing could more effectually rob the Son of God of His glory than to teach that man possesses by nature an immortal soul, and is capable of an eternal existence independent of faith in a Redeemer. Were this so, the mission of Christ to give life would have been in vain.
"""
        lessons = MarkdownProcessor.parse_lessons(content)
        
        # Check that we parsed one lesson
        self.assertEqual(len(lessons), 1)
        
        # Check lesson details
        lesson = lessons[0]
        self.assertEqual(lesson['number'], '1')
        self.assertEqual(lesson['title'], 'Nature of Man')
        self.assertEqual(lesson['date'], 'April 1, 1905')
        
        # Check questions
        print(lesson['questions'])
        self.assertEqual(len(lesson['questions']), 5)
        self.assertIn('Gen. 1:26, 27', lesson['questions'][0].get('text', ''))
        
        # Check notes
        self.assertTrue(lesson['notes'])
        self.assertIn('God did not purpose', lesson['notes'])

    def test_state_of_the_dead_format(self):
        """Test parsing the State of the Dead lesson format."""
        content = """
# Lesson 2 - The State of the Dead

April 8, 1905

## Questions

1. What question is asked concerning those who are dead? Job 14:10.
2. What answer is given? Verse 12.
3. What did the Lord say would be the result of transgression? Gen. 2:17.
16. When will the righteous be gathered home? John 14:1-3; Matt. 24:31.

## Notes

1. The Lord warned man that the penalty for sin was death. Satan plainly contradicted the word of God by stating that man would not die, but be "as God, knowing good and evil." The doctrine therefore of consciousness in death has its origin wholly from this declaration of Satan in Eden. To make good his statement, "Ye shall not die," he has filled the world with the false idea of an immortal soul which survives the stroke of death, and continues to live separate from the body.

3. At creation, the Lord breathed into the man whom He had made the breath of life. In death the process is reversed. The Lord takes from every living creature that which was given at creation, viz., the breath, and death results. Ps. 104:29. But that which the Lord takes from man at death was not a conscious entity prior to the time man received it; neither is it after death.
"""
        lessons = MarkdownProcessor.parse_lessons(content)
        
        # Check that we parsed one lesson
        self.assertEqual(len(lessons), 1)
        
        # Check lesson details
        lesson = lessons[0]
        self.assertEqual(lesson['number'], '2')
        self.assertEqual(lesson['title'], 'The State of the Dead')
        self.assertEqual(lesson['date'], 'April 8, 1905')
        
        # Check questions
        self.assertEqual(len(lesson['questions']), 4)
        self.assertIn('Job 14:10', lesson['questions'][0].get('text', ''))
        
        # Check notes
        self.assertTrue(lesson['notes'])
        self.assertIn('The Lord warned man', lesson['notes'])

    def test_resurrection_format(self):
        """Test parsing the Resurrection lesson format."""
        content = """
# Lesson 3 - Resurrection

April 15, 1905

## Questions

1. Who has the key to the grave? Rev. 1:18. Note 1.
2. What precious promise is made to those who sleep in the grave? Hos. 13:14; Isa. 26:19.
"""
        lessons = MarkdownProcessor.parse_lessons(content)
        
        # Check that we parsed one lesson
        self.assertEqual(len(lessons), 1)
        
        # Check lesson details
        lesson = lessons[0]
        self.assertEqual(lesson['number'], '3')
        self.assertEqual(lesson['title'], 'Resurrection')
        self.assertEqual(lesson['date'], 'April 15, 1905')
        
        # Check questions
        self.assertEqual(len(lesson['questions']), 2)
        self.assertIn('Rev. 1:18', lesson['questions'][0].get('text', ''))
        self.assertIn('Note 1', lesson['questions'][0].get('text', ''))
        self.assertIn('Hos. 13:14', lesson['questions'][1].get('text', ''))

    def test_parse_questions_function(self):
        """Test the parse_questions_from_markdown function."""
        questions_text = """
1. Who came from the East to Jerusalem, shortly after the birth of Christ? Matt. 2:1. *See note 1.*

2. For whom did they inquire? and why? Verse 2.

3. How was man created? What was given him? Gen. 2:7.

4. What answer is given? Verse 12. Ans. — They will not come back from the grave until God wakes them.
"""
        questions = MarkdownProcessor.parse_questions_from_markdown(questions_text)
        
        # Check number of questions
        self.assertEqual(len(questions), 4)
        
        # Check scripture references
        self.assertIn('See note 1', questions[0].get('scripture', ''))
        self.assertIn('Matt. 2:1', questions[0].get('text', ''))
        self.assertIn('Verse 2', questions[1].get('text', ''))
        self.assertIn('Gen. 2:7', questions[2].get('text', ''))
        
        # Check answer
        self.assertEqual(questions[3].get('answer'), 'They will not come back from the grave until God wakes them.')


if __name__ == '__main__':
    unittest.main()