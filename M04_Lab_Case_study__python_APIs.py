from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

 

# Book model
class Book(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   book_name = db.Column(db.String(100))
   author = db.Column(db.String(100))
   publisher = db.Column(db.String(100))

   def to_dict(self):
       return {
           'id': self.id,
           'book_name': self.book_name,
           'author': self.author,
           'publisher': self.publisher
       }   
@app.route('/')
def index():
   return 'Hello!'


# Get all b..>@app.route('/books', methods=['GET'])
def get_books():
   books = Book.query.all()
   return jsonify([book.to_dict() for book in books])

 

# Get a specific b..>@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
   book = Book.query.get(book_id)
   if book:
       return jsonify(book.to_dict())
   else:
       return jsonify({'message': 'Book not found'})

 

# Create a new b..>@app.route('/books', methods=['POST'])
def create_book():
   new_book = Book(
       book_name=request.json['book_name'],
       author=request.json['author'],
       publisher=request.json['publisher']
   )
   db.session.add(new_book)
   db.session.commit()
   return jsonify(new_book.to_dict())

 

# Update a b..>@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
   book = Book.query.get(book_id)
   if book:
       book.book_name = request.json.get('book_name', book.book_name)
       book.author = request.json.get('author', book.author)
       book.publisher = request.json.get('publisher', book.publisher)
       db.session.commit()
       return jsonify(book.to_dict())
   else:
       return jsonify({'message': 'Book not found'})

 

# Delete a b..>@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
   book = Book.query.get(book_id)
   if book:
       db.session.delete(book)
       db.session.commit()
       return jsonify({'message': 'Book deleted'})
   else:
       return jsonify({'message': 'Book not found'})

 

if __name__ == '__main__':
   with app.app_context():
       db.create_all()
   app.run(debug=True, port=3000)

 