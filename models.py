import sqlite3

# Connect to (or create) the database file
def get_db_connection():
    conn = sqlite3.connect('moviegeek.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a table
def initialize_db():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                passhash TEXT NOT NULL
            )
        ''')
        conn.commit()

def register_user(username, passhash):
    username = username.lower()
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, passhash) VALUES (?, ?)", (username, passhash))
            conn.commit()
            return {"message": "Registered successfully!"}, 201
        except sqlite3.IntegrityError:
            return {"error": "Username already exists."}, 409
        except sqlite3.Error as e:
            return {"error": "An error occurred while registering the user."}, 500  # Internal server error

def get_user(username):
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            data = cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            return data.fetchone()
        except sqlite3.Error as e:
            return {"error": "Can't find User."}, 500
    
def get_userbyid(user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        data = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return data.fetchone()
    
def edit_user(user_id , name = "" , about = ""):
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE users SET name = ? , about = ? WHERE id = ?",(name , about , user_id,))
            conn.commit()
        except sqlite3.Error as e:
            return {"error": "An error occurred while updating the user."}, 500

def create_tables():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_id TEXT NOT NULL,
                title TEXT NOT NULL,
                poster_path TEXT,
                year TEXT,
                genres TEXT,
                list TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE (user_id, movie_id)
            )
        ''')
        conn.commit()

def get_movies(user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        data = cur.execute("SELECT * FROM movies WHERE user_id = ? ORDER BY id DESC", (user_id,))
        return data.fetchall()
    

def addmovie(movie_id ,title, year, genres, poster_path, user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO movies (movie_id ,title, year, genres, poster_path, user_id) VALUES (?,?, ?, ?, ?, ?)", (movie_id ,title, year, genres, poster_path, user_id))
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()  # Rollback in case of error
            return {"error": "An error occurred while adding the movie."}, 500

def removemovie(movie_id , user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM movies WHERE movie_id = ? AND user_id = ?" , (movie_id , user_id))
        conn.commit()