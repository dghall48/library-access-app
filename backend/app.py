from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import init_db
from models import User, Book, BorrowingRecord, Reservation, Review

app = Flask(__name__)
CORS(app)  # Enable CORS for Android app

# Initialize database on first run
init_db()

# Landing page
@app.route('/')
def index():
    """Simple landing page"""
    return render_template('index.html')

# Authentication endpoints
@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    phone = data.get('phone')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.create(username, email, password, full_name, phone)
    if user:
        return jsonify({'message': 'User created successfully', 'user': user}), 201
    else:
        return jsonify({'error': 'Username or email already exists'}), 409

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({'error': 'Missing credentials'}), 400
    
    user = User.authenticate(username, password)
    if user:
        user.pop('password_hash', None)
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Book endpoints
@app.route('/api/books', methods=['GET'])
def get_books():
    """Get all books with optional search and category filter"""
    search = request.args.get('search')
    category = request.args.get('category')
    books = Book.get_all(search, category)
    return jsonify(books), 200

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    book = Book.get_by_id(book_id)
    if book:
        return jsonify(book), 200
    else:
        return jsonify({'error': 'Book not found'}), 404

# Borrowing endpoints
@app.route('/api/borrow', methods=['POST'])
def borrow_book():
    """Borrow a book"""
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    
    if not all([user_id, book_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    book = Book.get_by_id(book_id)
    if not book or book['available_copies'] <= 0:
        return jsonify({'error': 'Book not available'}), 400
    
    record_id = BorrowingRecord.create(user_id, book_id)
    return jsonify({'message': 'Book borrowed successfully', 'record_id': record_id}), 201

@app.route('/api/return/<int:record_id>', methods=['POST'])
def return_book(record_id):
    """Return a borrowed book"""
    fine = BorrowingRecord.return_book(record_id)
    if fine is not None:
        return jsonify({'message': 'Book returned successfully', 'fine': fine}), 200
    else:
        return jsonify({'error': 'Record not found'}), 404

@app.route('/api/user/<int:user_id>/borrowed', methods=['GET'])
def get_user_borrowed(user_id):
    """Get all books borrowed by a user"""
    records = BorrowingRecord.get_user_borrowed(user_id)
    return jsonify(records), 200

# Reservation endpoints
@app.route('/api/reserve', methods=['POST'])
def reserve_book():
    """Reserve a book"""
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    
    if not all([user_id, book_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    reservation_id = Reservation.create(user_id, book_id)
    return jsonify({'message': 'Book reserved successfully', 'reservation_id': reservation_id}), 201

@app.route('/api/user/<int:user_id>/reservations', methods=['GET'])
def get_user_reservations(user_id):
    """Get all reservations for a user"""
    reservations = Reservation.get_user_reservations(user_id)
    return jsonify(reservations), 200

# Review endpoints
@app.route('/api/reviews', methods=['POST'])
def create_review():
    """Create a review for a book"""
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    rating = data.get('rating')
    review_text = data.get('review_text')
    
    if not all([user_id, book_id, rating]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    review_id = Review.create(user_id, book_id, rating, review_text)
    return jsonify({'message': 'Review created successfully', 'review_id': review_id}), 201

@app.route('/api/books/<int:book_id>/reviews', methods=['GET'])
def get_book_reviews(book_id):
    """Get all reviews for a book"""
    reviews = Review.get_book_reviews(book_id)
    return jsonify(reviews), 200

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check"""
    return jsonify({'status': 'healthy', 'message': 'Library API is running'}), 200

if __name__ == '__main__':
    print("Starting Library Access API...")
    print("API running on http://localhost:5001")
    print("\nTest the API:")
    print("  - Landing page: http://localhost:5001/")
    print("  - Health check: http://localhost:5001/api/health")
    print("  - View books: http://localhost:5001/api/books")
    app.run(debug=True, host='0.0.0.0', port=5001)