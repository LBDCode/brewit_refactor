from common.database import ConnectionFromPool

class Ingredient:
    def __init__(self, recipe_id, ingredient, ingredient_id):
        self.recipe_id = recipe_id
        self.ingredient = ingredient
        self.ingredient_id = ingredient_id


    def __repr__(self):
         return "<Ingredient {}>".format(self.ingredient)


    def save_to_db(self, title):
        with ConnectionFromPool() as cursor:
                cursor.execute("INSERT INTO ingredients (recipe_id, ingredient) SELECT recipe_id, %s from recipes where title = %s",
                               (self.ingredient, title))


    @classmethod
    def load_from_db_by_id(cls, recipe_id):
        with ConnectionFromPool() as cursor:
                cursor.execute("SELECT * from ingredients WHERE recipe_id=%s", (recipe_id,))
                recipe_data = cursor.fetchone()
                return cls(ingredient_id=recipe_data[1], recipe_id=recipe_data[2], ingredient=recipe_data[3])