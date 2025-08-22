from dataclasses import asdict

from src.match.db.models.match_finish_id import MatchFinishId
from src.match.db.models.match_record_final import MatchRecordFinal
from src.match.db.models.match_record_old import MatchRecordOld
from src.match.db.session import SessionLocal
from src.match.utils.match_utils import *

db=SessionLocal()

def batch_query_by_key(model, key_column,  batch_size=1000):
    """
       分批查询数据
       :param model: 数据库模型类
       :param key_column: 用于排序的键列
       :param batch_size: 每批查询的数据量
       :return: 生成器，每次返回一批数据
       """
    last_key_value = None
    last_id = None
    while True:
        query = db.query(model)

        # 如果有上次的键值，则使用 WHERE 条件进行分页
        if last_key_value is not None:
            # 添加复合排序条件，处理键值相同的情况
            query = query.filter(
                (key_column > last_key_value) |
                ((key_column == last_key_value) & (model.id > last_id))
            )

        # 使用传入的 batch_size 参数
        batch = query.order_by(key_column, model.id).limit(batch_size).all()

        if not batch:
            break

        yield batch

        # 记录最后一条记录的键值和ID，用于下一批查询
        last_record = batch[-1]
        last_key_value = getattr(last_record, key_column.name)
        last_id = last_record.id


def genTwoMatchRecordFinal(match: MatchFinishId, record: MatchRecordOld):
    # 大于45 的上半场
    sort_match_time=45 if 0==record.is_half and record.match_time>45 else record.match_time;
    # 我方是主队
    my_home = MatchRecordFinal()
    my_home.league_id = match.league_id
    my_home.match_id = match.match_id
    my_home.is_home = 1
    my_home.start_pk = match.start_pk
    my_home.my_score = record.home_score
    my_home.other_score = record.guest_score
    my_home.match_start_time = match.match_start_time
    my_home.my_team_id = record.home_team_id
    my_home.other_team_id = record.guest_team_id
    my_home.is_half=record.is_half
    my_home.match_time = record.match_time
    my_home.sort_match_time = sort_match_time
    my_home.pankou = record.pankou
    my_home.proprity=record.proprity
    my_home.curr_odd = record.home_odd
    my_home.odd_time=record.odd_time
    my_home.odd_change= 1 if "up"==record.odd_change else -1 if "down"==record.odd_change else 0

    my_home.my_attack = record.home_attack
    my_home.other_attack = record.guest_attack
    my_home.my_ctl = record.home_ctl
    my_home.other_ctl = record.guest_ctl
    my_home.my_jiaoqiu = record.home_jiaoqiu
    my_home.other_jiaoqiu = record.guest_jiaoqiu
    my_home.my_ser_attack = record.home_ser_attack
    my_home.other_ser_attack = record.guest_ser_attack
    my_home.my_short = record.home_short
    my_home.other_short = record.guest_short
    my_home.my_short_ok = record.home_short_ok
    my_home.other_short_ok = record.guest_short_ok
    my_home.my_yellow_card=record.ext_home_tech1
    my_home.other_yellow_card= record.ext_guest_tech1
    my_home.my_red_card = record.ext_home_tech2
    my_home.other_red_card = record.ext_guest_tech2


    my_home.final_my_score = match.home_score
    my_home.final_other_score = match.guest_score
    # 补充的属性
    my_home.final_result = get_match_result(match.home_score, match.guest_score)
    my_home.final_mult_short = calculate_ratio(add_num(match.home_short,match.home_short_ok),add_num(match.guest_short,match.guest_short_ok))
    my_home.final_mult_short_jiao = calculate_ratio(add_num(match.home_short,match.home_short_ok,match.home_jiaoqiu),add_num(match.guest_short,match.guest_short_ok,match.guest_jiaoqiu))
    my_home.final_mult_ser_attack = calculate_ratio(match.home_ser_attack,match.guest_ser_attack)
    my_home.final_mult_attack = calculate_ratio(add_num(match.home_attack,match.home_ser_attack),add_num(match.guest_attack,match.guest_ser_attack))
    my_home.final_other_yellow_card = match.ext_guest_tech1
    my_home.final_yellow_card = match.ext_home_tech1
    my_home.final_other_yellow_card = match.ext_guest_tech1
    my_home.final_red_card = match.ext_home_tech2
    my_home.final_other_red_card = match.ext_guest_tech2
    my_home.bet_win_goals = get_win_goals(record.home_score, record.guest_score, match.home_score, match.guest_score)
    my_home.bet_win_pankou = get_win_pankou(my_home.pankou, my_home.bet_win_goals)
    my_home.bet_win_amt = get_win_amt(my_home.bet_win_pankou, my_home.curr_odd)


    # 我方是客队
    my_away = MatchRecordFinal()
    my_away.league_id = match.league_id
    my_away.match_id = match.match_id
    my_away.is_home = 0
    my_away.is_half=record.is_half
    my_away.match_time = record.match_time
    my_away.sort_match_time = sort_match_time
    my_away.start_pk = -match.start_pk
    my_away.my_score = record.guest_score
    my_away.other_score = record.home_score
    my_away.match_start_time = match.match_start_time
    my_away.my_team_id = record.guest_team_id
    my_away.other_team_id = record.home_team_id

    my_away.pankou = -record.pankou
    my_away.proprity = record.proprity
    my_away.curr_odd = record.guest_odd
    my_away.odd_time = record.odd_time
    my_away.odd_change = -1 if "up" == record.odd_change else 1 if "down" == record.odd_change else 0


    my_away.my_attack = record.guest_attack
    my_away.other_attack = record.home_attack
    my_away.my_ctl = record.guest_ctl
    my_away.other_ctl = record.home_ctl
    my_away.my_jiaoqiu = record.guest_jiaoqiu
    my_away.other_jiaoqiu = record.home_jiaoqiu
    my_away.my_ser_attack = record.guest_ser_attack
    my_away.other_ser_attack = record.home_ser_attack
    my_away.my_short = record.guest_short
    my_away.other_short = record.home_short
    my_away.my_short_ok = record.guest_short_ok
    my_away.other_short_ok = record.home_short_ok

    my_away.other_yellow_card = record.ext_home_tech1
    my_away.my_yellow_card = record.ext_guest_tech1
    my_away.other_red_card = record.ext_home_tech2
    my_away.my_red_card = record.ext_guest_tech2


    my_away.final_my_score = match.guest_score
    my_away.final_other_score = match.home_score
    # 补充的属性
    my_away.final_result = get_match_result(match.guest_score, match.home_score)
    my_away.final_mult_short = calculate_ratio(add_num(match.guest_short,match.guest_short_ok), add_num(match.home_short,match.home_short_ok))
    my_away.final_mult_short_jiao = calculate_ratio(add_num(match.guest_short, match.guest_short_ok,
                                                            match.guest_jiaoqiu),
                                                    add_num(match.home_short, match.home_short_ok, match.home_jiaoqiu))

    my_away.final_mult_ser_attack = calculate_ratio(match.guest_ser_attack, match.home_ser_attack)
    my_away.final_mult_attack = calculate_ratio(add_num(match.guest_attack,match.guest_ser_attack),add_num(match.home_attack,match.home_ser_attack))
    my_away.final_yellow_card = match.ext_guest_tech1
    my_away.final_other_yellow_card = match.ext_home_tech1
    my_away.final_red_card = match.ext_guest_tech2
    my_away.final_other_red_card = match.ext_home_tech2
    my_away.bet_win_goals=get_win_goals(record.guest_score,record.home_score,match.guest_score,match.home_score)
    my_away.bet_win_pankou = get_win_pankou(my_away.pankou,my_away.bet_win_goals)
    my_away.bet_win_amt = get_win_amt(my_away.bet_win_pankou,my_away.curr_odd)
    return my_home, my_away





lastRecordOld:MatchRecordOld=None
def deal_one_match(record_old:MatchRecordOld,match:MatchFinishId):
    global lastRecordOld
    # 每条比赛数据
    print("finish_match:",match.match_id)
    print("match_record_old:",record_old.match_id)
    record_match_id=record_old.match_id
    record_match_time=record_old.match_time

    # 主要技术统计,如射门，危险进攻，都为空，则跳过
    if(record_old.home_ser_attack is None or record_old.guest_ser_attack is None
            or record_old.guest_short is None or record_old.home_short is None
            or record_old.pankou is None or record_old.home_odd is None or record_old.guest_odd is None):
        return

    #如果比赛id和比赛时间重复，则跳过
    if lastRecordOld is not  None and lastRecordOld.is_half==record_old.is_half  and  lastRecordOld.match_id==record_match_id and lastRecordOld.match_time>=record_match_time:
        return
    ## 数据相同也没必要添加
    if lastRecordOld is not None and lastRecordOld.home_ser_attack==record_old.home_ser_attack \
        and lastRecordOld.guest_ser_attack==record_old.guest_ser_attack \
        and lastRecordOld.guest_short_ok == record_old.guest_short_ok \
        and lastRecordOld.home_short_ok == record_old.home_short_ok\
        and lastRecordOld.guest_short == record_old.guest_short \
        and lastRecordOld.home_short==record_old.home_short :
        lastRecordOld=record_old
        return
    #生成你方，我方2条数据
    my_home,my_away= genTwoMatchRecordFinal(match,record_old)
    db.add(my_home)
    db.add(my_away)
    #没两条提交一次
    db.commit()
    lastRecordOld = record_old


match:MatchFinishId=None
#遍历过程中，没有获取到finishMatch的Id
matchNoneId= None
# 使用示例
def process_data(batch):
    global match
    global matchNoneId
    print(f"正在处理数据...{type(batch)},{len(batch)}")
    for record_old in batch:
        if matchNoneId is not None and matchNoneId==record_old.match_id:
            continue
        if match is None or match.match_id != record_old.match_id:
            match = db.query(MatchFinishId).filter(MatchFinishId.match_id == record_old.match_id).first()
            if match is None:
                matchNoneId=record_old.match_id
                continue
        matchNoneId=None
        deal_one_match(record_old,match)



for batch in batch_query_by_key(MatchRecordOld, MatchRecordOld.match_id,batch_size=10000):
    process_data(batch)
