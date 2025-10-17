import sqlite3
from datetime import datetime

DATABASE_NAME = 'library.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Initialize the database with tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            phone TEXT,
            account_status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publisher TEXT,
            publication_year INTEGER,
            category TEXT,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1,
            description TEXT,
            cover_image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Borrowing records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowing_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP NOT NULL,
            return_date TIMESTAMP,
            status TEXT DEFAULT 'borrowed',
            fine_amount REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE
        )
    ''')
    
    # Reservations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expiry_date TIMESTAMP NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE
        )
    ''')
    
    # Reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            review_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
