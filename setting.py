from pygame import*
import sys
from math import *
    
def setting():
    init()
    size = width, height = 860, 750  # 设置窗口大小
    screen = display.set_mode(size)  # 显示窗口
    background = image.load('./image/board.png')
    b=[]
    r=[]
    for i in range(10):
        b.append(image.load('./image/蓝棋'+str(i)+'.png'))
    for i in range(10):
        r.append(image.load('./image/红棋'+str(i)+'.png'))
    
    select_image = image.load("./image/select.png").convert_alpha()
    net_mode_image = image.load("./image/net_mode.png").convert_alpha()
    ai_mode_image = image.load("./image/ai_mode.png").convert_alpha()
    repent_image = image.load("./image/repent.png").convert_alpha()
    restart_image = image.load("./image/restart.png").convert_alpha()
    quit_image = image.load("./image/quit.png").convert_alpha()
    sound_background = mixer.Sound("./sound/background.wav")
    sound_move = mixer.Sound("./sound/move.wav")
    area= background.get_rect()  # 获取矩形区域
    screen.blit(background, area)
    dd=64
    h=450
    dx=sqrt(3)/2*dd
    dy=dd*0.5
    #棋子初始坐标
    xy_b=[(5,h), (5+3*dx,h+3*dy), (5+3*dx,h-dy), (5+3*dx,h+dy), (5+3*dx,h-3*dy),
              (5+2*dx,h-2*dy), (5+2*dx,h), (5+2*dx,h+2*dy), (5+dx,h+dy), (5+dx,h-dy)]
    xy_r=[(800,h),(800-3*dx,h-3*dy), (800-3*dx,h+dy), (800-3*dx,h-dy), (800-3*dx,h+3*dy),
              (800-2*dx,h+2*dy), (800-2*dx,h), (800-2*dx,h-2*dy), (800-dx,h-dy), (800-dx,h+dy)]
    # screen.blit(select_image,area)
    dd=160
    ss=28
    h=145
    screen.blit(net_mode_image, (ss, h+3))
    screen.blit(ai_mode_image, (ss+dd ,h))
    screen.blit(repent_image, (ss+dd*2, h))
    screen.blit(restart_image, (ss+dd*3,h))
    screen.blit(quit_image, (ss+dd*4,h+7))
    for i in range(10):
        screen.blit(b[i],xy_b[i])
        screen.blit(r[i],xy_r[i])
    
    #sound_background.play()

        
            
