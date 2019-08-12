import pygame
import sys

def init():
    pygame.init()  # 初始化pygame
    size = width, height = 860, 750  # 设置窗口大小
    screen = pygame.display.set_mode(size)  # 显示窗口
    background = pygame.image.load('./image/board.png')
    b=[]
    r=[]
    for i in range(10):
        b.append(pygame.image.load('./image/蓝棋'+str(i)+'.png'))
    for i in range(10):
        r.append(pygame.image.load('./image/红棋'+str(i)+'.png'))
    sound_background = pygame.mixer.Sound("./sound/background.wav")
    select_image = pygame.image.load("./image/select.png").convert_alpha()
    net_mode_image = pygame.image.load("./image/net_mode.png").convert_alpha()
    ai_mode_image = pygame.image.load("./image/ai_mode.png").convert_alpha()
    repent_image = pygame.image.load("./image/repent.png").convert_alpha()
    restart_image = pygame.image.load("./image/restart.png").convert_alpha()
    quit_image = pygame.image.load("./image/quit.png").convert_alpha()
    
    sound_move = pygame.mixer.Sound("./sound/move.wav")
    area= background.get_rect()  # 获取矩形区域
    while True:  # 死循环确保窗口一直显示
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
        screen.blit(background, area)
        screen.blit(select_image,area)
        dd=160
        ss=28
        h=145
        screen.blit(net_mode_image, (ss, h+3))
        screen.blit(ai_mode_image, (ss+dd ,h))
        screen.blit(repent_image, (ss+dd*2, h))
        screen.blit(restart_image, (ss+dd*3,h))
        screen.blit(quit_image, (ss+dd*4,h+7))
       
        screen.blit(b[0],(5,450))
        
        screen.blit(r[0],(800,450))
        
        sound_background.play()
        
        pygame.display.flip()  # 更新全部显示
    pygame.quit()  # 退出pygame

if __name__ == '__main__':
    init()
