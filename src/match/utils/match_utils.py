def add_num(*args):
    """
    安全地对任意数量的数字求和，处理 None 值

    :param args: 任意数量的数字参数（可以包含 None）
    :return: 所有数字的和，None 值被视为 0
    """
    total = 0
    for arg in args:
        if arg is not None:
            total += arg
    return total


def get_match_result(my_score, other_score):
    """
    根据比分计算比赛结果
    :param my_score: 我方得分
    :param other_score: 对方得分
    :return: 3(胜), 1(平), 0(负)
    """
    if my_score > other_score:
        return 3
    elif my_score == other_score:
        return 1
    else:
        return 0

def calculate_ratio(my_value, other_value):
    """
    计算比率，避免除以零的情况
    :param my_value: 我方数值
    :param other_value: 对方数值
    :return: 比率值，如果对方为0且我方不为0则返回负数表示倍数
    """


    if other_value is None or other_value == 0:
            # 用负数表示对方是我方的多少倍（这里表示无穷大倍，用一个特殊值表示）
            return 1 if my_value==0 else my_value

    if my_value is None or my_value == 0:
        # 用负数表示对方是我方的多少倍（这里表示无穷大倍，用一个特殊值表示）
        return 1 if other_value == 0 else -other_value
    # 正常情况比较
    if my_value >= other_value:
        # 我方比对方大或相等，用我方除以对方
        return my_value / other_value
    else:
        # 对方比我方大，用对方除以我方，结果为负数
        return -(other_value / my_value)

def get_win_goals(my_score, guest_score, my_final_score, guest_final_score):
    """
    :param my_score: 开始我方比分
    :param guest_score: 开始对方比分
    :param my_final_score: 最终我方比分
    :param guest_final_score: 最终对方比分
    :return: 追了多少比分，落后则为负数
    """
    # 计算初始比分差
    initial_diff = my_score - guest_score

    # 计算最终比分差
    final_diff = my_final_score - guest_final_score

    # 计算追分差值：最终差值 - 初始差值
    # 正数表示我方相对对方追了分，负数表示我方相对对方落后更多或追分减少
    goal_difference = final_diff - initial_diff
    return goal_difference


def get_win_pankou(my_pankou, my_win_goals):
    """
    :param my_pankou: 当前实时盘口，如我方让0.5球，即-0.5
    :param my_win_goals: 最终追了多少球，如我方追了1球
    :return: 则1-0.5=0.5
    """
    return my_win_goals+my_pankou


def get_win_amt(bet_win_pankou:float,curr_odd:float):
    """
    :param bet_win_pankou:  赢了多少盘口，如0.5或0.25（赢一半），或-0.25（输一半）
    :param curr_odd: 当前水位
    :return: 根据赢的不同盘口，返回水位*对应的系数。赢的盘口为正数则为盈利，负数则为亏钱
    系数：大于等于0.5=水位， 0.25=水位*0.5,0=0，-0.25=-水位*0.5,小于等于-0.5=-水位
    """
    # 根据盘口赢球情况确定系数
    if bet_win_pankou >= 0.5:
        coefficient = 1.0
    elif bet_win_pankou == 0.25:
        coefficient = 0.5
    elif bet_win_pankou == 0:
        coefficient = 0
    elif bet_win_pankou == -0.25:
        coefficient = -0.5
    elif bet_win_pankou <= -0.5:
        return -1
    else:
        # 处理其他可能的值，默认为0
        coefficient = 0

    # 计算盈利金额
    bet_win_amt = (curr_odd-1) * coefficient
    return bet_win_amt


