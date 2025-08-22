from typing import List, Union, Callable
import numpy as np


def FilterByPositions(
    filters: list,
    second_limit: Union[int, range, List[int]],
    input_combinations: np.ndarray
) -> np.ndarray:
    """
    位置組合過濾
    
    Args:
        filters: 位置篩選器資料，每個位置包含允許的號碼列表
        second_limit: 二次限定值，可以是整數、範圍或列表
        input_combinations: 輸入的組合陣列
        
    Returns:
        布林遮罩陣列，True表示通過篩選的組合
    """
    input_combinations = np.atleast_2d(input_combinations)
    hits = np.zeros(input_combinations.shape[0], dtype=int)

    for i in range(5):
        # 檢查每個組合的第i個位置
        column_values = input_combinations[:, i]
        # 檢查每個組合該位置的數是否存在於filter中，並回傳T或F陣列
        mask = np.isin(column_values, filters[i])
        hits += mask.astype(int)
    
    valid_mask = np.isin(hits, second_limit)
    return valid_mask


def FilterByCriteria(
    filters: list,
    second_limit: Union[int, range, List[int]],
    input_combinations: np.ndarray
) -> np.ndarray:
    """
    號碼組合過濾
    
    Args:
        filters: 條件篩選器資料，包含(範圍, 號碼池)的元組列表
        second_limit: 二次限定值，可以是整數、範圍或列表
        input_combinations: 輸入的組合陣列
        
    Returns:
        布林遮罩陣列，True表示通過篩選的組合
    """
    input_combinations = np.atleast_2d(input_combinations)
    hits = np.zeros(input_combinations.shape[0], dtype=int)
    
    for match_range, match_pool in filters:
        start, end = match_range
        match_range = list(range(start, end + 1))
        
        # 針對每條pool去比對，輸出T或F矩陣
        match_mask = np.isin(input_combinations, match_pool)
        # 每個組合看有幾個match
        match_count = match_mask.sum(axis=1)
        # 看是否符合match_range
        pass_mask = np.isin(match_count, match_range)
        hits += pass_mask.astype(int)
    
    valid_mask = np.isin(hits, second_limit)
    return valid_mask


def OuterLayerFilter(
    filters_set: list,
    second_limit_set: list,
    second_limit: Union[int, range, List[int]],
    input_combinations: list,
    InnerLayerFilter: Callable
) -> list:
    """
    外層篩選過濾
    
    Args:
        filters_set: 篩選器集合列表
        second_limit_set: 二次限定值集合列表
        second_limit: 外層二次限定值
        input_combinations: 輸入的組合列表
        InnerLayerFilter: 內層篩選函數
        
    Returns:
        通過篩選的組合列表
    """
    input_combinations = np.array(input_combinations)
    hits = np.zeros(input_combinations.shape[0], dtype=int)
    
    for filters, inner_2lim in zip(filters_set, second_limit_set):
        if not inner_2lim:
            continue
            
        mask = InnerLayerFilter(
            filters=filters,
            second_limit=inner_2lim,
            input_combinations=input_combinations
        )
        hits += mask.astype(int)  # 把T或F陣列轉01
    
    valid_mask = np.isin(hits, second_limit)
    passed_combinations = input_combinations[valid_mask]
    
    return passed_combinations.tolist()


