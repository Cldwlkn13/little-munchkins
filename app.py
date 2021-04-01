import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, jsonify)
from flask_pymongo import PyMongo, GridFS
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DB"] = os.environ.get("MONGO_DB")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    recipecard = mongo.db.recipes.find_one(
        {"_id": ObjectId("604de9e6104b280ad6fa8464")})
    if recipecard['steps'] is not None:
        prep_time = 0
        cook_time = 0
        for k, step in recipecard['steps'].items():
            if step['type'] == "prepare":
                prep_time = prep_time + step['time']
            elif step['type'] == "cook":
                cook_time = cook_time + step['time']
        recipecard['prep_time'] = prep_time
        recipecard['cook_time'] = cook_time
    return render_template("home.html", recipecard=recipecard)


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route("/get_recipes/<id>")
def get_recipes(id):
    if id == '0':
        recipes = mongo.db.recipes.find()
        return jsonifylist(recipes)
    else:
        recipe = mongo.db.recipes.find({"_id": ObjectId(str(id))})
        return jsonifylist(recipe)


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
            "country": request.form.get("country").lower()
        }
        mongo.db.users.insert_one(register)

        session['user'] = request.form.get("username").lower()
        flash('Regisration Succcessful')
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
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    myrecipes = list(mongo.db.recipes.find(
        {"created_by": session["user"]}))
    for recipecard in myrecipes:
        recipecard['prep_time'] = calculateTiming(recipecard, "prepare")
        recipecard['cook_time'] = calculateTiming(recipecard, "cook")
    if session['user']:
        return render_template(
            "profile.html", user=user, myrecipes=myrecipes)
    return redirect(url_for("login"))


@app.route("/builder", methods=['GET', 'POST'])
def builder():
    if session.get('user'):
        return render_template("builder.html")
    return redirect(url_for("home"))


@app.route("/addrecipe", methods=['GET', 'POST'])
def addrecipe():
    recipecard = recipeCardBuilder(request)
    mongo.db.recipes.insert_one(recipecard)
    if 'recipe_img' in request.files:
        filename = request.files['recipe_img'].filename
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext in app.config['UPLOAD_EXTENSIONS']:
                path = "static/images/public/" + filename
                request.files['recipe_img'].save(path)
    flash(f"{recipecard['title']} has been added to your recipes")
    return redirect(url_for("profile", username=session['user']))


@app.route("/preview", methods=['POST'])
def preview():
    recipecard = recipeCardBuilder(request)
    recipecard['prep_time'] = calculateTiming(recipecard, "prepare")
    recipecard['cook_time'] = calculateTiming(recipecard, "cook")
    if 'recipe_img' in request.files:
        filename = request.files['recipe_img'].filename
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext in app.config['UPLOAD_EXTENSIONS']:
                path = "static/images/public/" + filename
                request.files['recipe_img'].save(path)
    return render_template("preview.html", recipecard=recipecard)


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop('user')
    return redirect(url_for("home"))


def jsonifylist(cursor):
    json_docs = []
    for doc in cursor:
        json_doc = json.dumps(doc, default=json_util.default)
        json_docs.append(json_doc)

    return jsonify(json_docs)


def recipeCardBuilder(request):
    recipecard = {
        "title": request.form.get("title"),
        "desc": request.form.get("desc"),
        "recipe_img": request.files['recipe_img'].filename,
        "created_by": session.get("user"),
        "portions": request.form.get("portions"),
        "suitableForMinMnths": request.form.get("min"),
        "suitableForMaxMnths": request.form.get("max"),
        "ingredients": ingredientsBuilder(
            groupFormKeys(request.form.keys(), "ingredient", 3)),
        "steps": stepsBuilder(
            groupFormKeys(request.form.keys(), "step", 3)),
    }
    return recipecard


def calculateTiming(recipecard, src):
    t = 0
    if recipecard['steps'] is not None:
        for k, step in recipecard['steps'].items():
            if step['type'] == src:
                t = t + int(step['time'])
    return t


def groupFormKeys(keys, keytype, props):
    keys = [key for key in keys if key.startswith(keytype)]
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
            "time": request.form.get("step-" + str(i) + "-time"),
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
                "measure": request.form.get(
                    "ingredient-" + str(i) + "-measure"),
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
