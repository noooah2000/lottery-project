# Lottery Filter System

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

## 功能

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


## 環境需求
- Python 3.13.5
- pip（Python 內建套件管理工具）
- 依賴套件版本：
  - numpy==2.3.1
  - PySide6==6.9.1
  - PySide6_Addons==6.9.1
  - PySide6_Essentials==6.9.1
  - shiboken6==6.9.1
  - python-dateutil==2.9.0.post0
  - pytz==2025.2
  - six==1.17.0
  - tzdata==2025.2


## 篩選器設定

篩選器資料及範例存放在 `filters_data.py` 中，包含：
- `positional_filters`: 位置篩選器設定
- `criteria_filters`: 條件篩選器設定
- `inner_positional_2lim`: 內部位置二次限定值
- `inner_criteria_2lim`: 內部條件二次限定值
目前設定初始為空的，使用者可自行更改程式碼

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


## 下載與使用
> 以下指令請在系統內建終端機 (Terminal / PowerShell / CMD) 執行。

### <span style="color:#FFD700">1. 安裝 Python</span>
- macOS
1. 安裝 [Homebrew](https://brew.sh/)
2. 執行：
   ~~~bash
   brew install python@3.13
   ~~~

- Windows
1. 到 [Python 官方網站](https://www.python.org/downloads/windows/) 下載 **Python 3.13.x (64-bit installer)**
2. 安裝時勾選 **Add python.exe to PATH**

完成後，輸入以下指令確認：
~~~bash
python --version
~~~
顯示 `Python 3.13.5` 代表成功。

### <span style="color:#FFD700">2. 下載專案</span>
~~~bash
git clone https://github.com/noooah2000/lottery_project.git
cd lottery_project
~~~

### <span style="color:#FFD700">3. 建立並啟用虛擬環境（名稱：.myvenv）</span>
- macOS / Linux
~~~bash
python3 -m venv .myvenv
source .myvenv/bin/activate
~~~

- Windows (PowerShell)
~~~powershell
py -3.13 -m venv .myvenv
.\.myvenv\Scripts\Activate.ps1
~~~

> 啟用成功後，命令列前綴會顯示 `(.myvenv)`。

### <span style="color:#FFD700">4. 安裝依賴套件（推薦使用 requirements.txt）</span>
~~~bash
pip install -r requirements.txt
~~~

如果專案沒有 `requirements.txt`，可直接安裝：
~~~bash
pip install ^
  numpy==2.3.1 ^
  PySide6==6.9.1 PySide6_Addons==6.9.1 PySide6_Essentials==6.9.1 shiboken6==6.9.1 ^
  python-dateutil==2.9.0.post0 six==1.17.0 ^
  pytz==2025.2 tzdata==2025.2
~~~
> 以上是 Windows PowerShell 的換行寫法（用 `^`）。macOS/Linux 可改成單行或用反斜線 `\` 換行。

### <span style="color:#FFD700">5. 驗證安裝（可選）</span>
~~~bash
python -c "import numpy, PySide6; print('numpy', numpy.__version__, '| PySide6', PySide6.__version__)"
~~~

### <span style="color:#FFD700">6. 執行主程式</span>
~~~bash
python main.py
~~~