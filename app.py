import requests
import os
from datetime import datetime
from functools import wraps
from flask_session import Session
from flask_caching import Cache
from models import initialize_db , get_db_connection , register_user , get_user , create_tables , get_movies , addmovie , removemovie ,get_userbyid , edit_user
from flask import Flask, request , render_template, jsonify , redirect, url_for , session ,flash
from werkzeug.security import check_password_hash, generate_password_hash

TMDB_ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(os.getcwd(), 'flask_session_files')
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
Session(app)

@app.cli.command('setup-db')
def setup_database():
    initialize_db()

@app.cli.command('create-db')
def setup_database():
    create_tables()

@app.context_processor
def inject_user():
    return dict(endpoint = request.endpoint)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template("error.html"), 404

@app.route('/')
def index():
    if "user_id" in session:
        userdata = get_userbyid(session["user_id"])
        return redirect("/profile/" + userdata["username"])
    return render_template('index.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route('/signup' , methods=['GET','POST'])
def signup():
    if "user_id" in session:
        user = get_userbyid(session["user_id"])
        return redirect("/profile/" + user["username"])
    if request.method == "POST":

        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):
            return render_template('signup.html' , message = 'Invalid Credentials')        
        
        username = request.form.get("username")
        response , status = register_user(username , generate_password_hash(request.form.get("password")))
        
        if status == 201:
            return redirect("/login")
        else:
            message = response.get("error")
            flash(message , 'error')
            return render_template('signup.html')
    
    return render_template('signup.html')


@app.route('/login' , methods=['GET','POST'])
def login():
    if "user_id" in session:
        user = get_userbyid(session["user_id"])
        return redirect("/profile/" + user["username"])
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            flash("Invalid Credentials")
            return render_template('login.html' , message = 'Invalid Credentials')
        
        
        user = get_user(request.form.get("username").lower())

        if user is None or not check_password_hash(user[2] , request.form.get("password")):
            flash("Invalid Credentials")
            return redirect('/login')

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect("/profile/" + user["username"])
    return render_template('login.html')


def search(query , api_url):
    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }
    try:
        response = requests.get(api_url, headers=headers, params={"query": query})
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.RequestException as e:
        flash("Error fetching details. Please try again later.", "error")
        return []


@app.route('/search/movie', methods=['GET'])
@login_required
def search_movie():
    
    movies = []
    query = request.args.get('query', '')
    api_url = 'https://api.themoviedb.org/3/search/movie'
    if query:
        movies = search(query , api_url)
    else:
        api_url = 'https://api.themoviedb.org/3/movie/popular'
        movies = search('', api_url)
    
    movies = [movie for movie in movies if movie.get('poster_path')]
    return render_template('search.html' , movies = movies)


@app.route('/search/person', methods=['GET'])
@login_required
def search_person():
    people = []
    query = request.args.get('query')
    api_url = 'https://api.themoviedb.org/3/search/person'
    if query:
        people = search(query , api_url)    
    else:
        api_url = 'https://api.themoviedb.org/3/person/popular'
        people = search('', api_url) 

    people = [person for person in people if person.get('profile_path')]
    return render_template('person.html' , people = people)


@app.route('/profile/<username>')
@login_required
def profile(username):
    user_data = get_user(username.lower())
    if user_data is None:
        return render_template('error.html'), 404
    user_movies = get_movies(user_data["id"])
    return render_template('profile.html' , movies = user_movies , user = user_data , editable = False)  


@app.route('/profile/edit' , methods = ['GET','POST'])
@login_required
def edit_profile():
    user_id = session["user_id"]
    user_data = get_userbyid(user_id)

    if request.method == 'POST':
        name = request.form.get('name')
        about = request.form.get('about')
        edit_user(user_id , name , about)
        return redirect('/profile/' + user_data["username"])

    user_movies = get_movies(user_id)
    return render_template('profile.html' , movies = user_movies , user = user_data , editable = True)  

@app.route('/home')
@login_required
def home():
    return render_template('home.html')


def modify_movie(action):
    movie_id = request.form.get('movie_id')
    user_id = session["user_id"]
    if action == 'add':
        title = request.form.get('title')
        year = request.form.get('year')
        genres = request.form.get('genres')
        poster_path = request.form.get('poster_path')
        addmovie(movie_id ,title, year, genres, poster_path, user_id)
        flash("Movie added successfully","success")
    elif action == 'remove':
        removemovie(movie_id , user_id)
        flash("Movie removed successfully","success")


def fetch_tmdb_data(api_url, params={}):
    headers = {
        'Authorization': f'Bearer {TMDB_ACCESS_TOKEN}',
        'Content-Type': 'application/json;charset=utf-8',
    }
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        flash(f"Error fetching data from TMDB: {e}", "error")
        return None

def fetch_credits(api_url):
    headers = {
        'Authorization': f'Bearer {TMDB_ACCESS_TOKEN}',
        'Content-Type': 'application/json;charset=utf-8',
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        flash(f"Error fetching data from TMDB: {e}", "error")
        return None

@app.route('/movie/<string:movie_id>' , methods=['GET','POST'])
@login_required
def movie_details(movie_id):
    if request.method == 'POST':
        action = request.form.get('action')
        modify_movie(action)
        return redirect(f'/movie/{movie_id}')

    movie_ids = [int(movie[2]) for movie in get_movies(session["user_id"])]
    moviedata = fetch_tmdb_data(f'https://api.themoviedb.org/3/movie/{movie_id}')
    credits = fetch_credits(f'https://api.themoviedb.org/3/movie/{movie_id}/credits')
    actors = []
    for member in credits.get("cast" , []):
        if member["profile_path"]:
            actors.append(member)
    if len(actors) > 14:
        actors = actors[:14]
    director = []
    writer = []
    producer = []
    for crew in credits.get("crew" , []):
        if crew["profile_path"]:
            if crew['job'] == "Director":
                director.append(crew)
            elif crew['job'] == "Screenplay" or crew['job'] == "Writer":
                writer.append(crew)
            elif crew['job'] == "Producer":
                producer.append(crew)

    if moviedata:
        date_object = datetime.strptime(moviedata["release_date"], "%Y-%m-%d")
        formatted_date = date_object.strftime("%B %d, %Y")
        return render_template('movie.html', moviedata=moviedata, formatted_date=formatted_date, movie_ids=movie_ids , actors = actors , writer = writer , director = director , producer = producer)
    else:
        return render_template('movie.html', moviedata=[], formatted_date="", movie_ids=movie_ids)
    

def format_biography(biography):
    paragraphs = biography.split("\n\n")
    return "\n\n".join(paragraphs[:2]) if len(paragraphs[0]) < 200 else biography


@app.route('/person/<string:person_id>' , methods=['GET','POST'])
@login_required
def person_details(person_id):
    persondata = fetch_tmdb_data(f'https://api.themoviedb.org/3/person/{person_id}')
    credits = fetch_credits(f"https://api.themoviedb.org/3/person/{person_id}/movie_credits")
    if persondata["known_for_department"] == "Acting":
        allmovies = credits.get("cast" , [])
    else:
        allmovies = credits.get("crew" , [])

    seen_ids = set()
    movies = []
    for movie in allmovies:
        if movie["id"] not in seen_ids:
            movies.append(movie)
            seen_ids.add(movie["id"])

    movies = sorted(movies, key=lambda x: x.get("vote_average", 0), reverse=True)
    if len(movies) >= 21:
        movies = movies[:21]
    if persondata:
        persondata["biography"] = format_biography(persondata["biography"])
        return render_template('persondata.html', persondata=persondata , movies = movies)
    else:
        return render_template('persondata.html', persondata={})

if __name__ == '__main__':
    app.run(debug=True)