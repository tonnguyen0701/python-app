# Report View
# UI for reports and statistics

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt
from services.report_service import ReportService
import pandas as pd


class ReportView(QMainWindow):
    """View for reports and statistics"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Báo cáo & Thống kê")
        self.setGeometry(100, 100, 1000, 600)
        
        self.report_service = ReportService()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        
        # Điểm trung bình Tab
        self.avg_tab = QWidget()
        self.setup_average_tab()
        self.tabs.addTab(self.avg_tab, "Điểm trung bình")
        
        # Export Tab
        self.export_tab = QWidget()
        self.setup_export_tab()
        self.tabs.addTab(self.export_tab, "Xuất dữ liệu")
        
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)

    def setup_average_tab(self):
        """Setup average scores tab"""
        layout = QVBoxLayout()

        # Table to display averages
        self.avg_table = QTableWidget()
        self.avg_table.setColumnCount(3)
        self.avg_table.setHorizontalHeaderLabels(["Mã HS", "Tên học sinh", "Điểm trung bình"])
        self.avg_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.avg_table)

        # Buttons
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("Làm mới")
        refresh_btn.clicked.connect(self.load_average_scores)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)

        self.avg_tab.setLayout(layout)
        self.load_average_scores()

    def setup_export_tab(self):
        """Setup export tab"""
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Xuất dữ liệu học sinh sang:"))

        # Buttons
        button_layout = QHBoxLayout()
        
        excel_btn = QPushButton("Xuất Excel")
        excel_btn.clicked.connect(self.export_to_excel)
        button_layout.addWidget(excel_btn)
        
        csv_btn = QPushButton("Xuất CSV")
        csv_btn.clicked.connect(self.export_to_csv)
        button_layout.addWidget(csv_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()

        self.export_tab.setLayout(layout)

    def load_average_scores(self):
        """Load and display average scores"""
        try:
            averages = self.report_service.get_average_scores()
            self.avg_table.setRowCount(0)
            for avg in averages:
                row = self.avg_table.rowCount()
                self.avg_table.insertRow(row)
                self.avg_table.setItem(row, 0, QTableWidgetItem(str(avg.get('student_id', ''))))
                self.avg_table.setItem(row, 1, QTableWidgetItem(str(avg.get('student_name', ''))))
                self.avg_table.setItem(row, 2, QTableWidgetItem(f"{avg.get('average', 0):.2f}"))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Tải điểm trung bình thất bại: {str(e)}")

    def export_to_excel(self):
        """Export data to Excel"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Lưu tệp Excel", "", "Tệp Excel (*.xlsx);;Tất cả tệp (*)"
            )
            if file_path:
                self.report_service.export_to_excel(file_path)
                QMessageBox.information(self, "Thành công", "Xuất dữ liệu sang Excel thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Xuất Excel thất bại: {str(e)}")

    def export_to_csv(self):
        """Export data to CSV"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Lưu tệp CSV", "", "Tệp CSV (*.csv);;Tất cả tệp (*)"
            )
            if file_path:
                self.report_service.export_to_csv(file_path)
                QMessageBox.information(self, "Thành công", "Xuất dữ liệu sang CSV thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Xuất CSV thất bại: {str(e)}")
