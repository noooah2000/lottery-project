import PySide6.QtWidgets as qtw
from filters_data import positional_filters, criteria_filters, inner_positional_2lim, inner_criteria_2lim
from utils import Parse2LimitInput, ParseFiltertstrToList
from core import CoreFunction
from gui_helpers import show_result_popup, MainEditorDialog
import sys


class LotteryApp(qtw.QWidget):
    """樂透篩選系統主視窗"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("篩選系統")

        # 初始化篩選器資料
        self.positional_filters = positional_filters
        self.criteria_filters = criteria_filters
        self.inner_positional_2lim = inner_positional_2lim
        self.inner_criteria_2lim = inner_criteria_2lim

        # 初始化輸出內容
        self.main_window_output_lines = ""
        self.valid_combinations_output_lines = ""
        self.hot_numbers_output_lines = ""

        self.setup_ui()

    def setup_ui(self):
        """設置UI介面"""
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        # 篩選器類型選擇
        self._setup_filter_type_section(layout)
        
        # 外層二次限定值
        self._setup_second_limit_section(layout)
        
        # 編輯條件按鈕
        self._setup_edit_buttons_section(layout)
        
        # 中獎號碼輸入
        self._setup_winning_numbers_section(layout)
        
        # 分析結果顯示
        self._setup_output_section(layout)
        
        # 查看結果按鈕
        self._setup_view_buttons_section(layout)

    def _setup_filter_type_section(self, layout):
        """設置篩選器類型選擇區域"""
        row1 = qtw.QHBoxLayout()
        row1.addWidget(qtw.QLabel("選擇篩選器類型:"))
        self.use_position_filter = qtw.QCheckBox(" 位置組")
        self.use_criteria_filter = qtw.QCheckBox(" 號碼組")
        row1.addWidget(self.use_position_filter)
        row1.addWidget(self.use_criteria_filter)
        layout.addLayout(row1)

    def _setup_second_limit_section(self, layout):
        """設置外層二次限定值區域"""
        row2 = qtw.QHBoxLayout()
        row2.addWidget(qtw.QLabel(" 二次限定值:"))
        self.positional_second_limit_entry = qtw.QLineEdit()
        self.criteria_second_limit_entry = qtw.QLineEdit()
        row2.addWidget(self.positional_second_limit_entry)
        row2.addWidget(self.criteria_second_limit_entry)
        layout.addLayout(row2)

    def _setup_edit_buttons_section(self, layout):
        """設置編輯條件按鈕區域"""
        row3 = qtw.QHBoxLayout()
        edit_position_button = qtw.QPushButton(" 編輯位置組條件")
        edit_position_button.clicked.connect(
            lambda: self.open_editor(" 編輯位置組條件", self.positional_filters, self.inner_positional_2lim)
        )
        edit_criteria_button = qtw.QPushButton(" 編輯號碼組條件")
        edit_criteria_button.clicked.connect(
            lambda: self.open_editor(" 編輯號碼組條件", self.criteria_filters, self.inner_criteria_2lim)
        )
        row3.addWidget(edit_position_button)
        row3.addWidget(edit_criteria_button)
        layout.addLayout(row3)

    def _setup_winning_numbers_section(self, layout):
        """設置中獎號碼輸入區域"""
        row4 = qtw.QHBoxLayout()
        row4.addWidget(qtw.QLabel(" 中獎號碼 (逗號分隔):"))
        self.winning_entry = qtw.QLineEdit()
        run_button = qtw.QPushButton(" 執行分析")
        run_button.clicked.connect(self.run_logic)
        row4.addWidget(self.winning_entry)
        row4.addWidget(run_button)
        layout.addLayout(row4)

    def _setup_output_section(self, layout):
        """設置分析結果顯示區域"""
        row5 = qtw.QHBoxLayout()
        self.output = qtw.QTextEdit()
        self.output.setReadOnly(True)
        row5.addWidget(self.output)
        layout.addLayout(row5)

    def _setup_view_buttons_section(self, layout):
        """設置查看結果按鈕區域"""
        row6 = qtw.QHBoxLayout()
        view_valid_button = qtw.QPushButton(" 查看通過號碼")
        view_valid_button.clicked.connect(
            lambda: show_result_popup(
                parent=self,
                title=" 通過號碼", 
                output=self.valid_combinations_output_lines
            )
        )
        view_hot_button = qtw.QPushButton(" 查看熱門號碼")
        view_hot_button.clicked.connect(
            lambda: show_result_popup(
                parent=self,
                title=" 熱門號碼", 
                output=self.hot_numbers_output_lines
            )
        )
        row6.addWidget(view_valid_button)
        row6.addWidget(view_hot_button)
        layout.addLayout(row6)

    def run_logic(self):
        """執行篩選邏輯"""
        try:
            # 格式轉換
            parsed_positional_filters = ParseFiltertstrToList(
                mode="position", 
                filters_set_str=self.positional_filters
            )
            parsed_criteria_filters = ParseFiltertstrToList(
                mode="criteria", 
                filters_set_str=self.criteria_filters
            )
            
            # 解析輸入參數
            (
                positional_second_limit,
                criteria_second_limit,
                inner_positional_2lim,
                inner_criteria_2lim,
                winning_numbers
            ) = Parse2LimitInput(
                positional_second_limit_str=self.positional_second_limit_entry.text(),
                criteria_second_limit_str=self.criteria_second_limit_entry.text(),
                inner_positional_2lim_str=self.inner_positional_2lim,
                inner_criteria_2lim_str=self.inner_criteria_2lim,
                positional_filters=parsed_positional_filters,
                criteria_filters=parsed_criteria_filters,
                winning_numbers_str=self.winning_entry.text()
            )
        except Exception as e:
            qtw.QMessageBox.critical(self, "錯誤", f"格式錯誤: {e}")
            return

        # 執行核心功能
        result = CoreFunction(
            use_position_filter=self.use_position_filter.isChecked(),
            use_criteria_filter=self.use_criteria_filter.isChecked(),
            positional_second_limit=positional_second_limit,
            criteria_second_limit=criteria_second_limit,
            inner_positional_2lim=inner_positional_2lim,
            inner_criteria_2lim=inner_criteria_2lim,
            positional_filter_data=parsed_positional_filters,
            criteria_filter_data=parsed_criteria_filters,
            winning_numbers=winning_numbers
        )

        # 更新輸出內容
        self.main_window_output_lines = result["main window output lines"]
        self.valid_combinations_output_lines = result["valid combinations output lines"]
        self.hot_numbers_output_lines = result["hot numbers output lines"]

        # 顯示主要輸出
        self.output.setPlainText(self.main_window_output_lines)

    def open_editor(self, title: str, filters_set: list, second_limit_set: list):
        """開啟編輯器對話框"""
        editor = MainEditorDialog(
            title=title, 
            parent=self, 
            filters_set=filters_set, 
            second_limit_set=second_limit_set
        )
        editor.exec()


def launch_app():
    """啟動應用程式"""
    app = qtw.QApplication(sys.argv)
    window = LotteryApp()
    window.show()
    app.exec()
