from pynput import mouse
def on_click(x,y,button,pressed):
    print(f"buzuodaoshijian,anniuwei:{button},zhuangtai{'anxia'if pressed else'songkai'}")
                                                        
with mouse.Listener(on_click=on_click) as listener:
    listener.join()