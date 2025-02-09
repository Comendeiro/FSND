import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink,db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    return jsonify(success=True, drinks=[drink.short() for drink in drinks])

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_long(token):
    drinks = Drink.query.all()
    return jsonify(success=True, drinks=[drink.long() for drink in drinks])


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(data,*args,**kwargs):
    # check if json has been posted
    if request.json is None:
        abort(400)
    
    # load json
    
    jsonData = request.json

    # check if the data is valid and in long format
    if "recipe" not in jsonData:
        abort(400)
    if "title" not in jsonData:
        abort(400)


    # check recipe is in long format
    if "color" not in jsonData["recipe"]:
        abort(400)
    if "name" not in jsonData["recipe"]:
        abort(400)
    if "parts" not in jsonData["recipe"]:
        abort(400)

    # create new drink
    try:
        drink = Drink(title=jsonData["title"], recipe = json.dumps(jsonData["recipe"]))
        drink.insert()
        return jsonify(success=True, drinks=[drink.long()])
    except:
        db.session.rollback()
        abort(500)




'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload,drink_id):
    # check if json has been posted
    if request.json is None:
        abort(400)
    
    # load json
    jsonData = request.json

    # create new drink
    try:
        drink = Drink.query.filter_by(id=drink_id).first()
        if drink is None:
            abort(404)
        
        # update the elements if in json
        if "title" in jsonData:
            drink.title = jsonData["title"]
        if "recipe" in jsonData:
            if "color" in jsonData["recipe"]:
                drink.recipe["color"] = jsonData["recipe"]["color"]
            if "name" in jsonData["recipe"]:
                drink.recipe["name"] = jsonData["recipe"]["name"]
            if "parts" in jsonData["recipe"]:
                drink.recipe["parts"] = jsonData["recipe"]["parts"]

        drink.update()
        return jsonify(success=True, drinks=[drink.long()])

    except:
        db.session.rollback()
        abort(500)




'''re
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.filter_by(id=drink_id).first()
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify(success=True, delete=drink_id)
    except:
        db.session.rollback()
        abort(500)





# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''



'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(500)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "database internal error"
    }), 500


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify({
                    "success": False,
                    "error": ex.status_code,
                    "message": ex.error
                    }), ex.status_code

