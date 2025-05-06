###############################################
#####################
###########
# this file is just for testing purposes and its not completed and not all the tests are implemented and its not working properly
###########
#####################
###############################################

import unittest
from corpus import *
from methodes import *
from questionClasses import RawQuestionC, CleanedQuestionC

class TestCorpus(unittest.TestCase):
    def test_init(self):
        corpus = CorpusC("StackOverflow")
        self.assertEqual(corpus.name, "StackOverflow")
        self.assertEqual(corpus.raw_questions, [])
        self.assertEqual(corpus.cleaned_questions, [])
        self.assertEqual(corpus.existing_ids, set())

    def test_fetch_questions(self):
        corpus = CorpusC("StackOverflow")
        access_token = "THA20obO92R6Ypx4rvw18w))"
        api_key = "rl_7QCUyb7FnDge43E41ooisGKHf"
        corpus.fetch_questions(access_token, api_key, pages=2)
        self.assertEqual(len(corpus.raw_questions), 100)
        self.assertEqual(len(corpus.existing_ids), 100)

    def test_load_raw_questions(self):
        corpus = CorpusC("StackOverflow")
        corpus.load_raw_questions()
        self.assertEqual(len(corpus.raw_questions), 100)
        self.assertEqual(len(corpus.existing_ids), 100)

    def test_save_raw_questions(self):
        corpus = CorpusC("StackOverflow")
        corpus.fetch_questions("THA20obO92R6Ypx4rvw18w))", "rl_7QCUyb7FnDge43E41ooisGKHf", pages=2)
        corpus.save_raw_questions()
        corpus2 = CorpusC("StackOverflow")
        corpus2.load_raw_questions()
        self.assertEqual(len(corpus2.raw_questions), 100)
        self.assertEqual(len(corpus2.existing_ids), 100)

    def test_load_cleaned_questions(self):
        corpus = CorpusC("StackOverflow")
        corpus.load_cleaned_questions()
        self.assertEqual(len(corpus.cleaned_questions), 100)

    def test_save_cleaned_questions(self):
        corpus = CorpusC("StackOverflow")
        corpus.fetch_questions("THA20obO92R6Ypx4rvw18w))", "rl_7QCUyb7FnDge43E41ooisGKHf", pages=2)
        corpus.clean_questions()
        corpus.save_cleaned_questions()
        corpus2 = CorpusC("StackOverflow")
        corpus2.load_cleaned_questions()
        self.assertEqual(len(corpus2.cleaned_questions), 100)

    def test_get_question_by_id(self):
        corpus = CorpusC("StackOverflow")
        corpus.fetch_questions(("THA20obO92R6Ypx4rvw18w"), "rl_7QCUyb7FnDge43E41ooisGKHf", pages=2)
        question = corpus.get_question_by_id(79505710)
        self.assertEqual(question.question_id, 79505710)
        
        

if __name__ == "__main__":
    unittest.main()