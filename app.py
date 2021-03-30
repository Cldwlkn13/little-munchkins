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
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    recipecard = mongo.db.recipes.find_one(
        {"_id": ObjectId("604de9e6104b280ad6fa8464")})
    return render_template("home.html", recipecard=recipecard)


#@app.route("/create")
#def create():
    #return '''
        #<form method="POST" action="/createimg" enctype="multipart/form-data">
        #<input type="file" name="recipe_img">
        #<input type="submit">
    #'''


#@app.route("/createimg", methods=['POST'])
#def createimg():
    #if 'recipe_img' in request.files:
        #recipe_img = request.files['recipe_img']
        #mongo.save_file(recipe_img.filename, recipe_img)
    #return redirect(url_for('create'))


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

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session['user']:
        return render_template("profile.html", username=username)
    return redirect(url_for("login"))


@app.route("/builder", methods=['GET', 'POST'])
def builder():
    return render_template("builder.html")

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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

