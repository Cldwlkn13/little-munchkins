import json
from bson import json_util
from flask import request, jsonify


class AppDefinitions(object):
    def isFavourited(self, user, _id):
        if 'favourites' in user:
            if str(_id) in user['favourites']:
                return True
        return False

    def jsonifylist(self, cursor):
        json_docs = []
        for doc in cursor:
            json_doc = json.dumps(doc, default=json_util.default)
            json_docs.append(json_doc)
        return jsonify(json_docs)

    def recipeCardBuilder(self, formrequest, user):
        recipecard = {
            "title": request.form.get("title").lower(),
            "desc": request.form.get("desc").lower(),
            "recipe_img": request.form.get('recipe_img_name'),
            "created_by": user,
            "portions": int(request.form.get("portions")),
            "suitableForMinMnths": int(request.form.get("min")),
            "suitableForMaxMnths": int(request.form.get("max")),
            "ingredients": self.ingredientsBuilder(
                self.groupFormKeys(
                    [key for key in request.form.keys() if key.startswith(
                        "ingredient")], 3), request),
            "steps": self.stepsBuilder(
                self.groupFormKeys(
                    [key for key in request.form.keys() if key.startswith(
                        "step")], 3), request),
        }
        return recipecard

    def calculateTiming(self, recipecard, src):
        t = 0
        if 'steps' in recipecard:
            for k, step in recipecard['steps'].items():
                if step['type'] == src:
                    t = t + int(step['time'])
        return t

    def groupFormKeys(self, keys, props):
        max_iter = 0
        if keys:
            max_iter = int(keys[-1].split("-")[1])
        _dict = dict({})
        mylist = []
        for x in range(max_iter):
            _dict[x] = []
            for k in keys:
                _iter = k.split("-")[1]
                if(int(_iter) == int((x + 1))):
                    _dict[x].append(k)
            if _dict[x]:
                mylist.append(_dict[x])
        return mylist

    def stepsBuilder(self, groupedkeys, request):
        max_iter = 0
        if groupedkeys:
            max_iter = int(groupedkeys[-1][0].split("-")[1]) + 1
        stepslist = []
        for i in range(1, max_iter):
            t = ""
            action = ""
            time = 0

            if "step-" + str(i) + "-type" in request.form:
                t = request.form.get("step-" + str(i) + "-type")

            if "step-" + str(i) + "-desc" in request.form:
                action = request.form.get("step-" + str(i) + "-desc")

            if "step-" + str(i) + "-time" in request.form:
                time = int(request.form.get("step-" + str(i) + "-time"))

            step = {}
            if action != "":
                step = {
                    "type": t,
                    "action": action,
                    "time": time,
                }
                stepslist.append(step)

        stepsdict = {}
        i = 0
        for s in stepslist:
            stepsdict.update({str(i): s})
            i = i + 1
        return stepsdict

    def ingredientsBuilder(self, groupedkeys, request):
        max_iter = 0
        if groupedkeys:
            max_iter = int(groupedkeys[-1][0].split("-")[1]) + 1
        ingredientslist = []
        for i in range(1, max_iter):
            desc = ""
            measure = 0
            unit = ""

            if "ingredient-" + str(i) + "-desc" in request.form:
                desc = request.form.get("ingredient-" + str(i) + "-desc")

            if "ingredient-" + str(i) + "-measure" in request.form:
                measure = int(request.form.get(
                        "ingredient-" + str(i) + "-measure"))

            if "ingredient-" + str(i) + "-unit" in request.form:
                unit = request.form.get("ingredient-" + str(i) + "-unit")

            ingredient = {}
            if desc != "":
                ingredient = {
                    "name": desc,
                    "qty": {
                        "measure": measure,
                        "unit": unit
                    }
                }
                ingredientslist.append(ingredient)

        ingredientsdict = {}
        i = 0
        for s in ingredientslist:
            ingredientsdict.update({str(i): s})
            i = i + 1
        return ingredientsdict
