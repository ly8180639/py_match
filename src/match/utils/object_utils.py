from sqlalchemy import inspect

from src.match.db.models.match_record_final import MatchRecordFinal
from src.match.db.models.match_record_final_step import MatchRecordFinalStep


def convert_model(source, target_class, **extra_fields):
    # 获取所有列属性
    attrs = {
        c.key: getattr(source, c.key)
        for c in inspect(source).mapper.columns
        if hasattr(target_class, c.key)
    }
    return target_class(**attrs, **extra_fields)

# m1=MatchRecordFinal()
# m1.is_half=1
# m1.sort_match_time=10
# m1.odd_time=3
# m2=convert_model(m1,MatchRecordFinalStep1)
# print(m2.__dict__)
