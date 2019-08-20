from brewit.models.recipes2 import Recipe2
from brewit.models.users import User
from brewit.models.ingredients2 import Ingredient2
from brewit import app, db, bcrypt, mail
from brewit.models.forms import SearchForm, SimpleSearchForm, TypeForm, SignupForm, LoginForm, UpdateForm, UpdateKey, \
    ResetRequest, ResetPassword
from flask import render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func, text
from uuid import uuid4
import json
from flask_mail import Message


# home
@app.route('/')
def home_template():
    styles = ['brown', 'ipa', 'amber', 'lager', 'cider', 'belgian', 'stout']
    form = SimpleSearchForm()
    typeForm = TypeForm()
    recipes = Recipe2.query.order_by(func.random()).limit(12)
    return render_template('index.html', styles=styles, form=form, typeform=typeForm, recipes=recipes)


# specific recipe
@app.route('/recipe/<string:recipe_id>')
def recipe_one(recipe_id):
    recipe = Recipe2.query.filter_by(recipe_id=recipe_id).first()
    return render_template('recipe.html', recipe=recipe)


# search
@app.route('/search', methods=["GET", "POST"])
def search_template():
    form = SearchForm()
    simpleForm = SimpleSearchForm()
    typeForm = TypeForm()
    recipes = []
    conditions = []
    parameters = []
    query = request.form.get("query")
    styles = ['brown', 'ipa', 'amber', 'lager', 'cider', 'belgian', 'stout']

    if typeForm.validate_on_submit():
        if (form.submitAdvanced.data is False) and (simpleForm.submitSimple.data is False):
            for style in styles:
                if typeForm[style].data:
                    query = '%' + style + '%'
                    form.query.data = style

            recipes = Recipe2.query.filter((Recipe2.type.ilike(query)) | (Recipe2.title.ilike(query))).all()

    if simpleForm.validate_on_submit():
        if simpleForm.submitSimple.data:
            form.query.data = query
            query = '%' + query + '%'
            recipes = Recipe2.query.filter((Recipe2.type.ilike(query)) | (Recipe2.title.ilike(query))).all()

    if form.validate_on_submit():
        if form.submitAdvanced.data:
            abv = request.form.get("abv")
            ibu = request.form.get("ibu")
            query = request.form.get("query")
            style = request.form.get("style")

            q = Recipe2.query

            if query:
                wildq = '%' + query + '%'
                q = q.filter((Recipe2.type.ilike(wildq)) | (Recipe2.title.ilike(wildq)))
            if style:
                wilds = '%' + style + '%'
                q = q.filter(Recipe2.type.ilike(wilds))
            if abv:
                if abv == '>10':
                    q = q.filter(Recipe2.abv >= 10)
                else:
                    min, max = abv.split('-')
                    q = q.filter(Recipe2.abv.between(min, max))
            if ibu:
                if ibu == '>100':
                    q = q.filter(Recipe2.ibu >= 100)
                else:
                    min, max = ibu.split('-')
                    q = q.filter(Recipe2.ibu.between(min, max))

        recipes = q.all()
    return render_template('search.html', form=form, recipes=recipes)


# browse
@app.route('/browse')
def browse_template():
    return render_template('browse.html')


# public API
@app.route('/public_api', methods=["GET", "POST"])
def public_template():
    return render_template('api.html', auth_status=current_user.is_authenticated)


# public API Docs
@app.route('/public_api/docs')
def docs_template():
    return render_template('docs.html', auth_status=current_user.is_authenticated)


# public API signup
@app.route('/public_api/signup', methods=["GET", "POST"])
def signup_template():
    form = SignupForm()
    if form.validate_on_submit():
        user = request.form.get("username")
        email = request.form.get("email")
        hashed = bcrypt.generate_password_hash(request.form.get("password")).decode("utf-8")
        new_user = User(username=user, email=email, password=hashed)
        db.session.add(new_user)
        db.session.commit()
        message = 'Account created, ' + user + '.  You can now log in.'
        flash(message, 'success')
        return redirect(url_for('signin_template'))
    return render_template('signup.html', form=form, auth_status=current_user.is_authenticated)


# public API login
@app.route('/public_api/signin', methods=["GET", "POST"])
def signin_template():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get("password")):
            login_user(user)
            redir = request.args.get('next') if request.args.get('next') else url_for('public_template')
            return redirect(redir)
        else:
            message = 'Login unsuccessful.'
            flash(message, 'danger')

    return render_template('signin.html', form=form, auth_status=current_user.is_authenticated)


# public API account
@app.route('/public_api/account', methods=["GET", "POST"])
@login_required
def account_template():
    form = UpdateForm()
    keyForm = UpdateKey()

    if form.validate_on_submit():
        if keyForm.submitNewKey.data is False:
            current_user.username = request.form.get("username")
            current_user.email = request.form.get("email")
            db.session.commit()
            message = 'Account updated successfully.'
            flash(message, 'success')
            return redirect(url_for('account_template'))
    elif keyForm.validate_on_submit():
        if form.submitUpdate.data is False:
            newkey = uuid4()
            current_user.key = newkey
            db.session.commit()
            message = 'API key updated successfully.'
            flash(message, 'success')
            return redirect(url_for('account_template'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

    return render_template('account.html', auth_status=current_user.is_authenticated, form=form, keyform=keyForm)

def send_reset(user):
    token = user.pw_reset_token()
    message = Message('brewIt Password Reset Request',
                      sender='brewit.mailer@gmail.com',
                      recipients=[user.email])
    message.body = f'''To reset your password, visit the following link:
{url_for('reset_template', token=token, _external=True)}

If you did not request a password reset, please disregard this email.  No changes will be made to your brewIt account.
    '''
    print(user.email)
    mail.send(message)

#public API password reset request
@app.route('/reset_password', methods=["GET", "POST"])
def request_template():
    reqform = ResetRequest()
    if reqform.validate_on_submit():
        user = User.query.filter_by(email=reqform.emailReq.data).first()
        send_reset(user)
        flash('An email has been sent with password reset instructions', 'info')
        return redirect(url_for('signin_template'))
    return render_template('request.html', auth_status=current_user.is_authenticated, reqform=reqform)

#public API password reset request
@app.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_template(token):
    user = User.verify_pw_reset(token)
    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('request_template'))
    resetform = ResetPassword()
    if resetform.validate_on_submit():
        pw = request.form.get("password")
        hashed = bcrypt.generate_password_hash(pw).decode("utf-8")
        user.password = hashed
        db.session.commit()
        message = 'Your password has been reset.  You can now log in.'
        flash(message, 'success')
        return redirect(url_for('signin_template'))
    return render_template('reset.html', auth_status=current_user.is_authenticated, resetform=resetform)

# public API logout
@app.route('/public_api/logout')
def logout_template():
    logout_user()
    return redirect(url_for('public_template'))


@app.route('/api/<string:query>')
def api_search(query):
    key = request.args.get("key")
    search = request.args.get("s")
    random = request.args.get("r")
    style = request.args.get("type")
    low_ibu = request.args.get("low-ibu")
    high_ibu = request.args.get("high-ibu")
    low_abv = request.args.get("low-abv")
    high_abv = request.args.get("high-abv")
    limit = request.args.get("limit")
    offset = request.args.get("offset")
    recipes = []

    #check key
    try:
        user = User.query.filter_by(key=key).first()
        user.account_active = True
    except:
        abort(400, {'Missing or incorrect API key'})

    #check query has search or random parameter
    try:
        if search or int(random) > 0:
            pass
    except:
        abort(400, {'Query must have search or random parameter'})

    #check abv and ibu parameters are numbers, if they exist
    for param in [low_ibu, high_ibu, low_abv, high_abv]:
        if param:
            try:
                float(param)
            except:
                abort(400, {'ABV and IBU parameters must be numbers'})

    # check limit and offset params are ints, if they exist
    for param in [limit, offset]:
        if param:
            try:
                int(param)
            except:
                abort(400, {'Limit and offset parameters must be integers'})

    #if try/excepts pass, build query
    q = Recipe2.query
    if search or (search and random):
        print(search, "this is a search")
        if search:
            wildq = '%' + search + '%'
            q = q.filter((Recipe2.type.ilike(wildq)) | (Recipe2.title.ilike(wildq)))
        if style:
            wilds = '%' + style + '%'
            q = q.filter(Recipe2.type.ilike(wilds))
        if low_abv or high_abv:
            if low_abv and high_abv:
                q = q.filter(Recipe2.abv.between(low_abv, high_abv))
            elif low_abv:
                q = q.filter(Recipe2.abv >= low_abv)
            elif high_abv:
                q = q.filter(Recipe2.abv <= high_abv)
        if low_ibu or high_ibu:
            if low_ibu and high_ibu:
                q = q.filter(Recipe2.ibu.between(low_ibu, high_ibu))
            elif low_ibu:
                q = q.filter(Recipe2.ibu >= low_ibu)
            elif high_ibu:
                q = q.filter(Recipe2.ibu <= high_ibu)
        if limit:
            limit = int(limit)
            if limit <= 50:
                result_limit = limit
            else:
                result_limit = 50
            q = q.limit(result_limit)
        if offset:
            offset = int(offset)
            q = q.offset(offset)
        recipes = q.all()
    elif random:
        random = int(random)
        if random <= 50:
            result_limit = random
        else:
            result_limit = 50
        recipes = q.order_by(func.random()).limit(result_limit)

    result = json.dumps(Recipe2.jsonify_data(recipes))
    return Response(result, content_type='application/json')


@app.route('/type/<string:beer_type>')
def recipe_type(beer_type):
    recipes = Recipe.find_type(beer_type)
    return Response(recipes, content_type='application/json')


def recipe_search(query):
    recipes = Recipe.general_query(query)
    return Response(recipes, content_type='application/json')
