from pygame import*
import sys
from math import *
import win32api,win32con
role='blue'
def role_change():
    global role
    if role=='blue':
        role='red'
    else:
        role='blue'
select_chess = None
selected=None
chess_pos =[[0]*15 for i in range(15)]
chess0 =[[] for i in range(8)]
dd=65
h=450
dx=sqrt(3)/2*dd
dy=dd*0.5
st=5
for j in range(7):
    for i in range(7-j):
        chess0[j].append((st+i*dx,h-i*dy))
    st+=dx
    h+=dy
        
st=400
h=220
for i in range(8):
    chess0[i].append((st,h+i*dd))
        
st=800
h=450
for j in range(7):
    for i in range(6-j,-1,-1):
        chess0[7-j].append((st-i*dx,h+i*dy))
    st-=dx
    h-=dy
for i in range(8):
    for j in range(8):
        chess_pos[i+7-j][i+j]=chess0[i][j]

'''
flag = [[-2]*15 for i in range(15) ]
for i in range(15):
    for j in range(15):
        if  i+j>6 and i+j<22 and (i+j) % 2==1 and i-j>=-7 and i-j<=7 :
            flag[i][j]=-1
for i in range(15):
    print(flag[i]) 
'''
flag=[[-2, -2, -2, -2, -2, -2, -2, -1, -2, -2, -2, -2, -2, -2, -2],
[-2, -2, -2, -2, -2, -2, -1, -2, -1, -2, -2, -2, -2, -2, -2],
[-2, -2, -2, -2, -2, -1, -2, -1, -2, -1, -2, -2, -2, -2, -2],
[-2, -2, -2, -2, -1, -2, -1, -2, -1, -2, -1, -2, -2, -2, -2],
[-2, -2, -2,4, -2, -1, -2, -1, -2, -1, -2, 11, -2, -2, -2],
[-2, -2, 5, -2, -1, -2, -1, -2, -1, -2, -1, -2, 17, -2, -2],
[-2, 9, -2, 3, -2, -1, -2, -1, -2, -1, -2, 12, -2, 18, -2],
[0, -2, 6, -2, -1, -2, -1, -2, -1, -2, -1, -2, 16, -2, 10],
[-2, 8, -2, 2, -2, -1, -2, -1, -2, -1, -2, 13, -2, 19, -2],
[-2, -2, 7, -2, -1, -2, -1, -2, -1, -2, -1, -2, 15, -2, -2],
[-2, -2, -2, 1, -2, -1, -2, -1, -2, -1, -2, 14, -2, -2, -2],
[-2, -2, -2, -2, -1, -2, -1, -2, -1, -2, -1, -2, -2, -2, -2],
[-2, -2, -2, -2, -2, -1, -2, -1, -2, -1, -2, -2, -2, -2, -2],
[-2, -2, -2, -2, -2, -2, -1, -2, -1, -2, -2, -2, -2, -2, -2],
[-2, -2, -2, -2, -2, -2, -2, -1, -2, -2, -2, -2, -2, -2, -2]]

b=[]
r=[]
init()
size = width, height = 860, 750  # 设置窗口大小
screen = display.set_mode(size)  # 显示窗口
select_image = image.load("./image/select.png").convert_alpha()
background = image.load('./image/board.png')
for i in range(10):
    b.append(image.load('./image/蓝棋'+str(i)+'.png'))
for i in range(10):
    r.append(image.load('./image/红棋'+str(i)+'.png'))
area=b[0].get_rect()
net_mode_image = image.load("./image/net_mode.png").convert_alpha()
ai_mode_image = image.load("./image/ai_mode.png").convert_alpha()
repent_image = image.load("./image/repent.png").convert_alpha()
restart_image = image.load("./image/restart.png").convert_alpha()
quit_image = image.load("./image/quit.png").convert_alpha()
sound_background = mixer.Sound("./sound/background.wav")
sound_move = mixer.Sound("./sound/move.wav")
area= background.get_rect()  # 获取矩形区域
def draw():
    global chess_pos
    global flag
    global select_chess 
    screen.blit(background, area)
    if select_chess !=None:
        screen.blit(select_image,chess_pos[select_chess[0]][select_chess[1]])
    display.set_caption("国际跳棋")
    #棋子初始坐标
    dd=160
    ss=28
    h=145
    screen.blit(net_mode_image, (ss, h+3))
    screen.blit(ai_mode_image, (ss+dd ,h))
    screen.blit(repent_image, (ss+dd*2, h))
    screen.blit(restart_image, (ss+dd*3,h))
    screen.blit(quit_image, (ss+dd*4,h+7))
    for i in range(15):
        for j in range(15):
            if flag[i][j]>-1:
                if flag[i][j]<10:
                    screen.blit(b[flag[i][j]],chess_pos[i][j])
                else:
                    screen.blit(r[flag[i][j]-10],chess_pos[i][j])

#sound_background.play()

def is_chess_clicked(x,y):
    d=54
    global role
    global chess_pos
    global flag
    for i in range(15):
        for j in range(15):
            if flag[i][j]>-1:
                if (role=='blue' and flag[i][j]<10)or(role=='red' and flag[i][j]>9):
                    if x>chess_pos[i][j][0] and x<chess_pos[i][j][0]+d and y>chess_pos[i][j][1] and y<chess_pos[i][j][1]+d :
                        return i,j
    return None

def is_space_clicked(x,y,select_chess):
    global chess_pos
    global flag
    d=54
    dd=90
    #被移动棋子的坐标
    xx,yy=select_chess
    print(select_chess)
    if (x-chess_pos[xx][yy][0])*(x-chess_pos[xx][yy][0])+(y-chess_pos[xx][yy][1])*(y-chess_pos[xx][yy][1])>dd*dd:
        return None
    '''
    for i in range(15):
       print(flag[i])
    '''
    #dxy=[(xx-1,yy-1),(xx,yy-2),(xx+1,yy-1),(xx-1,yy+1),(xx,yy+2),(xx+1,yy+1)]
    dxy=[(xx-1,yy-1),(xx-2,yy),(xx+1,yy-1),(xx-1,yy+1),(xx+2,yy),(xx+1,yy+1)]

    for xy in dxy:
        i=xy[0]
        j=xy[1]
        print(i,j)
        if flag[i][j]==-1:
            if x>chess_pos[i][j][0] and x<chess_pos[i][j][0]+d and y>chess_pos[i][j][1] and y<chess_pos[i][j][1]+d :        
                return i,j
    return None


if __name__ == '__main__':
    firsttime = 1
    draw()
    while True:  # 死循环确保窗口一直显示
        for e in event.get():  # 遍历所有事件
            if e.type == QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
            # 按Esc则退出游戏
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    sys.exit()
                    
            if e.type == MOUSEBUTTONDOWN:
                x,y = mouse.get_pos()
                selected = is_chess_clicked(x,y)
                if selected is not None:
                        print('本次点击点击到了棋子')
                        print(selected)
                        select_chess=selected
                        selected=None
                elif select_chess != None:
                    selected=is_space_clicked(x,y,select_chess)
                    if selected is not None:
                        print('本次点击点击到了可移动的空格')
                        print(selected)
                        i,j=selected
                        ii,jj=select_chess
                        flag[i][j]=flag[ii][jj]
                        flag[ii][jj]=-1
                        selected=None
                        select_chess = None
                        role_change()
                else:
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
                    elif x in range(ss+dd*4,ss+dd*4+xx) and y in range(h,h+yy) :
                        print('游戏结束')
            draw()
            display.flip()  # 更新全部显示
            if firsttime == 1:
                firsttime = 0
                win32api.MessageBox(0, "石头剪刀布，谁赢谁先出！", "提示",win32con.MB_OK)

    quit()  # 退出pygame

