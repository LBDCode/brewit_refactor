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
        for item in data:
            recipe = {'recipe_id': item.recipe_id, 'title': item.title, 'type': item.type,
                                 'image_url': item.image_url, 'beer_url': item.beer_url,
                                 'batch': item.batch, 'original_gravity': item.original_gravity,
                                 'final_gravity': item.final_gravity, 'abv': item.abv, 'ibu': item.ibu,
                                 'directions': item.directions, 'ingredients': []}
            ser_ingredients = item.ingredients
            for i in ser_ingredients:
                recipe['ingredients'].append(i.ingredient)
            result.append(recipe)
        return result


