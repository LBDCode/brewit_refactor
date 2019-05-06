from psycopg2 import pool


class Database:
    __connection_pool = None

    @classmethod
    def initialize(cls, **kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(1,
                                                          10,
                                                          **kwargs)
    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, conn):
        Database.__connection_pool.putconn(conn)

    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()

    @classmethod
    def create_tables(cls):
        tables = (
        "CREATE TABLE recipes (recipe_id SERIAL PRIMARY KEY, title VARCHAR UNIQUE, type VARCHAR, image_url VARCHAR, beer_url VARCHAR, batch VARCHAR, original_gravity REAL, final_gravity REAL, abv REAL, ibu REAL, directions TEXT)",
        "CREATE TABLE ingredients (ingredient_id SERIAL PRIMARY KEY, recipe_id INTEGER, FOREIGN KEY(recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE, ingredient VARCHAR )"
        )
        with ConnectionFromPool() as cursor:
            for table in tables:
                cursor.execute(table)



class ConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()

        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)

