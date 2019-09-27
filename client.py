# coding:utf-8
# client
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

# 网络设置
ip = '127.0.0.1'  # '192.168.43.204'
serverPort = 50005
serveraddr = ip, serverPort
clientIp = '127.0.0.1'  # '192.168.43.204'
clientPort = random.randint(100, 1000)
clientaddr = clientIp, clientPort
NameList = ['Lucy', 'John', 'Lexi', 'lily', 'Mike', 'Max', 'Alen', 'Jakson']
name = NameList[random.randint(0, len(NameList)-1)]
oppName = ''
if(sys.version[:1] == "3"):
    import queue as Queue
    from _thread import *
else:
    import Queue
    from thread import *


# 全局变量初始化
times = [0 for i in range(10)]
length_of_chess = 54  # 直径
time = -1  # 思考时间
total = -1  # 总时间
overtime_side = -1
stop_side = -1
gameid = None
gameside = -1
clientSocket = None
net_flag = -1
timeout_flag = -1
quit_flag = -1
stop_flag = -1
expression = ''
mode = 'p2p'
role = 'red'
num = []
input_flag = 0
current_string = []
ok = 0
blue_sum, red_sum = 0, 0
last_moment = 0
pre_space = None
pre_chess = None
pre_key = None
pygame.font.init()
ans = []
game_end = False
select_chess = None
selected = None
chess_pos = [[0]*15 for i in range(15)]
chess0 = [[] for i in range(8)]
dd = 65
h = 450
dx = sqrt(3)/2*dd
dy = dd*0.5
st = 5
for j in range(7):
    for i in range(7-j):
        chess0[j].append((st+i*dx, h-i*dy))
    st += dx
    h += dy
st = 400
h = 220
for i in range(8):
    chess0[i].append((st, h+i*dd))
st = 800
h = 450
for j in range(7):
    for i in range(6-j, -1, -1):
        chess0[7-j].append((st-i*dx, h+i*dy))
    st -= dx
    h -= dy
for i in range(8):
    for j in range(8):
        chess_pos[i+7-j][i+j] = chess0[i][j]

flag = [[-2, -2, -2, -2, -2, -2, -2, -1, -2, -2, -2, -2, -2, -2, -2],
        [-2, -2, -2, -2, -2, -2, -1, -2, -1, -2, -2, -2, -2, -2, -2],
        [-2, -2, -2, -2, -2, -1, -2, -1, -2, -1, -2, -2, -2, -2, -2],
        [-2, -2, -2, -2, -1, -2, -1, -2, -1, -2, -1, -2, -2, -2, -2],
        [-2, -2, -2, 4, -2, -1, -2, -1, -2, -1, -2, 11, -2, -2, -2],
        [-2, -2, 5, -2, -1, -2, -1, -2, -1, -2, -1, -2, 17, -2, -2],
        [-2, 9, -2, 2, -2, -1, -2, -1, -2, -1, -2, 13, -2, 18, -2],
        [0, -2, 6, -2, -1, -2, -1, -2, -1, -2, -1, -2, 16, -2, 10],
        [-2, 8, -2, 3, -2, -1, -2, -1, -2, -1, -2, 12, -2, 19, -2],
        [-2, -2, 7, -2, -1, -2, -1, -2, -1, -2, -1, -2, 15, -2, -2],
        [-2, -2, -2, 1, -2, -1, -2, -1, -2, -1, -2, 14, -2, -2, -2],
        [-2, -2, -2, -2, -1, -2, -1, -2, -1, -2, -1, -2, -2, -2, -2],
        [-2, -2, -2, -2, -2, -1, -2, -1, -2, -1, -2, -2, -2, -2, -2],
        [-2, -2, -2, -2, -2, -2, -1, -2, -1, -2, -2, -2, -2, -2, -2],
        [-2, -2, -2, -2, -2, -2, -2, -1, -2, -2, -2, -2, -2, -2, -2]]

weight = copy.deepcopy(flag)

b = []
r = []
pygame.init()
size = width, height = 860, 750  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
select_image = pygame.image.load("./image/select.png").convert_alpha()
background = pygame.image.load('./image/board.png')
for i in range(10):
    b.append(pygame.image.load('./image/蓝棋'+str(i)+'.png'))
for i in range(10):
    r.append(pygame.image.load('./image/红棋'+str(i)+'.png'))
blue_sign = pygame.image.load("./image/蓝棋.png").convert_alpha()
red_sign = pygame.image.load("./image/红棋.png").convert_alpha()
ok_sign = pygame.image.load("./image/ok.jpg").convert_alpha()  # 对勾，人机模式
mode_select_image = pygame.image.load(
    "./image/mode_select.png").convert_alpha()
repent_image = pygame.image.load("./image/repent.png").convert_alpha()  # 悔棋
restart_image = pygame.image.load(
    "./image/restart.png").convert_alpha()  # 重新开局
quit_image = pygame.image.load("./image/quit.png").convert_alpha()  # 叫停
#sound_background = pygame.mixer.Sound("./sound/background.wav")
sound_move = pygame.mixer.Sound("./sound/move.wav")
area = background.get_rect()  # 获取矩形区域


def display_box(message):  # 显示

    fontobject = pygame.font.SysFont("Ink Free", 25)
    screen.blit(fontobject.render('Input:  ', 1,
                                  (47, 79, 79)), (15, 620))  # 颜色，坐标
    fontobject = pygame.font.SysFont("Segoe Script", 30)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (25, 25, 112)), (20, 650))


def check():
    global current_string
    global num, expression
    num0 = []
    for i in current_string:
        if i >= '0' and i <= '9':
            num0.append(int(i))
    if len(num0) != len(num):
        return None
    if set(num0) != set(num):
        return None
    ans = "".join(current_string)  # 返回通过指定字符连接序列中元素后生成的新字符串
    bracket_should_be = '('
    for i in range(len(num)):
        if num[i] == '(' or num[i] == ')':
            if num[i] != bracket_should_be:
                return None
            elif bracket_should_be == '(':
                bracket_should_be = ')'
            else:
                bracket_should_be = '('
    if bracket_should_be != '(':
        return None
    op = ['+', '-', '/', '*']
    if ans[0] in op or ans[0] == ')' or ans[-1] in op or ans[-1] == '(':
        return None
    l = len(current_string)
    for i in range(l-1):
        if ans[i] in op and ans[i+1] in op:
            return None
    expression = ans
    ans = eval(ans)
    return ans


def role_change():
    global role
    if role == 'blue':
        role = 'red'
    else:
        role = 'blue'


def draw():
    global chess_pos, flag
    global select_chess
    global selected
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
    global expression
    global current_string
    global name
    global oppName, gameside
    global timeout_flag, quit_flag, stop_flag
    global net_flag
    global overtime_side, stop_side
    screen.blit(background, area)
    font = pygame.font.SysFont("Ink Free", 30)
    if mode == 'net':
        if gameside == 0:
            RedName = name
            BlueName = oppName
        else:
            RedName = oppName
            BlueName = name

        Red_surf = font.render(RedName, 1, (220, 20, 60))
        Blue_surf = font.render(BlueName, 1, (65, 105, 225))
        screen.blit(Blue_surf, (130, 270))
        screen.blit(Red_surf, (580, 270))
        if timeout_flag == 1:
            if overtime_side == gameside:
                pygame.display.set_caption("您已超时，游戏结束，你输了！")
            elif overtime_side != gameside:
                pygame.display.set_caption("对方超时，游戏结束，你赢了！")

        if stop_flag == 1:
            if stop_side == gameside:
                pygame.display.set_caption("您已点击算分叫停，游戏结束！")
            elif stop_side != gameside:
                pygame.display.set_caption("对方点击算分叫停，游戏结束！")

        elif net_flag == 0:
            if quit_flag == 1:
                pygame.display.set_caption("对方主动退出，你赢了!")
            elif input_flag == 0:
                pygame.display.set_caption("轮到您出棋!")
            else:
                pygame.display.set_caption("请直接输入式子，并按回车确认")

        elif net_flag == 1:
            if quit_flag == 1:
                pygame.display.set_caption("对方主动退出，你赢了!")
            else:
                pygame.display.set_caption("对方下棋中……")
    elif mode == 'ai':
        Red_surf = font.render('COMPUTER', 1, (220, 20, 60))
        Blue_surf = font.render('PLAYER', 1, (65, 105, 225))
        screen.blit(Blue_surf, (130, 270))
        screen.blit(Red_surf, (570, 270))

        if role == 'red':
            screen.blit(ok_sign, (130, 666))
            pygame.display.set_caption("点击 ‘勾’ ，就到电脑下棋了，玩家您就不能悔棋了哦！")
        else:
            pygame.display.set_caption("电脑下棋中……")
    else:
        Red_surf = font.render('PLAYER 1', 1, (220, 20, 60))
        Blue_surf = font.render('PLAYER 2', 1, (65, 105, 225))
        screen.blit(Blue_surf, (130, 270))
        screen.blit(Red_surf, (580, 270))

        pygame.display.set_caption("国际数棋")

    if (input_flag == 1 and (net_flag == 0 or mode != 'net')):
        display_box(''.join(current_string))
    elif expression != '':
        display_box(expression)
    if game_end:
        final_text2 = "blue final score is:  " + str(blue_sum)
        final_text1 = "red final score is:  " + str(red_sum)
        font = pygame.font.SysFont("Ink Free", 30)
        ft1_surf = font.render(final_text1, 1, (220, 20, 60))
        ft2_surf = font.render(final_text2, 1, (65, 105, 225))
        screen.blit(ft2_surf, (70, 210))
        screen.blit(ft1_surf, (520, 210))

    if pre_space != None:
        screen.blit(select_image, chess_pos[pre_space[0]][pre_space[1]])
    if pre_chess != None:
        screen.blit(select_image, chess_pos[pre_chess[0]][pre_chess[1]])
    if select_chess != None:
        screen.blit(select_image, chess_pos[select_chess[0]][select_chess[1]])

    # 棋子初始坐标
    dd = 160
    ss = 28
    h = 145
    screen.blit(blue_sign, (70, 260))
    screen.blit(red_sign, (730, 260))
    if role == 'blue':
        screen.blit(select_image, (70, 260))
    else:
        screen.blit(select_image, (730, 260))
    if mode == 'ai' and role==ai.other_man and input_flag==0:
        if ans != []:
            font = pygame.font.SysFont("Segoe Script", 40)
            hh = 555
            if role == 'red':
                for each in ans:
                    ft2_surf = font.render(each, 1, (65, 105, 225))
                    screen.blit(ft2_surf, (20, hh))
                    hh += 30
            else :
                for each in ans:
                    ft2_surf = font.render(each, 1, (220, 20, 60))
                    screen.blit(ft2_surf, (690, hh))
                    hh += 30

    if mode == 'p2p':
        screen.blit(mode_select_image, (ss+dd/2-15, h-20-8))
    elif mode == 'ai':
        screen.blit(mode_select_image, (ss+dd-20, h+20-8))
    else:
        screen.blit(mode_select_image, (ss-15, h+20-8))

    font = pygame.font.SysFont("Ink Free", 20)
    ft0 = font.render("Net Mode", 1, (0, 100, 0))
    screen.blit(ft0, (ss, h+20))
    ft0 = font.render("AI Mode", 1, (0, 100, 0))
    screen.blit(ft0, (ss+dd, h+20))
    ft0 = font.render("P2P Mode", 1, (0, 100, 0))
    screen.blit(ft0, (ss+dd/2, h-20))
    screen.blit(repent_image, (ss+dd*2, h))
    screen.blit(restart_image, (ss+dd*3, h))
    screen.blit(quit_image, (ss+dd*4, h+7))
    for i in range(15):
        for j in range(15):
            if flag[i][j] > -1:
                if flag[i][j] < 10:
                    screen.blit(b[flag[i][j]], chess_pos[i][j])
                else:
                    screen.blit(r[flag[i][j]-10], chess_pos[i][j])
# sound_background.play()


def dfs(num, ans, goal):
    if len(num) < 1:
        return []
    if len(num) == 1:
        if (goal == num[0] and role == 'blue') or (goal-10 == num[0] and role == 'red'):
            return ans
    size = len(num)
    ans0 = copy.deepcopy(ans)
    for num1 in range(size):
        for num2 in range(num1+1, size):
            next_num = copy.deepcopy(num)
            next_num.pop(num2)
            next_num.pop(num1)
            num0 = copy.deepcopy(next_num)
            tmp = num[num1]+num[num2]
            next_num.append(tmp)
            ans.append(str(num[num1])+'+'+str(num[num2])+'='+str(tmp))
            ret = dfs(next_num,  ans,  goal)
            if ret != []:
                return ret

            next_num = copy.deepcopy(num0)
            ans = copy.deepcopy(ans0)
            tmp = num[num1]-num[num2]
            next_num.append(tmp)
            ans.append(str(num[num1])+'-'+str(num[num2])+'='+str(tmp))
            ret = dfs(next_num,  ans,  goal)
            if ret != []:
                return ret

            next_num = copy.deepcopy(num0)
            ans = copy.deepcopy(ans0)
            tmp = num[num2]-num[num1]
            next_num.append(tmp)
            ans.append(str(num[num2])+'-'+str(num[num1])+'='+str(tmp))
            ret = dfs(next_num,  ans,  goal)
            if ret != []:
                return ret

            next_num = copy.deepcopy(num0)
            ans = copy.deepcopy(ans0)
            tmp = num[num1]*num[num2]
            next_num.append(tmp)
            ans.append(str(num[num1])+'*'+str(num[num2])+'='+str(tmp))
            ret = dfs(next_num,  ans,  goal)
            if ret != []:
                return ret

            if num[num2] != 0 and num[num1] % num[num2] == 0:
                next_num = copy.deepcopy(num0)
                ans = copy.deepcopy(ans0)
                tmp = num[num1]//num[num2]
                next_num.append(tmp)
                ans.append(str(num[num1])+'/'+str(num[num2])+'='+str(tmp))
                ret = dfs(next_num,  ans,  goal)
                if ret != []:
                    return ret

            if num[num1] != 0 and num[num2] % num[num1] == 0:
                next_num = copy.deepcopy(num0)
                ans = copy.deepcopy(ans0)
                tmp = num[num2]/num[num1]
                next_num.append(tmp)
                ans.append(str(num[num2])+'/'+str(num[num1])+'='+str(tmp))
                ret = dfs(next_num,  ans,  goal)
                if ret != []:
                    return ret
    return []


def is_chess_clicked(x, y):
    global length_of_chess
    d = length_of_chess
    global role
    global chess_pos
    global flag
    for i in range(15):
        for j in range(15):
            if flag[i][j] > -1:
                if (role == 'blue' and flag[i][j] < 10)or(role == 'red' and flag[i][j] > 9):
                    if x > chess_pos[i][j][0] and x < chess_pos[i][j][0]+d and y > chess_pos[i][j][1] and y < chess_pos[i][j][1]+d:
                        return i, j
    return None


def removable(x, y, select_chess):
    global chess_pos
    global selected
    global flag
    global role
    global ans
    global num
    global input_flag
    global length_of_chess
    d = length_of_chess
    # 被移动棋子的坐标
    xx, yy = select_chess
    # 移
    dxy = [(xx-1, yy-1), (xx-2, yy), (xx+1, yy-1),
           (xx-1, yy+1), (xx+2, yy), (xx+1, yy+1)]
    for xy in dxy:
        i = xy[0]
        j = xy[1]
        if i >= 0 and i <= 14 and j >= 0 and j <= 14:
            if flag[i][j] == -1:
                if x > chess_pos[i][j][0] and x < chess_pos[i][j][0]+d and y > chess_pos[i][j][1] and y < chess_pos[i][j][1]+d:
                    input_flag = 0
                    return i, j
    # 邻
    for xy in dxy:
        i = xy[0]
        j = xy[1]
        if i >= 0 and i <= 14 and j >= 0 and j <= 14:
            if flag[i][j] > -1:
                dx = i-xx
                dy = j-yy
                i = dx+i
                j = dy+j
                if i >= 0 and i <= 14 and j >= 0 and j <= 14:
                    if flag[i][j] == -1:
                        if x > chess_pos[i][j][0] and x < chess_pos[i][j][0]+d and y > chess_pos[i][j][1] and y < chess_pos[i][j][1]+d:
                            input_flag = 0
                            return i, j

    # 单跨
    for i in range(15):
        for j in range(15):
            if flag[i][j] == -1:
                if x > chess_pos[i][j][0] and x < chess_pos[i][j][0]+d and y > chess_pos[i][j][1] and y < chess_pos[i][j][1]+d:
                    # 选择到一个空格
                    num = []
                    # 左斜.
                    if i+j == xx+yy:
                        if i > xx:
                            ii = i-1
                            jj = j+1
                        else:
                            ii = i+1
                            jj = j-1
                        if flag[ii][jj] > -1:
                            for iii in range(min(i, xx), max(i, xx)+1):
                                for jjj in range(min(j, yy), max(j, yy)+1):
                                    if flag[iii][jjj] > -1 and iii+jjj == xx+yy:
                                        num.append(flag[iii][jjj])
                    # 右斜
                    elif i-j == xx-yy:
                        if i > xx:
                            ii = i-1
                            jj = j-1
                        else:
                            ii = i+1
                            jj = j+1
                        if flag[ii][jj] > -1:
                            for iii in range(min(i, xx), max(i, xx)+1):
                                for jjj in range(min(j, yy), max(j, yy)+1):
                                    if flag[iii][jjj] > -1 and iii-jjj == xx-yy:
                                        num.append(flag[iii][jjj])
                    # 竖直
                    elif j == yy:
                        if i > xx:
                            ii = i-2
                            jj = j
                        else:
                            ii = i+2
                            jj = j
                        if flag[ii][jj] > -1 and ii >= 0 and ii <= 14 and jj >= 0 and jj <= 14:
                            for iii in range(min(i, xx), max(i, xx)+1, 2):
                                if flag[iii][j] > -1:
                                    num.append(flag[iii][j])
                    else:
                        break
                    if num == []:
                        break
                    if mode == 'p2p' or (mode == 'ai' and role == 'blue') or mode == 'net':
                        input_flag = 1
                        selected = i, j
                    if flag[xx][yy] in num:
                        num.remove(flag[xx][yy])
                    # 确保空格旁边有棋子

                    num_len = len(num)
                    for each in range(num_len):
                        if num[each] > 9:
                            num[each] = num[each]-10

                    if mode == 'ai':
                        ans = dfs(num, [], flag[xx][yy])
                        if ans != []:
                            return i, j

    return None


class AI:
    def __init__(self, ai_man, other_man):
        self.ai_man = ai_man
        self.other_man = other_man
        self.maxdepth = 3
        self.act_step = 0
        self.best_move = None
        
    # 局面评估函数
    '''
        局面评估函数：红方-极大值，蓝方-极小值
            （30-红方每个棋子到每个蓝方对应位置的距离）*权值
            -（30-蓝方每个棋子到每个红方对应位置的距离）*权值
    '''

    def situation_vl(self):
        global flag
        global weight
        sit_value = 0
        for i in range(15):
            for j in range(15):
                if flag[i][j] > 9:
                    chess_v = flag[i][j]-10
                    if chess_v == 0:
                        chess_v = 1
                    v = 0
                    for x in range(4, 11):
                        for y in range(0, 4):
                            if weight[x][y] > 0:
                                v += weight[x][y]*(30-abs(i-x)-abs(j-y))
                    sit_value -= (v*chess_v)
                elif flag[i][j] >= 0:
                    chess_v = flag[i][j]
                    if chess_v == 0:
                        chess_v = 1
                    v = 0
                    for x in range(4, 11):
                        for y in range(11, 15):
                            if weight[x][y] > 0:
                                v += (weight[x][y]-10)*(30-abs(i-x)-abs(j-y))
                    sit_value += (v*chess_v)
        return sit_value
    # 生成player方所有走法,return ()

    def generate_exercise(self, player):
        global flag
        global chess_pos
        if player == 'red':
            limit = 10
        else:
            limit = 0
        nodes=[]
        for chess_x in range(15):
            for chess_y in range(15):
                if flag[chess_x][chess_y] >= limit and flag[chess_x][chess_y] < limit+10:
                    for x in range(15):
                        for y in range(15):
                            if flag[x][y] == -1:
                                node = removable(chess_pos[x][y][0]+20, chess_pos[x][y][1]+20, (chess_x, chess_y))
                                if node !=None:
                                    nodes.append(((chess_x,chess_y),node))
        return nodes

    # 极大极小搜索及Alpha—Beta剪枝函数
    def alphaBeta_search(self, depth, alpha, beta, player):
        global flag
        #print(depth, alpha, beta)
        if self.maxdepth == depth or terminal(flag):  # 到达搜索深度
            return self.situation_vl()  # 返回局面评估值
        nodes = self.generate_exercise(player)
        if player == 'blue':
            player = 'red' 
        else:
            player = 'blue'
        for node in nodes:
            chess,space=node
            chess_x,chess_y=chess
            space_x,space_y=space
            flag[space_x][space_y] = copy.deepcopy(flag[chess_x][chess_y])
            flag[chess_x][chess_y] = -1
            value = -self.alphaBeta_search(depth+1, -beta, -alpha, player)
            flag[chess_x][chess_y] = copy.deepcopy(flag[space_x][space_y])
            flag[space_x][space_y] = -1
            #print(value)
            if value >= beta:  
                return beta
            if value > alpha:  # val大于了下界alpha，修改alpha，这是一个PV节点
                if depth == 0:  # 第0层时，当出现了优于目前的alpha值则记录最佳走法
                    self.best_move = node
                alpha = value
        return alpha

def apply_for_join_game(name_):
    applying = {"type": 0,
                "msg": {
                    "name": name_
                }
                }
    return applying


def send_msg_to(client, msg):
    packet = json.dumps(msg)
    if (sys.version[:1] == "3"):
        packet = packet.encode('utf-8')
    #print(client.addr[0] + ":" + str(client.addr[1]) + "\t" + str(msg))
    # client.conn.send(packet)
    client.send(packet)


def receive_msg_1(new_mes):
    global mode
    global gameid
    global gameside
    global time
    global total
    global net_flag
    print("已和下列玩家匹配：", new_mes)
    gameid = new_mes['game_id']
    gameside = new_mes['side']
    time = new_mes['think_time']
    total = new_mes['total_time']
    net_flag = 0
    mode = 'net'
    net_flag = copy.deepcopy(gameside)


def receive_msg_2(new_mes):
    global flag
    global pre_space, pre_chess, selected, select_chess
    global net_flag
    global expression
    j, i = new_mes['dst']['x'], new_mes['dst']['y']
    jj, ii = new_mes['src']['x'], new_mes['src']['y']
    if new_mes["exp"] != "":
        expression = new_mes['exp']
    else:
        expression = ""
    flag[i][j] = copy.deepcopy(flag[ii][jj])
    flag[ii][jj] = -1
    pre_space = i, j
    pre_chess = ii, jj
    selected = None
    select_chess = None
    net_flag = 0
    role_change()


def receive_msg_3(new_mes):
    print("执行stop消息处理")
    global game_end
    global stop_flag, stop_side
    global blue_sum, red_sum
    stop_side = new_mes['side']
    game_end = True
    blue_sum = 0
    for i in range(11, 15):
        for j in range(4, 11):
            if flag[j][i] > 0 and flag[j][i] < 10:
                blue_sum += (weight[j][i]-10)*flag[j][i]

    red_sum = 0
    for i in range(0, 4):
        for j in range(4, 11):
            if flag[j][i] > 9:
                red_sum += weight[j][i]*(flag[j][i]-10)
    msg = {"type": 3, "side": gameside}
    send_msg_to(clientSocket, msg)
    stop_flag = 1
    print("执行完毕")


def receive_msg_4():
    print("执行quit消息处理")
    global quit_flag
    global clientSocket
    msg = {"type": 3, "side": gameside}
    quit_flag = 1
    send_msg_to(clientSocket, msg)
    print("执行完毕")


def receive_msg_5(new_mes):
    print("执行over_time消息处理")
    global clientSocket
    global overtime_side
    global timeout_flag
    overtime_side = new_mes['side']
    timeout_flag = 1
    msg = {"type": 3, "side": gameside}
    send_msg_to(clientSocket, msg)
    print("执行完毕")


def client_thread(conn, addr):
    global oppName
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("收到的初始消息为：", data)
        data = json.loads(data)
        print("解压后消息为：", data)
        if oppName == '' and 'counterpart_name' in data:
            oppName = data['counterpart_name']
        if not 'status'in data:
            receive_msg_2(data)
        elif data['status'] == 1:
            receive_msg_1(data)
        elif "exp" in data:
            receive_msg_2(data)
        elif data['status'] == 2 and data['request'] == "stop":
            receive_msg_3(data)
        elif data['status'] == 2 and data['request'] == "quit":
            receive_msg_4()
            break
        elif data['status'] == 3:
            receive_msg_5(data)
            break

    conn.close()


def key_Processing(e):
    global current_string
    global selected
    global select_chess
    global pre_key
    global input_flag
    global current_string
    global num
    global chess_pos
    global pre_space
    global pre_chess
    global flag
    global mode
    global gameid
    global gameside
    global clientSocket
    global expression
    global net_flag

    if e.key == pygame.K_ESCAPE:
        sys.exit()
    elif input_flag == 1:
        if e.key == pygame.K_BACKSPACE:
            current_string = current_string[0:-1]
        elif e.unicode == '\r':
            x, y = selected
            removable(x, y, select_chess)
            if len(num) < 2:
                return
            correct = check()
            ii, jj = select_chess
            if correct == None:
                print('Input Error!')
            elif correct != flag[ii][jj] % 10:
                print('Wrong! Please input again')
            else:
                fflag = 0
                d = length_of_chess
                for i in range(15):
                    for j in range(15):
                        if flag[i][j] == -1:
                            if x > chess_pos[i][j][0] and x < chess_pos[i][j][0]+d and y > chess_pos[i][j][1] and y < chess_pos[i][j][1]+d:
                                fflag = 1
                                x, y = i, j
                                break
                    if fflag == 1:
                        break
                print(x, y, ii, jj)
                if flag[ii][jj] > 9:
                    send_num = flag[ii][jj]-10
                else:
                    send_num = flag[ii][jj]
                flag[x][y] = copy.deepcopy(flag[ii][jj])
                flag[ii][jj] = -1
                pre_space = x, y
                pre_chess = ii, jj
                selected = None
                select_chess = None
                if mode == 'net':
                    ms = {"type": 1, "msg": {"game_id": gameid, "side": gameside,
                                             "num":  send_num, "src": {"x": jj, "y": ii},
                                             "dst": {"x": y, "y": x},
                                             "exp": expression}
                          }
                    send_msg_to(clientSocket, ms)
                    net_flag = 1
                role_change()
                current_string = []
                input_flag = 0

        elif e.key == pygame.K_KP_MINUS or e.key == pygame.K_MINUS:
            current_string.append("-")
        elif e.key == pygame.K_KP_PLUS or e.key == pygame.K_PLUS:
            current_string.append("+")
        elif e.key == pygame.K_KP_MULTIPLY or e.key == pygame.K_ASTERISK:
            current_string.append("*")
        elif e.key == pygame.K_KP_DIVIDE or e.key == pygame.K_SLASH:
            current_string.append("/")

        elif e.key == pygame.K_9:
            if pre_key == 42 or pre_key == 54:
                current_string.append("(")
            else:
                current_string.append("9")
        elif e.key == pygame.K_0:
            if pre_key == 42 or pre_key == 54:
                current_string.append(")")
            else:
                current_string.append("0")
        elif e.key == pygame.K_EQUALS:
            if pre_key == 42 or pre_key == 54:
                current_string.append("+")
        elif e.key == pygame.K_8:
            if pre_key == 42 or pre_key == 54:
                current_string.append("*")
            else:
                current_string.append("8")

        elif e.key >= 48 and e.key <= 57:
            current_string.append(chr(e.key))
        elif e.key == pygame.K_KP0:
            current_string.append('0')
        elif e.key == pygame.K_KP1:
            current_string.append('1')
        elif e.key == pygame.K_KP2:
            current_string.append('2')
        elif e.key == pygame.K_KP3:
            current_string.append('3')
        elif e.key == pygame.K_KP4:
            current_string.append('4')
        elif e.key == pygame.K_KP5:
            current_string.append('5')
        elif e.key == pygame.K_KP6:
            current_string.append('6')
        elif e.key == pygame.K_KP7:
            current_string.append('7')
        elif e.key == pygame.K_KP8:
            current_string.append('8')
        elif e.key == pygame.K_KP9:
            current_string.append('9')
    pre_key = e.scancode

def terminal(flag):
    blue_score_flag = 0
    red_score_flag = 0
    for i in range(0, 4):
        for j in range(4, 11):
            if flag[j][i] > 9:
                red_score_flag += 1
    for i in range(11, 15):
        for j in range(4, 11):
            if flag[j][i] > -1 and flag[j][i] < 10:
                blue_score_flag += 1
    # 如果有一方全部棋子都到位

    if red_score_flag == 10 or blue_score_flag == 10:
        return True
    else :
        return False


def Calculate_Point_And_Call_Of():
    global flag
    global net_flag
    global mode
    global gameid
    global gameside
    global clientSocket
    global game_end
    global blue_sum, red_sum
    global stop_flag, stop_side
    if terminal(flag):
        if mode == 'net':
            ms = {
                "type": 2,
                "msg": {
                    "request": "stop",
                    "game_id": gameid,
                    "side": gameside}
            }
            send_msg_to(clientSocket, ms)
        game_end = True
        stop_flag = 1
        stop_side = gameside
        blue_sum = 0
        for i in range(11, 15):
            for j in range(4, 11):
                if flag[j][i] > 0 and flag[j][i] < 10:
                    blue_sum += (weight[j][i]-10)*flag[j][i]

        red_sum = 0
        for i in range(0, 4):
            for j in range(4, 11):
                if flag[j][i] > 9:
                    red_sum += weight[j][i]*(flag[j][i]-10)
    else:
        game_end = False


if __name__ == '__main__':
    draw()
    dd = 160
    ss = 28
    h = 145
    xx = 150
    yy = 50
    pygame.display.flip()
    while True:
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                if mode == 'net':
                    ms = {
                        "type": 2,
                        "msg": {
                            "request": "quit",
                            "game_id": gameid,
                            "side": gameside}
                    }
                    send_msg_to(clientSocket, ms)
                    pygame.display.set_caption("主动退出，你输了!")
                sys.exit()
                pygame.quit()

            elif e.type == pygame.KEYDOWN:
                key_Processing(e)

            elif (role == 'red' and mode == 'ai' and ok == 1):
                # 模式切换，网络切换过来应该先退出，然后重新初始化
                ai.best_move = -1
                ai.alphaBeta_search(0,-100000,100000,role)
                chess,space=ai.best_move
                print(ai.best_move)
                ans = []
                chess_x,chess_y=chess
                space_x,space_y=space
                removable(chess_pos[space_x][space_y][0]+20, chess_pos[space_x][space_y][1]+20, chess)
                flag[space_x][space_y] = copy.deepcopy(flag[chess_x][chess_y])
                flag[chess_x][chess_y] = -1
                pre_space = copy.deepcopy(space)
                pre_chess = copy.deepcopy(chess)
                ok = 0
                role_change()
                

            elif e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if mode == 'ai' and x in range(130, 200) and y in range(666, 720):
                    # AI模式中勾选确认式子输入完毕
                    ok = 1
                elif x in range(ss+dd//2, ss+dd//2+xx) and y in range(h-20, h-20+yy):
                    print('P2P模式')
                    mode = 'p2p'
                elif x in range(ss, ss+xx) and y in range(h+3, h+3+yy):
                    print('网络模式')
                    # 匹配玩家
                    clientSocket = socket(AF_INET, SOCK_STREAM)
                    clientSocket.bind((clientaddr))
                    clientSocket.connect((serveraddr))
                    applying_ = apply_for_join_game(name)
                    send_msg_to(clientSocket, applying_)
                    start_new_thread(client_thread, (clientSocket, serveraddr))
                    #t = Thread(target=client_thread, args=(clientSocket,addr))
                    # t.start()
                    # t.join()
                elif x in range(ss+dd, ss+dd+xx) and y in range(h, h+yy):
                    print('ai模式')
                    mode = 'ai'
                    role = 'blue'
                    ai=AI('red',role)
                elif x in range(ss+dd*2, ss+dd*2+xx) and y in range(h, h+yy):
                    print('悔棋')
                    game_end = False
                    if pre_chess != None:
                        ii, jj = pre_space
                        i, j = pre_chess
                        flag[i][j] = flag[ii][jj]
                        flag[ii][jj] = -1
                        role_change()
                        pre_chess = None
                        pre_space = None
                        ans = []
                elif x in range(ss+dd*3, ss+dd*3+xx) and y in range(h, h+yy):
                    print('重新开始')
                    game_end = False
                    role = 'blue'
                    select_chess = None
                    selected = None
                    re_chess = None
                    flag = weight
                    break
                elif x in range(ss+dd*4, ss+dd*4+xx) and y in range(h, h+yy):
                    Calculate_Point_And_Call_Of()

                # 点击走棋
                elif mode == 'p2p' or (role == 'blue' and mode == 'ai') or (mode == 'net' and net_flag == 0):
                    # 未选择棋子，当前应该选择棋子
                    clicked = is_chess_clicked(x, y)
                    if clicked is not None:
                        print('本次点击点击到了棋子')
                        ans = []
                        show_exp_flag = 0
                        last_moment = 0
                        selected = copy.deepcopy(clicked)
                        select_chess = copy.deepcopy(clicked)
                    # 已经选择了棋子，当前应该选择可移动的位置，或者再次选择
                    elif select_chess != None:
                        clicked = removable(x, y, select_chess)
                        if clicked is not None and input_flag == 0:
                            print('本次点击点击到了可移动的空格')
                            i, j = clicked
                            ii, jj = select_chess
                            flag[i][j] = copy.deepcopy(flag[ii][jj])
                            flag[ii][jj] = -1
                            pre_space = copy.deepcopy(clicked)
                            pre_chess = copy.deepcopy(select_chess)
                            selected = None
                            select_chess = None
                            if flag[i][j] > 9:
                                send_num = flag[i][j]-10
                            else:
                                send_num = flag[i][j]
                            if mode == 'net':
                                ms = {
                                    "type": 1,
                                    "msg": {
                                        "game_id": gameid,
                                        "side": gameside,
                                        "num":  send_num,
                                        "src": {
                                            "x": jj,
                                            "y": ii
                                        },
                                        "dst": {
                                            "x": j,
                                            "y": i
                                        },
                                        "exp": expression
                                    }
                                }
                                send_msg_to(clientSocket, ms)
                                net_flag = 1
                            role_change()

                    #start_new_thread(client_thread, (clientSocket, addr))

            draw()
            pygame.display.flip()  # 更新全部显示
            if quit_flag == 1 or stop_flag == 1:
                sys.exit()
                pygame.quit()

    quit()  # 退出pygame
    #start_new_thread(draw_thread, ())

clientSocket.close()
