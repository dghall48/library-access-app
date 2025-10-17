from database import init_db, get_db_connection
from models import User

def seed_database():
    """Populate database with sample data"""
    # Initialize database first
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create sample users
    print("Creating sample users...")
    User.create('testuser', 'test@example.com', 'password123', 'Test User', '555-0100')
    User.create('john', 'john@example.com', 'password123', 'John Doe', '555-0101')
    User.create('jane', 'jane@example.com', 'password123', 'Jane Smith', '555-0102')
    
    # Sample books data
    books = [
        ('9780061120084', 'To Kill a Mockingbird', 'Harper Lee', 'Harper Perennial', 1960, 'Fiction', 3, 3, 'A gripping tale of racial injustice and childhood innocence.'),
        ('9780451524935', '1984', 'George Orwell', 'Signet Classic', 1949, 'Fiction', 2, 2, 'A dystopian social science fiction novel.'),
        ('9780743273565', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 1925, 'Fiction', 4, 4, 'A novel about the American dream.'),
        ('9780345339683', 'The Hobbit', 'J.R.R. Tolkien', 'Del Rey', 1937, 'Fantasy', 2, 2, 'A fantasy adventure about a hobbit\'s journey.'),
        ('9780062315007', 'The Alchemist', 'Paulo Coelho', 'HarperOne', 1988, 'Fiction', 3, 3, 'A philosophical book about following your dreams.'),
        ('9780316769174', 'The Catcher in the Rye', 'J.D. Salinger', 'Little, Brown', 1951, 'Fiction', 2, 1, 'A story about teenage rebellion and alienation.'),
        ('9780141439518', 'Pride and Prejudice', 'Jane Austen', 'Penguin Classics', 1813, 'Romance', 3, 3, 'A romantic novel of manners.'),
        ('9780544003415', 'The Lord of the Rings', 'J.R.R. Tolkien', 'Mariner Books', 1954, 'Fantasy', 2, 2, 'An epic high fantasy trilogy.'),
        ('9780679783268', 'Crime and Punishment', 'Fyodor Dostoevsky', 'Vintage', 1866, 'Fiction', 2, 2, 'A psychological novel about morality.'),
        ('9780060935467', 'To the Lighthouse', 'Virginia Woolf', 'Harcourt', 1927, 'Fiction', 2, 2, 'A modernist novel exploring consciousness.'),
        ('9780142437339', 'Moby-Dick', 'Herman Melville', 'Penguin Classics', 1851, 'Adventure', 2, 2, 'The quest for a great white whale.'),
        ('9780735219090', 'Educated', 'Tara Westover', 'Random House', 2018, 'Biography', 3, 3, 'A memoir about education and family.'),
        ('9780374533557', 'Thinking, Fast and Slow', 'Daniel Kahneman', 'Farrar, Straus', 2011, 'Psychology', 2, 2, 'Explores the two systems of thinking.'),
        ('9780307887894', 'The Lean Startup', 'Eric Ries', 'Crown Business', 2011, 'Business', 2, 2, 'A methodology for developing businesses.'),
        ('9780262033848', 'Introduction to Algorithms', 'Thomas Cormen', 'MIT Press', 2009, 'Computer Science', 3, 3, 'Comprehensive guide to algorithms.'),
        ('9780134685991', 'Effective Java', 'Joshua Bloch', 'Addison-Wesley', 2017, 'Computer Science', 2, 2, 'Best practices for Java programming.'),
        ('9781491950357', 'Designing Data-Intensive Applications', 'Martin Kleppmann', "O'Reilly", 2017, 'Computer Science', 2, 1, 'Guide to building scalable systems.'),
        ('9780135957059', 'The Pragmatic Programmer', 'David Thomas', 'Addison-Wesley', 2019, 'Computer Science', 3, 3, 'Your journey to mastery.'),
        ('9780596517748', 'JavaScript: The Good Parts', 'Douglas Crockford', "O'Reilly", 2008, 'Computer Science', 2, 2, 'The definitive guide to JavaScript.'),
        ('9781617294945', 'Kotlin in Action', 'Dmitry Jemerov', 'Manning', 2017, 'Computer Science', 2, 2, 'Comprehensive guide to Kotlin programming.')
    ]
    
    print("Adding sample books...")
    for book in books:
        cursor.execute('''
            INSERT INTO books (isbn, title, author, publisher, publication_year, 
                             category, total_copies, available_copies, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', book)
    
    conn.commit()
    conn.close()
    print(f"Database seeded successfully with {len(books)} books and 3 users!")
    print("\nSample login credentials:")
    print("  Username: testuser, Password: password123")
    print("  Username: john, Password: password123")
    print("  Username: jane, Password: password123")

if __name__ == '__main__':
    seed_database()