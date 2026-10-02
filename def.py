import mss
import cv2
import numpy as np
import msvcrt
import pyautogui
from pynput import mouse,keyboard
sct  = mss.MSS()
is_following = False
running = True
# 定义鼠标监听的回调函数
def on_click(x, y, button, pressed):
    global is_following
    # 检测鼠标右键是否被按下
    if button == mouse.Button.right:
        if  pressed:
            is_following = True  # 按下右键，允许吸附
            print(f"右键按下状态: {is_following}")
        else:
            is_following = False # 松开右键，停止吸附
            print(f"右键按下状态: {is_following}")
def on_esc(key):
     global running
     if key==keyboard.Key.esc:
          running = False
          print("正在退出程序")
# 启动鼠标监听线程（后台运行）
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_esc)
mouse_listener.start()
keyboard_listener.start()
##引入数据库
sct  = mss.MSS()
print("程序正在运行,按'Q'退出程序")
def def_sct():
    screenshot = sct.grab(sct.monitors[1])
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img
def mask(img):
    ##掩膜转换
            hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            low_blue = np.array([100,100,80])##颜色识别
            high_blue = np.array([130,255,255])
            blue_mask = cv2.inRange(hsv_img,low_blue,high_blue)
            ##高亮消除
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            _,bai_mask = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
            finall_mask = cv2.bitwise_and(blue_mask,cv2.bitwise_not(bai_mask))
            return finall_mask
def def_part(finall_mask):
    part,_ = cv2.findContours(finall_mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if part :
        max_part = max(part,key=cv2.contourArea)
        x,y,w,h= cv2.boundingRect(max_part)
        return x,y,w,h
def def_distance(x,y,w,h):
        zhongx = int(x+w/2)      
        zhongy = int(y+h/2) 
        screen_width, screen_height = pyautogui.size() 
        if zhongx < 0 or zhongx > screen_width or zhongy < 0 or zhongy > screen_height:
            return None
        mouse_x,mouse_y = pyautogui.position()
        distance = ((mouse_x-zhongx)**2+(mouse_y-zhongy)**2)**0.5
        if distance < 200:##距离判断
                pyautogui.moveTo(zhongx,zhongy,duration=0.3)
        if 200<distance<=300:
                print("现在距离很近，接近中",end="\r")
        if distance >300:
                print(f"距离较远,距离{int(distance)}",end="\r")
        return distance        
try:
    pyautogui.FAILSAFE = True
    while running:
        img = def_sct()
        finally_mask = mask(img)
        part= def_part(finally_mask)
        ##screen_width, screen_height = pyautogui.size() 
        if is_following and part:
            x,y,w,z=part;
            distance = def_distance(x,y,w,z)
          ##  if distance >0:
           ##     print(f"当前鼠标距离: {int(distance)}")
          ##  else: print("0")
except KeyboardInterrupt:
    print("\n检测到强制中断,正在清理窗口...")
finally:
    # 给 Windows 一点点时间（0.5 秒）去处理销毁窗口的请求
    mouse_listener.stop()
    keyboard_listener.stop()
    sct.close()
    print("✅ 程序已安全退出！")