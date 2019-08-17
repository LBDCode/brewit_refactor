from brewit import db

class Ingredient2(db.Model):
    __tablename__ = "ingredient"

    ingredient_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.recipe_id'), nullable=False)
    ingredient = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Recipe('{self.ingredient_id}', '{self.recipe_id}', '{self.ingredient}')"