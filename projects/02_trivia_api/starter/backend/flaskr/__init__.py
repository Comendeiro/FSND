import os
from flask import Flask, request, abort, jsonify
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import *

QUESTIONS_PAGE = 10


def paginate(request, subset, page):
  if page == False:
    page = request.args.get('page', 1, type = int)

  start = (page - 1) * QUESTIONS_PAGE
  end = start + QUESTIONS_PAGE

  quests = [q.format() for q in subset]

  return quests[start:end]



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # set cors for all origines on all the routes
  cors = CORS(app, resources={r"/*": {"origins": "*"}})
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type,Authorization,true'
    )
    response.headers.add(
      'Access-Control-Allow-Methods',
      'GET,PUT,POST,DELETE,OPTIONS'
    )
    return response



  ### MOCK API
  @app.route('/test', methods=['GET'])
  def test_api():
    return jsonify({'hello':'hello world'})




  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    cats = Category.query.all()
    if not cats:
      abort(404)
    return jsonify({
      'success': True,
      'categories': {cat.id:cat.type for cat in cats}
    }), 200


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  @app.route('/questions/<int:page>', methods=['GET'])
  def getQuestions(page=False):
    cats = Category.query.all()

    question = Question.query.all()
    qq = paginate(request,question,page)

    if not qq:
      abort(404)

    return jsonify({
      'questions':qq,
      'categories': {cat.id:cat.type for cat in cats},
      'success': True,
      'total_questions': len(question),
      'next_url': url_for('getQuestions', page=page+1)
    }), 200
    


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:quest_id>', methods=['DELETE'])
  def deleteQuestion(question_id):
    # Checks that question ID is not 0.
    if not question_id:
      abort(400)

    question = Question.query.get(question_id)
    # Checks if question ID exists.
    if not question:
      abort(404)

    try:
      question.delete()
      db.session.commit()

    except:
      db.session.rollback()

      abort(500)

    return jsonify({
      'id': question_id,
      'success': True
      }), 200

 
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def addQuestion():
    req = request.get_json()

    # check validi of request
    if 'question' not in req:
      abort(400)
    if 'answer' not in req:
      abort(400)
    if 'category' not in req:
      abort(400)
    if 'difficulty' not in req:
      abort(400)

    question = req['question']
    answer = req['answer']
    category = req['category']
    difficulty = req['difficulty']

    body = Question(question, answer, category, difficulty)

    try:
      db.session.add(body)
      db.session.commit()
      dataReturn = {
        'id': body.id,
        'question': body.question,
        'answer': body.answer,
        'category': body.category,
        'difficulty': body.difficulty
      }

    except:
      db.session.rollback()
      abort(500)

    return jsonify({
      'question': dataReturn,
      'success': True
    }), 200

  

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def search():
    req = request.get_json()
    searchTerm = req['searchTerm']
    searchData = Question.query.filter(Question.question.like('%'+searchTerm+'%')).all()

    if not searchData:
      abort(404)

    return jsonify({
      'questions': [info.format() for info in searchData],
      'success': True,
      'total_questions': len(searchData)
    }), 200


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category>/questions', methods=['GET'])
  @app.route('/categories/<category>/questions/<int:page>', methods=['GET'])
  def getCategoryQuestions(category, page=False):
    
    # validate category
    catData = False
    if category.isnumeric():
      catData = Category.query.get(category)
      catID = category
    
    if not catData:
      catData = Category.query.filter_by(type=category).first()
      catID = catData.id

    if not catData:
      abort(404)

    # get the questions for the category
    question = Question.query.filter_by(category=catID).all()
    # paginate the questions
    qq = paginate(request,question,page)

    if not qq:
      abort(404)

    return jsonify({
      'questions': qq,
      'success': True,
      'total_questions': len(question),
      'next_url': url_for('getCategoryQuestions', category=category, page=page+1)
    }), 200




  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play():
    req = request.get_json()
    cat = req['category']
    #validate category
    if isinstance(cat, dict):
      catId = int(cat['id]'])
    else:
      catId = int(cat)
    
    # check previous questions
    if 'previous_questions' in req:
      prevQuestion = req['previous_questions']
    else:
      prevQuestion = []

    # query db
    question = Question.query

    if catId is not 0:
      quzCat = Category.query.get(catId)

      if not quzCat:
        abort(404)

      question = question.filter_by(category=catId)

    if prevQuestion:
      question = question.filter(Question.id.notin_(prevQuestion))

    # materialize the query
    question = question.all()

    # abort if nothing left
    if not question:
      abort(404)

    return jsonify({
      'category': cat,
      'previous_questions': prevQuestion,
      'question': random.choice(question).format(),
      'success': True
    }), 200




  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  # handle 400
  @app.errorhandler(400)
  def badRequest(error):
    return jsonify({
      'success': False,
      'error':400,
      'message': 'Bad Request'
    }), 400


  # handle 404
  @app.errorhandler(404)
  def notFound(error):
    return jsonify({
      'success': False,
      'error':404,
      'message': 'Not Found'
    }), 404

  # handle 422
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error':422,
      'message': 'Unprocessable Entity'
    }), 422

  # handle 500
  @app.errorhandler(500)
  def serverError(error):
    return jsonify({
      'success': False,
      'error':500,
      'message': 'Server Error'
    }), 500



  # add-on, home route for testing start
  @app.route('/')
  def home_func():
    return jsonify({'home':'success'})

  return app

    