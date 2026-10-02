import mss
import cv2
import numpy as np
import pyautogui
from pynput import mouse, keyboard
is_following = False
running = True
sct = mss.MSS()
def on_click(x, y, button, pressed):
    global is_following
    if button == mouse.Button.right:
        # 标准逻辑
        if pressed:
            is_following = True
            print("✅ 吸附开启")
        else:
            is_following = False
            print("⏸️ 吸附停止")
def on_key_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        print("🚨 按下了Esc，正在安全退出...")
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener.start()
keyboard_listener.start()
print("程序运行中：长按右键吸附，松开停止。按 Esc 键随时安全退出。")
def def_sct():
    screenshot = sct.grab(sct.monitors[1])
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img
def mask(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low_blue = np.array([100, 100, 80])
    high_blue = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv_img, low_blue, high_blue)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bai_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    final_mask = cv2.bitwise_and(blue_mask, cv2.bitwise_not(bai_mask))
    return final_mask
def def_part(mask_img):
    contours, _ = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_part = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_part)
        return x, y, w, h
    else:
        return None
def def_distance(x, y, w, h):
    zhongx = int(x + w / 2)
    zhongy = int(y + h / 2)
    screen_width, screen_height = pyautogui.size()
    if zhongx < 0 or zhongx > screen_width or zhongy < 0 or zhongy > screen_height:
        return
    mouse_x, mouse_y = pyautogui.position()
    distance = ((mouse_x - zhongx) ** 2 + (mouse_y - zhongy) ** 2) ** 0.5
    # 吸附范围
    if distance < 150:
        pyautogui.moveTo(zhongx, zhongy, duration=0.2)
try:
    pyautogui.FAILSAFE = True
    while running:
        img = def_sct()
        final_mask = mask(img)
        part = def_part(final_mask)
        
        # 主逻辑：找到目标 且 按住右键，才移动鼠标
        if part and is_following:
            x, y, w, h = part
            def_distance(x, y, w, h)
except KeyboardInterrupt:
    print("\n检测到强制中断...")
finally:
    mouse_listener.stop()
    keyboard_listener.stop()
    sct.close()
    print("✅ 程序已安全退出！")