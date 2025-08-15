from src.match.db.session import SessionLocal
from src.match.repositories.user_repo import UserRepository

if __name__ == '__main__':
    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_by_id(3)
    print(user.__dict__)