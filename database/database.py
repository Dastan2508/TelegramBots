import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_table(self):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()


            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_id  (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS database_for_data  (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone_number TEXT,  
                    visit_date TEXT,    
                    food_rating INTEGER,
                    cleanliness_rating INTEGER,
                    review_extra_comments TEXT,
                    tg_id INTEGER
                )
            """)


            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dishes  (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_of_Food TEXT,
                    price INTEGER,  
                    from_countre TEXT,    
                    category TEXT
                )
            """)

            connection.commit()

    def execute(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.path) as connection:
            connection.execute(query, params)
            connection.commit()

    def fetch(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall()
            return [dict(row) for row in data]