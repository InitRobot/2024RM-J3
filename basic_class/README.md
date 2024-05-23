# README

## msg解析

[cmd_id, len...]

len指其之后的位数

#### 当cmd_id == 0:

- 内容为 [cmd_id, len, mouse_press, mouse_x, mouse_y, seq, key_num, key_1, key2, ….]
- mouse_press: 1为鼠标右键, 2为鼠标左键, 4为鼠标中间
- mouse_x : 鼠标移动距离, 范围-100 ~ 100
- mouse_y : 鼠标移动距离, 范围-100 ~ 100
- seq: 序列号 0~255
- key_num: 识别到的按键数, 最多识别三个按键
- key1: 键值

#### 当cmd_id == 1:

- 内容为 [cmd_id, len, 4(?), time, 0(?), 200(?), 0(?), health, 0(?),  ammo, 0(?), 144/133(?), 1(?)]
- time: 剩余时间（好像前一分钟是特殊的）
- health: 血量
- ammo: 发弹量

## connect.py

### class TCP_connect

用于TCP相关连接，断开，消息接收等功能

#### 	def connect

与机器人控制命令端口建立 TCP 连接

#### 	def disconnect

与机器人控制命令端口断开 TCP 连接

#### 	def IN

检测并向机器发送message

#### 	def try_get_message

这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。

#### 	def OUT

检测机器回复

#### 	def IN_OUT

检测并向机器发送message，检测机器回复

#### 	def connect_enter_SDK

与机器人控制命令端口建立 TCP 连接，并进入SDK模式控制

### class UDP_connect

用于UCP相关连接，断开，消息接收等功能

#### 	def connect

与机器人控制命令端口建立 UDP 连接

#### 	def disconnect

与机器人控制命令端口断开UDP 连接

#### 	def try_get

这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。

## solve.py

### def solve_game

用于解析赛事数据推送

### def solve_information

用于从赛事数据推送1中获得信息

### def solve_key

用于从赛事数据推送0中获得键位

### def solve_key_name

将获得键位转换为真实名称

### def solve_game_msg

将获得信息转换为具体信息

### def solve_gimbal

### def solve_chassis_position

## Chassis_Solve.py

### def Stright_Solve

底盘常规控制

### def Disk_solve

底盘小陀螺控制

### def move

底盘运动

# 使用示例：

以下为连接TCP,UDP获取赛事引擎数据的示例

```python
print("start")
TCP = connect.TCP_connection(printing=False)
UDP = connect.UDP_connection(printing=False)
TCP.connect_enter_SDK(printing=False)
UDP.connect(printing=False)
TCP.IN_OUT("game_msg on;",printing=False)
while True:
	msg = UDP.try_get(timeout=1,printing=False)
	if msg != "no_OUT":
		msg_solved = solve.solve_game(msg,printing=False)
		if msg_solved[0] == 0:
			keys = solve.solve_key(msg_solved,printing=False)
			keyname = solve.solve_key_name(keys,printing=False)
			print("keynames:", keyname)
		elif msg_solved[0] == 1:
			print("Unknow:",msg_solved)
		else:
			print("-----???-----",msg_solved)
UDP.disconnect()
TCP.disconnect()
```



# 日志

- 20240420
    - 12:44 完成
        - class TCP_connection
    - 13:12 完成
        - class UDP_connect
        - def solve_game
        - def solve_key
        - solve_key_name
        - def solve_gimbal
        - def solve_chassis_position
    - 13:31完成样例代码
- 20240421
    - 11:22 debug，目前可获取赛事数据
        - 注意到自检过程中会无法接受数据
        - 有时会出现cmd_id为1的赛事数据（一般键位收到的是0），猜测是赛事官方的时间
        - game msg push [1, 11, 4, 1, 0, 200, 0, 200, 0, 72, 0, 141, 1];
        - 猜测第二位表示阶段（此处为第四阶段即手动2），第四位表示剩余时间（剩余一秒），倒数第四位发单量，倒数第六位血量
    - 11:59
        - 完成部分msg解析
    - 12:56
        - 优化为import文件
    - 13:55
        - 完成def solve_game_msg
    - 17:10
        - 完成优化solve_game_msg中的mouse
    - 17:52
        - 解决一些小问题
- 20240422
    - 6:53 开始完成chassis解算
- 20240423
    - 6:40 完成chassis:straight_solve，未测试
- 20240424
    - 17:49 完成小陀螺和直排控制，未设置回中
- 20240425
    - 6:45 完成回中，但操作延迟有点大
- 20240426
    - 6:11 完善程序
- 20240429
    - 17:54 发现好像一定要自由模式才可以控制底盘移动
- 20240430
    - 6:47 实现实时控制
    - 18:17 实现所有功能
    - 19:38 可控制速度
- 20240502
    - 14:20 尝试加入自瞄
    - 16:03 发现RMSDK与SDK不兼容，准备将原来的代码改成RMSDK
    - 16:35 发现RMSDK没有赛事数据推送到文档，有BUG，放弃
- 20240503
    - 13:11 试图优化视频流
    - 16:32 实现延时在3秒左右的视频流，发现无法作为库来调![image-20240505164551577](C:\Users\Victor\AppData\Roaming\Typora\typora-user-images\image-20240505164551577.png)
- 20240504
    - 13:10 发现是因为导入auto_aim导致的
    - 14:56 经过研究不知道为啥TCP_video连不上，决定使用官方的robot_connect
    - 16:05 我的大脑在燃烧
- 20240505
    - 11:54 
        - 梳理目前情况
            - 完成了基于SDK的底盘控制
            - 完成基于RMSDK的自瞄
            - 完成基于SDK的视频流推送最后一帧获取（减少延时）
        - 当前方案
            - SDK 可以选择自己继续研究如何同时开启TCP以及TCP_view	
                - 优点：可以保留之前的底盘控制文件	
                - 缺点：BUG多
            - SDK 可以基于官方的robot_control
                - 优点：如果要进行其他推送可以减少工作
                - 缺点：底盘控制从头写，BUG多
            - RMSDK 发现原来的赛事数据推送虽然没有文档，但有样例代码
                - 优点：只要在样例代码上修改
                - 缺点：环境配置迁移麻烦，底盘控制有大段弃用代码，不确定赛事官方信息推送格式（貌似不会有cmd_id？无法判断比赛开始？）
        - 决定：首先尝试RMSDK，主要观察赛事数据的推送。若无法实现转为官方SDK样例。
    - 13:57 回忆起来官方的RMSDK样例代码是报错的，调整为继续官方SDK（robot_control）
    - 14:02 官方的RobotLiveview运行无法返回视频，发现原来写好的tmp_fast2.py也无法正常运行
    - 15:26 SDK_dji_control/RobotLiveview.py实现视频流获取，计划改为最后一帧
    - 15:31 SDK_dji_control/RobotLiveview.py实现最后一帧获取
    - 16:19 尝试auto_aim.py
    - 16:43 香橙派上貌似出了问题![](C:\Users\Victor\AppData\Roaming\Typora\typora-user-images\image-20240505164617110.png)
    - 17:19 实现自瞄
    - 17:45 target格式略有问题，先下班
- 20240506
    - 6:55 在为避免画面卡住增加quit，command后反倒无法开始video_socket
- 20240513
    - 6:57 开始配置摄像头所需环境[基于香橙派 调用USB摄像头 的两种方法（命令&脚本）_香橙派dakaiusb-CSDN博客](https://blog.csdn.net/Super_Fisher_man/article/details/137027059?ops_request_misc=&request_id=&biz_id=102&utm_term=香橙派摄像头&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-137027059.142^v100^pc_search_result_base8&spm=1018.2226.3001.4187)[香橙派使用摄像头_ov13855-CSDN博客](https://blog.csdn.net/m0_58944591/article/details/129788061?ops_request_misc=%7B%22request%5Fid%22%3A%22171555329516800226580626%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=171555329516800226580626&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-129788061-null-null.142^v100^pc_search_result_base8&utm_term=香橙派摄像头&spm=1018.2226.3001.4187)


