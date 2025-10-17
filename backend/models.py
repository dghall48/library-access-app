from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from datetime import datetime, timedelta

class User:
    @staticmethod
    def create(username, email, password, full_name=None, phone=None):
        """Create a new user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, phone))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return {'user_id': user_id, 'username': username, 'email': email}
        except Exception as e:
            conn.close()
            return None
    
    @staticmethod
    def authenticate(username, password):
        """Verify user credentials"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            return dict(user)
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

class Book:
    @staticmethod
    def get_all(search=None, category=None):
        """Get all books with optional search and category filter"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM books WHERE 1=1'
        params = []
        
        if search:
            query += ' AND (title LIKE ? OR author LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        cursor.execute(query, params)
        books = cursor.fetchall()
        conn.close()
        return [dict(book) for book in books]
    
    @staticmethod
    def get_by_id(book_id):
        """Get book by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
        book = cursor.fetchone()
        conn.close()
        return dict(book) if book else None
    
    @staticmethod
    def update_availability(book_id, change):
        """Update available copies (change can be +1 or -1)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE books 
            SET available_copies = available_copies + ? 
            WHERE book_id = ?
        ''', (change, book_id))
        conn.commit()
        conn.close()

class BorrowingRecord:
    @staticmethod
    def create(user_id, book_id, days=14):
        """Create a new borrowing record"""
        conn = get_db_connection()
        cursor = conn.cursor()
        due_date = datetime.now() + timedelta(days=days)
        
        cursor.execute('''
            INSERT INTO borrowing_records (user_id, book_id, due_date)
            VALUES (?, ?, ?)
        ''', (user_id, book_id, due_date))
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        # Decrease available copies
        Book.update_availability(book_id, -1)
        return record_id
    
    @staticmethod
    def return_book(record_id):
        """Mark a book as returned"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get the record
        cursor.execute('SELECT * FROM borrowing_records WHERE record_id = ?', (record_id,))
        record = cursor.fetchone()
        
        if not record:
            conn.close()
            return None
        
        # Calculate fine if overdue
        due_date = datetime.fromisoformat(record['due_date'])
        return_date = datetime.now()
        fine = 0.0
        
        if return_date > due_date:
            days_overdue = (return_date - due_date).days
            fine = days_overdue * 0.50  # $0.50 per day
        
        # Update record
        cursor.execute('''
            UPDATE borrowing_records 
            SET return_date = ?, status = 'returned', fine_amount = ?
            WHERE record_id = ?
        ''', (return_date, fine, record_id))
        conn.commit()
        conn.close()
        
        # Increase available copies
        Book.update_availability(record['book_id'], 1)
        return fine
    
    @staticmethod
    def get_user_borrowed(user_id):
        """Get all currently borrowed books for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT br.*, b.title, b.author, b.isbn
            FROM borrowing_records br
            JOIN books b ON br.book_id = b.book_id
            WHERE br.user_id = ? AND br.status = 'borrowed'
            ORDER BY br.due_date
        ''', (user_id,))
        records = cursor.fetchall()
        conn.close()
        return [dict(record) for record in records]

class Reservation:
    @staticmethod
    def create(user_id, book_id, days=7):
        """Create a new reservation"""
        conn = get_db_connection()
        cursor = conn.cursor()
        expiry_date = datetime.now() + timedelta(days=days)
        
        cursor.execute('''
            INSERT INTO reservations (user_id, book_id, expiry_date)
            VALUES (?, ?, ?)
        ''', (user_id, book_id, expiry_date))
        conn.commit()
        reservation_id = cursor.lastrowid
        conn.close()
        return reservation_id
    
    @staticmethod
    def get_user_reservations(user_id):
        """Get all reservations for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, b.title, b.author
            FROM reservations r
            JOIN books b ON r.book_id = b.book_id
            WHERE r.user_id = ? AND r.status = 'pending'
            ORDER BY r.reservation_date
        ''', (user_id,))
        reservations = cursor.fetchall()
        conn.close()
        return [dict(res) for res in reservations]

class Review:
    @staticmethod
    def create(user_id, book_id, rating, review_text=None):
        """Create a new review"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reviews (user_id, book_id, rating, review_text)
            VALUES (?, ?, ?, ?)
        ''', (user_id, book_id, rating, review_text))
        conn.commit()
        review_id = cursor.lastrowid
        conn.close()
        return review_id
    
    @staticmethod
    def get_book_reviews(book_id):
        """Get all reviews for a book"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, u.username, u.full_name
            FROM reviews r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.book_id = ?
            ORDER BY r.created_at DESC
        ''', (book_id,))
        reviews = cursor.fetchall()
        conn.close()
        return [dict(review) for review in reviews]
