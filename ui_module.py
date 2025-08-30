from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QGroupBox, QFormLayout, QDateEdit, QMessageBox,
                            QHeaderView, QSplitter, QComboBox, QStatusBar,
                            QGridLayout, QLineEdit, QFrame)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal, QTimer, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush

#用户登录界面UI
class main_ui(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化UI
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("H77 - 测试界面")
        self.resize(1200, 900)

        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 6px;
                padding: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
                font-weight: bold;
            }
            QPushButton {
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
                border: none;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                padding: 6px;
                font-weight: bold;
            }
            /* 弹窗样式 */
            QMessageBox {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 6px;
            }
            QMessageBox QLabel {
                font-family: "SimHei";
                font-size: 12px;
                color: #333333;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                padding: 6px 15px;
                margin: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: #2980b9;
            }
            QMessageBox QPushButton:default {
                background-color: #2ecc71; /* 默认按钮（如"确定"）高亮 */
            }
            .LightFrame {
                border-radius: 10px;
                border: 2px solid #ddd;
            }
        """)

        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.connection_status = QLabel("未连接")
        self.connection_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        self.detection_status = QLabel("自动检测中...")
        self.statusBar.addPermanentWidget(QLabel("连接状态: "))
        self.statusBar.addPermanentWidget(self.connection_status)
        self.statusBar.addPermanentWidget(QLabel("    "))  # 间隔
        self.statusBar.addPermanentWidget(self.detection_status)

