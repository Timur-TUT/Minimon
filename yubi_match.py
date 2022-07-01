import random

player1 = [1,1] # monster
player2 = [1,1] # player

#モンスターのAI
#自分が負ける場合のリストを作成、-2～4の評価をする
#0が一番良い評価(相手の指が0)
#-1が自分の負けリストにある場合
def monster(who,partner):
    my_lose_list = []
    for n in who:
        try:
            my_lose_list.append(5-n)
        except TypeError:
            None
    next_list = []
    for i in player1:
        for j in player2:
            if (type(i)==int) and (type(j)==int):
                next_num = (i+j)%5
                if next_num in my_lose_list:
                    next_list.append(-1)
                else:
                    next_list.append(next_num)
            else:
                next_list.append(-2)
    if 0 in next_list:
        return next_list.index(0)
    else:
        return next_list.index(max(next_list))

#入力をもとに表示
def Num(re):
    if re == 0:
        print("左を左")
        return "左","左"
    elif re == 1:
        print("左を右")
        return "左","右"
    elif re == 2:
        print("右を左")
        return "右","左"
    elif re == 3:
        print("右を右")
        return "右","右"
    
#選択肢の表示
def input_direction(who,partner):
    dir_l = []
    dir_s = ""
    if (type(who[0])==int) and (type(partner[0])==int):
        dir_s += "Playerの左をMonster左：0\n"
        dir_l.append(0)
    if (type(who[0])==int) and (type(partner[1])==int):
        dir_s += "Playerの左をMonster右：1\n"
        dir_l.append(1)
    if (type(who[1])==int) and (type(partner[0])==int):
        dir_s += "Playerの右をMonster左：2\n"
        dir_l.append(2)
    if (type(who[1])==int) and (type(partner[1])==int):
        dir_s += "Playerの右をMonster右：3\n"
        dir_l.append(3)
    return dir_l,dir_s

#指を足す関数
def addition(turn,who,partner):
    if turn == "Monster":
        me,you = Num(monster(who,partner))
    elif turn == "player":
        while True:            
            re = input("選択してください。\n"+input_direction(who,partner)[1])
            try:
                if int(re) in input_direction(who,partner)[0]:
                    break
            except ValueError:
                print("選択肢から選んでください")
        me,you = Num(int(re))
    if me == "右":
        hand = who[1]
    elif me == "左":
        hand = who[0]        
    if you == "右":
        partner[1] += hand
    elif you == "左":
        partner[0] += hand
    return you

#5を基準にした計算
def check(who,you):
    if you == "右":
        who[1] %= 5
        if who[1] == 0:
            who[1] = "×"
    if you == "左":
        who[0] %= 5
        if who[0] == 0:
            who[0] = "×"

#情報の表示   
def show(t,turn,who,partner):
    print("--------------------------")
    print(f"{t}:{turn}") 
    print(f"monster:右{partner[1]} 左{partner[0]}")
    print(f"player :左{who[0]} 右{who[1]}")
            
#メイン
def play(game):
    formatting()
    t = 0 #turn数
    draw_list = [["×",2,"×",4],["×",2,4,"×"],[2,"×","×",4],[2,"×",4,"×"]]
    while True:
        t += 1
        show(t,"player",player2,player1)  
        check(player1,addition("player",player2,player1))
        if player1 == ["×","×"]:    #勝ち
            print("You are Winner!")
            if game.boss_item:  #アイテムがあれば追加
                new_item = game.boss_item.pop(random.randint(0,len(game.boss_item)-1))
                game.player_item.append(new_item)
                print(f"アイテムをゲットしました：{new_item}")

            return game

        elif (player1+player2 in draw_list) or (t == 30):   #引き分け
            print("draw")
            print("もう一回！")
            formatting()
            play(game)
            break
        
        t += 1
        show(t,"Monster",player2,player1)     
        check(player2,addition("Monster",player1,player2))
        if player2 == ["×","×"]:    #負け
            print("You are Loser...")
            if game.minigame_defeat == 0:   #1回目だから、まだ機は減らない
                game.minigame_defeat += 1
                print("やり直し！")
                formatting()
                play(game)
                break
            elif game.minigame_defeat == 1: #2回目の負け
                game.minigame_defeat = 0    #リセット
                game.zanki -= 1             #機を減らす
                if game.zanki == 0:
                    print("残機が0になりました\nゲームオーバー")
                    return game
                print("機が減った")
                game.show_life()
                formatting()
                play(game)                  #再度プレイ
                break
        elif (player1+player2 in draw_list) or (t == 20):   #引き分け
            print("draw")
            print("もう一回！")
            formatting()
            play(game)
            break

def run(game):
    explanation(game)
    play(game)

def explanation(game):
    game.display_text("この部屋は指マッチの部屋です。(別名指スマ、棒倒し)\nこのゲームは２人で向き合って指をだし、相手の指の本数を増やすゲームです。\n最初はお互い両指１本ずつで始まり、指が５本ちょうどになったらその手は使えなくなり×の表記になります。\n５を超えた場合は超えた分の本数になります。\n自分の片手を選択し、相手の片手を選択して攻撃します。\n攻撃された手は攻撃してきた手の指の本数だけ+されます。\n相手の自分の手に攻撃したり、自分の手を分裂させたりすることはできません。\n先に相手の左右の指を×にした方が勝ちです。\n")

#初期化
def formatting():
    global player1, player2

    player1 = [1,1] # monster
    player2 = [1,1] # player