import os, psycopg2, time


from flask import Flask, session, request, render_template, redirect, url_for, g, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError
from werkzeug.security import check_password_hash, generate_password_hash
import requests

from db import db
from helpers import login_requiredUser
from forms import register_user
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.jinja_env.globals['g'] = g # to use an a global variable in templates
app.secret_key = os.getenv("SECRET_KEY")  # Establece una clave secreta segura
api_key = os.getenv("GOOGLEBOOKS_APIKEY") # Api Google maps






# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.before_request
def before_request():
    if 'user_id' in session:

        queryLogin = text("SELECT name, lastname FROM users WHERE (user_id = :user_id)")
        user_row = db.execute(queryLogin, {"user_id":session['user_id']}).fetchone()

        session['name'] = user_row[0]
        session['lastname'] = user_row[1]

        g.user_id = session['user_id']
        g.name = session['name']
        g.lastname = session['lastname']



def get_thumbnail_url(isbn):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}'
    response = requests.get(url).json()
    
    imgAlternative = url_for('static', filename='img/no_vista.png')

    if 'items' in response and 'volumeInfo' in response['items'][0] and 'imageLinks' in response['items'][0]['volumeInfo']:
        items = response['items'][0]['volumeInfo']['imageLinks']
        return items.get('thumbnail', imgAlternative)  # Reemplaza 'URL_de_imagen_alternativa' con la URL de una imagen alternativa
    else:
        return imgAlternative # Reemplaza 'URL_de_imagen_alternativa' con la URL de una imagen alternativa



@app.route("/", methods=["GET", "POST"])
def index():
    register_success = request.args.get('registerSuccess', 0)  # obtiene el parámetro de consulta 'registerSuccess'

   

    query= text("""SELECT book.book_id, book.isbn, book.title, book.year,
  COUNT(reviews.book_id) AS review_count
  FROM reviews
  JOIN book ON reviews.book_id = book.book_id
  GROUP BY book.book_id, book.isbn, book.title, book.year
  ORDER BY review_count DESC
  LIMIT 5 """)
    
    mostCommentBooks = db.execute(query).fetchall()

    dtBook = []

    for books in mostCommentBooks:
        book_info = {
            'book_id': books.book_id,
            'isbn': books.isbn,
            'title': books.title,
            'year': books.year,
            'review_count': books.review_count,
            'thumbnail_url': get_thumbnail_url(books.isbn)
        }
        dtBook.append(book_info)


    query2 = text(""" SELECT
(SELECT COUNT(*) FROM users) AS total_users,
(SELECT COUNT(*) FROM book) AS total_books; """)
    
    totalUsersAndBooks = db.execute(query2).fetchone()

    return render_template("home.html", registerSuccess=register_success, mostCommentBooks=dtBook, totalUsersAndBooks=totalUsersAndBooks)

@app.route("/check_logged", methods=["GET"])
def check_logged():
    if 'user_id' in session:
        return jsonify(logged_in=1)
    else:
        return jsonify(logged_in=2)


@app.route("/search", methods=["GET", "POST"])
@login_requiredUser
def search():
    if request.method == 'POST':

        search = request.form['searchInput']

        query = text(""" SELECT book.book_id, book.isbn, book.title, authors.name as author, book.year
FROM book
JOIN authors_books ON book.book_id = authors_books.book_id
JOIN authors ON authors_books.author_id = authors.author_id
WHERE book.isbn ILIKE :ISBN OR book.title ILIKE :title """)
        results = db.execute(query,{"ISBN": f"%{search}%", "title": f"%{search}%"}).fetchall()
        
        areResults = 1

        if results == []:
            areResults = 0

        return render_template("search.html", results = results, search=search, areResults = areResults)

    return render_template("search.html")

@app.route("/login_user", methods=["GET", "POST"])
def login_user():

    email = request.form['email']
    password = request.form['password']

    queryLogin = text("SELECT * FROM users WHERE (email = :email) LIMIT 1")
    user_row = db.execute(queryLogin, {"email":email}).fetchone()

    if user_row:
        user_password = user_row[4]
        user_id = user_row[0]
        name = user_row[1]
        lastname = user_row[2]
    
        if check_password_hash(user_password, password):
            session['user_id'] = user_id
            session['name'] = name
            session['lastname'] = lastname
            return jsonify(login_successful=1)
    return jsonify(login_successful= 2)

@app.route("/register", methods=["GET", "POST"])
def register():

    form = register_user()

    confirmando = False
    if form.validate_on_submit():
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))

        query = text("INSERT INTO users (name, lastname, password, email) VALUES (:name, :lastname, :password, :email)")
        db.execute(query, {"name": name, "lastname": lastname, "password": password, "email": email})
        db.commit()

        return redirect(url_for('index', registerSuccess=1))

    else:
        print(form.errors)


        return render_template('auth/register.html', form=form, registerSuccess = 0)

@app.route('/book_view/<string:book_id>', methods=["GET", "POST"])
@login_requiredUser
def book_view(book_id): 
    

    query = text("""
SELECT book.book_id, book.isbn, book.title, authors.name as author, book.year 
FROM book
JOIN authors_books ON book.book_id = authors_books.book_id
JOIN authors ON authors_books.author_id = authors.author_id
WHERE book.book_id = :book_id""")
    book_data= db.execute(query, {"book_id": book_id}).fetchone()

    isbn = book_data[1]

    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}'
    response = requests.get(url).json()


    coverImg =  get_thumbnail_url(isbn)

    





    query2 = text("""WITH TimeDifference AS (
    SELECT
        reviews.review_id,
        age(now(), reviews.review_date) as age
    FROM
        reviews
    JOIN
        users ON reviews.user_id = users.user_id
    JOIN
        book ON reviews.book_id = book.book_id
    WHERE
        book.book_id = :book_id
)
SELECT
    reviews.review_id,
    book.book_id,
    users.user_id,
    users.name,
    users.lastname,
    reviews.score_review,
    reviews.book_review,
    reviews.review_date,
    CASE 
        WHEN extract(epoch from TimeDifference.age) < 60 THEN format('Hace %s segundos', extract(epoch from TimeDifference.age)::INTEGER)
        WHEN extract(epoch from TimeDifference.age) < 3600 THEN format('Hace %s minutos', (extract(epoch from TimeDifference.age)/60)::INTEGER)
        WHEN extract(epoch from TimeDifference.age) < 86400 THEN format('Hace %s horas', (extract(epoch from TimeDifference.age)/3600)::INTEGER)
        WHEN extract(epoch from TimeDifference.age) < 2592000 THEN format('Hace %s días', (extract(epoch from TimeDifference.age)/86400)::INTEGER)
        WHEN extract(epoch from TimeDifference.age) < 31536000 THEN format('Hace %s meses', (extract(epoch from TimeDifference.age)/2592000)::INTEGER)
        ELSE format('Hace %s años', (extract(epoch from TimeDifference.age)/31536000)::INTEGER)
    END as time_ago
FROM
    reviews
JOIN
    users ON reviews.user_id = users.user_id
JOIN
    book ON reviews.book_id = book.book_id
JOIN
    TimeDifference ON reviews.review_id = TimeDifference.review_id
WHERE
    book.book_id = :book_id
ORDER BY
    reviews.review_date DESC;
""")
    
    reviews_data =  db.execute(query2,{"book_id": book_id}).fetchall()

    if request.method == "POST":
       
        rating = request.form.get('rating')
        text_review = request.form.get('text-area-review')
        
        query = text("""INSERT INTO reviews (user_id, book_id, score_review, book_review, review_date)
                     VALUES (:user_id, :book_id, :score_review, :book_review, CURRENT_TIMESTAMP)""")
        db.execute(query,{"user_id": g.user_id, "book_id": book_id, "score_review": rating, "book_review": text_review })
        
        db.commit()
        
        return redirect(url_for('book_view', book_id=book_id, reviewSucess = 1))
    review_sucess = request.args.get('reviewSucess', '0')


    return render_template('book_view.html', book_data=book_data, reviews_data=reviews_data, reviewSucess=review_sucess, coverImg=coverImg)

@app.route("/book_view_json/<string:isbn>")
@login_requiredUser
def book_view_json(isbn):

    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}'
    response = requests.get(url).json()



    if 'items' in response:
        items = response['items'][0]['volumeInfo']
        response_jsonBook = {
        'title': items.get('title', 'Titulo desconocido'),
        'author': items.get('authors', 'Autor desconocido'),
        'year': items.get('publishedDate', 'Año desconocido'),
        'isbn': isbn,
        'review_count': items.get('ratingsCount', '0'),
        'avarage_score': items.get('averageRating', '0')
        }

    else:
        abort(404, description='No se encontraron resultados para el ISBN proporcionado')
    

    return jsonify(response_jsonBook)



@app.route('/Cerrar_Sesion')
def Cerrar_Sesion():
    
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('lastname', None)
    return redirect(url_for('index'))

# Ejecuta la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run()