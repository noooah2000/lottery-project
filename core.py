from itertools import combinations
from typing import List, Union
from filters_function import FilterByPositions, FilterByCriteria, OuterLayerFilter
from utils import CountElement, CalculatePrize


def CoreFunction(
    use_position_filter: bool,
    use_criteria_filter: bool,
    positional_second_limit: Union[int, range, List[int]],
    criteria_second_limit: Union[int, range, List[int]],
    inner_positional_2lim: list,
    inner_criteria_2lim: list, 
    positional_filter_data: list,
    criteria_filter_data: list,
    winning_numbers: list
) -> dict:
    """
    樂透篩選系統核心功能
    
    Args:
        use_position_filter: 是否使用位置篩選器
        use_criteria_filter: 是否使用條件篩選器
        positional_second_limit: 位置篩選器二次限定值
        criteria_second_limit: 條件篩選器二次限定值
        inner_positional_2lim: 內部位置二次限定值列表
        inner_criteria_2lim: 內部條件二次限定值列表
        positional_filter_data: 位置篩選器資料
        criteria_filter_data: 條件篩選器資料
        winning_numbers: 中獎號碼列表
        
    Returns:
        包含篩選結果的字典
    """
    # 產生所有 C(39,5) 組合
    combinations_all = list(combinations(range(1, 40), 5))
    filtered = combinations_all

    # 依序應用兩種篩選器邏輯
    if use_position_filter:
        filtered = OuterLayerFilter(
            filters_set=positional_filter_data,
            second_limit_set=inner_positional_2lim,
            second_limit=positional_second_limit,
            input_combinations=filtered,
            InnerLayerFilter=FilterByPositions
        )
    
    if use_criteria_filter:
        filtered = OuterLayerFilter(
            filters_set=criteria_filter_data,
            second_limit_set=inner_criteria_2lim,
            second_limit=criteria_second_limit,
            input_combinations=filtered,
            InnerLayerFilter=FilterByCriteria
        )

    # 統計篩選結果
    result_crit = {
        "valid_combinations": filtered, 
        "valid_count": len(filtered), 
        "filtered_count": 575757 - len(filtered)
    }

    # 統計元素出現次數
    element_counts = CountElement(filtered)

    # 計算獎金（比對中獎號碼）
    prize_info = None
    if winning_numbers:
        prize_info = CalculatePrize(
            winning_number=winning_numbers,
            my_number=filtered
        )

    # 準備主要視窗輸出內容
    main_window_output_lines = [
        f"通過組合數: {result_crit['valid_count']}",
        f"被篩掉組合數: {result_crit['filtered_count']}"
    ]
    
    if prize_info:
        main_window_output_lines.append("\n獎金統計:")
        main_window_output_lines.append(f"總獎金：{prize_info['total_prize']}")
        main_window_output_lines.extend([
            f"{k}: {v}" for k, v in prize_info['detail_number'].items()
        ])

    # 準備通過號碼輸出內容
    valid_combinations_output_lines = [
        ", ".join(str(num) for num in combination) 
        for combination in result_crit['valid_combinations']
    ]
    
    # 準備熱門號碼輸出內容
    hot_numbers_output_lines = [
        f"號碼 {k:<4}-> {v:>3} 次" 
        for k, v in element_counts.items()
    ]

    return {
        "main window output lines": "\n".join(main_window_output_lines), 
        "valid combinations output lines": "\n".join(valid_combinations_output_lines), 
        "hot numbers output lines": "\n".join(hot_numbers_output_lines)
    }

    