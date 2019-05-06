from common.database import Database
from models.recipes import Recipe
from flask import Flask, render_template, request, Response, session, make_response, jsonify
from itertools import groupby


app = Flask(__name__)
app.secret_key = "beer"


Database.initialize()

# Database.create_tables()



@app.route('/api/recipes')
def recipe_all():
    recipes = Recipe.find_all()
    # print(recipes)
    # grouped_recipes = groupby(recipes, key=lambda each: each['title'])
    # for recipe in grouped_recipes:
    #     print(recipe)
    return Response(recipes, content_type='application/json')
    # return render_template("api.html")


if __name__ == '__main__':
    app.run()