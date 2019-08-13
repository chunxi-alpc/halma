from pygame import*
import sys
from setting import*
#from netmode import*
#from local import*
if __name__ == '__main__':
    setting()
    while True:  # 死循环确保窗口一直显示
        for e in event.get():  # 遍历所有事件
            if e.type == QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
            # 按Esc则退出游戏
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    exit()
            if e.type == MOUSEBUTTONDOWN:
                x,y = mouse.get_pos()
                dd=160
                ss=28
                h=145
                xx=150
                yy=50
                if x in range(ss,ss+xx) and y in range(h+3,h+3+yy) :
                    print('网络模式')
                    #net_mode()
                elif x in range(ss+dd,ss+dd+xx) and y in range(h,h+yy) :
                    print('人机模式')
                   # local()
                elif x in range(ss+dd*2,ss+dd*2+xx) and y in range(h,h+yy) :
                    print('悔棋')
                elif x in range(ss+dd*3,ss+dd*3+xx) and y in range(h,h+yy) :
                    print('重新开始')
                    setting()
                elif x in range(ss+dd*4,ss+dd*4+xx) and y in range(h,h+yy) :
                    print('游戏结束')
                    
            pressed_keys = key.get_pressed()
            # 这里获取鼠标的按键情况
            pressed_mouse = mouse.get_pressed()
            
        display.flip()  # 更新全部显示

    quit()  # 退出pygame

