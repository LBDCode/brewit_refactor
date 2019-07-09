from common.database import Database
from models.recipes import Recipe
from flask import Flask, render_template, request, Response, session, make_response, jsonify
from env.config import db_config


app = Flask(__name__)

Database.initialize(database=db_config['database'], user=db_config['user'], password=db_config['password0'], host=db_config['host'])


#home
@app.route('/')
def home_template():
    recipes = Recipe.find_random(12)
    return render_template('index.html', recipes=recipes)

# specific recipe
@app.route('/recipe/<string:recipe_id>')
def recipe_one(recipe_id):
    recipe = Recipe.find_id(recipe_id)
    print(recipe)
    return render_template('recipe.html', recipe=recipe[0])

@app.route('/api/search/<string:query>')
def api_search(query):
    query = query.split("search/")
    query = query[0].split("&")
    print(query)
    print()
    if query[0].split("=")[0] == 's':
        print(query, "this is a search")
        return render_template("api.html")
    elif query[0].split("=")[0] == 'r':
        result_limit = query[0].split("=")[1]
        return recipe_random(int(result_limit))
    else:
        return render_template("api.html")


@app.route('/api/recipes')
def recipe_all():
    recipes = Recipe.find_all()
    return Response(recipes, content_type='application/json')


def recipe_random(results):
    recipes = Recipe.find_random(results)
    return Response(recipes, content_type='application/json')
    # return render_template("api.html")

@app.route('/type/<string:beer_type>')
def recipe_type(beer_type):
    recipes = Recipe.find_type(beer_type)
    return Response(recipes, content_type='application/json')

def recipe_search(query):
    recipes = Recipe.general_query(query)
    return Response(recipes, content_type='application/json')


if __name__ == '__main__':
    app.run()