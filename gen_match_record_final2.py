from dataclasses import asdict
from typing import List

from src.match.db.models.match_record_final_step import MatchRecordFinalStep
from src.match.db.session import SessionLocal
from sqlalchemy.orm import Session
from src.match.db.models.match_record_final import MatchRecordFinal
from src.match.utils.object_utils import convert_model



# league_stats_updater.py
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy import text

from src.match.db.models.match_record_final_step import MatchRecordFinalStep
from src.match.db.models.match_league_summary import MatchLeagueSummary

logger = logging.getLogger(__name__)



class LeagueStatsUpdater:
    def __init__(self, session):
        self.session = session

    def get_all_summary_batches(self) -> List[str]:
        """
        获取所有联赛批次数据，按时间倒序排列
        """
        result = self.session.execute(
            text("SELECT DISTINCT summary_batch_no FROM match_league_summary ORDER BY summary_batch_no DESC")
        )
        return [row[0] for row in result.fetchall()]

    def get_league_summary_by_batch(self, batch_no: str) -> List[MatchLeagueSummary]:
        """
        获取指定批次的所有联赛统计数据
        """
        # result = self.session.execute(
        #     text("SELECT * FROM match_league_summary WHERE summary_batch_no = :batch_no"),
        #     {"batch_no": batch_no}
        # )
        #
        # columns = result.keys()
        # return [dict(zip(columns, row)) for row in result.fetchall()]
        return self.session.query(MatchLeagueSummary) \
            .filter(MatchLeagueSummary.summary_batch_no == batch_no) \
            .all()

    def get_matches_without_league_stats(self) -> List[MatchRecordFinalStep]:
        """
        获取所有未更新联赛统计数据的比赛记录
        按比赛时间倒序排列
        """
        return self.session.query(MatchRecordFinalStep)\
            .filter(MatchRecordFinalStep.league_count.is_(None))\
            .order_by(MatchRecordFinalStep.match_start_time.desc())\
            .all()

    def get_matches_after_date(self, date_str: str) -> List[MatchRecordFinalStep]:
        """
        获取指定日期之后的比赛记录
        """
        # 从批次号中解析日期 (假设格式为 YYYYMMDD)
        try:
            batch_date = datetime.strptime(date_str, '%Y%m%d')
            batch_date_one=batch_date+timedelta(days=1)
            return self.session.query(MatchRecordFinalStep)\
                .filter(MatchRecordFinalStep.match_start_time > batch_date_one)\
                .filter(MatchRecordFinalStep.league_count.is_(None))\
                .order_by(MatchRecordFinalStep.match_start_time.desc())\
                .all()
        except ValueError:
            logger.error(f"Invalid date format: {date_str}")
            return []

    def organize_league_stats_by_id(self, league_stats: List[MatchLeagueSummary]) -> Dict[int, MatchLeagueSummary]:
        """
        将联赛统计数据按league_id组织成字典，便于快速查找
        """
        return {stat.league_id: stat for stat in league_stats}

    def update_match_with_league_stats(self, match: MatchRecordFinalStep, league_stats_dict: Dict[int, MatchLeagueSummary]):
        """
        使用联赛统计数据更新比赛记录
        """
        league_stat: MatchLeagueSummary = league_stats_dict.get(match.league_id)
        if not league_stat:
            logger.warning(f"No league stats found for match {match.id}, league_id: {match.league_id}")
            match.league_count =0
            return True
        # 更新联赛统计字段
        match.league_count = league_stat.match_count
        match.home_win_rate = float(league_stat.home_win_rate) if league_stat.home_win_rate is not None else None
        match.home_noloose_rate = float(league_stat.home_noloose_rate) if league_stat.home_noloose_rate is not None else None
        match.eq_rate = float(league_stat.eq_rate) if league_stat.eq_rate is not None else None
        match.cross_pk_count = league_stat.cross_pk_count
        match.cross_pk_win_rate = float(league_stat.cross_rate) if league_stat.cross_rate is not None else None
        match.eq_pk_rate = float(league_stat.pan_eq0_eq_rate) if league_stat.pan_eq0_eq_rate is not None else None

        # 盘口小于等于0.25的数量为 pan_le025_count/league_count
        if league_stat.pan_le025_count is not None and league_stat.match_count is not None and league_stat.match_count > 0:
            match.pk_le025_rate = float(league_stat.pan_le025_count) / float(league_stat.match_count)
        else:
            match.pk_le025_rate = None

        match.goals0_rate = float(league_stat.goals0_rate) if league_stat.goals0_rate is not None else None
        match.goalsle1_rate = float(league_stat.goalsle1_rate) if league_stat.goalsle1_rate is not None else None
        match.goalsle2_rate = float(league_stat.goalsle2_rate) if league_stat.goalsle2_rate is not None else None

        # 大于等于三球率为1-小于等于2球率
        if league_stat.goalsle2_rate is not None:
            match.goalsge3_rate = 1.0 - float(league_stat.goalsle2_rate)
        else:
            match.goalsge3_rate = None

        match.tech_advan1_count = league_stat.tech_advan1_count
        match.tech_advan1_win_rate = float(league_stat.tech_advan1_win_rate) if league_stat.tech_advan1_win_rate is not None else None
        match.tech_advan1_noloose_rate = float(league_stat.tech_advan1_noloose_rate) if league_stat.tech_advan1_noloose_rate is not None else None
        match.tech_advan2_count = league_stat.tech_advan2_count
        match.tech_advan2_win_rate = float(league_stat.tech_advan2_win_rate) if league_stat.tech_advan2_win_rate is not None else None
        match.tech_advan2_noloose_rate = float(league_stat.tech_advan2_noloose_rate) if league_stat.tech_advan2_noloose_rate is not None else None
        match.tech_advan3_count = league_stat.tech_advan3_count
        match.tech_advan3_win_rate = float(league_stat.tech_advan3_win_rate) if league_stat.tech_advan3_win_rate is not None else None
        match.tech_advan3_noloose_rate = float(league_stat.tech_advan3_noloose_rate) if league_stat.tech_advan3_noloose_rate is not None else None

        return True

    def process_batch(self, batch_no: str):
        """
        处理单个批次的数据
        """
        logger.info(f"Processing batch: {batch_no}")

        # 获取该批次的联赛统计数据
        league_stats:List[MatchLeagueSummary] = self.get_league_summary_by_batch(batch_no)
        if not league_stats:
            logger.warning(f"No league stats found for batch: {batch_no}")
            return

        # 按league_id组织数据
        league_stats_dict:[int, MatchLeagueSummary] = self.organize_league_stats_by_id(league_stats)

        # 获取需要更新的比赛（根据批次日期筛选）
        matches = self.get_matches_after_date(batch_no)
        logger.info(f"Found {len(matches)} matches to update for batch {batch_no}")

        updated_count = 0
        for match in matches:
            if self.update_match_with_league_stats(match, league_stats_dict):
                updated_count += 1

        # 提交事务
        self.session.commit()
        logger.info(f"Updated {updated_count} matches for batch {batch_no}")

    def update_all_league_stats(self):
        """
        更新所有联赛统计数据
        """
        logger.info("Starting league stats update process")

        # 获取所有批次
        batches = self.get_all_summary_batches()
        logger.info(f"Found {len(batches)} batches to process")

        # 按批次处理
        for batch_no in batches:
            try:
                self.process_batch(batch_no)
            except Exception as e:
                logger.error(f"Error processing batch {batch_no}: {str(e)}")
                self.session.rollback()

        logger.info("League stats update process completed")

# 使用示例
def main():
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # 假设你已经有了数据库session
    db=SessionLocal()
    updater = LeagueStatsUpdater(db)
    updater.update_all_league_stats()
    pass

if __name__ == "__main__":
    """
    新增联赛近期统计数据
    """
    main()