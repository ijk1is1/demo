### 2. Day 6作业 - 编写炸金花游戏程序
# 自己写一个程序，实现发牌、比大小判断输赢。
# #### 游戏规则：
# 一付扑克牌，去掉大小王，每个玩家发3张牌，最后比大小，看谁赢。
# 有以下几种牌：
# 豹子：三张一样的牌，如3张6.
# 顺金：又称同花顺，即3张同样花色的顺子， 如红桃 5、6、7
# 顺子：又称拖拉机，花色不同，但是顺子，如红桃5、方片6、黑桃7，组成的顺子
# 对子：2张牌一样
# 单张：单张最大的是A
# 这几种牌的大小顺序为， **豹子>顺金>顺子>对子>单张**
#
# #### 需程序实现的点：
#
# 1. 先生成一付完整的扑克牌
#
# 2. 给5个玩家随机发牌
#   random.choice() 然后remove掉。
# 3. 统一开牌，比大小，输出赢家是谁

# 思路   [不写思路简直难受，以后注意]
# 红桃 方片  黑桃 梅花 2—14 用列表
import random

# 生成一副扑克，没有大小王
def newpuke():
    """
    生成一副扑克，没有大小王
    :return: 一副扑克。
    """
    # 扑克牌
    puke = []
    # 扑克牌的花型
    puke_class = ['红桃', '方片', '黑桃', '梅花']
    # 扑克牌的面值
    puke_name = [i for i in range(2,11)]
    puke_name = puke_name + [i for i in 'JQKA']

    # 每种花型制作
    for i in range(0,4):
        # 每个牌面赋值
        for j in range(0,13):
            temp = str(puke_class[i])+str(puke_name[j])
            puke.append(temp)
    return puke



import faker
# alex = faker.Faker(locale="zh_CN") # en_US

# 去除大小王，发牌。返回第一次分牌的结果
def fapai(puke,player_list=['张三','李四','王五','赵六','刘七']):
    """
    去除大小王，发牌。
    :param puke: 扑克牌。
    :param player_list: 玩家列表。
    :return: 返回第一次分牌的结果
    """
    # 参照物，用来拿到扑克的位置，计算牌面值。
    cankao = newpuke()
    # 玩家列表
    # player_list = []

    # 发牌的结果
    result = {}
    # for i in range(0, len(player_list)):
    #     player_list.append('玩家：' + str(1 + i))

    for player in player_list:
        # 玩家发牌的结果，存储到列表里
        result[player] = []
        # 玩家拿到三张牌的面值,面值作为第一个元素
        puke_total_value = 0

        for i in range(0,3):
            # 随机发牌
            temp = random.choice(puke)
            # 玩家拿到牌
            result[player].append(temp)
            # 用作发牌的扑克删掉发完的牌
            puke.remove(temp)
            # 拿到发到的扑克牌的面值， 并插入
            puke_value = cankao.index(temp)%13 + 2
            result[player].append(puke_value)

            # 计算结果值
            puke_total_value += puke_value

            # 验证
            # debug 看面值是否计算正确。
            # print(puke_total_value)
            # 看是否真的删除掉发完的牌了
            # print(len(puke))
        result[player].append(puke_total_value)

    return result

# 判断牌的类型，计算牌值。 返回游戏结果。
def panduan(game):
    """
    判断牌的类型
    :param game:
    :return:  返回 玩家的牌型，牌的分。
    """
    # 判断牌类型，给出值
    # **豹子>顺金>顺子>对子>单张**
    # 1000  500 200  100  50  基础分
    # 同类型，比较牌面面值 加分。
    # 如果是面值相等，那牌就相等了。

    for player in game:
        # print(game[player])
        if game[player][1] == game[player][3] and game[player][1] == game[player][5]:
            # print('豹子')
            game[player].append('豹子')
            game[player][-2] += 1000
        elif game[player][1] == game[player][3] or game[player][1] == game[player][5] or game[player][3] == game[player][5]:
            # print('对子')
            game[player].append('对子')
            game[player][-2] += 100
        elif ((game[player][1] - game[player][3])**2 + (game[player][1] - game[player][5])**2) == 5:
            if game[player][0][0:2] == game[player][2][0:2] and game[player][0][0:2] == game[player][4][0:2] :
                # print('顺金')
                game[player].append('顺金')
                game[player][-2] += 500
            else:
                # print('顺子')
                game[player].append('顺子')
                game[player][-2] += 200
        else:
            # print('单张')
            game[player].append('单张')
            game[player][-2] += 50
    return game

# 对判断牌型后的结果，排序。返回排序后的结果
def rank(res):
    # 按比较后的牌面的值，降序排序
    tmplist = sorted(res.items(), key=lambda item:item[1][-2], reverse=True)
    result = {}
    for player in tmplist:
        result[player[0]] = []
        for puke in player[1]:
            result[player[0]].append(puke)
    return result

# 入口
def play(playerlist=[]):
    """
    :param playerlist:  列表类型，元素是字符串。是玩家。
    :return:  返回哪个玩家赢了。
    """
    # 展示一副新扑克
    anewpuke = newpuke()
    # 发牌。不传用户，则默认五个。
    # 校验用户数量
    if len(playerlist) > 17:
        print('请游戏参与人数在17人及以下！',end='')
        return
    elif len(playerlist) <= 1:
        print('请两个及以上用户参与游戏！',end='')
        print('以下是默认游戏结果，默认5人。')
        print('-------------------分割线------------------')
        result1 = fapai(anewpuke)
    else:
        result1 = fapai(anewpuke,player_list=playerlist)
    # 牌型，牌的面值判断
    result2 = panduan(result1)
    # 牌面值排序
    rank_result = rank(result2)
    # print(rank_result)

    # 玩家，和得分，牌型拿出来
    for player in rank_result.items():
        # 拿到第一个的值
        win_score = player[1][-2]
        break

    # print(win_score)
    winner = []
    print('炸金花游戏开始，大家拿到的牌分别是：')
    for player in rank_result.items():
        print(f'玩家：{player[0]}，Ta拿到的牌型是{player[1][-1]}，Ta的牌是{player[1][0], player[1][2], player[1][4]}，Ta的得分{player[1][-2]}')
        if player[1][-2] == win_score:
            winner.append(player[0])
            winner.append(player[1][-1])
            winner.append(player[1][0])
            winner.append(player[1][2])
            winner.append(player[1][4])
            winner.append(player[1][-2])
    print(f'获胜者是{winner[0]}，Ta拿到的牌型是{winner[1]}，Ta的牌是{winner[2],winner[3],winner[4]},Ta的得分{winner[5]}')

if __name__ == "__main__":

    # panduan 方法里设置。
    # **豹子>顺金>顺子>对子>单张**
    # 1000  500 200  100  50  基础分
    import time
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    print(time.strftime( ISOTIMEFORMAT, time.localtime()))


    # 示例，只操作206 行即可。
    # play()，传参，如小明和小红， ['小明','小红']，人数请控制在2人及以上，少于17人。
    play(['小明','小红'])
    # play()