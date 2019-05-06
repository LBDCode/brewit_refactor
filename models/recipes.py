from common.database import ConnectionFromPool
import json
from itertools import groupby

class Recipe:
    def __init__(self, title, type, image_url, beer_url, batch, original_gravity, final_gravity, abv, ibu, directions, recipe_id):
        self.title = title
        self.type = type
        self.image_url = image_url
        self.beer_url = beer_url
        self.batch = batch
        self.original_gravity = original_gravity
        self.final_gravity = final_gravity
        self.abv = abv
        self.ibu = ibu
        self.directions = directions
        self.recipe_id = recipe_id


    # def __repr__(self):
    #      return "<Recipe {}>".format(self.title)

    def save_to_db(self):
        with ConnectionFromPool() as cursor:
                cursor.execute("INSERT INTO recipes(title, type, image_url, beer_url, batch, original_gravity, final_gravity, abv, ibu, directions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                               (self.title, self.type, self.image_url, self.beer_url, self.batch, self.original_gravity, self.final_gravity, self.abv, self.ibu, self.directions))


    @staticmethod
    def jsonify_data(data):
        result = []
        for recipe_id, recipes in groupby(data, key=lambda each: each['recipe_id']):
            recipes = list(recipes)
            recipe = recipes[0].copy()
            recipe_dictionary = {'recipe_id': recipe['recipe_id'], 'title': recipe['title'], 'type': recipe['type'],
                                 'image_url': recipe['image_url'], 'beer_url': recipe['beer_url'],
                                 'batch': recipe['batch'],
                                 'original_gravity': recipe['original_gravity'],
                                 'final_gravity': recipe['final_gravity'],
                                 'abv': recipe['abv'], 'ibu': recipe['ibu'], 'directions': recipe['directions'],
                                 'ingredients': []}
            for rec in recipes:
                ingredient = rec['ingredient']
                recipe_dictionary['ingredients'].append(ingredient)

            result.append(recipe_dictionary)
        return result

    @classmethod
    def load_from_db_by_id(cls, recipe_id):
        with ConnectionFromPool() as cursor:
                cursor.execute("SELECT * from recipes WHERE recipe_id=%s", (recipe_id,))
                recipe_data = cursor.fetchone()
                print(recipe_data)
                return cls(recipe_id=recipe_data[0], title=recipe_data[1], type=recipe_data[2], image_url=recipe_data[3], beer_url=recipe_data[4],
                           batch=recipe_data[5], original_gravity=recipe_data[6], final_gravity=recipe_data[7],
                           abv=recipe_data[8], ibu=recipe_data[9], directions=recipe_data[10])
    @classmethod
    def find_all(cls):
        with ConnectionFromPool() as cursor:
                cursor.execute("SELECT recipes.recipe_id, recipes.title, recipes.type, recipes.image_url, recipes.beer_url, recipes.batch, recipes.original_gravity, recipes.final_gravity, recipes.abv, recipes.ibu, recipes.directions, ingredients.ingredient FROM recipes, ingredients WHERE recipes.recipe_id = ingredients.recipe_id")
                columns = [desc[0] for desc in cursor.description]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                result = Recipe.jsonify_data(rows)

                return json.dumps(result)

    @classmethod
    def find_random(cls, num_resuls):
        with ConnectionFromPool() as cursor:
                cursor.execute("SELECT recipes.recipe_id, recipes.title, recipes.type, recipes.image_url, recipes.beer_url, recipes.batch, recipes.original_gravity, recipes.final_gravity, recipes.abv, recipes.ibu, recipes.directions, ingredients.ingredient FROM recipes, ingredients WHERE recipes.recipe_id = ingredients.recipe_id")
                columns = [desc[0] for desc in cursor.description]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                result = Recipe.jsonify_data(rows)

                return json.dumps(result)

