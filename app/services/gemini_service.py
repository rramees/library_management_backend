import google.generativeai as genai
from app.core.config import settings

# Configure the API key
genai.configure(api_key=settings.GOOGLE_API_KEY)



def generate_sql_query(natural_language_query: str) -> str:
    
    """
    Use Google's Gemini (PaLM API) to generate an SQL query from a natural language query.
    """
    # Static prompt with database schema and sample data
    prompt = f"""
    You are an expert SQL assistant. The following is the schema of the database:

    Table: users
    Columns:
      - id (INTEGER)
      - username (VARCHAR)
      - password (VARCHAR)
      - full_name (VARCHAR)
      - email (VARCHAR)
      - phone_no (VARCHAR)
      - role (ENUM: 'librarian', 'user')
      - api_key (VARCHAR)
      - status (ENUM: 'active', 'inactive')
    Relationships:
      - Referenced by borrowing (user_id)

    Table: books
    Columns:
      - id (INTEGER)
      - title (VARCHAR)
      - publisher (VARCHAR)
      - category_id (INTEGER)
      - total_copies (INTEGER)
      - available_copies (INTEGER)
      - language (VARCHAR)
    Relationships:
      - Referenced by borrowing (book_id)
      - References categories (category_id)

    Table: categories
    Columns:
      - id (INTEGER)
      - name (VARCHAR)
    Relationships:
      - Referenced by books (category_id)

    Table: borrowing
    Columns:
      - id (INTEGER)
      - user_id (INTEGER)
      - book_id (INTEGER)
      - borrow_date (DATETIME)
      - due_date (DATETIME)
      - return_date (DATETIME, nullable)
      - status (ENUM: 'borrowed', 'returned', 'overdue')
    Relationships:
      - References users (user_id)
      - References books (book_id)

    Table: authors
    Columns:
      - id (INTEGER)
      - name (VARCHAR)
      - nationality (VARCHAR)
    Relationships:
      - Many-to-Many with books via book_authors

    Table: book_authors
    Columns:
      - book_id (INTEGER)
      - author_id (INTEGER)
    Relationships:
      - References books (book_id)
      - References authors (author_id)

    Sample Data:
    Table: users
      - {{'id': 1, 'username': 'jdoe', 'email': 'jdoe@example.com', 'role': 'librarian'}}
      - {{'id': 2, 'username': 'asmith', 'email': 'asmith@example.com', 'role': 'user'}}

    Table: books
      - {{'id': 1, 'title': 'The Great Gatsby', 'publisher': 'Scribner', 'category_id': 1, 'total_copies': 10, 'available_copies': 5, 'language': 'English'}}
      - {{'id': 2, 'title': '1984', 'publisher': 'Secker & Warburg', 'category_id': 2, 'total_copies': 8, 'available_copies': 3, 'language': 'English'}}

    Table: borrowing
      - {{'id': 1, 'user_id': 2, 'book_id': 5, 'borrow_date': '2023-09-01', 'due_date': '2023-09-15', 'return_date': None, 'status': 'borrowed'}}
      - {{'id': 2, 'user_id': 1, 'book_id': 3, 'borrow_date': '2023-08-15', 'due_date': '2023-08-30', 'return_date': '2023-08-25', 'status': 'returned'}}

    Convert the following natural language query into an SQL query:
    Query: "{natural_language_query}"
    SQL:
    """

    try:
        # Use the correct model name and method
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Error generating SQL query: {str(e)}")