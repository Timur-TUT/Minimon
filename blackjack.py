import random
from time import sleep
import copy

#手番
player = 0
enemy = 1

#山札
deck_list = []

#プレイヤーの手札
player_num_list = []

#敵の手札
enemy_num_list = []

def run(game):
    explanation(game)
    play(game)

def play(game):
    initialize()
    deal_cards()
    display_info()
    turn = player
    player_demand = ""
    enemy_demand = ""
    num_turn = 1
    while True:
        if turn == player:
            print("-------------------------")
            sleep(1)
            print(f"{num_turn}ターン目")
            if player_demand == "n":
                turn = enemy
                continue
            elif sum(player_num_list) < 21:
                player_demand = input("プレイヤー、カードを引きますか？　引く→「y」を入力　引かない→「n」を入力\n")
                if player_demand == "y":
                    y = deck_list.pop(random.randint(0, len(deck_list)-1))
                    player_num_list.append(y)
                    turn = enemy
                elif player_demand == "n" and enemy_demand == "n":
                    print()
                    break
                elif player_demand == "n":
                    turn = enemy
                else:
                    continue
            else:
                player_demand = "n"
                turn = enemy
        elif turn == enemy:
            num_turn += 1
            enemy_demand = ai_enemy()
            print(f"敵 : {enemy_demand}")
            if enemy_demand == "y":
                y = deck_list.pop(random.randint(0, len(deck_list)-1))
                enemy_num_list.append(y)
                display_info()
                turn = player
            elif player_demand == "n" and enemy_demand == "n":
                print()
                break
            elif enemy_demand == "n":
                display_info()
                turn = player
            else:
                continue

    display_all_info()
    display_result(game)

#始めの2枚を配る
def deal_cards():
    global deck_list, player_num_list, enemy_num_list
    for i in range(2):
        num = deck_list.pop(random.randint(0, len(deck_list)-1))
        player_num_list.append(num)
        num = deck_list.pop(random.randint(0, len(deck_list)-1))
        enemy_num_list.append(num)

def display_info():
    global deck_list, player_num_list, enemy_num_list
    sleep(1)
    print("-------------------------")
    deck_list_copy = copy.deepcopy(deck_list)
    deck_list_copy.append(enemy_num_list[-1])
    deck_list_copy = sorted(deck_list_copy)
    print(f"山札：{deck_list_copy}")
    print(f"プレイヤーの手札：{player_num_list}\nプレイヤーの合計：{sum(player_num_list)}")
    display_enemy_num_list = copy.deepcopy(enemy_num_list[:-1])
    display_enemy_num_list.append("?")
    print(f"敵の手札：{display_enemy_num_list}\n敵の合計：{sum(display_enemy_num_list[:-1])}以上")
    sleep(1)
    print()
        
def display_all_info():
    global deck_list, player_num_list, enemy_num_list
    print("-------------------------")
    print("結果発表")
    sleep(1)
    print(f"山札：{deck_list}")
    sleep(1)
    print(f"プレイヤーの手札：{player_num_list}\nプレイヤーの合計：{sum(player_num_list)}")
    sleep(1)
    print(f"敵の手札：{enemy_num_list}\n敵の合計：{sum(enemy_num_list)}")
    print()

def display_result(game):
    global player_num_list, enemy_num_list

    player = sum(player_num_list)
    enemy = sum(enemy_num_list)
    if (player > 21 and enemy > 21) or player == enemy:
        print("引き分けです。")
        print("もう一回！")
        play(game)
    elif player > 21 or (enemy < 22 and enemy > player):
        print("敵の勝ちです。")
        if game.minigame_defeat == 0:   #1回目だから、まだ機は減らない
            game.minigame_defeat += 1
            print("やり直し！")
            play(game)
        elif game.minigame_defeat == 1: #2回目の負け
            game.minigame_defeat = 0    #リセット
            game.zanki -= 1             #機を減らす
            print("機が減った " + "♥"*game.zanki)
            if game.zanki == 0:
                return game
            else:
                play(game)                  #再度プレイ
    elif (enemy > 21) or (player > enemy):
        print("プレイヤーの勝ちです")
        if game.boss_item:  #アイテムがあれば追加
            new_item = game.boss_item.pop(random.randint(0,len(game.boss_item)-1))
            game.player_item.append(new_item)
            print(f"アイテムをゲットしました：{new_item}")
            sleep(1)
        
def ai_enemy():
    global enemy_num_list
    if sum(enemy_num_list) < 20:
        return "y"
    else:
        return "n"
    
def explanation(game):
    text = "ブラックジャックだよ～ん\n手札の数字の合計が21に近いほうが勝ちだよ♪\nただし、21を超えたら負けなんですよね～\nちなみに数字は1～10が1つずつしかないよｗ\n数字の1を11にすることはできないのん♪\n表示される敵の手札は、敵が数字を引く度に増えていくよ！！\nLet’s Play! Good Luck Have Fun!\n"
    game.display_text(text)

def initialize():
    global deck_list, player_num_list, enemy_num_list

    deck_list = [i for i in range(1, 10+1)]
    player_num_list = []
    enemy_num_list = []