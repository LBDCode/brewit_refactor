# from brewit.models.recipes import Recipe
#from brewit.models.recipes2 import Recipe2
from brewit.models.users import User
from brewit import app, db, bcrypt
from brewit.models.forms import SearchForm, SimpleSearchForm, TypeForm, SignupForm, LoginForm
from flask import render_template, request, Response, flash, redirect, url_for



#home
@app.route('/')
def home_template():
    styles = ['brown', 'ipa',  'amber', 'lager', 'cider', 'belgian', 'stout']
    form = SimpleSearchForm()
    typeForm = TypeForm()
    # recipes = Recipe.find_random(12)
    return render_template('index.html', styles=styles, form=form, typeform=typeForm, recipes=[])

# specific recipe
@app.route('/recipe/<string:recipe_id>')
def recipe_one(recipe_id):
    #recipe = Recipe.find_id(recipe_id)
    return render_template('recipe.html', recipe=[])

#search
@app.route('/search', methods=["GET", "POST"])
def search_template():
    return render_template('browse.html')
#     form = SearchForm()
#     simpleForm = SimpleSearchForm()
#     typeForm = TypeForm()
#     recipes = []
#     conditions = []
#     parameters = []
#     query = request.form.get("query")
#     styles = ['brown', 'ipa',  'amber', 'lager', 'cider', 'belgian', 'stout']
#
#     if typeForm.validate_on_submit():
#         if (form.submitAdvanced.data is False) and (simpleForm.submitSimple.data is False):
#             for style in styles:
#                 if typeForm[style].data:
#                     query = style
#                     form.query.data = style
#
#             if query:
#                 c = '(LOWER(recipes.title) LIKE LOWER(%s) OR LOWER(recipes.type) LIKE LOWER(%s))'
#                 wildq = '%' + query + '%'
#                 p = [wildq, wildq]
#                 conditions.append(c)
#                 for param in p:
#                     parameters.append(param)
#             q = "WHERE "
#             q += " AND ".join(conditions)
#
#             recipes = Recipe.find_generic(q, parameters)
#
#
#
#     if simpleForm.validate_on_submit():
#         if simpleForm.submitSimple.data:
#             if query:
#                 c = '(LOWER(recipes.title) LIKE LOWER(%s) OR LOWER(recipes.type) LIKE LOWER(%s))'
#                 wildq = '%' + query + '%'
#                 p = [wildq, wildq]
#                 conditions.append(c)
#                 for param in p:
#                     parameters.append(param)
#             q = "WHERE "
#             q += " AND ".join(conditions)
#
#             recipes = Recipe.find_generic(q, parameters)
#
#
#     if form.validate_on_submit():
#         if form.submitAdvanced.data:
#             abv = request.form.get("abv")
#             ibu = request.form.get("ibu")
#             query = request.form.get("query")
#             style = request.form.get("style")
#
#             if query:
#                 c = '(LOWER(recipes.title) LIKE LOWER(%s) OR LOWER(recipes.type) LIKE LOWER(%s))'
#                 wildq = '%' + query + '%'
#                 p = [wildq, wildq]
#                 conditions.append(c)
#                 for param in p:
#                     parameters.append(param)
#
#             if abv:
#                 if abv == '>10':
#                     c = 'recipes.abv > %s '
#                     p = [10]
#                 else:
#                     c = 'recipes.abv BETWEEN %s AND %s'
#                     p = abv.split('-')
#
#                 conditions.append(c)
#                 for param in p:
#                     parameters.append(float(param))
#
#             if ibu:
#                 if ibu == '>100':
#                     c = 'recipes.ibu > %s '
#                     p = [100]
#                 else:
#                     c = 'recipes.ibu BETWEEN %s AND %s'
#                     p = ibu.split('-')
#                 conditions.append(c)
#                 for param in p:
#                     parameters.append(float(param))
#
#             if style:
#                 wilds = '%' + style + '%'
#                 conditions.append("LOWER(recipes.type) LIKE LOWER(%s)")
#                 parameters.append(wilds)
#
#             q = "WHERE "
#             q += " AND ".join(conditions)
#
#             recipes = Recipe.find_generic(q, parameters)
#
#     return render_template('search.html', form=form, recipes=recipes)

#browse
@app.route('/browse')
def browse_template():
    return render_template('browse.html')

#public API
@app.route('/public_api', methods=["GET", "POST"])
def public_template():
    return render_template('api.html')

#public API Docs
@app.route('/public_api/docs')
def docs_template():
    return render_template('docs.html')

#public API signup
@app.route('/public_api/signup', methods=["GET", "POST"])
def signup_template():
    form = SignupForm()
    if form.validate_on_submit():
        user = request.form.get("user_name")
        email = request.form.get("email")
        hashed = bcrypt.generate_password_hash(request.form.get("password")).decode("utf-8")
        new_user = User(username=user, email=email, password=hashed)
        db.session.add(new_user)
        db.session.commit()
        message = 'Account created, ' + user + '.  You can now log in.'
        flash(message, 'success')
        return redirect(url_for('signin_template'))
    return render_template('signup.html', form=form)

#public API login
@app.route('/public_api/signin', methods=["GET", "POST"])
def signin_template():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        print(email)
        if email == 'admin@test.com':
            message = 'Welcome back, ' + email + '!'
            flash(message, 'success')
            return redirect(url_for('public_template'))
        else:
            print(email)
    return render_template('signin.html', form=form)

#public API account
@app.route('/public_api/account')
def account_template():
    return render_template('account.html')


@app.route('/api/search/<string:query>')
def api_search(query):
    query = query.split("search/")
    query = query[0].split("&")
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

