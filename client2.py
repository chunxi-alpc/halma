# coding:utf-8
#client
from socket import *
import sys
import json
import uuid 
import time 
from threading import Thread, Lock
import pygame 
from math import *
import itertools
import copy
import random

serverName = '127.0.0.1'
serverPort =50005


addr = serverName,serverPort
name = 'Mary'
side = -1
time = -1
total = -1
gameid = None
gameside = -1
clientSocket = None
net_flag = -1
request = None
msg_type = -1

def apply_for_join_game(name_):
        applying = {"type":0,
                            "msg":{
                                    "name":name_
                            }
                }
        return applying

def send_msg_to(client,msg):
	packet = json.dumps(msg)
	if (sys.version[:1] == "3"):
		packet = packet.encode('utf-8')
	#print(client.addr[0] + ":" + str(client.addr[1]) + "\t" + str(msg))
	#client.conn.send(packet)
	client.send(packet)

def receive_msg():
         mes = clientSocket.recv(1024)
         new_mes = json.loads(mes)
         return new_mes
#开始游戏
num=[]
input_flag=0
current_string = []
ok=0


last_moment=0
pre_space=None
pre_chess=None
pygame.font.init()
blue_sum=0
red_sum=0
ans=[]     
game_end=False            
mode = 'p2p'
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

blue_sign=pygame.image.load("./image/蓝棋.png").convert_alpha()
red_sign=pygame.image.load("./image/红棋.png").convert_alpha()
ok_sign=pygame.image.load("./image/ok.jpg").convert_alpha()
mode_select_image = pygame.image.load("./image/mode_select.png").convert_alpha()
repent_image = pygame.image.load("./image/repent.png").convert_alpha()
restart_image =pygame.image.load("./image/restart.png").convert_alpha()
quit_image = pygame.image.load("./image/quit.png").convert_alpha()
#sound_background = pygame.mixer.Sound("./sound/background.wav")
sound_move = pygame.mixer.Sound("./sound/move.wav")
area= background.get_rect()  # 获取矩形区域

def display_box(message):
    #print(message)
    pygame.display.set_caption("请直接输入式子，并按回车确认")
    fontobject = pygame.font.SysFont("Ink Free", 25)
    screen.blit(fontobject.render('Input:  ', 1, (47,79,79)),(15,620))
    fontobject = pygame.font.SysFont("Segoe Script", 30)
    '''
    pygame.draw.rect(screen, (245,255,250),
                    (15,720,300,30), 0)
    pygame.draw.rect(screen, (47,79,79),
                    (15-2,720-2,304,34), 1)
    '''
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (25,25,112)),(20,650))

def check():
    global current_string
    global num
    num0=[]
    for i in current_string:
        if i>='0' and i<='9':
            num0.append(int(i))
    print(num)
    print(num0)
    
    if len(num0)!=len(num):
        return None
    if set(num0)!=set(num):
        return None
    ans="".join(current_string)
    op= ['+','-','/','*']
    if ans[0] in op or ans[0]==')' or ans[-1] in op or ans[-1]=='(':
        return None
    l=len(current_string)
    for i in range(l-1):
        if ans[i] in op and ans[i+1] in op:
            return None
    ans=eval(ans)
    print(ans)
    return ans

def role_change():
    global role
    if role=='blue':
        role='red'
    else:
        role='blue'
        
def draw():
    global chess_pos
    global flag
    global select_chess
    global ai_s
    global ai_t
    global ft2_surf
    global ft1_surf
    global blue_sum
    global red_sum
    global ans
    global mode
    global pre_space
    global pre_chess
    global input_flag
    global current_string
    
    final_text2 = "Blue final score is:  " + str(blue_sum)
    final_text1 = "Red final score is:  " + str(red_sum)
    font = pygame.font.SysFont("Ink Free", 30)
    ft1_surf = font.render(final_text1, 1, (220, 20, 60))                                                 
    ft2_surf = font.render(final_text2, 1, (65,105,225))      
    screen.blit(background, area)
    print(net_flag,gameside)
    if input_flag==1 and net_flag ==gameside:
        display_box("".join(current_string))
    if game_end:
        screen.blit(ft2_surf, (70,210))  
        screen.blit(ft1_surf, (520,210))

    if pre_space !=None:
        screen.blit(select_image,chess_pos[pre_space[0]][pre_space[1]])
    if pre_chess !=None:
        screen.blit(select_image,chess_pos[pre_chess[0]][pre_chess[1]])
    if select_chess !=None:
        screen.blit(select_image,chess_pos[select_chess[0]][select_chess[1]])
    if input_flag==0:
        pygame.display.set_caption("国际数棋")
    #棋子初始坐标
    dd=160
    ss=28
    h=145
    screen.blit(blue_sign, (70,260))
    screen.blit(red_sign, (730,260))
    if role=='blue' :
        screen.blit(select_image,(70,260))
        if ans!=[]:
            font = pygame.font.SysFont("Segoe Script", 40)
            hh=555
            for each in ans:
                ft2_surf = font.render(each, 1, (220, 20, 60))            
                screen.blit(ft2_surf, (690,hh))
                hh+=30
            
    else :
        screen.blit(select_image,(730,260))
        if ans!=[]:
            font = pygame.font.SysFont("Segoe Script", 40)
            hh=555
            for each in ans:
                ft2_surf = font.render(each, 1, (65,105,225))      
                screen.blit(ft2_surf, (20,hh))
                hh+=30
        
        if mode == 'ai':
            screen.blit(ok_sign, (130,666))
            pygame.display.set_caption("点击 ‘勾’ ，就到电脑下棋了，玩家就不能悔棋了哦！")
    if mode=='p2p':
        screen.blit(mode_select_image, (ss+dd/2-15 ,h-20-8))
    elif mode=='ai':
        screen.blit(mode_select_image, (ss+dd-20 ,h+20-8))
    else :
        screen.blit(mode_select_image, (ss-15 ,h+20-8))
        
    font = pygame.font.SysFont("Ink Free", 20)
    ft0 = font.render("Net Mode", 1, (0,100,0))            
    screen.blit(ft0, (ss, h+20))
    ft0 = font.render("AI Mode", 1, (0, 100, 0))            
    screen.blit(ft0, (ss+dd ,h+20))
    ft0 = font.render("P2P Mode", 1, (0, 100, 0))            
    screen.blit(ft0, (ss+dd/2 ,h-20))
    
    
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

def dfs(num,ans,goal):
    if len(num)<1:
        return []
    if len(num)==1:
        if ( goal == num[0] and role=='blue') or (goal-10 == num[0] and role=='red'):
            return ans
    size=len(num)
    ans0=copy.deepcopy(ans)
    for num1 in range(size):
        for num2 in range(num1+1,size):
            next_num=copy.deepcopy(num)
            next_num.pop(num2)
            next_num.pop(num1)
            num0=copy.deepcopy(next_num)
            tmp=num[num1]+num[num2]
            next_num.append(tmp)
            ans.append(str(num[num1])+'+'+str(num[num2])+'='+str(tmp))
            ret=dfs(next_num,  ans ,  goal)
            if ret!=[]:
                return ret
            
            next_num=copy.deepcopy(num0)
            ans=copy.deepcopy(ans0)
            tmp=num[num1]-num[num2]
            next_num.append(tmp)
            ans.append(str(num[num1])+'-'+str(num[num2])+'='+str(tmp))
            ret=dfs(next_num,  ans ,  goal)
            if ret!=[]:
                return ret
            
            next_num=copy.deepcopy(num0)
            ans=copy.deepcopy(ans0)
            tmp=num[num2]-num[num1]
            next_num.append(tmp)
            ans.append(str(num[num2])+'-'+str(num[num1])+'='+str(tmp))
            ret=dfs(next_num,  ans ,  goal)
            if ret!=[]:
                return ret
            
            next_num=copy.deepcopy(num0)
            ans=copy.deepcopy(ans0)
            tmp=num[num1]*num[num2]
            next_num.append(tmp)
            ans.append(str(num[num1])+'*'+str(num[num2])+'='+str(tmp))
            ret=dfs(next_num,  ans ,  goal)
            if ret!=[]:
                return ret
            
            if num[num2]!=0 and num[num1] % num[num2]==0:
                next_num=copy.deepcopy(num0)
                ans=copy.deepcopy(ans0)
                tmp=num[num1]//num[num2]
                next_num.append(tmp)
                ans.append(str(num[num1])+'/'+str(num[num2])+'='+str(tmp))
                ret=dfs(next_num,  ans ,  goal)
                if ret!=[]:
                    return ret
                
            if num[num1]!=0 and num[num2] % num[num1]==0:
                next_num=copy.deepcopy(num0)
                ans=copy.deepcopy(ans0)
                tmp=num[num2]/num[num1]
                next_num.append(tmp)
                ans.append(str(num[num2])+'/'+str(num[num1])+'='+str(tmp))
                ret=dfs(next_num,  ans ,  goal)
                if ret!=[]:
                    return ret
    return []
            
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
    global ans
    global num
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
                    if mode=='p2p' or (mode=='ai' and role=='blue') or mode == 'net':
                        global input_flag
                        input_flag=1
                    num=[]
                    #左斜.
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
                                if flag[iii][j]>-1:
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
                    '''
                    ans=dfs(num,[],flag[xx][yy])
                    print(ans)
                    if ans!=[]:
                        return i,j
                    '''
    return None


times=[0 for i in range(10)]

#默认red为电脑方
def ai_go(i,j,xx,yy):
    global times
    global flag
    flag[i][j]=copy.deepcopy(flag[xx][yy])
    print(flag[xx][yy])
    times[flag[xx][yy]-10]-=2
    flag[xx][yy]=-1
    global pre_space
    global pre_chess
    pre_space=i,j
    pre_chess=xx,yy
    global selected
    global select_chess
    selected=None
    select_chess = None
    role_change()
    
def left_line(xx,yy):
    #左斜
    global flag
    global ans
    for i in range(14,xx,-1):
        j=xx+yy-i
        if flag[i][j]==-1:
        #(i,j)为空格的位置
            num=[]
            ii=i-1
            jj=j+1
            if flag[ii][jj]>-1 and ii!=xx:
                for iii in range(ii,15):
                    jjj=xx+yy-iii
                    if flag[iii][jjj]>-1:
                        num.append(flag[iii][jjj])
            num_len=len(num)
            for each in range(num_len):
                if num[each]>9:
                    num[each]=num[each]-10
            ans=dfs(num,[],flag[xx][yy])
            print(ans)
            if ans!=[]:
                ai_go(i,j,xx,yy)
                return True
    return False

def right_line(xx,yy):
    #右斜
    global flag
    global ans
    for i in range(0,xx):
        j=i-xx+yy
        if flag[i][j]==-1:
        #(i,j)为空格的位置
            num=[]
            ii=i+1
            jj=j+1
            if flag[ii][jj]>-1 and ii!=xx:
                for iii in range(ii,xx):
                    jjj=yy-xx+iii
                    if flag[iii][jjj]>-1:
                        num.append(flag[iii][jjj])
            num_len=len(num)
            for each in range(num_len):
                if num[each]>9:
                    num[each]=num[each]-10
            ans=dfs(num,[],flag[xx][yy])
            print(ans)
            if ans!=[]:
                ai_go(i,j,xx,yy)
                return True
    return False

def one_step(xx,yy):
    global flag
    global last_moment
    if last_moment==1:
        dxy=[(xx-1,yy-1),(xx-2,yy),(xx+1,yy-1),(xx-1,yy+1),(xx+2,yy),(xx+1,yy+1)]
    else:
        dxy=[(xx-1,yy-1),(xx+1,yy-1)]
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
                        ai_go(i,j,xx,yy)
                        return True
    return False

def two_step(xx,yy):
    global flag
    global last_moment
    if last_moment==1:
        dxy=[(xx-1,yy-1),(xx-2,yy),(xx+1,yy-1),(xx-1,yy+1),(xx+2,yy),(xx+1,yy+1)]
    else:
        dxy=[(xx-1,yy-1),(xx+1,yy-1)]
    #移
    for xy in dxy:
        i=xy[0]
        j=xy[1]
        if i>=0 and i<=14 and j>=0 and j<=14:
            if flag[i][j]==-1:
                ai_go(i,j,xx,yy)
                return True
    return False
    
def ai():
    global chess_pos
    global flag
    global ans
    global times
    
    value=[0 for i in range(10)]
    #按照f(x)=abs(dx)+abs(dy)排序尝试的棋子
    
    cc=[0 for i in range(10)]
    #存储red所有棋子的位置
    
    for i in range(15):
        for j in range(15):
            if flag[i][j]>9:
                v=flag[i][j]-10
                dis=abs(i-7)+abs(j)
                value[v]=dis+times[v]
                cc[v]=i,j
    
    for kk in range(10):
        it=value.index(max(value))
        print(it) 
        #it为当前尝试移动棋子编号，红色棋子>9
        xx=cc[it][0]
        yy=cc[it][1]
        q=[0,1,2,3]
        random.shuffle(q)
        print(q)
        for each in q:
            if each==0:
                if left_line(xx,yy):
                    return
            elif each==1:
                if right_line(xx,yy):
                    return
            elif each==2:
                if one_step(xx,yy):
                    return
            else:
                if two_step(xx,yy):
                    return
        value[it]=-99999


if __name__ == '__main__':
    draw()
    pygame.display.flip() 
    dd=160
    ss=28
    h=145
    xx=150
    yy=50
    pre_key=None
    while True:  # 死循环确保窗口一直显示
        for e in pygame.event.get():  # 遍历所有事件
            if e.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
                pygame.quit()
            # 按Esc则退出游戏
            elif e.type == pygame.KEYDOWN:
                inkey=e.key
                if inkey == pygame.K_ESCAPE:
                    sys.exit()
                elif input_flag==1:# and net_flag==gameside:
                    if inkey == pygame.K_BACKSPACE:
                        current_string = current_string[0:-1]
                    elif e.unicode== '\r':
                        print(x,y,select_chess)
                        selected=removable(x,y,select_chess)
                        if len(num)<2:
                            continue
                        correct=check()
                        ii,jj=select_chess
                        if correct==None:
                            print('Input Error!')
                        elif correct!=flag[ii][jj]%10:
                            print('Wrong! Please input again')
                        else:
                            print('本次点击点击到了可移动的空格')
                            fflag=0
                            print(x,y)
                            d=54
                            for i in range(15):
                                for j in range(15):
                                    if flag[i][j]==-1:
                                        print(chess_pos[i][j])
                                        if x>chess_pos[i][j][0] and x<chess_pos[i][j][0]+d and y>chess_pos[i][j][1] and y<chess_pos[i][j][1]+d :        
                                            fflag=1
                                            x,y=i,j
                                            
                                            break
                                if fflag==1:
                                    break
                            flag[x][y]=copy.deepcopy(flag[ii][jj])
                            flag[ii][jj]=-1
                            pre_space=x,y
                            pre_chess=ii,jj
                            selected=None
                            select_chess = None
                            if mode == 'net':
                                    ms = {"type": 1,"msg":{"game_id":gameid,"side": gameside,"num":  flag[ii][jj],"src": {"x": ii,"y": jj},
                                                            "dst":{ "x": x, "y": y},
                                                           "exp": current_string}
                                          }
                                    send_msg_to(clientSocket,ms)
                                    net_flag = 1
                            role_change()
                            current_string = []
                            input_flag=0
                            #net_flag==abs(gameside-1)
                  
                    elif inkey == pygame.K_KP_MINUS or inkey == pygame.K_MINUS:
                        current_string.append("-")
                    elif inkey == pygame.K_KP_PLUS or inkey == pygame.K_PLUS:
                        current_string.append("+")
                    elif inkey == pygame.K_KP_MULTIPLY or inkey == pygame.K_ASTERISK:
                        current_string.append("*")
                    elif inkey == pygame.K_KP_DIVIDE or inkey == pygame.K_SLASH:
                        current_string.append("/")
                        
                    elif e.key==pygame.K_9:
                        if pre_key==42 or pre_key==54:
                            current_string.append("(")
                        else :current_string.append("9")
                    elif e.key == pygame.K_0:
                        if pre_key==42 or pre_key==54:
                            current_string.append(")")
                        else :current_string.append("0")
                    elif e.key == pygame.K_EQUALS:
                        if pre_key==42 or pre_key==54:
                            current_string.append("+")
                    elif e.key== pygame.K_8:
                        if pre_key==42 or pre_key==54:
                            current_string.append("*")
                        else :current_string.append("8")
                        
                    elif inkey>=48 and inkey<=57:
                        current_string.append(chr(inkey))
                    elif inkey==pygame.K_KP0:
                        current_string.append('0')
                    elif inkey==pygame.K_KP1:
                        current_string.append('1')
                    elif inkey==pygame.K_KP2:
                        current_string.append('2')
                    elif inkey==pygame.K_KP3:
                        current_string.append('3')
                    elif inkey==pygame.K_KP4:
                        current_string.append('4')
                    elif inkey==pygame.K_KP5:
                        current_string.append('5')
                    elif inkey==pygame.K_KP6:
                        current_string.append('6')
                    elif inkey==pygame.K_KP7:
                        current_string.append('7')
                    elif inkey==pygame.K_KP8:
                        current_string.append('8')
                    elif inkey==pygame.K_KP9:
                        current_string.append('9')
                pre_key=e.scancode
            elif (role=='red' and mode=='ai' and ok==1):
                    #pygame.time.delay(2000)
                    ai()
                    last_moment=1
                    ok=0
                    
            elif e.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                print(x,y)
                if x in range(130,200) and y in range(666,720) :
                    ok=1
                elif x in range(ss+dd//2,ss+dd//2+xx) and y in range(h-20,h-20+yy) :
                    print('P2P模式')
                    mode = 'p2p'
                elif x in range(ss,ss+xx) and y in range(h+3,h+3+yy) :
                    print('网络模式')
                    #匹配玩家
                    clientSocket=socket(AF_INET,SOCK_STREAM)
                    clientSocket.connect((serverName,serverPort))
                    applying_ = apply_for_join_game(name)
                    send_msg_to(clientSocket,applying_)
                    print("已和下列玩家匹配：")
                    new_mes = receive_msg()
                    gameid =new_mes["game_id"]
                    gameside =new_mes["side"]
                    time = new_mes["think_time"]
                    total = new_mes["total_time"]
                    mode = 'net'
                    net_flag=gameside
                    if gameside ==0:
                            pygame.display.set_caption("you fisrt !")
                                
                elif x in range(ss+dd,ss+dd+xx) and y in range(h,h+yy) :
                    print('人机模式')
                    mode = 'ai'
                elif x in range(ss+dd*2,ss+dd*2+xx) and y in range(h,h+yy) :
                    print('悔棋')
                    game_end=False
                    if pre_chess!=None:
                        ii,jj=pre_space
                        i,j=pre_chess
                        flag[i][j]=flag[ii][jj]
                        flag[ii][jj]=-1
                        role_change()
                        pre_chess=None
                        pre_space=None
                        ans=[]
                elif x in range(ss+dd*3,ss+dd*3+xx) and y in range(h,h+yy) :
                    print('重新开始')
                    game_end=False
                    role='blue'
                    select_chess = None
                    selected=None
                    re_chess=None
                    flag=weight
                    break
                elif x in range(ss+dd*4,ss+dd*4+xx) and y in range(h,h+yy) or request == "stop":
                    print('算分叫停')
                    if mode=='net':
                            if net_flag == gameside:
                                    ms = {
                                        "type": 2,
                                        "msg": {
                                        "request": "stop",
                                        "game_id":gameid,
                                        "side": gameside } 
                                      }
                                    send_msg_to(clientSocket,ms)
                                                      
                    game_end=True
                    blue_sum=0
                    for i in range(11,15):
                        for j in range(4,11):
                            if flag[j][i]>0 and flag[j][i]<10:
                                blue_sum+=(weight[j][i]-10)*flag[j][i]
                                print(weight[j][i],flag[j][i])
                    red_sum=0
                    for i in range(0,4):
                        for j in range(4,11):
                            if flag[j][i]>9 :
                                red_sum+=weight[j][i]*(flag[j][i]-10)
                                print(weight[j][i],flag[j][i])
                    print(blue_sum)
                    print(red_sum)
                
                elif mode=='p2p' or (role=='blue' and mode=='ai'):
                    selected = is_chess_clicked(x,y)
                    if selected is not None:
                            print('本次点击点击到了棋子')
                            ans=[]
                            last_moment=0
                            print(selected)
                            select_chess=copy.deepcopy(selected)

                    elif select_chess != None:
                        selected=removable(x,y,select_chess)
                        if selected is not None:
                            print('本次点击点击到了可移动的空格')
                            print(selected)
                            i,j=selected
                            ii,jj=select_chess
                            flag[i][j]=copy.deepcopy(flag[ii][jj])
                            flag[ii][jj]=-1
                            pre_space=selected
                            pre_chess=select_chess
                            selected=None
                            select_chess = None
                            role_change()
                elif mode =='net':
                        if net_flag == 0:
                                selected = is_chess_clicked(x,y)
                                if selected is not None:
                                    print('本次点击点击到了棋子')
                                    ans=[]
                                    last_moment=0
                                    print(selected)
                                    select_chess=copy.deepcopy(selected)
                                elif select_chess != None:
                                        selected=removable(x,y,select_chess)
                                        if selected is not None:
                                            print('本次点击点击到了可移动的空格')
                                            print(selected)
                                            i,j=selected#选中空格的坐标
                                            ii,jj=select_chess#选中棋子的坐标
                                            flag[i][j]=copy.deepcopy(flag[ii][jj])
                                            flag[ii][jj]=-1
                                            pre_space=selected
                                            pre_chess=select_chess
                                            selected=None
                                            select_chess = None
                                            ms = {
                                                                "type": 1,
                                                                "msg":{
                                                                                "game_id":gameid,
                                                                                "side": gameside,
                                                                                "num":  flag[i][j],
                                                                         "src": {
                                                                                                "x": ii,
                                                                                                "y": jj
                                                                                                },
                                                                                "dst":{
                                                                                                "x": i,
                                                                                                "y": j
                                                                                         },
                                                                                  "exp": current_string
                                                                                }
                                                        }
                                            send_msg_to(clientSocket,ms)
                                            net_flag = 1
                                            role_change()
                        else:
                                new_mes=receive_msg()
                                i,j = new_mes["dst"]["x"],new_mes["dst"]["y"]
                                ii,jj = new_mes["src"]["x"],new_mes["src"]["y"]
                                #if new_mes["exp"] != null
                                flag[i][j]=copy.deepcopy(flag[ii][jj])
                                flag[ii][jj]=-1
                                pre_space= i,j
                                pre_chess=ii,jj
                                selected=None
                                select_chess = None
                                net_flag = 0
                                role_change()
                                            

            draw()
            pygame.display.flip()  # 更新全部显示
            
    quit()  # 退出pygame



#print(mes)

clientSocket.close() 
        
        
