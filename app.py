from common.database import Database
from models.recipes import Recipe
from models.forms import SearchForm
from flask import Flask, render_template, request, Response, session, make_response, jsonify
from flask_wtf import FlaskForm
from env.config import db_config


app = Flask(__name__)
app.config['SECRET_KEY'] = 'soopersecret'

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

#search
@app.route('/search', methods=["GET", "POST"])
def search_template():
    form = SearchForm()
    recipes = []
    if form.validate_on_submit():
        abv = request.form["abv"]
        ibu = request.form["ibu"]
        query = request.form["query"]
        style = request.form["style"]

        conditions = []
        parameters = []

        if query:
            c = '(LOWER(recipes.title) LIKE LOWER(%s) OR LOWER(recipes.type) LIKE LOWER(%s))'
            wildq = '%' + query + '%'
            p = [wildq, wildq]
            conditions.append(c)
            for param in p:
                parameters.append(param)

        if abv:
            if abv == '>10':
                c = 'recipes.abv > %s '
                p = [10]
            else:
                c = 'recipes.abv BETWEEN %s AND %s'
                p = abv.split('-')

            conditions.append(c)
            for param in p:
                parameters.append(float(param))

        if ibu:
            if ibu == '>100':
                c = 'recipes.ibu > %s '
                p = [100]
            else:
                c = 'recipes.ibu BETWEEN %s AND %s'
                p = ibu.split('-')
            conditions.append(c)
            for param in p:
                parameters.append(float(param))

        if style:
            conditions.append("style = ?")
            parameters.append(style)


        q = "WHERE "
        q += " AND ".join(conditions)

        print(q, parameters)

        recipes = Recipe.find_generic(q, parameters)
    return render_template('search.html', form=form, recipes=recipes)

#browse
@app.route('/browse')
def browse_template():
    return render_template('browse.html')

#public API
@app.route('/public_api')
def public_template():
    return render_template('api.html')

#public API Docs
@app.route('/public_api/docs')
def docs_template():
    return render_template('docs.html')

#public API signup
@app.route('/public_api/signup')
def signup_template():
    return render_template('signup.html')

#public API login
@app.route('/public_api/signin')
def signin_template():
    return render_template('signin.html')

#public API account
@app.route('/public_api/account')
def account_template():
    return render_template('account.html')


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