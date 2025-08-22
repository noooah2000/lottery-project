import numpy as np
from typing import List, Union, Optional
from ast import literal_eval


def CountElement(passed_combinations: list) -> dict:
    """
    統計號碼出現次數並排序
    
    Args:
        passed_combinations: 通過篩選的組合列表
        
    Returns:
        包含號碼出現次數的字典，按次數降序排列
    """
    if not passed_combinations:
        return {}  # 避免空列表處理錯誤
    
    flat_list = np.ravel(passed_combinations)  # 展平成一維陣列
    count_list = np.bincount(flat_list, minlength=40)  # 忽略0，保留1~39

    # 找出非0的數字，存於大小剛好的陣列中，倒序是為了最後小的key在前面
    nonzero_key_list = np.nonzero(count_list)[0][::-1]
    values_list = count_list[nonzero_key_list]  # 將其對應值，也存於大小剛好的陣列中
    
    # 根據value找出擺放順序
    sorted_idx = np.argsort(values_list, kind='stable')[::-1]
    result_dict = {int(nonzero_key_list[i]): int(values_list[i]) for i in sorted_idx}
    
    return result_dict


def CalculatePrize(winning_number: list, my_number: list) -> dict:
    """
    計算獎金（比對中獎號碼）
    
    Args:
        winning_number: 中獎號碼列表
        my_number: 我的號碼組合列表
        
    Returns:
        包含獎金統計的字典
    """
    prize_dict = {
        2: 50,      # 肆等獎
        3: 300,     # 參等獎
        4: 200000,  # 貳等獎
        5: 8000000, # 壹等獎
    }

    my_number = np.atleast_2d(my_number)
    match_mask = np.isin(my_number, winning_number)
    match_count = match_mask.sum(axis=1)
    each_prizes_count = np.bincount(match_count, minlength=6)[2:6]
    prize_array = np.array(list(prize_dict.values()))
    total_prize = each_prizes_count @ prize_array

    return {
        "total_prize": int(total_prize),
        "detail_number": {
            "壹等獎": int(each_prizes_count[3]),
            "貳等獎": int(each_prizes_count[2]),
            "參等獎": int(each_prizes_count[1]),
            "肆等獎": int(each_prizes_count[0]),
        }
    }


def SetSecondLimit(data: list, second_limit: Union[int, range, List[int]]) -> list:
    """
    建立一個list存放該資料所有二次限定值
    
    Args:
        data: 資料列表
        second_limit: 二次限定值，可以是整數、範圍或列表
        
    Returns:
        包含二次限定值的列表
        
    Raises:
        ValueError: 當二次限定值類型不支援時
    """
    if isinstance(second_limit, (int, range, list)):
        second_limit = [second_limit] if isinstance(second_limit, int) else list(second_limit)
    else:
        raise ValueError("Unsupported type for second_limit")
    
    second_limit_list = [second_limit for _ in range(len(data))]
    return second_limit_list


def ParseTextToList(sec_text: str, filter_data: list) -> Optional[List[int]]:
    """
    轉換二次限定格式(str -> list)
    
    Args:
        sec_text: 二次限定文字
        filter_data: 篩選器資料
        
    Returns:
        解析後的整數列表，如果輸入為空則返回None
        
    Raises:
        ValueError: 當格式錯誤時
    """
    try:
        sec_text = sec_text.strip()
        if not sec_text:
            return None
            
        if sec_text.lower() == 'a':
            return [len(filter_data)]
        elif '-' in sec_text:
            start, end = map(int, sec_text.split('-'))
            return list(range(start, end + 1))
        elif ',' in sec_text:
            return list(map(int, sec_text.split(',')))
        else:
            return [int(sec_text)]
    except Exception as e:
        raise ValueError(f"二次限定格式錯誤: {e}")


def Parse2LimitInput(
    positional_second_limit_str: str,
    criteria_second_limit_str: str,
    inner_positional_2lim_str: list,
    inner_criteria_2lim_str: list,
    positional_filters: list,
    criteria_filters: list,
    winning_numbers_str: list
) -> tuple:
    """
    解析二次限定輸入參數
    
    Args:
        positional_second_limit_str: 位置篩選器二次限定字串
        criteria_second_limit_str: 條件篩選器二次限定字串
        inner_positional_2lim_str: 內部位置二次限定字串列表
        inner_criteria_2lim_str: 內部條件二次限定字串列表
        positional_filters: 位置篩選器資料
        criteria_filters: 條件篩選器資料
        winning_numbers_str: 中獎號碼字串
        
    Returns:
        解析後的參數元組
    """
    # 解析位置篩選器二次限定
    positional_second_limit = ParseTextToList(
        positional_second_limit_str, 
        [filter_data for filter_data in positional_filters if filter_data]
    )
    
    # 解析條件篩選器二次限定
    criteria_second_limit = ParseTextToList(
        criteria_second_limit_str, 
        [filter_data for filter_data in criteria_filters if filter_data]
    )
    
    # 解析內部位置二次限定
    inner_positional_2lim = [
        ParseTextToList(second_limit, filter_data) 
        for second_limit, filter_data in zip(inner_positional_2lim_str, positional_filters)
    ]
    
    # 解析內部條件二次限定
    inner_criteria_2lim = [
        ParseTextToList(second_limit, filter_data) 
        for second_limit, filter_data in zip(inner_criteria_2lim_str, criteria_filters)
    ]
    
    # 解析中獎號碼
    winning_numbers = (
        list(map(int, winning_numbers_str.split(','))) 
        if winning_numbers_str.strip() else []
    )

    return (
        positional_second_limit, 
        criteria_second_limit, 
        inner_positional_2lim, 
        inner_criteria_2lim, 
        winning_numbers
    )


def ParseFiltertstrToList(mode: str, filters_set_str: list) -> list:
    """
    解析篩選器字串為列表格式
    
    Args:
        mode: 解析模式 ("position" 或 "criteria")
        filters_set_str: 篩選器字串列表
        
    Returns:
        解析後的篩選器資料列表
    """
    if mode == "position":
        return [
            [list(map(int, line.split(','))) for line in filters.splitlines()] 
            for filters in filters_set_str
        ]
    elif mode == "criteria":
        result_list = []
        for filters in filters_set_str: 
            result = []
            for line in filters.splitlines():
                parts = [x.strip() for x in line.split(',')]
                key = literal_eval(parts[0] + "," + parts[1])        
                values = list(map(int, parts[2:]))
                result.append((key, values))
            result_list.append(result)
        return result_list
