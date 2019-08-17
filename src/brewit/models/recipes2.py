from brewit import db
from itertools import groupby

class Recipe2(db.Model):
    __tablename__ = "recipe"

    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    image_url = db.Column(db.String(), nullable=False)
    beer_url = db.Column(db.String(), nullable=False)
    batch = db.Column(db.String(), nullable=False)
    original_gravity = db.Column(db.REAL(), nullable=False)
    final_gravity = db.Column(db.REAL(), nullable=False)
    abv = db.Column(db.REAL(), nullable=False)
    ibu = db.Column(db.REAL(), nullable=False)
    directions = db.Column(db.Text(), nullable=False)
    ingredients = db.relationship('Ingredient2', backref='recipe')

    def __repr__(self):
        return f"Recipe('{self.recipe_id}', '{self.title}', '{self.type}')"

    @staticmethod
    def jsonify_data(data):
        result = []
        for recipe_id, recipes in groupby(data, key=lambda each: each['recipe_id']):
            recipes = list(recipes)
            for recipe in recipes:
                print(recipe)
            # recipe = recipes[0].copy()
            # recipe_dictionary = {'recipe_id': recipe['recipe_id'], 'title': recipe['title'], 'type': recipe['type'],
            #                      'image_url': recipe['image_url'], 'beer_url': recipe['beer_url'],
            #                      'batch': recipe['batch'],
            #                      'original_gravity': recipe['original_gravity'],
            #                      'final_gravity': recipe['final_gravity'],
            #                      'abv': recipe['abv'], 'ibu': recipe['ibu'], 'directions': recipe['directions'],
            #                      'ingredients': []}
            # for rec in recipes:
            #     ingredient = rec['ingredient']
            #     recipe_dictionary['ingredients'].append(ingredient)
            result.append(recipe_dictionary)
        return result


