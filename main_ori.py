"""
樂透篩選系統 - 原始版本
此檔案包含不使用GUI的命令列版本篩選邏輯
"""

from itertools import combinations
from filters_data import (
    positional_filters, 
    inner_positional_2lim, 
    criteria_filters, 
    inner_criteria_2lim
)
from filters_function import FilterByPositions, FilterByCriteria, OuterLayerFilter
from utils import CountElement, CalculatePrize, Parse2LimitInput, ParseFiltertstrToList


def main():
    """主函數：執行樂透篩選邏輯"""
    
    # ===== 使用者設定區 =====
    apply_position_filter = True
    apply_criteria_filter = True
    positional_second_limit = "3"
    criteria_second_limit = "a"
    show_top_n = 10
    winning_numbers = "6, 14, 24, 37, 38"

    # ===== 資料轉換區 =====
    parsed_positional_filters = ParseFiltertstrToList(
        mode="position", 
        filters_set_str=positional_filters
    )
    parsed_criteria_filters = ParseFiltertstrToList(
        mode="criteria", 
        filters_set_str=criteria_filters
    )

    # 解析二次限定參數
    (
        positional_second_limit,
        criteria_second_limit,
        inner_positional_2lim,
        inner_criteria_2lim,
        winning_numbers
    ) = Parse2LimitInput(
        positional_second_limit_str=positional_second_limit,
        criteria_second_limit_str=criteria_second_limit,
        inner_positional_2lim_str=inner_positional_2lim,
        inner_criteria_2lim_str=inner_criteria_2lim,
        positional_filters=parsed_positional_filters,
        criteria_filters=parsed_criteria_filters,
        winning_numbers_str=winning_numbers
    )

    # ===== 產生所有 C(39,5) 組合 =====
    combinations_all = list(combinations(range(1, 40), 5))
    filtered = combinations_all

    # ===== 依序應用兩種篩選器邏輯 =====
    if apply_position_filter:
        filtered = OuterLayerFilter(
            filters_set=parsed_positional_filters,
            second_limit_set=inner_positional_2lim,
            second_limit=positional_second_limit,
            input_combinations=filtered,
            InnerLayerFilter=FilterByPositions
        )
    
    if apply_criteria_filter:
        filtered = OuterLayerFilter(
            filters_set=parsed_criteria_filters,
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

    # ===== 統計元素出現次數 =====
    element_count = CountElement(filtered)

    # ===== 計算獎金（比對中獎號碼） =====
    prize_result = CalculatePrize(
        winning_number=winning_numbers,
        my_number=filtered
    )

    # ===== 顯示輸出結果 =====
    print("通過組合數:", result_crit["valid_count"])
    print("被篩掉組合數:", result_crit["filtered_count"])
    
    print(f"\n前 {show_top_n} 筆通過組合:")
    for combo in result_crit["valid_combinations"][:show_top_n]:
        print(combo)

    print("\n元素出現次數 (依頻率排序):")
    print(element_count)

    print("\n獎金統計:")
    print("總獎金：", prize_result["total_prize"])
    for k, v in prize_result["detail_number"].items():
        print(k, ":", v)


if __name__ == "__main__":
    main()
