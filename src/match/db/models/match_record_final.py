# match_record_final.py
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, SmallInteger, DECIMAL, TIMESTAMP
from .base import BaseModel
class MatchRecordFinal(BaseModel):
    __tablename__ = "match_record_final_origin"

    # 主键
    id = Column(Integer, primary_key=True, comment="主键")

    # 基本比赛信息
    match_id = Column(Integer, nullable=False, comment="比赛ID", index=True)
    league_id = Column(Integer, nullable=False, comment="联赛ID")
    proprity = Column(Integer, nullable=False, comment="优先级，0野鸡比赛，1单场，2竞彩")
    match_start_time = Column(DateTime, nullable=False, comment="比赛开始时间(北京时间)")
    my_team_id = Column(Integer, nullable=False, comment="我队ID")
    other_team_id = Column(Integer, nullable=False, comment="他队ID")
    is_home = Column(Integer, nullable=False, comment="是否主场(1:主场,0:客场)")

    # 盘口数据
    start_pk = Column(Float, comment="比赛初盘")
    my_score = Column(Integer, comment="我队当前得分")
    other_score = Column(Integer, comment="他队当前得分")

    is_half = Column(Integer)  # 0:上半场，1：下半场
    match_time = Column(SmallInteger, comment="比赛时间(分钟)")
    sort_match_time=Column(SmallInteger, comment="有顺序的比赛时间（上半场超过45分钟按45分钟算）")
    pankou = Column(Float, comment="当前盘口")
    odd_time = Column(SmallInteger, comment="水位时间")
    #但数据库存的不对，都是down，所以不能作为指标
    odd_change = Column(SmallInteger, comment="1表示上升，-1表示下降")
    curr_odd = Column(Float, comment="当前赔率")

    # 比赛过程数据
    my_short = Column(Integer, comment="我队射门次数")
    other_short = Column(Integer, comment="他队射门次数")
    my_short_ok = Column(Integer, comment="我队射正门次数")
    other_short_ok = Column(Integer, comment="他队射正门次数")
    my_jiaoqiu = Column(Integer, comment="我队角球数量")
    other_jiaoqiu = Column(Integer, comment="他队角球数量")
    my_attack = Column(Integer, comment="我队总进攻数量")
    other_attack = Column(Integer, comment="他队总进攻数量")
    my_ser_attack = Column(Integer, comment="我队危险进攻数量")
    other_ser_attack = Column(Integer, comment="他队危险进攻数量")
    my_ctl = Column(Float, comment="我队控球率(%)")
    other_ctl = Column(Float, comment="他队控球率(%)")
    my_yellow_card = Column(Integer, comment="我队黄牌数量")
    other_yellow_card = Column(Integer, comment="他队黄牌数量")
    my_red_card = Column(Integer, comment="我队红牌数量")
    other_red_card = Column(Integer, comment="他队红牌数量")

    # 最终对比数据(负值表示对方是我方多少倍)
    final_my_score = Column(Integer, comment="我队最终得分")
    final_other_score = Column(Integer, comment="他队最终得分")
    final_result = Column(Integer, comment="我队结果(3:胜,1:平,0:负)")

    final_mult_short = Column(Float, comment="我队最终射门比")
    final_mult_short_jiao = Column(Float, comment="我队最终射门+角球比")
    final_mult_ser_attack = Column(Float, comment="我队最终危险进攻比")
    final_mult_attack = Column(Float, comment="我队最终总进攻比")

    # 最终结果数据
    final_yellow_card = Column(Integer, comment="最终我队黄牌数量")
    final_other_yellow_card = Column(Integer, comment="最终他队黄牌数量")
    final_red_card = Column(Integer, comment="最终我队红牌数量")
    final_other_red_card = Column(Integer, comment="最终他队红牌数量")

    # 比赛结果和投注相关
    bet_win_goals = Column(Float, comment="押注我队(追几球,被追为负数)")
    bet_win_pankou = Column(Float, comment="押注我队盈利盘口数(1:全赢,0.5:赢一半,0:走水,-0.5:输一半,-1:全输)")
    bet_win_amt = Column(DECIMAL(5, 2), comment="押注我队盈利金额")

    # 创建时间
    create_time:datetime = Column(TIMESTAMP, default=datetime.utcnow, comment="创建时间")
