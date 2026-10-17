import copy, unittest
from grammar_catalog import PRESENT, REQUESTS, apply
from add_topics import pack, IT, IT_PHRASES, DAILY, DAILY_PHRASES

class CurriculumTests(unittest.TestCase):
    def test_topic_packs(self):
        for rows, phrases in [(IT,IT_PHRASES),(DAILY,DAILY_PHRASES)]:
            lesson=pack('topic','title',rows,phrases)
            self.assertEqual(len(lesson['words']),20)
            self.assertEqual(len(lesson['phrases']),12)
            self.assertEqual(len(lesson['questions']),96)
            self.assertEqual(len({q['prompt'] for q in lesson['questions']}),96)
            for q in lesson['questions']:
                self.assertTrue(q['explanation'])
                if q['type']=='choice':
                    self.assertIn(q['answer'],q['options'])
                    self.assertEqual(len(q['options']),len(set(q['options'])))
    def test_grammar_does_not_replace_exercises(self):
        lesson=pack('IT','IT',IT,IT_PHRASES)
        original=copy.deepcopy(lesson['questions'])
        apply(lesson)
        self.assertEqual(lesson['questions'],original)
        self.assertEqual(lesson['grammar'],REQUESTS)
    def test_theory_structure(self):
        for g in [PRESENT,REQUESTS]:
            self.assertTrue(g['sources'])
            for s in g['sections']:
                self.assertTrue(s['title'])
                for r in s.get('rows',[]):self.assertEqual(len(r),len(s['columns']))

if __name__=='__main__': unittest.main()
