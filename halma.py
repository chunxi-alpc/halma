import pygame 
import sys
from math import *
import itertools
import random
pygame.font.init()

font = pygame.font.SysFont("Arial", 50)

def role_change():
    global role
    if role=='blue':
        role='red'
    else:
        role='blue'
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

weight=[[-2, -2, -2, -2, -2, -2, -2, -1, -2, -2, -2, -2, -2, -2, -2],
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
pygame.init()
size = width, height = 860, 750  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
select_image = pygame.image.load("./image/select.png").convert_alpha()
background = pygame.image.load('./image/board.png')
for i in range(10):
    b.append(pygame.image.load('./image/蓝棋'+str(i)+'.png'))
for i in range(10):
    r.append(pygame.image.load('./image/红棋'+str(i)+'.png'))
area=b[0].get_rect()
blue_sign=pygame.image.load("./image/蓝棋.png").convert_alpha()
red_sign=pygame.image.load("./image/红棋.png").convert_alpha()

net_mode_image = pygame.image.load("./image/net_mode.png").convert_alpha()
ai_mode_image = pygame.image.load("./image/ai_mode.png").convert_alpha()
repent_image = pygame.image.load("./image/repent.png").convert_alpha()
restart_image =pygame.image.load("./image/restart.png").convert_alpha()
quit_image = pygame.image.load("./image/quit.png").convert_alpha()
sound_background = pygame.mixer.Sound("./sound/background.wav")
sound_move = pygame.mixer.Sound("./sound/move.wav")
area= background.get_rect()  # 获取矩形区域
def draw():
    global chess_pos
    global flag
    global select_chess 
    screen.blit(background, area)
    if select_chess !=None:
        screen.blit(select_image,chess_pos[select_chess[0]][select_chess[1]])
    pygame.display.set_caption("国际跳棋")
    #棋子初始坐标
    dd=160
    ss=28
    h=145
    screen.blit(blue_sign, (70,260))
    screen.blit(red_sign, (730,260))
    if role=='blue' :
        screen.blit(select_image,(70,260))
    else :
        screen.blit(select_image,(730,260))
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

def removable(x,y,select_chess):
    global chess_pos
    global flag
    global role
    d=54
    
    #dd=170
    #被移动棋子的坐标
    xx,yy=select_chess
   # if (x-chess_pos[xx][yy][0])*(x-chess_pos[xx][yy][0])+(y-chess_pos[xx][yy][1])*(y-chess_pos[xx][yy][1])>dd*dd:
     #   return None
    
    #移
    dxy=[(xx-1,yy-1),(xx-2,yy),(xx+1,yy-1),(xx-1,yy+1),(xx+2,yy),(xx+1,yy+1)]
    for xy in dxy:
        i=xy[0]
        j=xy[1]
        if i>=0 and i<=14 and j>=0 and j<=14:
            if flag[i][j]==-1:
                if x>chess_pos[i][j][0] and x<chess_pos[i][j][0]+d and y>chess_pos[i][j][1] and y<chess_pos[i][j][1]+d :        
                    return i,j
    #邻
    for xy in dxy:
        i=xy[0]
        j=xy[1]
        if i>=0 and i<=14 and j>=0 and j<=14:
            if flag[i][j]>-1:
                dx=i-xx
                dy=j-yy
                i=dx+i
                j=dy+j
                if i>=0 and i<=14 and j>=0 and j<=14:
                    if flag[i][j]==-1:
                        if x>chess_pos[i][j][0] and x<chess_pos[i][j][0]+d and y>chess_pos[i][j][1] and y<chess_pos[i][j][1]+d :        
                            return i,j

    #单跨
    for i in range(15):
        for j in range(15):
            if flag[i][j]==-1:
                if x>chess_pos[i][j][0] and x<chess_pos[i][j][0]+d and y>chess_pos[i][j][1] and y<chess_pos[i][j][1]+d :        
                #选择到一个空格
                    num=[]
                    #左斜
                    if i+j==xx+yy:
                        if i>xx:
                            ii=i-1
                            jj=j+1
                        else:
                            ii=i+1
                            jj=j-1
                        if flag[ii][jj]>-1:
                            for iii in range(min(i,xx),max(i,xx)+1):
                                for jjj in range(min(j,yy),max(j,yy)+1):
                                    if flag[iii][jjj]>-1 and iii+jjj==xx+yy:
                                        num.append(flag[iii][jjj])               
                    #右斜 
                    elif i-j==xx-yy:
                        if i>xx:
                            ii=i-1
                            jj=j-1
                        else:
                            ii=i+1
                            jj=j+1
                        if flag[ii][jj]>-1:
                            for iii in range(min(i,xx),max(i,xx)+1):
                                for jjj in range(min(j,yy),max(j,yy)+1):
                                    if flag[iii][jjj]>-1 and iii-jjj==xx-yy:
                                        num.append(flag[iii][jjj])     
                    #竖直
                    elif j==yy:
                        if i>xx:
                            ii=i-2
                            jj=j
                        else:
                            ii=i+2
                            jj=j
                        if flag[ii][jj]>-1 and ii>=0 and ii<=14 and jj>=0 and jj<=14:
                            for iii in range(min(i,xx),max(i,xx)+1,2):
                                num.append(flag[iii][j])     
                    else:
                        break
                    if num==[]:
                        break
                    if flag[xx][yy] in num:
                        num.remove(flag[xx][yy])
                    #确保空格旁边有棋子

                    num_len=len(num)
                    for each in range(num_len):
                        if num[each]>9:
                            num[each]=num[each]-10
                    num_list=[[] for i in range(num_len)]
                    print(num)
                    num_list[num_len-1]=list(itertools.permutations(num,num_len))
                    while num_len>1:
                        print(num_list)
                        for e in range(len(num_list[num_len-1])):
                            num1=num_list[num_len-1][e][0]
                            num2=num_list[num_len-1][e][1]
                            next_list=num_list[num_len-1][e][2:]
                            next_list=next_list+(num1+num2,)
                            num_list[num_len-2].append(next_list)
                            
                            next_list=num_list[num_len-1][e][2:]
                            next_list=next_list+(num1-num2,)
                            num_list[num_len-2].append(next_list)
                            
                            next_list=num_list[num_len-1][e][2:]
                            next_list=next_list+(num1*num2,)
                            num_list[num_len-2].append(next_list)

                            if num2!=0:
                                next_list=num_list[num_len-1][e][2:]
                                next_list=next_list+(num1//num2,)
                                num_list[num_len-2].append(next_list)
                            
                        num_len-=1
                        tot=len(num_list[num_len-1])
                        for e in  range(tot):
                            num_list[num_len-1]+=itertools.permutations(num_list[num_len-1][e],num_len)
                        num_list[num_len-1]=list(set(num_list[num_len-1]))
                    print(num_list)
                    if ((flag[xx][yy],) in num_list[0] and role=='blue') or ((flag[xx][yy]-10,) in num_list[0] and role=='red'):
                        return i,j
    return None

pre_space=None
pre_chess=None

if __name__ == '__main__':
    
    draw()
    while True:  # 死循环确保窗口一直显示
        for e in pygame.event.get():  # 遍历所有事件
            if e.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
            # 按Esc则退出游戏
            if e.type == pygame.KEYDOWN:
                if e.key == K_ESCAPE:
                    sys.exit()
                    
            if e.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                selected = is_chess_clicked(x,y)
                if selected is not None:
                        print('本次点击点击到了棋子')
                        print(selected)
                        select_chess=selected
                        selected=None
                elif select_chess != None:
                    selected=removable(x,y,select_chess)
                    if selected is not None:
                        print('本次点击点击到了可移动的空格')
                        print(selected)
                        i,j=selected
                        ii,jj=select_chess
                        flag[i][j]=flag[ii][jj]
                        flag[ii][jj]=-1
                        pre_space=selected
                        pre_chess=select_chess
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
                        if pre_chess!=None:
                            ii,jj=pre_space
                            i,j=pre_chess
                            flag[i][j]=flag[ii][jj]
                            flag[ii][jj]=-1
                            role_change()
                            pre_chess=None
                    elif x in range(ss+dd*3,ss+dd*3+xx) and y in range(h,h+yy) :
                        print('重新开始')
                        role='blue'
                        select_chess = None
                        selected=None
                        re_chess=None
                        flag=weight
                        break
                    elif x in range(ss+dd*4,ss+dd*4+xx) and y in range(h,h+yy) :
                        print('算分叫停')
                        blue_sum=0
                        for i in range(11,15):
                            for j in range(4,11):
                                if flag[j][i]>0 and flag[j][i]<10:
                                    blue_sum+=(weight[j][i]-10)*flag[j][i]
                                    print(weight[j][i],flag[j][i])
                        red_sum=0
                        cnt=0
                        for i in range(0,4):
                            for j in range(4,11):
                                if flag[j][i]>-2:
                                    cnt+=1
                                if flag[j][i]>9 :
                                    red_sum+=weight[j][i]*(flag[j][i]-10)
                                    print(weight[j][i],flag[j][i])
                        print(blue_sum)
                        print(red_sum)
                        
                        final_text2 = "Blue final score is:  " + str(blue_sum)
                        final_text1 = "Red final score is:  " + str(red_sum)
                        font = pygame.font.SysFont("Ink Free", 30)
                        ft1_surf = font.render(final_text1, 1, (220, 20, 60))                                                 
                        ft2_surf = font.render(final_text2, 1, (65,105,225))                            
                        screen.blit(ft2_surf, (70,210))  
                        screen.blit(ft1_surf, (520,210))  
                        pygame.display.flip()                                                            # 更新整个待显示的Surface对象到屏幕上
                        sys.exit()
            draw()
            pygame.display.flip()  # 更新全部显示
            
    quit()  # 退出pygame

