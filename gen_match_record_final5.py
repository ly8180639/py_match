# gen_match_record_final5.py
import logging
from datetime import timedelta, datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from sqlalchemy.exc import SQLAlchemyError

from src.match.db.models.match_record_final_step import MatchRecordFinalStep
from src.match.db.models.match_record_final_step_start import MatchRecordFinalStepStart
from src.match.db.models.match_finish_id import MatchFinishId
from src.match.db.session import SessionLocal
from src.match.utils.match_utils import calculate_ratio, add_num

logger = logging.getLogger(__name__)

# 批处理大小
BATCH_SIZE = 100

def process_all_matches():
    """
    从MatchRecordFinalStep中抽取数据，每场比赛有多条数据，只取my_team_id不一致的两条数据
    直接复制到MatchRecordFinalStepStart中
    """
    db: Session = SessionLocal()
    # 获取所有不重复的match_id
    match_ids = db.query(func.distinct(MatchRecordFinalStep.match_id)) \
                      .all()
    logger.info(f"共找到 {len(match_ids)} 场不同的比赛")

    # 提取match_id值
    match_id_list = [match_id[0] for match_id in match_ids]
    processed_records = 0

    # 对于每个match_id，只选择my_team_id不一致的两条记录
    for match_id in match_id_list:
        # 获取该match_id的所有记录
        all_records = db.query(MatchRecordFinalStep) \
                        .filter(MatchRecordFinalStep.match_id == match_id) \
                        .all()

        # 找出my_team_id不一致的两条记录
        selected_records = []
        used_my_team_ids = set()

        for record in all_records:
            if record.my_team_id not in used_my_team_ids:
                selected_records.append(record)
                used_my_team_ids.add(record.my_team_id)

                # 只取前两条my_team_id不一致的记录
                if len(selected_records) == 2:
                    break

        # 复制选中的记录到新表
        for record in selected_records:
            try:
                new_record = create_start_record_from_final_step(record)
                db.add(new_record)
                processed_records += 1

            except Exception as e:
                logger.error(f"处理比赛ID {record.match_id} 时出错: {str(e)}")
                continue
        # 提交当前批次的事务
        if processed_records % BATCH_SIZE == 0:
            db.commit()
            logger.info(f"已处理 {processed_records} 条记录")

    db.commit()





def create_start_record_from_final_step(match: MatchRecordFinalStep) -> MatchRecordFinalStepStart:
    """
    从MatchRecordFinalStep创建MatchRecordFinalStepStart记录（直接复制）

    Args:
        match: 原始比赛记录
    """
    record = MatchRecordFinalStepStart()

    # 基本比赛信息
    record.match_id = match.match_id
    record.league_id = match.league_id
    record.match_start_time = match.match_start_time
    record.proprity = match.proprity
    record.my_team_id = match.my_team_id
    record.other_team_id = match.other_team_id
    record.is_home = match.is_home

    # 盘口数据
    record.start_pk = match.start_pk

    # 最终比分和结果
    record.final_my_score = match.final_my_score
    record.final_other_score = match.final_other_score
    record.final_result = match.final_result

    # 联赛统计数据
    record.league_count = match.league_count
    record.home_win_rate = match.home_win_rate
    record.home_noloose_rate = match.home_noloose_rate
    record.eq_rate = match.eq_rate

    # 盘口与进球概率相关
    record.cross_pk_count = match.cross_pk_count
    record.cross_pk_win_rate = match.cross_pk_win_rate
    record.eq_pk_rate = match.eq_pk_rate
    record.pk_le025_rate = match.pk_le025_rate
    record.goals0_rate = match.goals0_rate
    record.goalsle1_rate = match.goalsle1_rate
    record.goalsle2_rate = match.goalsle2_rate
    record.goalsge3_rate = match.goalsge3_rate

    # 技术统计领先相关
    record.tech_advan1_count = match.tech_advan1_count
    record.tech_advan1_win_rate = match.tech_advan1_win_rate
    record.tech_advan1_noloose_rate = match.tech_advan1_noloose_rate
    record.tech_advan2_count = match.tech_advan2_count
    record.tech_advan2_win_rate = match.tech_advan2_win_rate
    record.tech_advan2_noloose_rate = match.tech_advan2_noloose_rate
    record.tech_advan3_count = match.tech_advan3_count
    record.tech_advan3_win_rate = match.tech_advan3_win_rate
    record.tech_advan3_noloose_rate = match.tech_advan3_noloose_rate

    # 近期天数
    record.recent_days = match.recent_days

    # 我方统计数据
    record.my_recent_count = match.my_recent_count
    record.my_avg_goals = match.my_avg_goals
    record.my_avg_loose_goals = match.my_avg_loose_goals
    record.my_win_rate = match.my_win_rate
    record.my_noloose_rate = match.my_noloose_rate
    record.my_rq_rate = match.my_rq_rate
    record.my_bei_rq_rate = match.my_bei_rq_rate
    record.my_tech_avg_short_all = match.my_tech_avg_short_all
    record.my_tech_avg_short_score = match.my_tech_avg_short_score
    record.my_tech_avg_bei_short_all = match.my_tech_avg_bei_short_all
    record.my_tech_avg_bei_short_score = match.my_tech_avg_bei_short_score

    # 我方最近一场数据
    record.my_recent1_start_pk = match.my_recent1_start_pk
    record.my_recent1_goals = match.my_recent1_goals
    record.my_recent1_loose_goals = match.my_recent1_loose_goals
    record.my_recent1_result = match.my_recent1_result
    record.my_recent1_mult_short_all = match.my_recent1_mult_short_all
    record.my_recent1_mult_attack_all = match.my_recent1_mult_attack_all

    # 我方最近二场数据
    record.my_recent2_start_pk = match.my_recent2_start_pk
    record.my_recent2_goals = match.my_recent2_goals
    record.my_recent2_loose_goals = match.my_recent2_loose_goals
    record.my_recent2_result = match.my_recent2_result
    record.my_recent2_mult_short_all = match.my_recent2_mult_short_all
    record.my_recent2_mult_attack_all = match.my_recent2_mult_attack_all

    # 对方统计数据
    record.other_recent_count = match.other_recent_count
    record.other_avg_goals = match.other_avg_goals
    record.other_avg_loose_goals = match.other_avg_loose_goals
    record.other_win_rate = match.other_win_rate
    record.other_noloose_rate = match.other_noloose_rate
    record.other_rq_rate = match.other_rq_rate
    record.other_bei_rq_rate = match.other_bei_rq_rate
    record.other_tech_avg_short_all = match.other_tech_avg_short_all
    record.other_tech_avg_short_score = match.other_tech_avg_short_score
    record.other_tech_avg_bei_short_all = match.other_tech_avg_bei_short_all
    record.other_tech_avg_bei_short_score = match.other_tech_avg_bei_short_score

    # 对方最近一场数据
    record.other_recent1_start_pk = match.other_recent1_start_pk
    record.other_recent1_goals = match.other_recent1_goals
    record.other_recent1_loose_goals = match.other_recent1_loose_goals
    record.other_recent1_result = match.other_recent1_result
    record.other_recent1_mult_short_all = match.other_recent1_mult_short_all
    record.other_recent1_mult_attack_all = match.other_recent1_mult_attack_all

    # 对方最近二场数据
    record.other_recent2_start_pk = match.other_recent2_start_pk
    record.other_recent2_goals = match.other_recent2_goals
    record.other_recent2_loose_goals = match.other_recent2_loose_goals
    record.other_recent2_result = match.other_recent2_result
    record.other_recent2_mult_short_all = match.other_recent2_mult_short_all
    record.other_recent2_mult_attack_all = match.other_recent2_mult_attack_all
    record.create_time=datetime.now()
    return record


if __name__ == '__main__':
    """
    从MatchRecordFinalStep中抽取部分数据，每场比赛有多条数据，只取my_team_id不一致的两条数据
    直接复制到MatchRecordFinalStepStart中
    """
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 处理所有比赛记录
    process_all_matches()
