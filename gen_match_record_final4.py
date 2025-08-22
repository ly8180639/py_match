import logging
from datetime import timedelta, datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from sqlalchemy.exc import SQLAlchemyError

from src.match.db.models.match_record_final_step import MatchRecordFinalStep
from src.match.db.models.match_finish_id import MatchFinishId
from src.match.db.session import SessionLocal
from src.match.utils.match_utils import calculate_ratio, add_num

logger = logging.getLogger(__name__)

def get_team_recent_matches(db: Session, team_id: int, match_start_time: datetime, days: int = 50) -> List[MatchFinishId]:
    """
    获取指定球队在指定时间前指定天数内的比赛数据

    Args:
        db: 数据库会话
        team_id: 球队ID
        match_start_time: 比赛开始时间
        days: 天数范围，默认50天

    Returns:
        球队近期比赛数据列表
    """
    start_time = match_start_time - timedelta(days=days)
    end_time = match_start_time

    matches = db.query(MatchFinishId).filter(
        and_(
            MatchFinishId.match_start_time >= start_time,
            MatchFinishId.match_start_time < end_time,
            or_(
                MatchFinishId.home_team_id == team_id,
                MatchFinishId.guest_team_id == team_id
            )
        )
    ).order_by(desc(MatchFinishId.match_start_time)).all()

    return matches

def calculate_match_statistics(match: MatchFinishId, team_id: int) -> Dict[str, Any]:
    """
    计算单场比赛的各项统计数据

    Args:
        match: 比赛数据
        team_id: 球队ID

    Returns:
        包含各项统计数据的字典
    """
    # 判断球队是主队还是客队
    is_home_team = match.home_team_id == team_id

    if is_home_team:
        goals_scored = match.home_score if match.home_score is not None else 0
        goals_conceded = match.guest_score if match.guest_score is not None else 0
        shots = match.home_short if match.home_short is not None else 0
        shots_on_target = match.home_short_ok if match.home_short_ok is not None else 0
        corners = match.home_jiaoqiu if match.home_jiaoqiu is not None else 0
        attacks = match.home_attack if match.home_attack is not None else 0
        dangerous_attacks = match.home_ser_attack if match.home_ser_attack is not None else 0
        # 对方数据
        opponent_shots = match.guest_short if match.guest_short is not None else 0
        opponent_shots_on_target = match.guest_short_ok if match.guest_short_ok is not None else 0
        opponent_attacks = match.guest_attack if match.guest_attack is not None else 0
        opponent_dangerous_attacks = match.guest_ser_attack if match.guest_ser_attack is not None else 0
        # 初盘数据字段
        start_pk = match.start_pk if match.start_pk is not None else 0
    else:
        goals_scored = match.guest_score if match.guest_score is not None else 0
        goals_conceded = match.home_score if match.home_score is not None else 0
        shots = match.guest_short if match.guest_short is not None else 0
        shots_on_target = match.guest_short_ok if match.guest_short_ok is not None else 0
        corners = match.guest_jiaoqiu if match.guest_jiaoqiu is not None else 0
        attacks = match.guest_attack if match.guest_attack is not None else 0
        dangerous_attacks = match.guest_ser_attack if match.guest_ser_attack is not None else 0
        # 对方数据
        opponent_shots = match.home_short if match.home_short is not None else 0
        opponent_shots_on_target = match.home_short_ok if match.home_short_ok is not None else 0
        opponent_attacks = match.home_attack if match.home_attack is not None else 0
        opponent_dangerous_attacks = match.home_ser_attack if match.home_ser_attack is not None else 0
        # 初盘数据字段
        start_pk = -match.start_pk if match.start_pk is not None else 0

        # 计算结果 (胜=3, 平=1, 负=0)
    if goals_scored > goals_conceded:
        result = 3  # 胜
    elif goals_scored == goals_conceded:
        result = 1  # 平
    else:
        result = 0  # 负

        # 计算各项比率
        # 我方射门总数（射门数+射正数）/对方射门总数（射门数+射正数）

    mult_short_all = calculate_ratio(add_num(shots,shots_on_target),add_num(opponent_shots,opponent_shots_on_target))
    # 我方进攻总数（进攻数+危险进攻数）/对方进攻总数（进攻数+危险进攻数）
    mult_attack_all = calculate_ratio(add_num(attacks,dangerous_attacks),add_num(opponent_attacks,opponent_dangerous_attacks))

    stats = {
        'start_pk': start_pk,
        'goals': goals_scored,
        'loose_goals': goals_conceded,
        'result': result,
        'mult_short_all': mult_short_all,
        'mult_attack_all': mult_attack_all
    }

    return stats

def update_match_records_for_team(db: Session, match_id: int, team_id: int, recent1_stats: Dict[str, Any], recent2_stats: Dict[str, Any],
                                  other_recent1_stats: Dict[str, Any], other_recent2_stats: Dict[str, Any]
                                ):
    """
    更新指定比赛和球队的记录

    Args:
        db: 数据库会话
        match_id: 比赛ID
        team_id: 球队ID
        recent1_stats: 最近第一场比赛统计数据
        recent2_stats: 最近第二场比赛统计数据
        other_recent1_stats:对方最近一场比赛的技术统计
        other_recent2_stats:对方最近第二比赛的技术统计
        is_my_team: 是否为我的球队（True为my_team_id，False为other_team_id）
    """
    # 更新my_team_id相关的记录
    records = db.query(MatchRecordFinalStep).filter(
        and_(
            MatchRecordFinalStep.match_id == match_id,
            MatchRecordFinalStep.my_team_id == team_id
        )
    ).all()

    for record in records:
        if recent1_stats:
            record.my_recent1_start_pk = recent1_stats['start_pk']
            record.my_recent1_goals = recent1_stats['goals']
            record.my_recent1_loose_goals = recent1_stats['loose_goals']
            record.my_recent1_result = recent1_stats['result']
            record.my_recent1_mult_short_all = recent1_stats['mult_short_all']
            record.my_recent1_mult_attack_all = recent1_stats['mult_attack_all']

        if recent2_stats:
            record.my_recent2_start_pk = recent2_stats['start_pk']
            record.my_recent2_goals = recent2_stats['goals']
            record.my_recent2_loose_goals = recent2_stats['loose_goals']
            record.my_recent2_result = recent2_stats['result']
            record.my_recent2_mult_short_all = recent2_stats['mult_short_all']
            record.my_recent2_mult_attack_all = recent2_stats['mult_attack_all']

        if other_recent1_stats:
            record.other_recent1_start_pk = other_recent1_stats['start_pk']
            record.other_recent1_goals = other_recent1_stats['goals']
            record.other_recent1_loose_goals = other_recent1_stats['loose_goals']
            record.other_recent1_result = other_recent1_stats['result']
            record.other_recent1_mult_short_all = other_recent1_stats['mult_short_all']
            record.other_recent1_mult_attack_all = other_recent1_stats['mult_attack_all']

        if other_recent2_stats:
            record.other_recent2_start_pk = other_recent2_stats['start_pk']
            record.other_recent2_goals = other_recent2_stats['goals']
            record.other_recent2_loose_goals = other_recent2_stats['loose_goals']
            record.other_recent2_result = other_recent2_stats['result']
            record.other_recent2_mult_short_all = other_recent2_stats['mult_short_all']
            record.other_recent2_mult_attack_all = other_recent2_stats['mult_attack_all']


def process_match_by_id(db: Session, match_id: int):
    """
    按match_id处理单场比赛

    Args:
        db: 数据库会话
        match_id: 比赛ID
    """
    # 获取该match_id的所有记录，找出主客场team_id和比赛开始时间
    match_records:List[MatchRecordFinalStep] = db.query(MatchRecordFinalStep).filter(
        MatchRecordFinalStep.match_id == match_id
    ).all()

    if not match_records:
        logger.warning(f"No records found for match_id: {match_id}")
        return

    # 取第一条记录获取基本信息
    first_record = match_records[0]
    my_team_id = first_record.my_team_id
    other_team_id = first_record.other_team_id
    match_start_time = first_record.match_start_time

    logger.info(f"Processing match_id: {match_id}, my_team_id: {my_team_id}, other_team_id: {other_team_id}")

    # 获取我方球队近50天的比赛数据
    my_team_matches = get_team_recent_matches(db, my_team_id, match_start_time)

    # 获取对方球队近50天的比赛数据
    other_team_matches = get_team_recent_matches(db, other_team_id, match_start_time)

    # 计算我方球队统计数据
    my_recent1_stats = None
    my_recent2_stats = None

    if len(my_team_matches) >= 1:
        my_recent1_stats = calculate_match_statistics(my_team_matches[0], my_team_id)

    if len(my_team_matches) >= 2:
        my_recent2_stats = calculate_match_statistics(my_team_matches[1], my_team_id)

    # 计算对方球队统计数据
    other_recent1_stats = None
    other_recent2_stats = None

    if len(other_team_matches) >= 1:
        other_recent1_stats = calculate_match_statistics(other_team_matches[0], other_team_id)

    if len(other_team_matches) >= 2:
        other_recent2_stats = calculate_match_statistics(other_team_matches[1], other_team_id)

    # 更新我方球队相关的记录（my_team_id作为home_team_id）
    update_match_records_for_team(db, match_id, my_team_id, my_recent1_stats, my_recent2_stats,other_recent1_stats, other_recent2_stats)

    # 更新对方球队相关的记录（other_team_id作为away_team_id）
    update_match_records_for_team(db, match_id, other_team_id, other_recent1_stats, other_recent2_stats,my_recent1_stats,my_recent2_stats)

def process_all_matches():
    """
    处理所有比赛记录（按match_id维度处理）
    """
    db = SessionLocal()
    try:
        # 获取所有不同的match_id
        match_ids = (db.query(MatchRecordFinalStep.match_id).distinct().all())
                     # filter(MatchRecordFinalStep.my_recent1_mult_short_all.is_(None)).all())
        match_ids = [match_id[0] for match_id in match_ids]

        logger.info(f"Total matches to process: {len(match_ids)}")

        for i, match_id in enumerate(match_ids):
            try:
                process_match_by_id(db, match_id)
                if (i + 1) % 100 == 0:
                    logger.info(f"Processed {i + 1} matches")
                    db.commit()  # 每100个match_id提交一次事务
            except Exception as e:
                logger.error(f"Error processing match_id {match_id}: {str(e)}")
                db.rollback()

        # 提交所有更改
        db.commit()
        logger.info("All matches processed successfully")

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    """
    更新每场比赛，近两场比赛的的数据，
    """
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # logger.info("ss")
    # 处理所有比赛记录
    process_all_matches()
