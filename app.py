import os
import numpy as np
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, send_from_directory)
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from recipeform import RecipeForm
from app_definitions import AppDefinitions
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DB"] = os.environ.get("MONGO_DB")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = "uploads"
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
Bootstrap(app)
defs = AppDefinitions()


@app.route("/")
@app.route("/home")
def home():
    result = list(mongo.db.recipes.find())
    if result:
        recipecard = result[0]
        recipecard['prep_time'] = defs.calculateTiming(recipecard, "prepare")
        recipecard['cook_time'] = defs.calculateTiming(recipecard, "cook")
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
        myfavourites = []

        for recipecard in myrecipes:
            recipecard['prep_time'] = defs.calculateTiming(
                recipecard, "prepare")
            recipecard['cook_time'] = defs.calculateTiming(recipecard, "cook")
            recipecard['isfavourite'] = defs.isFavourited(user, recipecard)

        if user['favourites']:
            objIds = []

            for _id in user['favourites']:
                if type(_id) is str:
                    objIds.append(ObjectId(str(_id)))

            for objId in objIds:
                recipecard = mongo.db.recipes.find_one({"_id": objId})
                recipecard['prep_time'] = defs.calculateTiming(
                    recipecard, "prepare")
                recipecard['cook_time'] = defs.calculateTiming(
                    recipecard, "cook")
                recipecard['isfavourite'] = defs.isFavourited(
                    user, str(recipecard['_id']))
                myfavourites.append(recipecard)
                myfavourites = list(myfavourites)

        if user and myrecipes and myfavourites:
            return render_template(
                "profile.html", user=user, myrecipes=myrecipes,
                myfavourites=myfavourites)

        elif user and myrecipes and not myfavourites:
            return render_template(
                "profile.html", user=user, myrecipes=myrecipes)

        elif user and myfavourites and not myrecipes:
            return render_template(
                "profile.html", user=user, myfavourites=myfavourites)

        else:
            return render_template(
                "profile.html", user=user)

    return redirect(url_for("login"))


@app.route("/user/edit", methods=['POST'])
def useredit():
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
    session["user"] = request.form.get("username").lower()
    return redirect(url_for(
        "profile", username=session["user"]))


@app.route("/user/delete", methods=['POST'])
def userdelete():
    session.pop('user')
    mongo.db.users.delete_one(
        {"_id": ObjectId(str(request.form.get("_id")))})
    flash("Delete successful")
    return redirect(url_for("home"))


@app.route("/recipes/search", methods=['GET', 'POST'])
def recipesearch():
    form = RecipeForm()
    user = ""
    if request.method == 'POST':
        if session['user']:
            user = mongo.db.users.find_one(
                {"username": session["user"]})

        if form.validate_on_submit() and user != "":
            title = form.title.data.lower()
            months = form.months.data

            if title and not months:
                results = list(mongo.db.recipes.find(
                    {
                        'title': {'$regex': title}
                    }))

            elif months and not title:
                results = list(mongo.db.recipes.find(
                    {
                        'suitableForMinMnths': {'$lte': months},
                        'suitableForMaxMnths': {'$gte': months}
                    }))

            elif not title and not months:
                results = list(mongo.db.recipes.find({}))

            else:
                results = list(mongo.db.recipes.find(
                    {
                        'title': {'$regex': title},
                        'suitableForMinMnths': {'$lte': months},
                        'suitableForMaxMnths': {'$gte': months}
                    }))

            for result in results:
                if defs.isFavourited(user, result['_id']):
                    result['isfavourite'] = True
                else:
                    result['isfavourite'] = False
                result['prep_time'] = defs.calculateTiming(result, "prepare")
                result['cook_time'] = defs.calculateTiming(result, "cook")

            if results:
                _nparr = np.array_split(results, 3)
                if len(results) == 1:
                    return render_template(
                        'search.html', form=form, results_one=_nparr[0])
                elif len(results) == 2:
                    return render_template(
                        'search.html', form=form, results_one=_nparr[0],
                        results_two=_nparr[1])
                else:
                    return render_template(
                        'search.html', form=form, results_one=_nparr[0],
                        results_two=_nparr[1], results_thr=_nparr[2])

    return render_template('search.html', form=form)


@app.route("/recipe/builder", methods=['GET', 'POST'])
def recipebuilder():
    if session.get('user'):
        return render_template("recipe_builder.html")

    flash("Could not identify user")
    return redirect(url_for("home"))


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route("/recipe/add", methods=['POST'])
def recipeadd():
    if session and session['user'] and request.form:
        recipecard = defs.recipeCardBuilder(request.form, session['user'])

        if 'recipe_img' in request.files:
            defs.saveImage(
                request,
                app.config['UPLOAD_EXTENSIONS'],
                app.config['UPLOAD_PATH'])

        mongo.db.recipes.insert_one(recipecard)

        flash(f"{recipecard['title']} has been added to your recipes")
        return redirect(url_for("profile", username=session['user']))
    return redirect(url_for("login"))


@app.route("/recipe/preview", methods=['POST'])
def recipepreview():
    recipecard = defs.recipeCardBuilder(request.form, session['user'])

    recipecard['prep_time'] = defs.calculateTiming(recipecard, "prepare")
    recipecard['cook_time'] = defs.calculateTiming(recipecard, "cook")
    recipecard['context'] = "preview"

    if 'recipe_img' in request.files:
        defs.saveImage(
            request,
            app.config['UPLOAD_EXTENSIONS'],
            app.config['UPLOAD_PATH']
        )

    return render_template("preview.html", recipecard=recipecard)


@app.route("/recipe/edit", methods=['POST'])
def recipeedit():
    objId = ObjectId(str(request.form.get('_id')))
    try:
        recipecard = list(mongo.db.recipes.find(
            {"_id": objId}))
        return render_template("recipe_editor.html", recipecard=recipecard[0])
    except(Exception):
        raise


@app.route("/recipe/edit/cancel", methods=['POST'])
def recipecanceledit():
    if session and session['user']:
        return redirect(url_for(
            "profile", username=session["user"]))
    flash("Could not identify user")
    return redirect(url_for('home'))


@app.route("/recipe/update", methods=['POST'])
def recipeupdate():
    recipecard = defs.recipeCardBuilder(request.form, session['user'])

    if 'recipe_img' in request.files:
        defs.saveImage(
            request,
            app.config['UPLOAD_EXTENSIONS'],
            app.config['UPLOAD_PATH']
        )

    mongo.db.recipes.update_one(
        {"_id": ObjectId(str(request.form.get("_id")))},
        {"$set": recipecard}, upsert=False)

    flash(f'{request.form.get("title")} has been updated')

    return redirect(url_for(
        "profile", username=session["user"]))


@app.route("/recipe/delete", methods=['POST'])
def recipedelete():
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


@app.route("/recipe/favourite", methods=['POST'])
def recipefavourite():
    user = mongo.db.users.find_one(
        {"username": session['user']})
    if user:
        _id = request.form.get('data')
        if defs.isFavourited(user, _id):
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


@app.route("/logout")
def logout():
    flash("You have been logged out")
    if session:
        session.pop('user')
        return redirect(url_for("home"))


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        code = e.code
        return render_template(
            "400_generic.html", e=e, code=code), code
    return render_template("500_generic.html", e=e), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
