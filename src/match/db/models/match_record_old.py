from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Float
from .base import BaseModel



class MatchRecordOld(BaseModel):
    __tablename__ = "match_record_old_240911_250714"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer)  # 比赛id
    league = Column(String(64))  # 联赛
    league_id = Column(Integer)
    home_team = Column(String(64))  # 主队
    home_team_id = Column(Integer)
    guest_team = Column(String(64))  # 客队
    guest_team_id = Column(Integer)
    proprity = Column(Integer)  # 级别，0野鸡比赛，1单场，2竞彩
    match_start_time = Column(DateTime)  # 比赛开始时间(北京时间)
    match_time = Column(SmallInteger)  # 比赛时间
    is_half = Column(Integer)  # 0:上半场，1：下半场
    start_pk = Column(Float)  # 初始盘口
    home_score = Column(Integer)  # 主队比分
    guest_score = Column(Integer)  # 客队比分
    pankou = Column(Float)  # 盘口
    odd_time = Column(String(32))  # 水位的时间
    home_odd = Column(Float)  # 主队水位
    guest_odd = Column(Float)  # 客队水位
    odd_change = Column(String(32))  # up/down 主队水位变化
    home_ctl = Column(Float)  # 主队控球率
    guest_ctl = Column(Float)  # 客队控球率
    home_attack = Column(Integer)  # 主队进攻数量
    guest_attack = Column(Integer)  # 客队进攻数量
    home_ser_attack = Column(Integer)  # 主队危险进攻次数
    guest_ser_attack = Column(Integer)  # 客队危险进攻次数
    home_short = Column(Integer)  # 主队射门次数
    guest_short = Column(Integer)  # 客队射门次数
    home_short_ok = Column(Integer)  # 主队射正次数
    guest_short_ok = Column(Integer)  # 客队射正次数
    start_dx = Column(String(32))  # 初始大小球盘口
    home_dx_odd = Column(Float)  # 大小球主队水位
    guest_dx_odd = Column(Float)  # 大小球客队水位
    dx_pankou = Column(String(32))  # 大小球盘口
    home_jiaoqiu = Column(Integer)  # 主队角球
    guest_jiaoqiu = Column(Integer)  # 客队角球
    ext_home_tech1 = Column(String(64))  # 主队其他技术统计
    ext_guest_tech1 = Column(String(64))  # 客队其他技术统计
    ext_home_tech2 = Column(String(64))
    ext_guest_tech2 = Column(String(64))
    ext_home_tech3 = Column(String(64))
    ext_guest_tech3 = Column(String(64))
    create_time = Column(DateTime, default=datetime.utcnow)  # 插入该条数据的时间
