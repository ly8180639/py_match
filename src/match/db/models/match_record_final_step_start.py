# match_record_final_step_start.py
from sqlalchemy import Column, Integer, SmallInteger, Float, DateTime, TIMESTAMP
from .base import BaseModel

class MatchRecordFinalStepStart(BaseModel):
    __tablename__ = "match_record_final_step_start"

    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")

    # 基本比赛信息
    match_id = Column(Integer, nullable=False, comment="比赛ID")
    league_id = Column(Integer, nullable=False, comment="联赛ID")
    match_start_time = Column(DateTime, nullable=False, comment="比赛开始时间(北京时间)")
    
    # 比赛属性
    proprity = Column(SmallInteger, default=0, comment="优先级，0野鸡比赛，1单场，2竞彩")
    my_team_id = Column(Integer, nullable=False, comment="我队ID")
    other_team_id = Column(Integer, nullable=False, comment="他队ID")
    is_home = Column(SmallInteger, nullable=False, comment="是否主场(1:主场,0:客场)")
    
    # 盘口与比分
    start_pk = Column(Float, comment="比赛初盘")
    final_my_score = Column(SmallInteger, comment="我队最终得分")
    final_other_score = Column(SmallInteger, comment="他队最终得分")
    final_result = Column(SmallInteger, comment="我队结果(3:胜,1:平,0:负)")
    
    # 联赛统计数据
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
    
    # 近期天数
    recent_days = Column(SmallInteger, comment="近期天数")
    
    # 我方统计数据
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
    my_tech_avg_bei_short_score = Column(Float, comment="我方平均被射门数（每被射多少次被攻破门一次）")
    
    # 我方最近一场数据
    my_recent1_start_pk = Column(Float, comment="我方近一场盘口")
    my_recent1_goals = Column(SmallInteger, comment="我方近一场进球")
    my_recent1_loose_goals = Column(SmallInteger, comment="我方近一场失球")
    my_recent1_result = Column(SmallInteger, comment="我方近一场结果")
    my_recent1_mult_short_all = Column(Float, comment="我方近一场总射门比")
    my_recent1_mult_attack_all = Column(Float, comment="我方近一场总进攻比")
    
    # 我方最近二场数据
    my_recent2_start_pk = Column(Float, comment="我方近2场盘口")
    my_recent2_goals = Column(SmallInteger, comment="我方近2场进球")
    my_recent2_loose_goals = Column(SmallInteger, comment="我方近2场失球")
    my_recent2_result = Column(SmallInteger, comment="我方近2场结果")
    my_recent2_mult_short_all = Column(Float, comment="我方近2场总射门比")
    my_recent2_mult_attack_all = Column(Float, comment="我方近2场总进攻比")
    
    # 对方统计数据
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
    
    # 对方最近一场数据
    other_recent1_start_pk = Column(Float, comment="对方近一场盘口")
    other_recent1_goals = Column(SmallInteger, comment="对方近一场进球")
    other_recent1_loose_goals = Column(SmallInteger, comment="对方近一场失球")
    other_recent1_result = Column(SmallInteger, comment="对方近一场结果")
    other_recent1_mult_short_all = Column(Float, comment="对方近一场总射门比")
    other_recent1_mult_attack_all = Column(Float, comment="对方近一场总进攻比")
    
    # 对方最近二场数据
    other_recent2_start_pk = Column(Float, comment="对方近2场盘口")
    other_recent2_goals = Column(SmallInteger, comment="对方近2场进球")
    other_recent2_loose_goals = Column(SmallInteger, comment="对方近2场失球")
    other_recent2_result = Column(SmallInteger, comment="对方近2场结果")
    other_recent2_mult_short_all = Column(Float, comment="对方近2场总射门比")
    other_recent2_mult_attack_all = Column(Float, comment="对方近2场总进攻比")
    
    # 创建时间
    create_time = Column(DateTime, comment="创建时间")
