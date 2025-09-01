from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                             QGroupBox, QFormLayout, QDateEdit, QMessageBox,
                             QHeaderView, QSplitter, QComboBox, QStatusBar,
                             QGridLayout, QLineEdit, QFrame, QDateTimeEdit, QTextBrowser)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal, QTimer, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
class main_ui(QMainWindow):

    def __init__(self):
        super().__init__()
        #初始化UI
        self.init_ui()

        self.tim_init()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("H77 - 测试界面")
        self.resize(1200, 900)

        # 应用样式表（QSS）美化界面外观
        self.apply_styles()

        # 创建中央部件并设置为窗口的中央部件，用于承载所有UI元素
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建垂直布局，管理中央部件内的元素排列
        main_layout = QVBoxLayout(central_widget)
        # 布局边距
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 测试界面标题组件
        self.add_headline_components(main_layout)

        # 连接管理组件
        self.add_connection_components(main_layout)

        #监控界面
        self.add_test_components(main_layout)

        #序列号输入窗口
        self.add_serial_input_components(main_layout)

    # 测试界面标题组件(版本号、标题、时间)
    def add_headline_components(self,parent_layout):
        #系统标题
        self.title_label = QLabel("H77测试界面")
        title_font = QFont("SimHei", 20)
        self.title_label.setFont(title_font)
        #上位机版本号
        self.version_label = QLabel("版本号: V1.0.0")
        version_font = QFont("SimHei", 8)
        self.version_label.setFont(version_font)
        #时间显示
        self.time_label = QLabel("年-月-日-时-分-秒")
        time_font = QFont("SimHei", 8)
        self.time_label.setFont(time_font)

        #将控件放置到顶部信息栏
        top_info_layout = QHBoxLayout()#水平布局
        top_info_layout.addWidget(self.version_label,alignment=Qt.AlignLeft)
        top_info_layout.addStretch()  # 空白占位
        top_info_layout.addWidget(self.title_label)
        top_info_layout.addStretch()#空白占位
        top_info_layout.addWidget(self.time_label,alignment=Qt.AlignRight)
        parent_layout.addLayout(top_info_layout)

    # 连接管理组件
    def add_connection_components(self,parent_layout):
        # 连接状态容器
        connection_group = QGroupBox("连接管理")
        connection_layout = QHBoxLayout()#水平布局
        # 连接状态显示
        self.connection_detail = QLabel("正在等待自动连接设备...")
        self.connection_detail.setStyleSheet("color: #666; font-style: italic;")
        # 刷新按钮
        self.refresh_btn = QPushButton("重新检测端口")
        self.refresh_btn.setStyleSheet("background-color: #3498db; color: white;")
        self.refresh_btn.clicked.connect(self.on_refresh_clicked)
        # 断开按钮
        self.disconnect_btn = QPushButton("断开连接")
        self.disconnect_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        self.disconnect_btn.clicked.connect(self.on_disconnect_clicked)

        connection_layout.addWidget(self.connection_detail)
        connection_layout.addStretch()  # 空白占位
        connection_layout.addWidget(self.refresh_btn)
        connection_layout.addWidget(self.disconnect_btn)
        connection_group.setLayout(connection_layout)
        parent_layout.addWidget(connection_group)

    def add_test_components(self,parent_layout):
        # 数据检测界面容器（外层总分组框）
        test_group = QGroupBox("数据检测")
        # 子分组框
        voltage_group = QGroupBox("电压")
        current_group = QGroupBox("电流")
        sv_group = QGroupBox("软件版本号")
        hv_group = QGroupBox("硬件版本号")
        mode_group = QGroupBox("灯效模式")
        serial_group = QGroupBox("序列号")
        # 数据显示控件
        self.voltage_data = QTextBrowser() 
        self.voltage_data.setText("-- V")  # 初始默认值
        self.voltage_data.setFont(QFont("SimHei", 14, QFont.Bold)) # 设置字体为黑体，大小14，加粗
        self.voltage_data.setStyleSheet("color: #333333; border: none;")  # 深灰字体+去边框
        self.voltage_data.setAlignment(Qt.AlignCenter)  # 居中显示
        voltage_layout = QVBoxLayout()  # 垂直布局
        voltage_layout.addWidget(self.voltage_data)
        voltage_group.setLayout(voltage_layout)

        self.current_data = QTextBrowser() 
        self.current_data.setText("-- A")
        self.current_data.setFont(QFont("SimHei", 14, QFont.Bold)) # 设置字体为黑体，大小14，加粗
        self.current_data.setStyleSheet("color: #333333; border: none;")  # 深灰字体+去边框
        self.current_data.setAlignment(Qt.AlignCenter)  # 居中显示
        current_layout = QVBoxLayout()  # 垂直布局
        current_layout.addWidget(self.current_data)
        current_group.setLayout(current_layout)

        self.sv_data = QTextBrowser() 
        self.sv_data.setText("未知")
        self.sv_data.setFont(QFont("SimHei", 14, QFont.Bold)) # 设置字体为黑体，大小14，加粗
        self.sv_data.setStyleSheet("color: #333333; border: none;")  # 深灰字体+去边框
        self.sv_data.setAlignment(Qt.AlignCenter)  # 居中显示
        sv_layout = QVBoxLayout()  # 垂直布局
        sv_layout.addWidget(self.sv_data)
        sv_group.setLayout(sv_layout)

        self.hv_data = QTextBrowser() 
        self.hv_data.setText("未知")
        self.hv_data.setFont(QFont("SimHei", 14, QFont.Bold)) # 设置字体为黑体，大小14，加粗
        self.hv_data.setStyleSheet("color: #333333; border: none;")  # 深灰字体+去边框
        self.hv_data.setAlignment(Qt.AlignCenter)  # 居中显示
        hv_layout = QVBoxLayout()  # 垂直布局
        hv_layout.addWidget(self.hv_data)
        hv_group.setLayout(hv_layout)

        self.mode_data = QTextBrowser() 
        self.mode_data.setText("未知")
        self.mode_data.setFont(QFont("SimHei", 14, QFont.Bold)) # 设置字体为黑体，大小14，加粗
        self.mode_data.setStyleSheet("color: #333333; border: none;")  # 深灰字体+去边框
        self.mode_data.setAlignment(Qt.AlignCenter)  # 居中显示
        mode_layout = QVBoxLayout()  # 垂直布局
        mode_layout.addWidget(self.mode_data)
        mode_group.setLayout(mode_layout)

        self.serial_data = QTextBrowser() 
        self.serial_data.setText("未知")
        self.serial_data.setFont(QFont("SimHei", 14, QFont.Bold)) # 设置字体为黑体，大小14，加粗
        self.serial_data.setStyleSheet("color: #333333; border: none;")  # 深灰字体+去边框
        self.serial_data.setAlignment(Qt.AlignCenter)  # 居中显示
        serial_layout = QVBoxLayout()  # 垂直布局
        serial_layout.addWidget(self.serial_data)
        serial_group.setLayout(serial_layout)
        
        test_layout = QGridLayout()#网格布局
        test_layout.addWidget(voltage_group,0,0)
        test_layout.addWidget(current_group,0,1)
        test_layout.addWidget(sv_group,1,0)
        test_layout.addWidget(hv_group,1,1)
        test_layout.addWidget(mode_group,2,0)
        test_layout.addWidget(serial_group,2,1)
        test_group.setLayout(test_layout)
        parent_layout.addWidget(test_group)

    def add_serial_input_components(self,parent_layout):
        # 序列号输入容器
        input_group = QGroupBox("序列号输入窗口")
        input_layout = QHBoxLayout()

        self.serial_input = QLineEdit()
        self.serial_input.returnPressed.connect(self.input_completed_signal)

        input_layout.addWidget(self.serial_input)
        input_group.setLayout(input_layout)
        parent_layout.addWidget(input_group)

    # 设置全局样式
    def apply_styles(self):
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
        if self.serial_thread and self.serial_thread.serial.is_open:
            self.serial_thread.stop()  # 直接调用停止方法
            self.connection_detail.setText("设备已断开连接")
        else:
            self.connection_detail.setText("未连接设备，无需断开")

    def on_refresh_clicked(self):
        """刷新端口按钮点击事件（直接处理逻辑）"""
        self.connection_detail.setText("正在重新检测端口...")
        if self.serial_thread:
            # 先停止当前连接
            if self.serial_thread.serial.is_open:
                self.serial_thread.stop()
            # 重新执行一次检测（注意：需先修改init_serial去掉死循环，否则会卡住）
            self.serial_thread.init_serial()

    def set_connection_detail(self, status):
        self.connection_detail.setText(status)

    def input_completed_signal(self):
        print("序列号输入完成:", self.serial_input.text())
        self.serial_input.clear()

    #弹窗
    def handle_serial_confirm(self):
        serial = self.serial_input.text().strip()
        if not serial:
            # 警告弹窗：黄色图标，提示用户修正
            QMessageBox.warning
            (
                self,
                "输入警告",
                "请先输入设备序列号！",
                QMessageBox.Ok
            )