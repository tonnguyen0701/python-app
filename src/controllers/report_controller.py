# Report Controller
# Frontend logic to trigger report generation and visualization

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QTabWidget, QFileDialog)
from PyQt6.QtCore import Qt
from services.report_service import ReportService
import pandas as pd


class ReportController(QMainWindow):
    """Controller for reports and statistics"""

    def __init__(self):
        super().__init__()
        self.report_service = ReportService()
        self.init_ui()

    def init_ui(self):
        """Initialize report UI"""
        self.setWindowTitle("Báo cáo & Thống kê")
        self.setGeometry(100, 100, 900, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Title
        title = QLabel("📊 Student Score Báo cáo & Thống kê")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Tabs
        self.tabs = QTabWidget()

        # Tab 1: Điểm trung bình
        self.avg_tab = QWidget()
        self.init_average_tab()
        self.tabs.addTab(self.avg_tab, "Điểm trung bình")

        # Tab 2: Export
        self.export_tab = QWidget()
        self.init_export_tab()
        self.tabs.addTab(self.export_tab, "Xuất dữ liệu")

        layout.addWidget(self.tabs)

        # Buttons
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("Làm mới")
        refresh_btn.clicked.connect(self.refresh_data)
        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def init_average_tab(self):
        """Initialize average scores tab"""
        layout = QVBoxLayout()

        # Statistics
        stats_layout = QHBoxLayout()
        self.total_label = QLabel("Total Học sinh: 0")
        self.avg_label = QLabel("Điểm trung bình: 0.0")
        self.high_label = QLabel("Điểm cao nhất: 0.0")
        self.low_label = QLabel("Điểm thấp nhất: 0.0")
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.avg_label)
        stats_layout.addWidget(self.high_label)
        stats_layout.addWidget(self.low_label)
        layout.addLayout(stats_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Mã HS", "Tên học sinh", "Điểm trung bình"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        plot_btn = QPushButton("Tạo biểu đồ")
        plot_btn.clicked.connect(self.generate_plot)
        button_layout.addWidget(plot_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.avg_tab.setLayout(layout)

    def init_export_tab(self):
        """Initialize export tab"""
        layout = QVBoxLayout()

        # Export options
        layout.addWidget(QLabel("Xuất dữ liệu thành:"))
        button_layout = QHBoxLayout()
        
        excel_btn = QPushButton("Xuất Excel")
        excel_btn.clicked.connect(self.export_to_excel)
        
        csv_btn = QPushButton("Xuất CSV")
        csv_btn.clicked.connect(self.export_to_csv)
        
        pdf_btn = QPushButton("Export to PDF (requires reportlab)")
        
        button_layout.addWidget(excel_btn)
        button_layout.addWidget(csv_btn)
        button_layout.addWidget(pdf_btn)
        layout.addLayout(button_layout)

        layout.addStretch()
        self.export_tab.setLayout(layout)

    def refresh_data(self):
        """Refresh report data"""
        try:
            df = self.report_service.average_by_student()
            self.table.setRowCount(0)
            for idx, row in df.iterrows():
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(row['student_id'])))
                self.table.setItem(row_idx, 1, QTableWidgetItem(row['student_name']))
                self.table.setItem(row_idx, 2, QTableWidgetItem(f"{row['avg_score']:.2f}"))

            # Update statistics
            if not df.empty:
                total = len(df)
                avg = df['avg_score'].mean()
                high = df['avg_score'].max()
                low = df['avg_score'].min()
                
                self.total_label.setText(f"Total Học sinh: {total}")
                self.avg_label.setText(f"Điểm trung bình: {avg:.2f}")
                self.high_label.setText(f"High Điểm: {high:.2f}")
                self.low_label.setText(f"Low Điểm: {low:.2f}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Failed to refresh data: {str(e)}")

    def generate_plot(self):
        """Generate and display plot"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Lưu biểu đồ", "", "Tệp PNG (*.png)")
            if file_path:
                self.report_service.plot_average_distribution(file_path)
                QMessageBox.information(self, "Thành công", f"Đã lưu biểu đồ vào {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Failed to generate plot: {str(e)}")

    def export_to_excel(self):
        """Export data to Excel"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Lưu tệp Excel", "", "Excel Files (*.xlsx)")
            if file_path:
                df = self.report_service.average_by_student()
                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Thành công", f"Dữ liệu đã được xuất đến {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Failed to export: {str(e)}")

    def export_to_csv(self):
        """Export data to CSV"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Lưu tệp CSV", "", "CSV Files (*.csv)")
            if file_path:
                df = self.report_service.average_by_student()
                df.to_csv(file_path, index=False)
                QMessageBox.information(self, "Thành công", f"Dữ liệu đã được xuất đến {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Failed to export: {str(e)}")
