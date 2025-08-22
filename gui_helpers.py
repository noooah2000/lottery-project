import sys
from typing import List, Optional
from PySide6 import QtWidgets as qtw


def show_result_popup(parent: qtw.QWidget, title: str, output: str) -> None:
    """顯示結果彈出視窗"""
    dialog = qtw.QDialog(parent)
    dialog.setWindowTitle(title)

    layout = qtw.QVBoxLayout(dialog)
    text_edit = qtw.QTextEdit()
    text_edit.setText(output)
    text_edit.setReadOnly(False)
    layout.addWidget(text_edit)

    dialog.exec()


class EditorPopup(qtw.QDialog):
    """編輯器彈出視窗類別"""
    
    def __init__(self, title: str, filters: str):
        super().__init__()
        self.setWindowTitle(title)
        self._filters = filters
        self._setup_ui()

    def _setup_ui(self):
        """設置UI元件"""
        layout = qtw.QVBoxLayout()
        self.text_edit = qtw.QTextEdit()
        self.text_edit.setPlainText(self._filters)
        layout.addWidget(self.text_edit)

        apply_button = qtw.QPushButton("套用")
        apply_button.clicked.connect(self._apply_data)
        layout.addWidget(apply_button)

        self.setLayout(layout)
        self.resize(750, 300)
        
    def _apply_data(self):
        """套用編輯的資料"""
        self._filters = self.text_edit.toPlainText()
        self.accept()

    def get_result(self) -> str:
        """取得編輯結果"""
        return self._filters


class ScrollableWidget(qtw.QScrollArea): 
    """可捲動的元件容器"""
    
    def __init__(self, parent: Optional[qtw.QWidget] = None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.inner_widget = qtw.QWidget()
        self.inner_layout = qtw.QVBoxLayout()
        self.inner_widget.setLayout(self.inner_layout)
        self.setWidget(self.inner_widget)

    def get_layout(self) -> qtw.QVBoxLayout:
        """取得內部佈局"""
        return self.inner_layout


class MainEditorDialog(qtw.QDialog):
    """主要編輯器對話框"""
    
    def __init__(self, title: str, parent: Optional[qtw.QWidget] = None, 
                 filters_set: Optional[List] = None, second_limit_set: Optional[List] = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.filters_set = filters_set or []
        self.second_limit_set = second_limit_set or []
        
        # 初始化元件列表
        self.row_number_list: List[qtw.QLabel] = []
        self.second_limit_list: List[qtw.QLineEdit] = []
        self.edit_filters_list: List[qtw.QPushButton] = []
        self.row_widgets_list: List[qtw.QWidget] = []
        self.next_row = 0

        self._setup_ui()

    def _setup_ui(self):
        """設置UI介面"""
        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)

        # 設置捲動區域
        self.scroll_area = ScrollableWidget()
        self.scroll_layout = self.scroll_area.get_layout()
        main_layout.addWidget(self.scroll_area)

        # 行數顯示和套用按鈕
        self._setup_row_controls()
        
        # 同步二次限定區域
        self._setup_sync_controls()
        
        # 新增/刪除控制區域
        self._setup_modify_controls()

        # 初始化編輯器內容
        self.init_editor()

    def _setup_row_controls(self):
        """設置行數控制元件"""
        row1 = qtw.QHBoxLayout()
        self.row_count_label = qtw.QLabel("0")
        self.oneclick_btn = qtw.QPushButton("快速編輯資料")
        self.apply_btn = qtw.QPushButton("套用資料")
        
        row1.addWidget(qtw.QLabel("當前列數目："))
        row1.addWidget(self.row_count_label)
        row1.addWidget(self.oneclick_btn)
        row1.addWidget(self.apply_btn)
        self.scroll_layout.addLayout(row1)

        self.apply_btn.clicked.connect(self._apply_all_data)
        self.oneclick_btn.clicked.connect(self.oneclick_setup)

    def _setup_sync_controls(self):
        """設置同步控制元件"""
        row2 = qtw.QHBoxLayout()
        row2.addWidget(qtw.QLabel("同步二次限定為:"))
        self.sync_entry = qtw.QLineEdit()
        self.sync_entry.setFixedWidth(80)
        self.sync_button = qtw.QPushButton("全部同步")
        self.sync_button.clicked.connect(self._sync_second_limit)
        
        row2.addWidget(self.sync_entry)
        row2.addStretch()
        row2.addWidget(self.sync_button)
        self.scroll_layout.addLayout(row2)

    def _setup_modify_controls(self):
        """設置修改控制元件"""
        row3 = qtw.QHBoxLayout()
        
        self.add_btn = qtw.QPushButton("新增欄位")
        self.delete_btn = qtw.QPushButton("刪除欄位")
        self.add_btn.clicked.connect(lambda: self._modify_rows("add"))
        self.delete_btn.clicked.connect(lambda: self._modify_rows("delete"))
        
        self.num_input = qtw.QLineEdit()
        self.num_input.setFixedWidth(60)
        
        row3.addWidget(self.add_btn)
        row3.addWidget(self.delete_btn)
        row3.addWidget(self.num_input)
        self.scroll_layout.addLayout(row3)

    def init_editor(self):
        """初始化編輯器內容"""
        if self.filters_set:
            self._add_rows(len(self.filters_set))

            for i in range(len(self.filters_set)):
                # 設定二次限定值
                if i < len(self.second_limit_set):
                    self.second_limit_list[i].setText(self.second_limit_set[i])

                # 設定按鈕樣式
                if self.filters_set[i].strip():
                    self.edit_filters_list[i].setStyleSheet("background-color: green;")
                else:
                    self.edit_filters_list[i].setStyleSheet("")

            self._update_row_number()
            self._update_row_count()

    def oneclick_setup(self):
        """一鍵設置功能"""
        filters_text = "\n-\n".join(filter.strip() for filter in self.filters_set)
        dialog = EditorPopup("快速編輯資料", filters_text)
        if dialog.exec():
            self._delete_rows(len(self.row_widgets_list))
            self.filters_set.clear()
            self.filters_set.extend(
                [filters_str.strip() for filters_str in dialog.get_result().strip().split("-")]
            )
            self.init_editor()

    def _apply_all_data(self):
        """套用所有資料"""
        self.second_limit_set.clear()
        for entry in self.second_limit_list:
            self.second_limit_set.append(entry.text())
        self.accept()

    def _sync_second_limit(self):
        """同步二次限定值"""
        text = self.sync_entry.text().strip()
        for filters, entry in zip(self.filters_set, self.second_limit_list):
            entry.setText(text if filters else "")

    def _update_row_number(self):
        """更新行號標籤"""
        for i, label in enumerate(self.row_number_list):
            label.setText(f"第 {i + 1} 組")

    def _update_row_count(self):
        """更新行數計數"""
        self.row_count_label.setText(str(len(self.second_limit_list)))

    def _create_row_widget(self, row_index: int) -> tuple:
        """創建行元件"""
        row_widget = qtw.QWidget()
        row_layout = qtw.QHBoxLayout(row_widget)
        
        # 創建標籤
        label = qtw.QLabel()
        label.setFixedWidth(40)
        
        # 創建輸入框
        entry = qtw.QLineEdit()
        entry.setFixedWidth(80)
        
        # 創建按鈕
        button = qtw.QPushButton("編輯篩選器內容")
        button.setFixedWidth(120)
        
        def editor_handler(idx: int, btn: qtw.QPushButton):
            def handler():
                dialog = EditorPopup(f"編輯第 {idx + 1} 組", self.filters_set[idx])
                if dialog.exec():
                    self.filters_set[idx] = dialog.get_result()
                    if self.filters_set[idx].strip():
                        btn.setStyleSheet("background-color: green;")
                    else:
                        btn.setStyleSheet("")
            return handler
        
        button.clicked.connect(editor_handler(row_index, button))
        
        # 添加元件到佈局
        row_layout.addWidget(label)
        row_layout.addWidget(entry)
        row_layout.addWidget(button)
        
        return row_widget, label, entry, button

    def _modify_rows(self, mode: str):
        """修改行數"""
        try:
            n = int(self.num_input.text().strip())
            if n <= 0:
                raise ValueError("請輸入正整數")
        except Exception as e:
            qtw.QMessageBox.critical(self, "格式錯誤", str(e))
            return

        if mode == "add":
            self._add_rows(n)
        elif mode == "delete":
            self._delete_rows(n)

        self._update_row_number()
        self._update_row_count()

    def _add_rows(self, n: int):
        """新增行"""
        for _ in range(n):
            row_index = len(self.row_widgets_list)
            
            # 確保 filters_set 有足夠的元素
            if len(self.filters_set) <= row_index:
                self.filters_set.append("")

            # 創建行元件
            row_widget, label, entry, button = self._create_row_widget(row_index)
            
            # 添加到捲動佈局
            self.scroll_layout.addWidget(row_widget)
            
            # 儲存參考
            self.row_number_list.append(label)
            self.second_limit_list.append(entry)
            self.edit_filters_list.append(button)
            self.row_widgets_list.append(row_widget)
            self.next_row += 1

    def _delete_rows(self, n: int):
        """刪除行"""
        for _ in range(min(n, len(self.row_widgets_list))):
            # 從列表中移除
            label = self.row_number_list.pop()
            entry = self.second_limit_list.pop()
            button = self.edit_filters_list.pop()
            row_widget = self.row_widgets_list.pop()
            
            # 刪除元件
            row_widget.deleteLater()
            self.next_row -= 1
        
        # 清理 filters_set
        while len(self.filters_set) > len(self.second_limit_list):
            self.filters_set.pop()
