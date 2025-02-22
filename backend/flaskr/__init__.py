import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    """
    To get questions per page:
    """
def paginate_questions(request, selections):
  page = request.args.get("page", 1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE 
  
  questions = [question.format() for question in selections]
  current_questions = questions[start:end]

  return current_questions
    
    """
    Successfully Set up CORS. Allowing '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources = {"/": {"origins": "*"}})
    
    """
    Used the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
        return response
    
    """
    CreateD an endpoint to handle GET requests
    for all available categories.
    """

     @app.route('/categories')
     def get_categories():
        
        #To get all the categories:
        
        data = Category.query.all()
        categories = {}
        for category in data:
          categories[category.id] = category.type
        
        # Abort process:to abort 404 if no questions
        if len(data) == 0:
          abort(404)
        
        # Else Return success message        
        return jsonify({
          'success': True,
          'categories': categories
        })

    """
    Created an endpoint to handle GET requests for questions,
    included pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        
       # to get all questions and paginate
        
       selection = Question.query.all()
       total_questions = len(selection)
       current_questions = paginate_questions(request, selection)

       # to get all categories
        
       categories = Category.query.all()
       categories_dict = {}
       for category in categories:
           categories_dict[category.id] = category.type

        # to abort 404 if no questions
        
        if (len(current_questions) == 0):
            abort(404)

        # to return success message
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': categories_dict
        })
    
    """
    Created an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['GET','DELETE'])
    def delete_question(id):
      #delete the question with specified question id

      try:
        question = Question.query.get(id)
        
        # to abort 404 if no questions
        if question is None:
          abort(404)
        question.delete()
      
        # to return success message
        return jsonify({
            'success': True,
            'deleted': id
         })
    
       # Aboort: message unprocessible
       except:
         abort(422)

    """
    Created an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        new_question = data['question']
        insert_answer = data['answer']
        insert_difficulty = data['difficulty']
        insert_category = data['category']

        if (len(new_question)==0) or (len(insert_answer)==0) or (len(insert_answer)==0) or (len(insert_answer)==0):
          abort(422)

        question = Question(
          question = new_question,
          answer = insert_answer,
          category=insert_category,
          difficulty=insert_difficulty
        )
        question.insert()
  
        all_questions = Question.query.all()
        current_questions = paginate_questions(request, all_questions)

        # to return success and message
        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'total_questions': len(all_questions)
        })
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

