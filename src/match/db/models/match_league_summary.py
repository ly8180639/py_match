
# match_league_summary.py
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric
from .base import BaseModel

class MatchLeagueSummary(BaseModel):
    __tablename__ = "match_league_summary"

    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")

    # 基本联赛信息
    league_id = Column(Integer, nullable=False, comment="联赛ID")
    league_name = Column(String(100), comment="联赛名")
    match_league = Column(Integer, comment="1表示联赛")
    proprity = Column(Integer, comment="优先级")
    summary_batch_no = Column(String(100), comment="summary_start-summary_end")
    summary_start = Column(Date, comment="统计开始日期，时间为12点")
    summary_end = Column(Date, comment="统计截止日期，时间为12点")

    # 比赛统计数据
    match_count = Column(Integer, comment="比赛数量")
    home_win_count = Column(Integer, comment="主队赢的数量")
    home_win_rate = Column(Numeric(4, 3), comment="主队胜率")
    home_noloose_count = Column(Integer, comment="主队不输的数量")
    home_noloose_rate = Column(Numeric(4, 3), comment="主队不败率")
    eq_count = Column(Integer, comment="平局数量")
    eq_rate = Column(Numeric(4, 3), comment="平局率")

    # 盘口统计数据
    cross_pk_count = Column(Integer, comment="存在穿盘情况（非平手盘）的数量")
    cross_count = Column(Integer, comment="穿盘数量，赢的分-让的盘>0")
    cross_rate = Column(Numeric(4, 3), comment="穿盘率")
    pan_eq0_count = Column(Integer, comment="平手盘数量")
    pan_eq0_eq_count = Column(Integer, comment="平手盘平局数量")
    pan_eq0_eq_rate = Column(Numeric(4, 3), comment="平手盘平局率")

    # 进球统计数据
    goals0_count = Column(Integer, comment="0球数量")
    goals0_rate = Column(Numeric(4, 3), comment="0球率")
    goals1_count = Column(Integer, comment="1球数量")
    goals1_rate = Column(Numeric(4, 3), comment="1球率")
    goals2_count = Column(Integer, comment="2球数量")
    goals2_rate = Column(Numeric(4, 3), comment="2球率")
    goals3_count = Column(Integer, comment="3球数量")
    goals3_rate = Column(Numeric(4, 3), comment="3球率")
    goalsle3_count = Column(Integer, comment="小于等于3球数量")
    goalsle3_rate = Column(Numeric(4, 3), comment="小于等于3球率")
    goalsle2_count = Column(Integer, comment="小于等于2球数量")
    goalsle2_rate = Column(Numeric(4, 3), comment="小于等于2球率")
    goalsle1_count = Column(Integer, comment="小于等于1球数量")
    goalsle1_rate = Column(Numeric(4, 3), comment="小于等于1球率")

    # 让球盘统计数据
    pan_le025_count = Column(Integer, comment="让0.25以内的数量")
    pan_le025_eq_count = Column(Integer, comment="让0.25以内（包括平手）的平局数量")
    pan_le025_eq_rate = Column(Numeric(4, 3), comment="让0.25以内（包括平手）的占比")
    pan_eq025_count = Column(Integer, comment="让0.25的数量")
    pan_eq025_win_count = Column(Integer, comment="让0.25的上盘赢的数量")
    pan_eq025_win_rate = Column(Numeric(4, 3), comment="让0.25的上盘赢的占比")
    pan_eq025_noloose_count = Column(Integer, comment="让0.25的上盘不输的数量")
    pan_eq025_noloose_rate = Column(Numeric(4, 3), comment="让0.25的上盘不输的占比")
    pan_eq05_count = Column(Integer, comment="让0.5的上盘数量")
    pan_eq05_win_count = Column(Integer, comment="让0.5的上盘赢的数量")
    pan_eq05_win_rate = Column(Numeric(4, 3), comment="让0.5的上盘赢的占比")
    pan_eq05_noloose_count = Column(Integer, comment="让0.5的上盘不输的数量")
    pan_eq05_noloose_rate = Column(Numeric(4, 3), comment="让0.5的上盘不输的占比")
    pan_gt05_count = Column(Integer, comment="让大于0.5的上盘数量")
    pan_gt05_win_count = Column(Integer, comment="让大于0.5的上盘赢的数量")
    pan_gt05_win_rate = Column(Numeric(4, 3), comment="让大于0.5的上盘赢的占比")
    pan_gt05_noloose_count = Column(Integer, comment="让大于0.5的上盘不输的数量")
    pan_gt05_noloose_rate = Column(Numeric(4, 3), comment="让大于0.5的上盘不输的占比")
    pan_ge05_count = Column(Integer, comment="让大于等于0.5的上盘数量")
    pan_ge05_win_count = Column(Integer, comment="让大于等于0.5的上盘赢的数量")
    pan_ge05_win_rate = Column(Numeric(4, 3), comment="让大于等于0.5的上盘赢的占比")
    pan_ge05_noloose_count = Column(Integer, comment="让大于等于0.5的上盘不输的数量")
    pan_ge05_noloose_rate = Column(Numeric(4, 3), comment="让大于等于0.5的上盘不输的占比")

    # 领先球统计数据
    pan_ge05_lead2_goals_count = Column(Integer, comment="让大于等于0.5的上盘领先2球的数量")
    pan_ge05_lead2_goals_rate = Column(Numeric(4, 3), comment="让大于等于0.5的上盘领先2球的占比")
    lead2_goals_count = Column(Integer, comment="领先2球的数量")
    lead2_goals_rate = Column(Numeric(4, 3), comment="领先2球的占比")

    # 技术统计领先数据
    effect_tech_count = Column(Integer, comment="有效技术统计数量")
    tech_advan1_count = Column(Integer, comment="技术统计领先1数量")
    tech_advan1_win_count = Column(Integer, comment="技术统计领先1赢球数量")
    tech_advan1_win_rate = Column(Numeric(4, 3), comment="技术统计领先1赢球率")
    tech_advan1_noloose_count = Column(Integer, comment="技术统计领先1不输数量")
    tech_advan1_noloose_rate = Column(Numeric(4, 3), comment="技术统计领先1不败率")
    tech_advan2_count = Column(Integer, comment="技术统计领先2数量")
    tech_advan2_win_count = Column(Integer, comment="技术统计领先2赢球数量")
    tech_advan2_win_rate = Column(Numeric(4, 3), comment="技术统计领先2赢球率")
    tech_advan2_noloose_count = Column(Integer, comment="技术统计领先2不输数量")
    tech_advan2_noloose_rate = Column(Numeric(4, 3), comment="技术统计领先2不败率")
    tech_advan3_count = Column(Integer, comment="技术统计领先3数量")
    tech_advan3_win_count = Column(Integer, comment="技术统计领先3赢球数量")
    tech_advan3_win_rate = Column(Numeric(4, 3), comment="技术统计领先3赢球率")
    tech_advan3_noloose_count = Column(Integer, comment="技术统计领先3不输数量")
    tech_advan3_noloose_rate = Column(Numeric(4, 3), comment="技术统计领先3不败率")
    tech_advan4_count = Column(Integer, comment="技术统计领先4数量")
    tech_advan4_win_count = Column(Integer, comment="技术统计领先4赢球数量")
    tech_advan4_win_rate = Column(Numeric(4, 3), comment="技术统计领先4赢球率")
    tech_advan4_noloose_count = Column(Integer, comment="技术统计领先4不输数量")
    tech_advan4_noloose_rate = Column(Numeric(4, 3), comment="技术统计领先4不败率")

    # 创建时间
    create_time = Column(DateTime, comment="创建时间")
