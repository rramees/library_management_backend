from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User, UserRole, UserStatus
from app.db.models.category import Category
from app.db.models.author import Author
from app.db.models.book import Book
from app.db.models.borrowing import Borrowing, BorrowStatus
from app.core.security import hash_password
from datetime import datetime, timedelta
import random
from faker import Faker

# Initialize Faker
fake = Faker()

def seed_data():
    db: Session = SessionLocal()

    try:
        # Seed Users
        users = [
            {
                "username": fake.user_name()[:45],  # Truncate to 45 characters (limit: 50)
                "password": hash_password("password123"),  # Password is hashed
                "full_name": fake.name()[:95],  # Truncate to 95 characters (limit: 100)
                "email": fake.email()[:250],  # Truncate to 250 characters (limit: 255)
                "phone_no": fake.phone_number()[:18],  # Truncate to 18 characters (limit: 20)
                "role": UserRole.USER,
                "status": UserStatus.ACTIVE,
            }
            for _ in range(1, 21)  # Create 20 users
        ]
        librarians = [
            {
                "username": fake.user_name()[:45],  # Truncate to 45 characters (limit: 50)
                "password": hash_password("password123"),  # Password is hashed
                "full_name": fake.name()[:95],  # Truncate to 95 characters (limit: 100)
                "email": fake.email()[:250],  # Truncate to 250 characters (limit: 255)
                "phone_no": fake.phone_number()[:18],  # Truncate to 18 characters (limit: 20)
                "role": UserRole.LIBRARIAN,
                "status": UserStatus.ACTIVE,
            }
            for _ in range(1, 6)  # Create 5 librarians
        ]
        for user_data in users + librarians:
            user = User(**user_data)
            db.add(user)

        # Seed Categories
        categories = [
            {"name": "Fiction"},
            {"name": "Non-Fiction"},
            {"name": "Science Fiction"},
            {"name": "Fantasy"},
            {"name": "Mystery"},
            {"name": "Biography"},
            {"name": "History"},
            {"name": "Self-Help"},
        ]
        for category_data in categories:
            category = Category(**category_data)
            db.add(category)

        # Seed Authors
        authors = [
            Author(
                name=fake.name()[:95],  # Truncate to 95 characters (limit: 100)
                nationality=fake.country()[:95],  # Truncate to 95 characters (limit: 100)
            )
            for _ in range(5)  # Generate 5 random authors
        ]
        db.add_all(authors)
        db.commit()

        # Seed Books
        books = [
            {
                "title": fake.sentence(nb_words=3)[:250],  # Truncate to 250 characters (limit: 255)
                "publisher": fake.company()[:250],  # Truncate to 250 characters (limit: 255)
                "category_id": random.randint(1, len(categories)),
                "total_copies": random.randint(5, 20),
                "available_copies": random.randint(1, 5),
                "language": random.choice(["English", "Spanish", "French"])[:45],  # Truncate to 45 characters (limit: 50)
                "authors": random.sample(authors, random.randint(1, 3)),  # Randomly assign 1-3 authors
            }
            for _ in range(1, 51)  # Create 50 books
        ]
        for book_data in books:
            book_authors = book_data.pop("authors")
            book = Book(**book_data)
            book.authors = book_authors
            db.add(book)

        # Seed Borrowing Records
        borrowings = [
            {
                "user_id": random.randint(1, 20),  # Random user
                "book_id": random.randint(1, 50),  # Random book
                "borrow_date": datetime.now() - timedelta(days=random.randint(1, 30)),
                "due_date": datetime.now() + timedelta(days=random.randint(1, 30)),
                "status": random.choice(list(BorrowStatus)),
            }
            for _ in range(30)  # Create 30 borrowing records
        ]

        # Ensure consistency between `status` and `return_date`
        for borrowing_data in borrowings:
            if borrowing_data["status"] == BorrowStatus.RETURNED:
                # If status is RETURNED, set a valid return_date
                borrowing_data["return_date"] = borrowing_data["borrow_date"] + timedelta(days=random.randint(1, 14))
            else:
                # If status is BORROWED, ensure return_date is None
                borrowing_data["return_date"] = None

        # Add borrowing records to the database         
        for borrowing_data in borrowings:
            borrowing = Borrowing(**borrowing_data)
            db.add(borrowing)

        # Commit all changes
        db.commit()
        print("Sample data seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
