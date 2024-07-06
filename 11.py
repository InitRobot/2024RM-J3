# -*- encoding: utf-8 -*-
# 测试环境：Python 3.6 版本
import serial

ser = serial.Serial()

# 配置串口 波特率 115200，数据位 8 位，1 个停止位，无校验位，超时时间 0.2 秒
ser.port = '/dev/ttyS0'
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.stopbits = serial.STOPBITS_ONE
ser.parity = serial.PARITY_NONE
ser.timeout = 0.2

# 打开串口
ser.open()

while True:

        # 等待用户输入控制指令
        msg = input(">>> please input SDK cmd: ")

        # 当用户输入 Q 或 q 时，退出当前程序
        if msg.upper() == 'Q':
                break

        # 添加结束符
        msg += ';'

        ser.write(msg.encode('utf-8'))

        recv = ser.readall()

        print(recv.decode('utf-8'))

# 关闭串口
ser.close()