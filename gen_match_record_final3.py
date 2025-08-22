import logging
from typing import List

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from src.match.db.models.match_record_final_step import MatchRecordFinalStep
from src.match.db.models.match_team_latest_summary_old import MatchTeamLatestSummaryOld
from src.match.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_match_record_final_step_orm(session):
    """
    使用ORM方式更新 match_record_final_step 表中的新增字段
    """
    try:
        logger.info("开始更新 match_record_final_step 记录")

        batch_size = 100
        last_max_match_id = 0
        batch_num = 0

        while True:
            try:
                batch_num += 1

                # 分批获取 match_id
                match_ids = session.query(MatchRecordFinalStep.match_id) \
                    .filter(MatchRecordFinalStep.match_id > last_max_match_id) \
                    .order_by(MatchRecordFinalStep.match_id) \
                    .limit(batch_size) \
                    .distinct() \
                    .all()

                # 提取 match_id 列表
                match_id_list = [match_id[0] for match_id in match_ids]

                # 如果没有更多记录，则退出循环
                if not match_id_list:
                    logger.info("没有更多记录需要处理")
                    break

                # 更新最大 match_id
                last_max_match_id = max(match_id_list)

                # 获取对应的 MatchRecordFinalStep 记录
                records: List[MatchRecordFinalStep] = session.query(MatchRecordFinalStep) \
                    .filter(MatchRecordFinalStep.match_id.in_(match_id_list)) \
                    .all()

                # 收集这批记录中涉及的 match_ids
                # match_ids = [record.match_id for record in records]

                # 获取相关的统计数据
                summaries: List[MatchTeamLatestSummaryOld] = session.query(MatchTeamLatestSummaryOld) \
                    .filter(MatchTeamLatestSummaryOld.curr_match_id.in_(match_id_list)) \
                    .all()

                # 创建一个便于查找的字典
                summary_dict = {}
                for summary in summaries:
                    summary_dict[summary.curr_match_id] = summary

                # 更新字段
                updated_count = 0
                for record in records:
                    match_id = record.match_id
                    my_team_id = record.my_team_id

                    if match_id not in summary_dict:
                        continue

                    summary: MatchTeamLatestSummaryOld = summary_dict[match_id]

                    # 根据 my_team_id 是主队还是客队来确定字段映射
                    is_my_team_main = (my_team_id == summary.team_id)

                    # 更新近期天数
                    record.recent_days = summary.recent_days

                    # 更新我方统计数据
                    if is_my_team_main:
                        record.my_recent_count = summary.my_recent_count
                        record.my_avg_goals = summary.my_avg_goals
                        record.my_avg_loose_goals = summary.my_avg_loose_goals
                        record.my_win_rate = summary.my_win_count / summary.my_recent_count if summary.my_recent_count > 0 else None
                        record.my_noloose_rate = (summary.my_recent_count - summary.my_loose_count) / summary.my_recent_count if summary.my_recent_count > 0 else None
                        record.my_rq_rate = summary.my_rq_count / summary.my_recent_count if summary.my_recent_count > 0 else None
                        record.my_bei_rq_rate = summary.my_bei_rq_count / summary.my_recent_count if summary.my_recent_count > 0 else None
                        record.my_tech_avg_short_all = summary.my_tech_avg_short_all
                        record.my_tech_avg_short_score = summary.my_tech_short_avg_score
                        record.my_tech_avg_bei_short_all = summary.my_tech_avg_bei_short_all
                        record.my_tech_avg_bei_short_score = summary.my_tech_bei_short_avg_score

                        # 更新我方最近一场数据
                        record.my_recent1_start_pk = summary.my_recent1_start_pk
                        record.my_recent1_goals = summary.my_recent1_goals
                        record.my_recent1_loose_goals = summary.my_recent1_loose_goals
                        record.my_recent1_result = summary.my_recent1_result
                        record.my_recent1_mult_short_all = summary.my_recent1_mult_short_all
                        record.my_recent1_mult_attack_all = summary.my_recent1_mult_attack_all

                        # 更新我方最近二场数据
                        record.my_recent2_start_pk = summary.my_recent2_start_pk
                        record.my_recent2_goals = summary.my_recent2_goals
                        record.my_recent2_loose_goals = summary.my_recent2_loose_goals
                        record.my_recent2_result = summary.my_recent2_result
                        record.my_recent2_mult_short_all = summary.my_recent2_mult_short_all
                        record.my_recent2_mult_attack_all = summary.my_recent2_mult_attack_all

                        # 更新对方统计数据
                        record.other_recent_count = summary.loose_recent_count
                        record.other_avg_goals = summary.loose_avg_goals
                        record.other_avg_loose_goals = summary.loose_avg_loose_goals
                        record.other_win_rate = summary.loose_win_count / summary.loose_recent_count if summary.loose_recent_count > 0 else None
                        record.other_noloose_rate = (summary.loose_recent_count - summary.loose_loose_count) / summary.loose_recent_count if summary.loose_recent_count > 0 else None
                        record.other_rq_rate = summary.loose_rq_count / summary.loose_recent_count if summary.loose_recent_count > 0 else None
                        record.other_bei_rq_rate = summary.loose_bei_rq_count / summary.loose_recent_count if summary.loose_recent_count > 0 else None
                        record.other_tech_avg_short_all = summary.loose_tech_avg_short_all
                        record.other_tech_avg_short_score = summary.loose_tech_short_avg_score
                        record.other_tech_avg_bei_short_all = summary.loose_tech_avg_bei_short_all
                        record.other_tech_avg_bei_short_score = summary.loose_tech_bei_short_avg_score

                        # 更新对方最近一场数据
                        record.other_recent1_start_pk = summary.loose_recent1_start_pk
                        record.other_recent1_goals = summary.loose_recent1_goals
                        record.other_recent1_loose_goals = summary.loose_recent1_loose_goals
                        record.other_recent1_result = summary.loose_recent1_result
                        record.other_recent1_mult_short_all = summary.loose_recent1_mult_short_all
                        record.other_recent1_mult_attack_all = summary.loose_recent1_mult_attack_all

                        # 更新对方最近二场数据
                        record.other_recent2_start_pk = summary.loose_recent2_start_pk
                        record.other_recent2_goals = summary.loose_recent2_goals
                        record.other_recent2_loose_goals = summary.loose_recent2_loose_goals
                        record.other_recent2_result = summary.loose_recent2_result
                        record.other_recent2_mult_short_all = summary.loose_recent2_mult_short_all
                        record.other_recent2_mult_attack_all = summary.loose_recent2_mult_attack_all
                    else:
                        # my_team_id 是对方球队，需要交换主客队数据
                        record.my_recent_count = summary.loose_recent_count
                        record.my_avg_goals = summary.loose_avg_goals
                        record.my_avg_loose_goals = summary.loose_avg_loose_goals
                        record.my_win_rate = summary.loose_win_count / summary.loose_recent_count if summary.loose_recent_count > 0 else None
                        record.my_noloose_rate = (summary.loose_recent_count - summary.loose_loose_count) / summary.loose_recent_count if summary.loose_recent_count > 0 else None
                        record.my_rq_rate = summary.loose_rq_count / summary.loose_recent_count if summary.loose_recent_count > 0 else None
                        record.my_bei_rq_rate = summary.loose_bei_rq_count / summary.loose_recent_count if summary.loose_recent_count > 0 else None
                        record.my_tech_avg_short_all = summary.loose_tech_avg_short_all
                        record.my_tech_avg_short_score = summary.loose_tech_short_avg_score
                        record.my_tech_avg_bei_short_all = summary.loose_tech_avg_bei_short_all
                        record.my_tech_avg_bei_short_score = summary.loose_tech_bei_short_avg_score

                        # 更新我方最近一场数据
                        record.my_recent1_start_pk = summary.loose_recent1_start_pk
                        record.my_recent1_goals = summary.loose_recent1_goals
                        record.my_recent1_loose_goals = summary.loose_recent1_loose_goals
                        record.my_recent1_result = summary.loose_recent1_result
                        record.my_recent1_mult_short_all = summary.loose_recent1_mult_short_all
                        record.my_recent1_mult_attack_all = summary.loose_recent1_mult_attack_all

                        # 更新我方最近二场数据
                        record.my_recent2_start_pk = summary.loose_recent2_start_pk
                        record.my_recent2_goals = summary.loose_recent2_goals
                        record.my_recent2_loose_goals = summary.loose_recent2_loose_goals
                        record.my_recent2_result = summary.loose_recent2_result
                        record.my_recent2_mult_short_all = summary.loose_recent2_mult_short_all
                        record.my_recent2_mult_attack_all = summary.loose_recent2_mult_attack_all

                        # 更新对方统计数据
                        record.other_recent_count = summary.my_recent_count
                        record.other_avg_goals = summary.my_avg_goals
                        record.other_avg_loose_goals = summary.my_avg_loose_goals
                        record.other_win_rate = summary.my_win_count / summary.my_recent_count if summary.my_recent_count > 0 else None
                        record.other_noloose_rate = (summary.my_recent_count - summary.my_loose_count) / summary.my_recent_count if summary.my_recent_count > 0 else None
                        record.other_rq_rate = summary.my_rq_count / summary.my_recent_count if summary.my_recent_count > 0 else None
                        record.other_bei_rq_rate = summary.my_bei_rq_count / summary.my_recent_count if summary.my_recent_count > 0 else None
                        record.other_tech_avg_short_all = summary.my_tech_avg_short_all
                        record.other_tech_avg_short_score = summary.my_tech_short_avg_score
                        record.other_tech_avg_bei_short_all = summary.my_tech_avg_bei_short_all
                        record.other_tech_avg_bei_short_score = summary.my_tech_bei_short_avg_score

                        # 更新对方最近一场数据
                        record.other_recent1_start_pk = summary.my_recent1_start_pk
                        record.other_recent1_goals = summary.my_recent1_goals
                        record.other_recent1_loose_goals = summary.my_recent1_loose_goals
                        record.other_recent1_result = summary.my_recent1_result
                        record.other_recent1_mult_short_all = summary.my_recent1_mult_short_all
                        record.other_recent1_mult_attack_all = summary.my_recent1_mult_attack_all

                        # 更新对方最近二场数据
                        record.other_recent2_start_pk = summary.my_recent2_start_pk
                        record.other_recent2_goals = summary.my_recent2_goals
                        record.other_recent2_loose_goals = summary.my_recent2_loose_goals
                        record.other_recent2_result = summary.my_recent2_result
                        record.other_recent2_mult_short_all = summary.my_recent2_mult_short_all
                        record.other_recent2_mult_attack_all = summary.my_recent2_mult_attack_all

                    updated_count += 1

                # 提交更新
                session.commit()
                logger.info(f"批次 {batch_num} 处理完成，更新了 {updated_count} 条记录")

            except Exception as e:
                session.rollback()
                logger.error(f"处理批次 {batch_num} 时出错: {str(e)}")
                raise
            finally:
                session.close()
                
        logger.info("所有记录更新完成")
        
    except SQLAlchemyError as e:
        logger.error(f"数据库操作出错: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"更新过程中出错: {str(e)}")
        raise

if __name__ == '__main__':
    """
    新增比赛最新统计数据
    """
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # 假设你已经有了数据库session
    db = SessionLocal()
    update_match_record_final_step_orm(db)
    pass
