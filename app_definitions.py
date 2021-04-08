import json
import os
from bson import json_util
from flask import jsonify


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

    def recipeCardBuilder(self, requestform, user):
        recipecard = {
            "title": requestform.get("title").lower(),
            "desc": requestform.get("desc").lower(),
            "recipe_img": requestform.get('recipe_img_name').lower(),
            "created_by": user,
            "portions": int(requestform.get("portions")),
            "suitableForMinMnths": int(requestform.get("min")),
            "suitableForMaxMnths": int(requestform.get("max")),
            "ingredients": self.ingredientsBuilder(
                self.groupFormKeys(
                    [key for key in requestform.keys() if key.startswith(
                        "ingredient")]), requestform),
            "steps": self.stepsBuilder(
                self.groupFormKeys(
                    [key for key in requestform.keys() if key.startswith(
                        "step")]), requestform),
        }
        return recipecard

    def saveImage(self, requestform, validExt):
        filename = requestform.files['recipe_img'].filename.lower()
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext in validExt:
                path = "static/images/public/" + filename
                requestform.files['recipe_img'].save(path)

    def calculateTiming(self, recipecard, src):
        t = 0
        if 'steps' in recipecard:
            for k, step in recipecard['steps'].items():
                if step['type'] == src:
                    t = t + int(step['time'])
        return t

    def groupFormKeys(self, keys):
        max_iter = 0
        _dict = dict({})
        mylist = []
        if len(keys) > 0:
            max_iter = int(keys[-1].split("-")[1])

            for x in range(max_iter):
                _dict[x] = []
                for k in keys:
                    _iter = k.split("-")[1]
                    if(int(_iter) == int((x + 1))):
                        _dict[x].append(k)
                if _dict[x]:
                    mylist.append(_dict[x])
        return mylist

    def stepsBuilder(self, groupedkeys, requestform):
        max_iter = 0
        if groupedkeys:
            max_iter = int(groupedkeys[-1][0].split("-")[1]) + 1
        stepslist = []
        for i in range(1, max_iter):
            t = ""
            action = ""
            time = 0

            if "step-" + str(i) + "-type" in requestform:
                t = requestform.get("step-" + str(i) + "-type")

            if "step-" + str(i) + "-desc" in requestform:
                action = requestform.get("step-" + str(i) + "-desc")

            if "step-" + str(i) + "-time" in requestform:
                time = int(requestform.get("step-" + str(i) + "-time"))

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

    def ingredientsBuilder(self, groupedkeys, requestform):
        max_iter = 0
        if groupedkeys:
            max_iter = int(groupedkeys[-1][0].split("-")[1]) + 1
        ingredientslist = []
        for i in range(1, max_iter):
            desc = ""
            measure = 0
            unit = ""

            if "ingredient-" + str(i) + "-desc" in requestform:
                desc = requestform.get("ingredient-" + str(i) + "-desc")

            if "ingredient-" + str(i) + "-measure" in requestform:
                measure = int(requestform.get(
                        "ingredient-" + str(i) + "-measure"))

            if "ingredient-" + str(i) + "-unit" in requestform:
                unit = requestform.get("ingredient-" + str(i) + "-unit")

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
