import unittest
from sabbath_school_reproducer.processor import MarkdownProcessor
import json

class TestWorldlySanctuaryFormat(unittest.TestCase):
    """Test parsing the Worldly Sanctuary lesson format with multiple question sections."""
    
    def test_worldly_sanctuary_format(self):
        """Test parsing a lesson with multiple question sections and an empty preliminary note."""
        content = """
# LESSON 2 — January 12, 1895

## THE WORLDLY SANCTUARY

### INSTRUCTION FOR BUILDING

1. Who gave instruction for building the sanctuary? Ex. 25:1, 8.
2. To whom was this instruction given?
3. Where and at what time was it given? Ex. 24:12-18.
4. What kind of offerings were to be brought for the sanctuary? Ex. 25:2. Note 1.
5. Of what were the offerings to consist? Verses 3-7.
6. For what purpose was the sanctuary to be built? Verse 8.
7. How did Moses know how to make it? Verse 9.
8. Who were called to have the direct supervision of the work? Ex. 31:1-11.
9. How were they fitted for it? Verses 3, 6.
10. Into how many apartments was the sanctuary divided, and what were they called? Ex. 26:33; Heb. 9:2 (margin), 3. See also Revised Version.

### MATERIALS FOR BUILDING

11. Of what were the sides composed? Ex. 26:15. Note 2.
12. Of what length and width were these boards? Verse 16. Note 3.
13. How many boards were there to be on the north and south sides of the tabernacle? Verses 18, 20.
14. How many on the west end? Verse 22. Note 4.
15. Of what did the corners consist? Verse 23.
16. What were all these boards to have in one end? Verse 17.
17. Into what were these tenons to fit? Verses 19, 21, 25.
18. Of what were these sockets made? and how much did they weigh? Ex. 38:27.
19. By what other means were the boards held in position? Ex. 26:26-28.
20. By what means were the bars held in place? Verse 29.
21. With what were the boards and bars overlaid? Verse 29.

### NOTES

1. There is an important lesson for us in the instruction which the Lord gave His people in regard to the offerings for the sanctuary. They were to offer willingly. We are to give "not grudgingly, or of necessity; for God loveth a cheerful giver." 2 Cor. 9:7. We may think, perhaps, that ancient Israel was a very wicked and rebellious people (and they were at times, and especially in the time of Christ), but their liberality in making offerings for the sanctuary is especially mentioned in the Scriptures. Ex. 36:5-7; 1 Chron. 29:9-17. We cannot afford to give grudgingly, or rob God in tithes and offerings, as the Lord declares we have done, and suffer His curse as a result. Mal. 3:8, 9. He wants us to cease robbing Him, that He may pour us out a blessing that we will not have room to receive. Verse 10. When we remember that the Jewish people gave about one-third of all their income to support the work of God ("Testimonies," vol. 3, page 395), and that the early church in the days of the apostles gave all to carry the gospel, we ought to be provoked unto love and good works, cheerfully give of our substance, and take joyfully the spoiling of our goods, knowing that we "have in heaven a better and an enduring substance." Heb. 10:34. And now, as we are right on the borders of the promised land, and can carry nothing over, we should sell and give alms, that we may lay up treasure in heaven, and have our affections and interests center there, instead of being dwellers on the earth. Luke 12:33-36.

2. "Shittim Wood." — The wood of the shittah tree. "A tree that furnished the precious wood of which the ark, tables, altars, boards, etc., of the Jewish tabernacle were made, now believed to have been the wood of the Acacia Seyal, which is hard, fine grained, and yellowish brown in color." — Webster. The original word is translated acacia in the Revised Version.

3. "Cubit." — There is no general agreement among the authorities in regard to the length of the cubit. The variation ranges from eighteen to twenty-two inches, hence the dimensions of the sanctuary and everything connected with it can be easily ascertained approximately in feet and inches.

4. "The sides of the tabernacle westward." Of course on the west there could be but one side, more properly, end. The Revised Version renders this, "The hinder part of the tabernacle westward," which is evidently correct, as the tabernacle faced the east.
        """
        
        lessons = MarkdownProcessor.parse_lessons(content)
        
        # Check that we parsed one lesson
        self.assertEqual(len(lessons), 1)
        
        # Check lesson details
        lesson = lessons[0]
        self.assertEqual(lesson['number'], '2')
        self.assertEqual(lesson['title'], 'THE WORLDLY SANCTUARY')
        self.assertEqual(lesson['date'], 'January 12, 1895')
        
        # Check that preliminary note is empty (this is the key assertion)
        # print(json.dumps(lesson, indent=2))
        self.assertEqual(lesson['preliminary_note'], '')
        
        # Check questions
        self.assertEqual(len(lesson['questions']), 21)
        
        # Check question section headers
        self.assertEqual(len(lesson['question_headers']), 2)
        
        self.assertTrue('INSTRUCTION FOR BUILDING' in lesson['question_headers'])
        self.assertTrue('MATERIALS FOR BUILDING' in lesson['question_headers'])
        
        # Check questions from different sections
        # Check a question from first section
        first_section_question = next((q for q in lesson['questions'] if q['section'] == 'INSTRUCTION FOR BUILDING' and q['text'].startswith('Who gave instruction')), None)
        self.assertIsNotNone(first_section_question)
        self.assertEqual(first_section_question['text'], 'Who gave instruction for building the sanctuary?')
        self.assertEqual(first_section_question['answer'], 'Ex. 25:1, 8.')
        
        # Check a question from second section
        second_section_question = next((q for q in lesson['questions'] if q['section'] == 'MATERIALS FOR BUILDING' and q['text'].startswith('Of what were the sides')), None)
        self.assertIsNotNone(second_section_question)
        self.assertEqual(second_section_question['text'], 'Of what were the sides composed?')
        self.assertEqual(second_section_question['answer'], 'Ex. 26:15. Note 2.')
        
        # Check notes
        self.assertTrue(lesson['notes'])
        self.assertIn('important lesson', lesson['notes'])
        self.assertIn('Shittim Wood', lesson['notes'])
        self.assertIn('Cubit', lesson['notes'])
        
        # Verify no additional sections (notes should not be in additional sections)
        self.assertEqual(len(lesson['additional_sections']), 0)

if __name__ == '__main__':
    unittest.main()