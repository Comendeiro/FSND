# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : 'Science',
'2' : 'Art',
'3' : 'Geography',
'4' : 'History',
'5' : 'Entertainment',
'6' : 'Sports'}

```

# API DOCUMENTATION


## Errors

The supported error messages are:

`400`, `404`, `422`, `500`

Note: All error handlers return a json object with the following structure, indicating the type of error, an explanatory message and whether the request was successful which is expected to be False in error messages.
```
{
    'error': 123,
    'message': 'Error type',
    'success': False
}
```

**400**
- 400 request non-completed due to malformed data, missing arguments.
```
{
	'error': 400,
	'message': 'Bad Request',
	'success': False
}
```
**404**
- 404 error when an item is not found on the database
```
{
	'error': 404,
	'message': 'Not Found',
	'success': False
}
```
**422**
- 422 error when request contains invalid arguments
```
{
	'success': False,
    'error':422,
    'message': 'Unprocessable Entity'
}
```
**500**
- 500 error is returned when the server cannot process something, might be due to database being unavailable or down.
```
{
	'success': False,
    'error':500,
    'message': 'Server Error'
}
```

## Endpoints

The API contains the following endpoints:
+ `GET '/categories'`
+ `GET '/questions'`
+ `POST '/questions'`
+ `POST '/search'`
+ `POST 'quizzes'`
+ `DELETE '/questions/<int:quest_id>'`

**GET '/categories'**
- Gets a dictionary of categories where the keys are the ids and the value is the category.
- Request Arguments: None
- Returns: An object with the key "categories" and a nested dictionary with the key id and the value of the category for each category. 
```
{
	'categories': {
		'1': 'Cat1',
		'2': 'Cat2',
        ...
        '123': 'Cat N',
	},
	'success': True
}
```


**GET '/questions', '/questions/<int:page>'**
- Gets a dictionary of all questions in the database with keys and values for the question answer, difficulty, ID, and category. Includes 'next url' link for the next url in the pagination order. 
- Request Arguments: Page number (Optional).
- Returns: A questions object with the question, answer, question ID, difficult, and category.

```
{
	'answer': 'Example Answer',
	'category': 2,
	'difficulty': 5,
	'id': 1,
	'question': 'Example question?'
}
```

**POST '/questions**
- Writes a new question to the database with question, answer, difficulty, and category.
- ID is given automatically
- Request arguments: Question, answer, category, difficulty level. All are mandatory. Example:
```
{
	'answer': 'Example Answer',
	'category': 2,
	'difficulty': 5,
	'id': 1,
	'question': 'Example question?'
}
```
- Returns: A dictionary including question, answer, category, difficulty, ID, and status.
```
{
	'question': {
		'answer': 'Example Answer',
        'category': 2,
        'difficulty': 5,
        'id': 1,
        'question': 'Example question?'
	},
	'success': True
}
```

**POST '/search'**
- Uses the search term to retrieve questions that include it.
- Request arguments: Search tearm (string), Required.
```
{
	'searchTerm': 'Example'
}
```
- Returns: A json object including all the questions related to the search.
```
{
	'questions': [
		{
			'answer': 'Example Answer',
            'category': 2,
            'difficulty': 5,
            'id': 1,
            'question': 'Example question?'
		}
	],
	'success': True,
	'totalQuestions': 1
}
```

**POST 'quizzes'**
- Gets a random question from a category, avoiding the previous question.
- Request arguments: Category (optional). 
```
{
	'category': 1
}
```
- Returns: JSON with category, previous questions, and a question dictionary object. 
```
{
    'category': 1,
    'previous_questions': [],
    'question': {
        'answer': 'Example Answer',
        'category': 2,
        'difficulty': 5,
        'id': 1,
        'question': 'Example question?'
    },
    'success': True
}
```

**DELETE '/questions/<int:quest_id>'**
- Deletes a question in the database.
- Request argument: Question id.
- Returns: Deleted ID plus status code
```
{
	'id': 1,
	'success': True
}
```
- 


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
