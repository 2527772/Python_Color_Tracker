# Python Color Tracker (实时颜色追踪与鼠标吸附)
这是一个基于 Python 和 OpenCV 的屏幕实时颜色追踪小项目。
## 🌟 功能特性
* 实时截取屏幕画面并捕捉特定颜色（如蓝色）。
* 智能去除屏幕高亮/白色文字干扰。
* 检测目标轮廓，计算中心坐标，并画出红框和绿色准星。
* 鼠标“距离吸附”功能：按住右键，鼠标会平滑吸附到目标上；松开即恢复自由。
* 安全机制：支持 `Esc` 键全局安全退出。
## 🛠️ 技术栈
* Python 3.14
* OpenCV (图像处理与轮廓识别)
* pynput (全局鼠标与键盘监听)
* pyautogui (鼠标位置控制)
## 🚀 如何运行
1. 克隆仓库：`git clone https://github.com/2527772/Python_Color_Tracker.git`
2. 创建虚拟环境并激活：`python -m venv .venv` / `.\.venv\Scripts\activate`
3. 安装依赖：`pip install mss opencv-python numpy pyautogui pynput`
4. 运行主程序：`python def.py`
## 📸 效果预览
*(你可以把仓库里的 screenshot.png 拖拽到这个 README 编辑框里，它就会自动显示成图片！)*
## 💡 注意事项
* 本程序仅供 Python/OpenCV 技术学习交流。
* 默认追踪蓝色，如果需要追踪其他颜色，请在代码中修改 HSV 阈值范围。
