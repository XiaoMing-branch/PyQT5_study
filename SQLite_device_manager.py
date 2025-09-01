import time
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal
from ui_module import main_ui

class SerialThread(QThread):
    # 定义信号：data_received接收bytes类型数据，status_signal接收str类型数据
    data_received = pyqtSignal(bytes)  	# 数据接收信号
    status_signal = pyqtSignal(str)     # 状态更新信号

    def __init__(self):
        super().__init__()
        self.serial = serial.Serial()
        self.running = True
        self.data_buffer = []  # 缓冲区，用于存储接收到的数据

    def find_ch340(self):  # 改为实例方法
        """自动检测并返回 CH340 设备的串口名称"""
        ch340_ids = {
            "VID": ["1A86", "5523"],
            "DESC_KEYWORDS": ["CH340", "CH341"]
        }

        for port in serial.tools.list_ports.comports():
            try:
                desc = str(getattr(port, 'description', '') or '')
                hwid = str(getattr(port, 'hwid', '') or '').upper()
                vid = getattr(port, 'vid', None)

                # 调试打印每个端口信息
                print(f"检测端口: {port.device}")
                print(f"  描述: {desc}")
                print(f"  HWID: {hwid}")
                print(f"  VID: {vid if vid else 'N/A'}")

                if vid:
                    vid_hex = f"{vid:04X}"
                    if (vid_hex in ch340_ids["VID"] or
                            any(kw in desc.upper() for kw in ch340_ids["DESC_KEYWORDS"])):  # 检查匹配条件
                        print(f"找到匹配的CH340设备: {port.device}")
                        return port.device
            except Exception as e:
                print(f"端口{port.device}检测异常: {str(e)}")
                continue
        print("未找到CH340设备")
        return None

    def connect(self, port, baudrate=115200):
        self.serial.port = port
        self.serial.baudrate = baudrate
        self.serial.timeout = 1

        try:
            self.serial.open()
            if self.serial.is_open:
                self.status_signal.emit(f"成功连接 {port}")
                return True
        except Exception as e:
            error_msg = f"{port}连接失败: {e}"
            self.status_signal.emit(error_msg)
        return False

    import serial  # 确保已导入serial模块

    def run(self):
        while self.running and self.serial.is_open:
            try:
                # 主动检测：无论是否有数据，都尝试读取1字节（利用超时机制）
                # 设备断开时，该操作会立即抛出SerialException
                data = self.serial.read(1)  # 读取1字节（非阻塞，因timeout=1）
                if data:  # 若有数据，继续读取剩余所有数据
                    data += self.serial.read_all()
                    self.data_received.emit(data)

                # 短暂休眠（平衡检测频率和CPU占用）
                time.sleep(0.1)  # 每100ms检测一次

            except serial.SerialException as e:
                # 捕获设备断开异常（拔插时必然触发）
                error_msg = f"设备已断开: {str(e)}"
                self.status_signal.emit(error_msg)  # 发送断开状态信号
                self.stop()  # 终止线程并关闭串口
                break
            except Exception as e:
                self.status_signal.emit(f"通信错误: {str(e)}")
                self.stop()
                break

    def stop(self):
        self.running = False
        if self.serial.is_open:
            self.serial.close()
        self.wait()  # 等待线程结束

    def init_serial(self):
        """仅检测一次CH340并尝试连接"""
        port = self.find_ch340()  # 单次检测
        if port:
            print(f"尝试连接检测到的端口: {port}")
            if self.connect(port):
                self.start()  # 连接成功启动线程
            else:
                self.status_signal.emit(f"连接端口 {port} 失败")
        else:
            self.status_signal.emit("未检测到CH340设备")

    def handle_data(self, data):
        """安全的数据处理方法（含缓冲区清理）"""
        if not data:  # 过滤空数据
            return
        # 1. 数据入队
        self.data_buffer.extend(data)  # 将新接收到的数据追加到缓冲区
        # 2. 协议解析与数据出队
        self.parse_protocol()
        # 3. 防止缓冲区膨胀（安全防护）
        if len(self.data_buffer) > 4096:  # 超过4KB未处理数据
            print("警告：缓冲区溢出，强制清空")
            self.data_buffer.clear()

    def parse_protocol(self):
        """协议解析示例（含数据出队）"""
        while len(self.data_buffer) >= 6:  # 假设协议包最小长度6字节
            # 查找帧头
            if self.data_buffer[0] != 0x55:
                del self.data_buffer[0]  # 丢弃无效头部字节
                continue
            # 检查完整包是否到达
            if len(self.data_buffer) < 6:
                break  # 数据不足
            # 提取完整数据包
            packet = bytes(self.data_buffer[:6])
            del self.data_buffer[:6]  # 移除已处理数据
            # 处理有效数据包
            self.process_packet(packet)

    def process_packet(self, packet):
        """处理完整数据包"""
        print("数据包字节分解:")
        for i, byte in enumerate(packet):
            print(f"[{i}] 0x{byte:02X}", end=' ')
        print()  # 换行