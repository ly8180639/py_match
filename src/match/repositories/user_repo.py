from typing import Optional

from sqlalchemy.orm import Session
from ..db.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, user_name: str) -> User | None:
        return self.db.query(User).filter(User.user_name == user_name).first()

        # 新增用户（已存在）
    def create(self, user_name: str, dept_id: str) -> User:
        user = User(user_name=user_name, dept_id=dept_id)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # 2. 新增修改用户方法
    def update(self, user_id: int, user_name: str = None, email: str = None) -> Optional[User]:
        """
        更新用户信息
        :param user_id: 要更新的用户ID
        :param user_name: 新用户名（可选）
        :return: 更新后的User对象或None（如果用户不存在）
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        if user_name is not None:
            user.user_name = user_name

        self.db.commit()
        self.db.refresh(user)
        return user