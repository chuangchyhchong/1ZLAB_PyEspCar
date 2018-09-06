'''
程序入口

注：目前各个子功能还在开发中，暂时还没有合并在一起。
'''
from car_config import gpio_dict
from motor import Motor

import webrepl

def init_motor():
    # 设定两个电机刚开始的转速为0
    # 不设定pwm的话，开发板上电电机会转

    # 左侧电机
    lmotor = Motor(gpio_dict['LEFT_MOTOR_A'], gpio_dict['LEFT_MOTOR_B']) #,motor_install_dir=False)
    # 左侧电机的速度设定为0
    lmotor.set_pwm(0)
    # 释放PWM资源
    lmotor.deinit()

    # 右侧电机
    rmotor = Motor(gpio_dict['RIGHT_MOTOR_A'], gpio_dict['RIGHT_MOTOR_B'])
    rmotor.set_pwm(0)
    rmotor.deinit()


def do_connect():
    import json
    import network
    # 尝试读取配置文件wifi_confi.json,这里我们以json的方式来存储WIFI配置
    # wifi_config.json在根目录下
    
    # 若不是初次运行,则将文件中的内容读取并加载到字典变量 config
    try:
        with open('wifi_config.json','r') as f:
            config = json.loads(f.read())
    # 若初次运行,则将进入excpet,执行配置文件的创建        
    except:
        essid = input('wifi name:') # 输入essid
        password = input('wifi passwrod:') # 输入password
        config = dict(essid=essid, password=password) # 创建字典
        with open('wifi_config.json','w') as f:
            f.write(json.dumps(config)) # 将字典序列化为json字符串,存入wifi_config.json
            
    #以下为正常的WIFI连接流程        
    wifi = network.WLAN(network.STA_IF)  
    if not wifi.isconnected(): 
        print('connecting to network...')
        wifi.active(True) 
        wifi.connect(config['essid'], config['password']) 
        import time
        time.sleep(5) #一般睡个5-10秒,应该绰绰有余
        
        if not wifi.isconnected():
            wifi.active(False) #关掉连接,免得repl死循环输出
            print('wifi connection error, please reconnect')
            import os
            # 连续输错essid和password会导致wifi_config.json不存在
            try:
                os.remove('wifi_config.json') # 删除配置文件
            except:
                pass
            do_connect() # 重新连接
        else:
            print('network config:', wifi.ifconfig()) 

if __name__ == '__main__':
    # 初始化电机
    init_motor()
    # # 连接WIFI
    # do_connect()
    # # 开启webrepl调试
    # webrepl.start()

# 设定程序执行入口

# 测试电机旋转
# exec(open('test_motor.py').read(), globals())

# 测试编码器
# exec(open('test_encoder.py').read(), globals())

# 串口PID控制电机旋转角度
# exec(open('test_uart_left_mac.py').read(), globals())

# 测试电机角度控制
# exec(open('test_pid_motor.py').read(), globals())

# 测试电机转速PID控制
# exec(open('test_motor_speed_pid.py').read(), globals())

# 测试串口调节电机转速
exec(open('test_uart_left_msc.py').read(), globals())

# 测试car
# exec(open('test_car.py').read(), globals())
# 小车前进1m
# car.move(1)