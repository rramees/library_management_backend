from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User
from app.core.security import generate_api_key

def fix_missing_api_keys():
    db: Session = SessionLocal()

    try:
        # Query all users with a NULL api_key
        users_without_api_key = db.query(User).filter(User.api_key == None).all()

        print(f"Found {len(users_without_api_key)} users without API keys.")

        for user in users_without_api_key:
            # Generate a new API key
            user.api_key = generate_api_key()
            print(f"Generated API key for user: {user.username}")

        # Commit the changes to the database
        db.commit()
        print("All missing API keys have been generated and saved.")

    except Exception as e:
        db.rollback()
        print(f"Error fixing missing API keys: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_missing_api_keys()