from common.database import Database
from models.recipes import Recipe
from flask import Flask, render_template, request, Response, session, make_response, jsonify
from env.config import db_config


app = Flask(__name__)

Database.initialize(database=db_config['database'], user=db_config['user'], password=db_config['password0'], host=db_config['host'])

# Database.create_tables()


@app.route('/api/recipes')
def recipe_all():
    recipes = Recipe.find_all()
    return Response(recipes, content_type='application/json')


@app.route('/random/<int:results>')
def recipe_random(results):
    recipes = Recipe.find_random(results)
    # return Response(recipes, content_type='application/json')
    return render_template("api.html")


if __name__ == '__main__':
    app.run()