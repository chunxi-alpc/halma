import pygame 
import sys
from math import *
import itertools
import copy
import random

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

mode_select_image = pygame.image.load("./image/mode_select.png").convert_alpha()
repent_image = pygame.image.load("./image/repent.png").convert_alpha()
restart_image =pygame.image.load("./image/restart.png").convert_alpha()
quit_image = pygame.image.load("./image/quit.png").convert_alpha()
#sound_background = pygame.mixer.Sound("./sound/background.wav")
sound_move = pygame.mixer.Sound("./sound/move.wav")
area= background.get_rect()  # 获取矩形区域



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
    global ft2_surf
    global ft1_surf
    global blue_sum
    global red_sum
    global ans
    global mode
    final_text2 = "Blue final score is:  " + str(blue_sum)
    final_text1 = "Red final score is:  " + str(red_sum)
    font = pygame.font.SysFont("Ink Free", 30)
    ft1_surf = font.render(final_text1, 1, (220, 20, 60))                                                 
    ft2_surf = font.render(final_text2, 1, (65,105,225))      
    screen.blit(background, area)

    if game_end:
        screen.blit(ft2_surf, (70,210))  
        screen.blit(ft1_surf, (520,210))

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
    print(ans)
    if num==[] or len(num)<1:
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
                    ans=dfs(num,[],flag[xx][yy])
                    print(ans)
                    if ans!=[]:
                        return i,j
                    
                    
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
            if num==[]:
                break
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
            print(i,j)
            num=[]
            ii=i+1
            jj=j+1
            if flag[ii][jj]>-1 and ii!=xx:
                for iii in range(ii,xx):
                    jjj=yy-xx+iii
                    if flag[iii][jjj]>-1:
                        num.append(flag[iii][jjj])
            if num==[]:
                break
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
    dxy=[(xx-1,yy-1),(xx-2,yy),(xx+1,yy-1),(xx-1,yy+1),(xx+2,yy),(xx+1,yy+1)]
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
    dxy=[(xx-1,yy-1),(xx-2,yy),(xx+1,yy-1),(xx-1,yy+1),(xx+2,yy),(xx+1,yy+1)]
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
        print(value) 
        #it为当前尝试移动棋子编号，红色棋子>9
        xx=cc[it][0]
        yy=cc[it][1]
        print(flag[xx][yy])
        q=[0,1,2,3]
        random.shuffle(q)
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
        value[it]=0

if __name__ == '__main__':
    draw()
    dd=160
    ss=28
    h=145
    xx=150
    yy=50
    while True:  # 死循环确保窗口一直显示
        for e in pygame.event.get():  # 遍历所有事件
            if e.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
                
            # 按Esc则退出游戏
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()
                    
            elif (role=='red' and mode=='ai'):
                    pygame.time.delay(2000)
                    ai()
                    
            elif e.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                print(x,y)
                if x in range(ss+dd//2,ss+dd//2+xx) and y in range(h-20,h-20+yy) :
                    print('P2P模式')
                    mode = 'p2p'
                elif x in range(ss,ss+xx) and y in range(h+3,h+3+yy) :
                    print('网络模式')
                    mode = 'net'
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
                elif x in range(ss+dd*3,ss+dd*3+xx) and y in range(h,h+yy) :
                    print('重新开始')
                    game_end=False
                    role='blue'
                    select_chess = None
                    selected=None
                    re_chess=None
                    flag=weight
                    break
                elif x in range(ss+dd*4,ss+dd*4+xx) and y in range(h,h+yy) :
                    print('算分叫停')
                    game_end=True
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
                elif mode=='p2p' or (role=='blue' and mode=='ai'):
                    selected = is_chess_clicked(x,y)
                    if selected is not None:
                            print('本次点击点击到了棋子')
                            ans=[]
                            print(selected)
                            select_chess=copy.deepcopy(selected)
                            selected=None
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
                

            draw()
            pygame.display.flip()  # 更新全部显示
            
    quit()  # 退出pygame

