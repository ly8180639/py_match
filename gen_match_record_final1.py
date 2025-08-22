from dataclasses import asdict
from typing import List

from src.match.db.models.match_record_final_step import MatchRecordFinalStep
from src.match.db.session import SessionLocal
from sqlalchemy.orm import Session
from src.match.db.models.match_record_final import MatchRecordFinal
from src.match.utils.object_utils import convert_model

db=SessionLocal()
def iterate_match_records_efficient(batch_size=1000):
    """
    更高效地遍历 match_record_final 表中的每一场比赛数据

    :param batch_size: 每批处理的比赛场次
    :return: 生成器，每次返回一批比赛的数据
    """
    db = SessionLocal()
    try:
        # 使用游标方式处理，避免一次性加载大量数据
        last_match_id = None

        while True:
            query = db.query(MatchRecordFinal)

            if last_match_id is not None:
                query = query.filter(MatchRecordFinal.match_id > last_match_id)

            # 获取一批比赛ID
            match_ids_batch = query.with_entities(MatchRecordFinal.match_id)\
                                  .distinct()\
                                  .order_by(MatchRecordFinal.match_id)\
                                  .limit(batch_size)\
                                  .all()

            if not match_ids_batch:
                break

            # 提取比赛ID
            match_ids = [mid[0] for mid in match_ids_batch]
            last_match_id = match_ids[-1]

            print(f"处理比赛ID范围: {match_ids[0]} - {match_ids[-1]}")

            # 获取这批比赛的所有记录
            records = db.query(MatchRecordFinal)\
                       .filter(MatchRecordFinal.match_id.in_(match_ids))\
                       .order_by(MatchRecordFinal.match_id)\
                       .all()

            yield records

    finally:
        db.close()


def process_each_match_records():
    """
    处理每一场比赛的数据
    """
    total_matches_processed = 0

    for batch_records in iterate_match_records_efficient(batch_size=1000):  # 每批处理1000场比赛
        print(f"当前批次包含 {len(batch_records)} 条记录")

        # 按比赛ID分组处理
        match_groups = {}
        for record in batch_records:
            if record.match_id not in match_groups:
                match_groups[record.match_id] = []
            match_groups[record.match_id].append(record)

        batch_match_count = len(match_groups)
        total_matches_processed += batch_match_count
        print(f"当前批次包含 {batch_match_count} 场比赛，累计已处理 {total_matches_processed} 场比赛")

        # 处理每一场比赛
        for match_id, records in match_groups.items():
            # 在这里处理单场比赛的所有记录
            process_single_match(match_id, records)


# 使用示例
def process_single_match(match_id, records:List[MatchRecordFinal]):
    """
    处理单场比赛的所有记录

    :param match_id: 比赛ID
    :param records: 该场比赛的所有记录列表
    """
    # 按时间排序
    sorted_records = sorted(records, key=lambda x: x.id or 0)

    #用字典表达式，创建一个字典，将每条记录的my_team_id+sort_match_time作为键，记录本身作为值
    records_dict = {(record.my_team_id,record.sort_match_time): record for record in sorted_records}

    # 示例处理逻辑 - 你可以在这里添加具体的处理逻辑
    # print(f"  比赛 {match_id} 有 {len(sorted_records)} 条记录")

    batch_records:List[MatchRecordFinalStep]=[]
    # 示例：分析比赛过程
    for record in sorted_records:
        is_half=record.is_half
        # 处理每条记录
        sort_match_time=record.sort_match_time
        #不考虑上半场5分钟的记录
        if sort_match_time<5 or sort_match_time>85:
            continue;
        #复制一个record_final->record_final_step1
        record_final_step1:MatchRecordFinalStep=convert_model(record, MatchRecordFinalStep)
        """
        5~9分钟：只有一个近4分钟
        10~14分钟：有一个近4分钟，近8分钟
        15~19分钟：有一个近4分钟，近8分钟，近13分钟
        20~24分钟：有一个近4分钟，近8分钟，近13分钟，近18分钟
        25~分钟：有一个近4分钟，近8分钟，近13分钟，近18分钟，近23分钟
        """
        # 根据时间范围处理不同的分钟区间
        if 5 <= sort_match_time <= 9:
            # 5~9分钟：只有一个近4分钟
            process_min_stats(record_final_step1,record, 4,records_dict)
        elif 10 <= sort_match_time <= 14:
            # 10~14分钟：有一个近4分钟，近8分钟
            for minutes in [4, 8]:
                process_min_stats(record_final_step1,record, minutes,records_dict)

        elif 15 <= sort_match_time <= 19:
            # 15~19分钟：有一个近4分钟，近8分钟，近13分钟
            for minutes in [4, 8, 13]:
                process_min_stats(record_final_step1,record, minutes,records_dict)

        elif 20 <= sort_match_time <= 24:
            # 20~24分钟：有一个近4分钟，近8分钟，近13分钟，近18分钟
            for minutes in [4, 8, 13, 18]:
                process_min_stats(record_final_step1,record, minutes,records_dict)

        elif sort_match_time >= 25:
            # 25~分钟：有一个近4分钟，近8分钟，近13分钟，近18分钟，近23分钟
            for minutes in [4, 8, 13, 18, 23]:
                process_min_stats(record_final_step1,record, minutes,records_dict)

        if is_half==1:
            process_min_stats(record_final_step1, record, "half", records_dict)

        batch_records.append(record_final_step1)
    db.add_all(batch_records)
    db.commit()
    print(f"成功批量插入 {len(batch_records)} 条记录")


def process_min_stats(record_final_step1:MatchRecordFinalStep, record, minutes, records_dict):
    minutes_record: MatchRecordFinal = None
    if minutes=="half":
        #下半场最开始的数据，以45~30为准
        for i in range(45,30,-1):
            key=(record.my_team_id, i)
            if key in records_dict:
                minutes_record= records_dict.get(key)
                break
    else:
        key=(record.my_team_id, record.sort_match_time-minutes)
        if key in records_dict:
            minutes_record=records_dict.get(key)
        else:
            #只处理上下一分钟的，拿不到就拿不到
            for i in range(minutes-1,record.sort_match_time):
                key = (record.my_team_id, record.sort_match_time - i)
                if key in records_dict:
                    minutes_record= records_dict.get(key)
                    break

    if minutes_record is None:
        # 没有找到对应时间范围的记录
        return
    fields_to_calculate = [
        'my_short', 'other_short', 'my_short_ok', 'other_short_ok',
        'my_jiaoqiu', 'other_jiaoqiu', 'my_attack', 'other_attack',
        'my_ser_attack', 'other_ser_attack'
    ]

    for field in fields_to_calculate:
        # 获取当前记录和历史记录的字段值
        current_value = getattr(record, field, 0) or 0
        past_value = getattr(minutes_record, field, 0) or 0

        # 计算差值
        diff_value = current_value - past_value
        # 确保差值不为负数
        diff_value = max(0, diff_value)

        # 动态设置record_final_step1中的对应字段
        target_field =  f"min{minutes}_{field}" if minutes != "half" else f"half_{field}"
        if hasattr(record_final_step1, target_field):
            setattr(record_final_step1, target_field, diff_value)


if __name__ == "__main__":
    """
    清洗数据，新增近几分钟的字段，并更新该数据，并且出去5分钟前，85分钟后的数据
    5~9分钟：只有一个近4分钟
    10~14分钟：有一个近4分钟，近8分钟
    15~19分钟：有一个近4分钟，近8分钟，近13分钟
    20~24分钟：有一个近4分钟，近8分钟，近13分钟，近18分钟
    25~分钟：有一个近4分钟，近8分钟，近13分钟，近18分钟，近23分钟
    """
    process_each_match_records()

