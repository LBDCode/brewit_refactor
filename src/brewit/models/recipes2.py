from brewit import db


class Recipe2(db.Model):
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
    ingredients = db.relationship('Ingredient', backref='recipe')

    def __repr__(self):
        return f"Recipe('{self.recipe_id}', '{self.title}', '{self.type}')"
