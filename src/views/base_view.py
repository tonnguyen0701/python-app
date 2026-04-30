# Base View
# Abstract base class for all views

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt


class BaseTableView(QMainWindow):
    """Base class for table-based views (CRUD operations)"""

    def __init__(self, title="", columns=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 900, 500)
        self.columns = columns or []
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.main_layout.addWidget(self.table)

        # Buttons
        self.create_buttons()

        self.central_widget.setLayout(self.main_layout)

    def create_buttons(self):
        """Create standard CRUD buttons - override in subclasses if needed"""
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Thêm")
        add_btn.clicked.connect(self.on_add)
        
        edit_btn = QPushButton("Sửa")
        edit_btn.clicked.connect(self.on_edit)
        
        delete_btn = QPushButton("Xóa")
        delete_btn.clicked.connect(self.on_delete)
        
        refresh_btn = QPushButton("Làm mới")
        refresh_btn.clicked.connect(self.on_refresh)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        
        self.main_layout.addLayout(button_layout)

    def add_search_bar(self, placeholder="Tìm kiếm..."):
        """Add search bar at top of view"""
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_input)
        self.main_layout.insertLayout(0, search_layout)

    def filter_table(self):
        """Filter table rows using search input text"""
        if not hasattr(self, 'search_input'):
            return

        keyword = self.search_input.text().strip().lower()
        for row in range(self.table.rowCount()):
            match = False
            if keyword == "":
                match = True
            else:
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item and keyword in item.text().lower():
                        match = True
                        break
            self.table.setRowHidden(row, not match)

    def load_table_data(self, data_list, row_mapper):
        """
        Load data into table
        row_mapper: function that takes an item and returns list of values for row
        """
        self.table.setRowCount(0)
        for item in data_list:
            row = self.table.rowCount()
            self.table.insertRow(row)
            row_values = row_mapper(item)
            for col, value in enumerate(row_values):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def get_selected_row_id(self):
        """Get Mã of selected row (first column)"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một mục!")
            return None
        return int(self.table.item(row, 0).text())

    # Abstract methods - override in subclasses
    def on_add(self):
        raise NotImplementedError

    def on_edit(self):
        raise NotImplementedError

    def on_delete(self):
        raise NotImplementedError

    def on_refresh(self):
        raise NotImplementedError
