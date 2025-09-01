import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore  # 新增这行，导入QtCore模块
from ui_module import main_ui
from ch340_device_manager import SerialThread


class MainApp:
    """主应用程序类，负责连接UI和设备管理模块"""
    def __init__(self):
        # 创建UI
        self.ui = main_ui()
        # 初始化串口管理器
        self.Serial=SerialThread()
        self.ui.serial_thread = self.Serial
        # 将串口数据接收信号连接到UI处理函数
        self.Serial.data_received.connect(self.Serial.handle_data)
        # 将状态信号连接到UI更新状态
        self.Serial.status_signal.connect(self.ui.set_connection_detail, QtCore.Qt.QueuedConnection)
        # 自动检测并连接CH340串口
        self.Serial.init_serial()

        self.ui.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置全局字体，确保中文显示正常
    font = app.font()
    font.setFamily("SimHei")
    app.setFont(font)

    main_app = MainApp()
    sys.exit(app.exec_())