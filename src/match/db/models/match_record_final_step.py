# match_record_final_step.py
from dataclasses import dataclass

from sqlalchemy import Column, Integer, SmallInteger, Float, DateTime, TIMESTAMP
from sqlalchemy.types import DECIMAL
from .base import BaseModel
class MatchRecordFinalStep(BaseModel):
    __tablename__ = "match_record_final_step"

    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")

    # 基本比赛信息
    match_id = Column(Integer, nullable=False, comment="比赛ID", index=True)
    league_id = Column(Integer, nullable=False, comment="联赛ID")

     #联赛相关统计
    league_count = Column(SmallInteger, comment="联赛数量")
    home_win_rate = Column(Float, comment="主队胜率")
    home_noloose_rate = Column(Float, comment="主队不败率")
    eq_rate = Column(Float, comment="平局率")

    # 盘口与进球概率相关
    cross_pk_count = Column(SmallInteger, comment="穿盘数量（非平局）")
    cross_pk_win_rate = Column(Float, comment="上盘赢球率")
    eq_pk_rate = Column(Float, comment="平手盘率")
    pk_le025_rate = Column(Float, comment="盘口小于等于0.25率")
    goals0_rate = Column(Float, comment="0球率")
    goalsle1_rate = Column(Float, comment="小于等于1球率")
    goalsle2_rate = Column(Float, comment="小于等于2球率")
    goalsge3_rate = Column(Float, comment="大于等于2球率")

    # 技术统计领先相关
    tech_advan1_count = Column(SmallInteger, comment="技术统计领先1数量")
    tech_advan1_win_rate = Column(Float, comment="技术统计领先1赢球率")
    tech_advan1_noloose_rate = Column(Float, comment="技术统计领先1不败率")
    tech_advan2_count = Column(SmallInteger, comment="技术统计领先2数量")
    tech_advan2_win_rate = Column(Float, comment="技术统计领先2赢球率")
    tech_advan2_noloose_rate = Column(Float, comment="技术统计领先2不败率")
    tech_advan3_count = Column(SmallInteger, comment="技术统计领先3数量")
    tech_advan3_win_rate = Column(Float, comment="技术统计领先3赢球率")
    tech_advan3_noloose_rate = Column(Float, comment="技术统计领先3不败率")

    # 新增字段 - 近期天数
    recent_days = Column(SmallInteger, comment="近期天数")

    # 新增字段 - 我方统计数据
    my_recent_count = Column(SmallInteger, comment="我方近期比赛数量")
    my_avg_goals = Column(Float, comment="我方平均进球数")
    my_avg_loose_goals = Column(Float, comment="我方平均失球数")
    my_win_rate = Column(Float, comment="我方赢球率")
    my_noloose_rate = Column(Float, comment="我方不败率")
    my_rq_rate = Column(Float, comment="我方让球盘率")
    my_bei_rq_rate = Column(Float, comment="我方被让球盘率")
    my_tech_avg_short_all = Column(Float, comment="我方平均射门总数")
    my_tech_avg_short_score = Column(Float, comment="我方平均射门得分数")
    my_tech_avg_bei_short_all = Column(Float, comment="我方平均被射门数")
    my_tech_avg_bei_short_score = Column(Float, comment="我方平均被射门数（每被设多少次被破门一次）")

    # 新增字段 - 我方最近一场数据
    my_recent1_start_pk = Column(Float, comment="我方近一场盘口")
    my_recent1_goals = Column(SmallInteger, comment="我方近一场进球")
    my_recent1_loose_goals = Column(SmallInteger, comment="我方近一场失球")
    my_recent1_result = Column(SmallInteger, comment="我方近一场结果")
    my_recent1_mult_short_all = Column(Float, comment="我方近一场总射门比")
    my_recent1_mult_attack_all = Column(Float, comment="我方近一场总进攻比")

    # 新增字段 - 我方最近二场数据
    my_recent2_start_pk = Column(Float, comment="我方近2场盘口")
    my_recent2_goals = Column(SmallInteger, comment="我方近2场进球")
    my_recent2_loose_goals = Column(SmallInteger, comment="我方近2场失球")
    my_recent2_result = Column(SmallInteger, comment="我方近2场结果")
    my_recent2_mult_short_all = Column(Float, comment="我方近2场总射门比")
    my_recent2_mult_attack_all = Column(Float, comment="我方近2场总进攻比")

    # 新增字段 - 对方统计数据
    other_recent_count = Column(SmallInteger, comment="对方近期比赛数量")
    other_avg_goals = Column(Float, comment="对方平均进球数")
    other_avg_loose_goals = Column(Float, comment="对方平均失球数")
    other_win_rate = Column(Float, comment="对方赢球率")
    other_noloose_rate = Column(Float, comment="对方不败率")
    other_rq_rate = Column(Float, comment="对方让球盘率")
    other_bei_rq_rate = Column(Float, comment="对方被让球盘率")
    other_tech_avg_short_all = Column(Float, comment="对方平均射门总数")
    other_tech_avg_short_score = Column(Float, comment="对方平均射门得分数")
    other_tech_avg_bei_short_all = Column(Float, comment="对方平均被射门数")
    other_tech_avg_bei_short_score = Column(Float, comment="对方平均被射门数（每被射多少次被攻破门一次）")

    # 新增字段 - 对方最近一场数据
    other_recent1_start_pk = Column(Float, comment="对方近一场盘口")
    other_recent1_goals = Column(SmallInteger, comment="对方近一场进球")
    other_recent1_loose_goals = Column(SmallInteger, comment="对方近一场失球")
    other_recent1_result = Column(SmallInteger, comment="对方近一场结果")
    other_recent1_mult_short_all = Column(Float, comment="对方近一场总射门比")
    other_recent1_mult_attack_all = Column(Float, comment="对方近一场总进攻比")

    # 新增字段 - 对方最近二场数据
    other_recent2_start_pk = Column(Float, comment="对方近2场盘口")
    other_recent2_goals = Column(SmallInteger, comment="对方近2场进球")
    other_recent2_loose_goals = Column(SmallInteger, comment="对方近2场失球")
    other_recent2_result = Column(SmallInteger, comment="对方近2场结果")
    other_recent2_mult_short_all = Column(Float, comment="对方近2场总射门比")
    other_recent2_mult_attack_all = Column(Float, comment="对方近2场总进攻比")

    proprity:int = Column(SmallInteger, default=0, comment="优先级，0野鸡比赛，1单场，2竞彩")
    match_start_time = Column(DateTime, nullable=False, comment="比赛开始时间(北京时间)")
    my_team_id = Column(Integer, nullable=False, comment="我队ID")
    other_team_id = Column(Integer, nullable=False, comment="他队ID")
    is_home = Column(SmallInteger, nullable=False, comment="是否主场(1:主场,0:客场)")

    # 盘口数据
    start_pk = Column(Float, comment="比赛初盘")
    my_score = Column(SmallInteger, comment="我队比分")
    other_score = Column(SmallInteger, comment="他队比分")
    is_half = Column(SmallInteger, comment="0:上半场，1：下半场")
    match_time = Column(SmallInteger, comment="比赛时间(分钟)")
    sort_match_time = Column(SmallInteger, comment="有顺序的比赛时间（上半场超过45分钟按45分钟算）")
    pankou = Column(Float, comment="当前盘口")
    curr_odd = Column(Float, comment="当前赔率")

    # 基础技术统计字段
    my_short = Column(SmallInteger, comment="我队射门次数")
    other_short = Column(SmallInteger, comment="他队射门次数")
    my_short_ok = Column(SmallInteger, comment="我队射正次数")
    other_short_ok = Column(SmallInteger, comment="他队射正次数")
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

    # 近4分钟技术统计
    min4_my_short = Column(SmallInteger, comment="近4分钟我队射门次数")
    min4_other_short = Column(SmallInteger, comment="近4分钟他队射门次数")
    min4_my_short_ok = Column(SmallInteger, comment="近4分钟我队射正次数")
    min4_other_short_ok = Column(SmallInteger, comment="近4分钟他队射正次数")
    min4_my_jiaoqiu = Column(SmallInteger, comment="近4分钟我队角球数量")
    min4_other_jiaoqiu = Column(SmallInteger, comment="近4分钟他队角球数量")
    min4_my_attack = Column(SmallInteger, comment="近4分钟我队进攻数量")
    min4_other_attack = Column(SmallInteger, comment="近4分钟他队进攻数量")
    min4_my_ser_attack = Column(SmallInteger, comment="近4分钟我队危险进攻数量")
    min4_other_ser_attack = Column(SmallInteger, comment="近4分钟他队危险进攻数量")

    # 近8分钟技术统计
    min8_my_short = Column(SmallInteger, comment="近8分钟我队射门次数")
    min8_other_short = Column(SmallInteger, comment="近8分钟他队射门次数")
    min8_my_short_ok = Column(SmallInteger, comment="近8分钟我队射正次数")
    min8_other_short_ok = Column(SmallInteger, comment="近8分钟他队射正次数")
    min8_my_jiaoqiu = Column(SmallInteger, comment="近8分钟我队角球数量")
    min8_other_jiaoqiu = Column(SmallInteger, comment="近8分钟他队角球数量")
    min8_my_attack = Column(SmallInteger, comment="近8分钟我队进攻数量")
    min8_other_attack = Column(SmallInteger, comment="近8分钟他队进攻数量")
    min8_my_ser_attack = Column(SmallInteger, comment="近8分钟我队危险进攻数量")
    min8_other_ser_attack = Column(SmallInteger, comment="近8分钟他队危险进攻数量")

    # 近13分钟技术统计
    min13_my_short = Column(SmallInteger, comment="近13分钟我队射门次数")
    min13_other_short = Column(SmallInteger, comment="极13分钟他队射门次数")
    min13_my_short_ok = Column(SmallInteger, comment="近13分钟我队射正次数")
    min13_other_short_ok = Column(SmallInteger, comment="近13分钟他队射正次数")
    min13_my_jiaoqiu = Column(SmallInteger, comment="近13分钟我队角球数量")
    min13_other_jiaoqiu = Column(SmallInteger, comment="近13分钟他队角球数量")
    min13_my_attack = Column(SmallInteger, comment="近13分钟我队进攻数量")
    min13_other_attack = Column(SmallInteger, comment="近13分钟他队进攻数量")
    min13_my_ser_attack = Column(SmallInteger, comment="近13分钟我队危险进攻数量")
    min13_other_ser_attack = Column(SmallInteger, comment="近13分钟他队危险进攻数量")

    # 近18分钟技术统计
    min18_my_short = Column(SmallInteger, comment="近18分钟我队射门次数")
    min18_other_short = Column(SmallInteger, comment="近18分钟他队射门次数")
    min18_my_short_ok = Column(SmallInteger, comment="近18分钟我队射正次数")
    min18_other_short_ok = Column(SmallInteger, comment="近18分钟他队射正次数")
    min18_my_jiaoqiu = Column(SmallInteger, comment="近18分钟我队角球数量")
    min18_other_jiaoqiu = Column(SmallInteger, comment="近18分钟他队角球数量")
    min18_my_attack = Column(SmallInteger, comment="近18分钟我队进攻数量")
    min18_other_attack = Column(SmallInteger, comment="近18分钟他队进攻数量")
    min18_my_ser_attack = Column(SmallInteger, comment="近18分钟我队危险进攻数量")
    min18_other_ser_attack = Column(SmallInteger, comment="近18分钟他队危险进攻数量")

    # 近23分钟技术统计
    min23_my_short = Column(SmallInteger, comment="近23分钟我队射门次数")
    min23_other_short = Column(SmallInteger, comment="近23分钟他队射门次数")
    min23_my_short_ok = Column(SmallInteger, comment="近23分钟我队射正次数")
    min23_other_short_ok = Column(SmallInteger, comment="近23分钟他队射正次数")
    min23_my_jiaoqiu = Column(SmallInteger, comment="近23分钟我队角球数量")
    min23_other_jiaoqiu = Column(SmallInteger, comment="近23分钟他队角球数量")
    min23_my_attack = Column(SmallInteger, comment="近23分钟我队进攻数量")
    min23_other_attack = Column(SmallInteger, comment="近23分钟他队进攻数量")
    min23_my_ser_attack = Column(SmallInteger, comment="近23分钟我队危险进攻数量")
    min23_other_ser_attack = Column(SmallInteger, comment="近23分钟他队危险进攻数量")

    # 半场技术统计
    half_my_short = Column(SmallInteger, comment="相对半场我队射门次数")
    half_other_short = Column(SmallInteger, comment="相对半场他队射门次数")
    half_my_short_ok = Column(SmallInteger, comment="相对半场我队射正次数")
    half_other_short_ok = Column(SmallInteger, comment="相对半场他队射正次数")
    half_my_jiaoqiu = Column(SmallInteger, comment="相对半场极队角球数量")
    half_other_jiaoqiu = Column(SmallInteger, comment="相对半场他队角球数量")
    half_my_attack = Column(SmallInteger, comment="相对半场我队进攻数量")
    half_other_attack = Column(SmallInteger, comment="相对半场他队进攻数量")
    half_my_ser_attack = Column(SmallInteger, comment="相对半场我队危险进攻数量")
    half_other_ser_attack = Column(SmallInteger, comment="相对半场他队危险进攻数量")

    # 最终结果字段
    final_my_score = Column(SmallInteger, comment="我队最终得分")
    final_other_score = Column(SmallInteger, comment="他队最终得分")
    final_result = Column(SmallInteger, comment="我队结果(3:胜,1:平,0:负)")
    final_mult_short = Column(Float, comment="我队最终射门比")
    final_mult_short_jiao = Column(Float, comment="我队最终射门角球比")
    final_mult_ser_attack = Column(Float, comment="我队最终危险进攻比")
    final_mult_attack = Column(Float, comment="我队最终总进攻比")
    final_yellow_card = Column(Integer, comment="最终我队黄牌数量")
    final_other_yellow_card = Column(Integer, comment="最终他队黄牌数量")
    final_red_card = Column(Integer, comment="最终我队红牌数量")
    final_other_red_card = Column(Integer, comment="最终他队红牌数量")
    bet_win_goals = Column(Float, comment="押注我队(追几球,被追为负数)")
    bet_win_pankou = Column(Float, comment="押注我队盈利盘口数")
    bet_win_amt = Column(DECIMAL(5, 2), comment="押注我队盈利金额")
    
    # 创建时间
    create_time = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", comment="创建时间")
