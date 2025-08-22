from src.match.db.session import SessionLocal
from src.match.repositories.match_record_old_repo import MatchRecordOldRepository
from src.match.repositories.user_repo import UserRepository

if __name__ == '__main__':
    db = SessionLocal()
    # repo = UserRepository(db)
    # user = repo.get_by_id(3)
    # print(user)

    matchRecordOldResp=MatchRecordOldRepository(db)
    m1=  matchRecordOldResp.get_by_id(58829451)
    #打印m1的所有属性值
    print(m1.__dict__ if m1 else None)

