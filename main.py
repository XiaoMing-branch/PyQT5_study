import sys
from PyQt5.QtWidgets import QApplication
from ui_module import main_ui
from device_manager import DeviceManager


class MainApp:
    """主应用程序类，负责连接UI和设备管理模块"""
    def __init__(self):
        # 创建UI
        self.ui = main_ui()

        # 显示UI
        self.ui.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置全局字体，确保中文显示正常
    font = app.font()
    font.setFamily("SimHei")
    app.setFont(font)

    main_app = MainApp()
    sys.exit(app.exec_())