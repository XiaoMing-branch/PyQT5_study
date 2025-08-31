from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                             QGroupBox, QFormLayout, QDateEdit, QMessageBox,
                             QHeaderView, QSplitter, QComboBox, QStatusBar,
                             QGridLayout, QLineEdit, QFrame, QDateTimeEdit, QTextBrowser)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal, QTimer, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
from PyQt5 import QtCore
#用户登录界面UI
class main_ui(QMainWindow):
    # 定义信号
    serial_disconnect_request = pyqtSignal()
    query_data_request = pyqtSignal(str, str)  # 开始日期, 结束日期
    clear_data_request = pyqtSignal()
    refresh_ports_request = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 初始化UI
        self.init_ui()

        self.tim_init()

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
        #CH340状态栏
        #创建一个QStatusBar对象，变量名自定义为statusBar_ch340（可体现功能，如关联CH340设备）
        self.statusBar_ch340 = QStatusBar()
        #将创建的状态栏设置为主窗口（self）的状态栏
        self.setStatusBar(self.statusBar_ch340)
        #创建"连接状态"标签，初始文本为"未连接"
        self.connection_status = QLabel("未连接")
        #为连接状态标签设置样式：深红色（#e74c3c）、加粗，突出显示连接状态
        self.connection_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        #创建"检测状态"标签，初始文本为"自动检测中..."
        self.detection_status = QLabel("自动检测中...")
        #将标签添加到状态栏
        self.statusBar_ch340.addPermanentWidget(QLabel("连接状态: "))
        self.statusBar_ch340.addPermanentWidget(self.connection_status)
        self.statusBar_ch340.addPermanentWidget(QLabel("    "))  # 间隔
        self.statusBar_ch340.addPermanentWidget(self.detection_status)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 顶部信息栏
        top_info_layout = QHBoxLayout()

        #系统标题
        self.title_label = QLabel("H77测试界面")
        title_font = QFont("SimHei", 20)
        self.title_label.setFont(title_font)

        #软/硬件版本号
        self.version_label = QLabel("软件版本：未知 | 硬件版本：未知")
        version_font = QFont("SimHei", 8)
        self.version_label.setFont(version_font)

        #时间显示
        self.time_label = QLabel("年-月-日-时-分-秒")
        time_font = QFont("SimHei", 8)
        self.time_label.setFont(time_font)

        #将控件放置到顶部信息栏
        top_info_layout.addWidget(self.version_label,alignment=Qt.AlignLeft)
        top_info_layout.addStretch()  # 空白占位
        top_info_layout.addWidget(self.title_label)
        top_info_layout.addStretch()#空白占位
        top_info_layout.addWidget(self.time_label,alignment=Qt.AlignRight)

        main_layout.addLayout(top_info_layout)

        # 连接状态区域
        connection_group = QGroupBox("连接管理")
        connection_layout = QHBoxLayout()
        # 断开按钮
        self.disconnect_btn = QPushButton("断开连接")
        self.disconnect_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        self.disconnect_btn.clicked.connect(self.on_disconnect_clicked)
        # 刷新按钮
        refresh_btn = QPushButton("重新检测端口")
        refresh_btn.setStyleSheet("background-color: #3498db; color: white;")
        refresh_btn.clicked.connect(self.on_refresh_clicked)
        # 连接状态显示
        self.connection_detail = QLabel("正在等待自动连接设备...")
        self.connection_detail.setStyleSheet("color: #666; font-style: italic;")

        connection_layout.addWidget(self.connection_detail, 1)
        connection_layout.addWidget(refresh_btn)
        connection_layout.addWidget(self.disconnect_btn)
        connection_group.setLayout(connection_layout)

        main_layout.addWidget(connection_group)

        #电流电压与模式区域
        self.voltage_textBrowser = QTextBrowser()
        self.voltage_textBrowser.setText("电压:")
        time_font = QFont("SimHei", 25)
        self.voltage_textBrowser.setFont(time_font)

        self.current_textBrowser = QTextBrowser()
        self.current_textBrowser.setText("电流:")
        time_font = QFont("SimHei", 25)
        self.current_textBrowser.setFont(time_font)

        self.mode_textBrowser = QTextBrowser()
        self.mode_textBrowser.setText("模式:")
        time_font = QFont("SimHei", 25)
        self.mode_textBrowser.setFont(time_font)
        #中间区域文本左侧垂直layout
        middle_txt_info_layout = QVBoxLayout()#垂直layout
        middle_txt_info_layout.addWidget(self.voltage_textBrowser)
        middle_txt_info_layout.addWidget(self.current_textBrowser)
        middle_txt_info_layout.addWidget(self.mode_textBrowser)

        middle_info_layout = QHBoxLayout()#中间区域水平layout
        middle_info_layout.addLayout(middle_txt_info_layout)

        main_layout.addLayout(middle_info_layout)


    #定时器初始化
    def tim_init(self):
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_tim_label)
        self.time_timer.start(1000)  # 每秒更新一次

    #定时器中断回调函数-更新文本时间
    def update_tim_label(self):
        tim_label = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.time_label.setText(tim_label)

    def on_disconnect_clicked(self):
        """断开连接按钮点击事件（直接处理逻辑）"""
        print("on_disconnect_clicked")
        if self.serial_thread and self.serial_thread.serial.is_open:
            self.serial_thread.stop()  # 直接调用停止方法
            self.connection_status.setText("已断开连接")
            self.connection_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
            self.connection_detail.setText("设备已断开连接")
        else:
            self.connection_detail.setText("未连接设备，无需断开")

    def on_refresh_clicked(self):
        """刷新端口按钮点击事件（直接处理逻辑）"""
        print("on_refresh_clicked")
        self.connection_detail.setText("正在重新检测端口...")
        if self.serial_thread:
            # 先停止当前连接
            if self.serial_thread.serial.is_open:
                self.serial_thread.stop()
            # 重新执行一次检测（注意：需先修改init_serial去掉死循环，否则会卡住）
            self.serial_thread.init_serial()

    #设置模式显示
    def set_mode(self, mode):
        self.mode_textBrowser.setText(mode)

    # 设置电流显示
    def set_current(self, current):
        self.current_textBrowser.setText(current)

    # 设置电压显示
    def set_voltage(self, voltage):
        self.voltage_textBrowser.setText(voltage)

    def set_connection_detail(self, status):
        self.connection_detail.setText(status)
        # 根据状态更新连接状态标签（同步更新状态栏的connection_status）
        if "成功连接" in status:
            self.connection_status.setText("已连接")
            self.connection_status.setStyleSheet("color: #2ecc71; font-weight: bold;")
        elif "设备已断开" in status or "连接失败" in status or "未检测到" in status:
            self.connection_status.setText("未连接")
            self.connection_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
