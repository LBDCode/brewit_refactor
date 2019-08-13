from src.common.database import ConnectionFromPool

class User:
    def __init__(self, email, password, user_id):
        self.email = email
        self.password = password
        self.user_id = user_id

    # def __repr__(self):
    #      return "<Recipe {}>".format(self.title)

    # def save_to_db(self):
    #     with ConnectionFromPool() as cursor:
    #             cursor.execute("INSERT INTO recipes(title, type, image_url, beer_url, batch, original_gravity, final_gravity, abv, ibu, directions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #                            (self.title, self.type, self.image_url, self.beer_url, self.batch, self.original_gravity, self.final_gravity, self.abv, self.ibu, self.directions))
