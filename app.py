import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, jsonify)
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets.html5 import NumberInput
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DB"] = os.environ.get("MONGO_DB")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
Bootstrap(app)


class RecipeForm(FlaskForm):
    title = StringField(
        'Search recipes by name', validators=[DataRequired()])
    months = IntegerField(
        "Age (months)", validators=[Optional()], widget=NumberInput())
    submit = SubmitField('Submit')


@app.route("/")
@app.route("/home")
def home():
    result = list(mongo.db.recipes.find())
    if result:
        recipecard = result[0]
        recipecard['prep_time'] = calculateTiming(recipecard, "prepare")
        recipecard['cook_time'] = calculateTiming(recipecard, "cook")
        return render_template("home.html", recipecard=recipecard)
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(
                request.form.get("password")),
            "email": request.form.get("email"),
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "dob": request.form.get("dob"),
            "country": request.form.get("country").lower(),
            "favourites": []
        }
        mongo.db.users.insert_one(register)
        session['user'] = request.form.get("username").lower()

        return redirect(url_for("profile", username=session['user']))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                        "profile", username=session["user"]))

            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for('login'))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for('login'))

    if session.get('user'):
        return redirect(url_for(
            "profile", username=session["user"]))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if session['user']:
        user = mongo.db.users.find_one(
            {"username": session["user"]})
        myrecipes = list(mongo.db.recipes.find(
            {"created_by": session["user"]}))

        for recipecard in myrecipes:
            recipecard['prep_time'] = calculateTiming(recipecard, "prepare")
            recipecard['cook_time'] = calculateTiming(recipecard, "cook")
            recipecard['isfavourite'] = isFavourited(user, recipecard)

        if user['favourites']:
            objIds = []
            myfavourites = []

            for _id in user['favourites']:
                if type(_id) is str:
                    objIds.append(ObjectId(str(_id)))

            for objId in objIds:
                recipecard = mongo.db.recipes.find_one({"_id": objId})
                recipecard['prep_time'] = calculateTiming(
                    recipecard, "prepare")
                recipecard['cook_time'] = calculateTiming(recipecard, "cook")
                recipecard['isfavourite'] = isFavourited(
                    user, str(recipecard['_id']))
                myfavourites.append(recipecard)
                myfavourites = list(myfavourites)
            return render_template(
                "profile.html", user=user, myrecipes=myrecipes,
                myfavourites=myfavourites)
        return render_template("profile.html", user=user, myrecipes=myrecipes)
    return redirect(url_for("login"))


@app.route("/edituser", methods=['POST'])
def edituser():
    user = dict(request.form)
    user.pop('_id')
    if len(user['favourites']) == 2:
        user['favourites'] = []
    else:
        user['favourites'] = user['favourites'].replace("[", "").replace(
            "]", "").replace("'", "").split(",")

    mongo.db.users.update_one(
        {"_id": ObjectId(str(request.form.get("_id")))},
        {"$set": user}, upsert=False)
    return redirect(url_for(
        "profile", username=session["user"]))


@app.route("/deleteuser", methods=['POST'])
def deleteuser():
    session.pop('user')
    mongo.db.users.delete_one(
        {"_id": ObjectId(str(request.form.get("_id")))})
    flash("Delete successful")
    return redirect(url_for("home"))


@app.route("/search", methods=['GET', 'POST'])
def search():
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    form = RecipeForm()

    if form.validate_on_submit() or not user:
        title = form.title.data.lower()
        months = form.months.data

        if months:
            results = list(mongo.db.recipes.find(
                {
                    'title': {'$regex': title},
                    'suitableForMinMnths': {'$lte': months},
                    'suitableForMaxMnths': {'$gte': months}
                }))
        else:
            results = list(mongo.db.recipes.find(
                {'title': {'$regex': title}}))

        for result in results:
            if isFavourited(user, result['_id']):
                result['isfavourite'] = True
            else:
                result['isfavourite'] = False
            result['prep_time'] = calculateTiming(result, "prepare")
            result['cook_time'] = calculateTiming(result, "cook")
        return render_template('search.html', form=form, results=results)
    return render_template('search.html', form=form)


@app.route("/recipebuilder", methods=['GET', 'POST'])
def recipebuilder():
    if session.get('user'):
        return render_template("recipe_builder.html")
    flash("Could not identify user")
    return redirect(url_for("home"))


@app.route("/addrecipe", methods=['POST'])
def addrecipe():
    recipecard = recipeCardBuilder(request)
    mongo.db.recipes.insert_one(recipecard)
    if 'recipe_img' in request.files:
        filename = request.files['recipe_img'].filename
        if filename != "":
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in app.config['UPLOAD_EXTENSIONS']:
                path = "static/images/public/" + filename.lower()
                request.files['recipe_img'].save(path)
    flash(f"{recipecard['title']} has been added to your recipes")
    return redirect(url_for("profile", username=session['user']))


@app.route("/previewrecipe", methods=['POST'])
def preview():
    recipecard = recipeCardBuilder(request)
    recipecard['prep_time'] = calculateTiming(recipecard, "prepare")
    recipecard['cook_time'] = calculateTiming(recipecard, "cook")
    recipecard['context'] = "preview"
    if 'recipe_img' in request.files:
        filename = request.files['recipe_img'].filename
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext in app.config['UPLOAD_EXTENSIONS']:
                path = "static/images/public/" + filename
                request.files['recipe_img'].save(path)
    return render_template("preview.html", recipecard=recipecard)


@app.route("/editrecipe", methods=['POST'])
def editrecipe():
    objId = ObjectId(str(request.form.get('_id')))
    recipecard = mongo.db.recipes.find_one(
        {"_id": objId})
    return render_template("recipe_editor.html", recipecard=recipecard)


@app.route("/updaterecipe", methods=['POST'])
def updaterecipe():
    recipecard = recipeCardBuilder(request)
    mongo.db.recipes.update_one(
        {"_id": ObjectId(str(request.form.get("_id")))},
        {"$set": recipecard}, upsert=False)
    flash(f'{request.form.get("title")} has been updated')
    return redirect(url_for(
        "profile", username=session["user"]))


@app.route("/deleterecipe", methods=['POST'])
def deleterecipe():
    mongo.db.recipes.delete_one(
        {"_id": ObjectId(str(request.form.get("_id")))})
    users = list(mongo.db.users.find(
        {"favourites": str(request.form.get("_id"))}))

    for user in users:
        _list = list(user['favourites'])

        for _recipeid in _list:
            if(_recipeid == str(request.form.get("_id"))):
                _list.remove(_recipeid)
        mongo.db.users.update_one(
            {"_id": ObjectId(str(user["_id"]))},
            {"$set": {"favourites": _list}})
    flash(f'{request.form.get("title")} has been deleted')
    return redirect(url_for(
        "profile", username=session["user"]))


@app.route("/favouriterecipe", methods=['POST'])
def addfavourite():
    user = mongo.db.users.find_one(
        {"username": session['user']})
    if user:
        _id = request.form.get('data')
        if isFavourited(user, _id):
            user['favourites'].remove(_id)
            mongo.db.users.update_one(
                {"_id": user['_id']},
                {"$set": user}, upsert=False)
            return ("False", 200)
        user['favourites'].append(_id)
        mongo.db.users.update_one(
                {"_id": user['_id']},
                {"$set": user}, upsert=False)
        return ("True", 200)
    flash("Could not identify user")
    return redirect(url_for('home'))


@app.route("/canceleditrecipe", methods=['POST'])
def canceledit():
    if session['user']:
        return redirect(url_for(
            "profile", username=session["user"]))
    flash("Could not identify user")
    return redirect(url_for('home'))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop('user')
    return redirect(url_for("home"))


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return render_template("500_generic.html", e=e), 500


def jsonifylist(cursor):
    json_docs = []
    for doc in cursor:
        json_doc = json.dumps(doc, default=json_util.default)
        json_docs.append(json_doc)
    return jsonify(json_docs)


def recipeCardBuilder(request):
    recipecard = {
        "title": request.form.get("title").lower(),
        "desc": request.form.get("desc").lower(),
        "recipe_img": request.form.get('recipe_img_name'),
        "created_by": session.get("user"),
        "portions": int(request.form.get("portions")),
        "suitableForMinMnths": int(request.form.get("min")),
        "suitableForMaxMnths": int(request.form.get("max")),
        "ingredients": ingredientsBuilder(
            groupFormKeys(
                [key for key in request.form.keys() if key.startswith(
                    "ingredient")], 3)),
        "steps": stepsBuilder(
            groupFormKeys(
                [key for key in request.form.keys() if key.startswith(
                    "step")], 3)),
    }
    return recipecard


def isFavourited(user, _id):
    if 'favourites' in user:
        if str(_id) in user['favourites']:
            return True
    return False


def calculateTiming(recipecard, src):
    t = 0
    if 'steps' in recipecard:
        for k, step in recipecard['steps'].items():
            if step['type'] == src:
                t = t + int(step['time'])
    return t


def groupFormKeys(keys, props):
    requestedcount = int(len(keys) / props)
    mylist = []
    for x in range(requestedcount):
        mylist2 = []
        for k in keys:
            _iter = k.split("-")[1]
            if(int(_iter) == int((x + 1))):
                mylist2.append(k)
        mylist.append(mylist2)
    return mylist


def stepsBuilder(groupedkeys):
    i = 1
    stepslist = []
    for s in groupedkeys:
        step = {
            "type": request.form.get("step-" + str(i) + "-type"),
            "action": request.form.get("step-" + str(i) + "-desc"),
            "time": float(request.form.get("step-" + str(i) + "-time")),
        }
        stepslist.append(step)
        i = i + 1

    stepsdict = {}
    i = 0
    for s in stepslist:
        stepsdict.update({str(i): s})
        i = i + 1
    return stepsdict


def ingredientsBuilder(groupedkeys):
    i = 1
    ingredientslist = []
    for s in groupedkeys:
        ingredient = {
            "name": request.form.get("ingredient-" + str(i) + "-desc"),
            "qty": {
                "measure": int(request.form.get(
                    "ingredient-" + str(i) + "-measure")),
                "unit": request.form.get("ingredient-" + str(i) + "-unit")
            }
        }
        ingredientslist.append(ingredient)
        i = i + 1

    ingredientsdict = {}
    i = 0
    for s in ingredientslist:
        ingredientsdict.update({str(i): s})
        i = i + 1
    return ingredientsdict


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
