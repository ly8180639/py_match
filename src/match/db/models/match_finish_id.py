# match_finish_id.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, SmallInteger
from .base import BaseModel


class MatchFinishId(BaseModel):
    __tablename__ = "match_finish_id240301_250714"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, unique=True)  # 唯一索引 match_id_unique_index
    league_id = Column(Integer, index=True)  # 索引 match_finish_id_league_id_IDX
    league = Column(String(192))
    home_team_id = Column(Integer)
    home_team = Column(String(192))
    guest_team_id = Column(Integer)
    guest_team = Column(String(192))
    proprity = Column(SmallInteger, default=0)  # 级别，默认值为0
    match_start_time = Column(DateTime, index=True)  # 索引 startTimeIndex
    start_pk = Column(Float)
    home_score = Column(Integer)
    guest_score = Column(Integer)
    home_ctl = Column(Float)
    guest_ctl = Column(Float)
    home_attack = Column(Integer)
    guest_attack = Column(Integer)
    home_ser_attack = Column(Integer)
    guest_ser_attack = Column(Integer)
    home_short = Column(Integer)
    guest_short = Column(Integer)
    home_short_ok = Column(Integer)
    guest_short_ok = Column(Integer)
    home_jiaoqiu = Column(Integer)
    guest_jiaoqiu = Column(Integer)
    ext_home_tech1 = Column(String(96))
    ext_guest_tech1 = Column(String(96))
    ext_home_tech2 = Column(String(96))
    ext_guest_tech2 = Column(String(96))
