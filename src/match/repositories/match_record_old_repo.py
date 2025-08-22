# match_record_old_repository.py
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import delete
from ..db.models.match_record_old import  MatchRecordOld


class MatchRecordOldRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, match_record: MatchRecordOld) -> MatchRecordOld:
        """
        创建单个 MatchRecordOld 记录

        Args:
            match_record: MatchRecordOld 实例

        Returns:
            MatchRecordOld: 创建后的实例
        """
        self.db_session.add(match_record)
        self.db_session.commit()
        self.db_session.refresh(match_record)
        return match_record

    def bulk_create(self, match_records: List[MatchRecordOld]) -> List[MatchRecordOld]:
        """
        批量插入 MatchRecordOld 记录

        Args:
            match_records: MatchRecordOld 实例列表

        Returns:
            List[MatchRecordOld]: 创建后的实例列表
        """
        self.db_session.add_all(match_records)
        self.db_session.commit()

        # 刷新所有记录以获取数据库生成的字段值
        for record in match_records:
            self.db_session.refresh(record)

        return match_records

    def get_by_id(self, record_id: int) -> Optional[MatchRecordOld]:
        """
        根据 ID 获取 MatchRecordOld 记录

        Args:
            record_id: 记录 ID

        Returns:
            Optional[MatchRecordOld]: 找到的记录或 None
        """
        return self.db_session.query(MatchRecordOld).filter(MatchRecordOld.id == record_id).first()

    def get_by_match_id(self, match_id: int) -> Optional[MatchRecordOld]:
        """
        根据比赛 ID 获取 MatchRecordOld 记录

        Args:
            match_id: 比赛 ID

        Returns:
            Optional[MatchRecordOld]: 找到的记录或 None
        """
        return self.db_session.query(MatchRecordOld).filter(MatchRecordOld.match_id == match_id).first()

    def list_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[MatchRecordOld]:
        """
        获取所有 MatchRecordOld 记录

        Args:
            limit: 限制返回记录数
            offset: 偏移量

        Returns:
            List[MatchRecordOld]: 记录列表
        """
        query = self.db_session.query(MatchRecordOld)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

    def update(self, record_id: int, **kwargs) -> bool:
        """
        更新 MatchRecordOld 记录

        Args:
            record_id: 记录 ID
            **kwargs: 需要更新的字段键值对

        Returns:
            bool: 更新是否成功
        """
        record = self.db_session.query(MatchRecordOld).filter(MatchRecordOld.id == record_id).first()
        if not record:
            return False

        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)

        self.db_session.commit()
        return True

    def delete(self, record_id: Union[int, List[int]]) -> int:
        """
        删除 MatchRecordOld 记录

        Args:
            record_id: 记录 ID 或 ID 列表

        Returns:
            int: 删除的记录数量
        """
        if isinstance(record_id, int):
            # 删除单个记录
            record = self.db_session.query(MatchRecordOld).filter(MatchRecordOld.id == record_id).first()
            if record:
                self.db_session.delete(record)
                self.db_session.commit()
                return 1
            return 0
        elif isinstance(record_id, list):
            # 批量删除
            deleted_count = self.db_session.query(MatchRecordOld).filter(MatchRecordOld.id.in_(record_id)).delete()
            self.db_session.commit()
            return deleted_count
        else:
            raise ValueError("record_id must be an integer or list of integers")

    def delete_by_match_id(self, match_id: int) -> int:
        """
        根据比赛 ID 删除记录

        Args:
            match_id: 比赛 ID

        Returns:
            int: 删除的记录数量
        """
        deleted_count = self.db_session.query(MatchRecordOld).filter(MatchRecordOld.match_id == match_id).delete()
        self.db_session.commit()
        return deleted_count
