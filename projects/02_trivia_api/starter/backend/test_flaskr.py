import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import *
from models import setup_db, Question, Category



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://postgres:1234@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # initial test to test that the test tests right
    def test_random_first(self):
        res = self.client().get('/test')
        data = json.loads(res.data)
        self.assertEqual(data['hello'], 'hello world')


    def test_get_all_categories(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code,200)

    def test_get_first_page(self):
        res = self.client().get('questions')
        info = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(info['success'])

        self.assertEqual(len(info['questions']), QUESTIONS_PAGE)

        question = Question.query.all()
        self.assertEqual(info['total_questions'], len(question))

    def test_get_second_page(self):
        res = self.client().get('questions/2')
        info = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(info['success'])

        question = Question.query.all()
        self.assertEqual(info['total_questions'], len(question))


    def test_delete_question(self):
        questionId = 3
        res = self.client().delete('questions/{}'.format(questionId))
        info = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(info['success'])
        self.assertEqual(info['id'], questionId)


    def test_return_404_for_non_existing_question(self):
        res = self.client().get('questions/1333330')
        info = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertFalse(info['success'])
        

    def test_create_new_question(self):
        questionData = {
            'question': 'What is the capital of Spain',
            'answer': 'Madrid',
            'category': 1,
            'difficulty': 1
        }

        res = self.client().post(
            '/questions', 
            data = json.dumps(questionData), 
            headers={'Content-Type': 'application/json'}
        )

        info = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(info['success'])
        self.assertEqual(info['question']['question'], questionData['question'])
        self.assertEqual(info['question']['answer'], questionData['answer'])
        self.assertEqual(info['question']['category'], questionData['category'])
        self.assertEqual(info['question']['difficulty'], questionData['difficulty'])

        newQuestion = Question.query.get(info['question']['id'])
        self.assertTrue(newQuestion)


    def test_not_missing_answer(self):
        questionData = {
            'question': 'What is the capital of Spain',
            'category': 1,
            'difficulty': 1
        }

        res = self.client().post(
            '/questions', 
            data = json.dumps(questionData), 
            headers={'Content-Type': 'application/json'}
        )

        info = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertFalse(info['success'])

    def test_non_existing_search(self):
        search = 'safjhsahfsofsa'
        search_json = {
            'searchTerm':search
        }

        res = self.client().post(
            '/search',
             data=json.dumps(search_json),
             headers={'Content-Type': 'application/json'}
        )
        info = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertFalse(info['success'])

    def test_return_random_question(self):
        cat = 4
        quizReq ={
            'category':cat
        }

        res = self.client().post(
            '/quizzes', 
            data=json.dumps(quizReq), 
            headers={'Content-Type': 'application/json'}
        )

        info = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(info['success'])

        self.assertEqual(info['question']['category'], cat)

        retQuestion = Question.query.get(info['question']['id'])
        self.assertEqual(info['question']['category'], retQuestion.category)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()