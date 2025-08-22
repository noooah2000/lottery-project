# 樂透篩選系統 (Lottery Filter System)

這是一個用於篩選樂透號碼組合的 Python 系統，支援位置組篩選器和號碼組篩選器兩種篩選方式。

## 專案結構

```
lottery_project/
├── main.py                 # 主程式入口點 (GUI版本)
├── main_ori.py            # 原始版本 (命令列版本)
├── core.py                # 核心篩選邏輯
├── gui.py                 # GUI主視窗
├── gui_helpers.py         # GUI輔助元件
├── filters_function.py     # 篩選器函數
├── utils.py               # 工具函數
├── filters_data.py        # 篩選器資料 (不變更)
└── README.md              # 專案說明文件
```

## 功能特色

### 篩選器類型
1. **位置組篩選器**: 根據號碼在組合中的位置進行篩選
2. **號碼組篩選器**: 根據號碼的數值範圍和出現次數進行篩選

### 二次限定系統
- 支援外層和內層二次限定
- 可設定篩選器通過的組合數量範圍
- 支援多種輸入格式 (單一數值、範圍、列表)

### 獎金計算
- 自動計算中獎組合的獎金
- 支援多個獎項等級的統計

## 使用方法

### GUI 版本
```bash
python main.py
```

### 命令列版本
```bash
python main_ori.py
```

## 系統需求

- Python 3.7+
- PySide6 (GUI版本)
- NumPy

## 安裝依賴

```bash
pip install PySide6 numpy
```

## 篩選器設定

篩選器資料存放在 `filters_data.py` 中，包含：
- `positional_filters`: 位置篩選器設定
- `criteria_filters`: 條件篩選器設定
- `inner_positional_2lim`: 內部位置二次限定值
- `inner_criteria_2lim`: 內部條件二次限定值

## 二次限定格式

支援以下輸入格式：
- Integer: `"3"`
- Range: `"1-5"`
- Select all: `"a"`

## 開發說明


### 主要模組功能
- `core.py`: 核心篩選邏輯，整合所有篩選器
- `filters_function.py`: 實現各種篩選算法
- `utils.py`: 提供資料解析和統計功能
- `gui.py`: 主視窗介面
- `gui_helpers.py`: 編輯器對話框和輔助元件
