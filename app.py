from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# Instantiate backend application and initate CORS
app = Flask(__name__)
CORS(app)

# Set up file location / configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

# Instantiate database functionality
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Setup Database
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, title, author, description, price):
        self.title = title
        self.author = author
        self.description = description
        self.price = price

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'description', 'price')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Instantiating the database / creating the database app.sqlite file
# >>> from app import db
# >>> from app import app
# >>> with app.app_context():
# >>>     db.create_all()
# MAKE SURE TO INDENT LAST LINE
# CHECK THAT app.sqlite was created


# API / endpoints
# endpoint
@app.route('/book/get', methods=['GET'])
# handler
def get_all_books():
    # SQLAlchemy query
    all_books = Book.query.all()
    # Convert SQL to JSONifiable format
    result = books_schema.dump(all_books)
    # Convert data to JSON and send back response
    return jsonify(result)

@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    result = book_schema.dump(book)
    
    return jsonify(result)

@app.route('/book/add', methods=['POST'])
def add_book():
    title = request.json.get('title')
    author = request.json.get('author')
    description = request.json.get('description')
    price = request.json.get('price')

    new_book = Book(title, author, description, price)
    db.session.add(new_book)
    db.session.commit()

    result = book_schema.dump(new_book)
    return jsonify(result)





if __name__ == "__main__":
    app.run(debug=True)