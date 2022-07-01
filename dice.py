import random

def run(game):
    explanation()
    play(game)

def play(game):
    while True:
        try:
            num1 = int(input("１つめの数字をセット："))
            num2 = int(input("２つめの数字をセット："))
            num3 = int(input("３つめの数字をセット："))
            for n in num1,num2,num3:
                if n < 1 or n > 6:
                    print("1～6の数字を入力してください\n")
                    break
            else:
                break
        except ValueError:
            print("数字で入力してください")

    player_list = [num1,num2,num3]
    saikoro = random.randint(1,6)

    print(f"サイコロ：{saikoro}")
    if saikoro in player_list:
        print("プレイヤー勝利")
        if game.boss_item:
            new_item = game.boss_item.pop(random.randint(0,len(game.boss_item)-1))
            game.player_item.append(new_item)
            print(f"アイテムをゲットしました：{new_item}")
        
        return game
    else:
        print("プレイヤー敗北")
        if game.minigame_defeat == 0:   #1回目だから、まだ機は減らない
            game.minigame_defeat += 1
            print("やり直し！")
            play(game)
        elif game.minigame_defeat == 1: #2回目の負け
            game.minigame_defeat = 0    #リセット
            game.zanki -= 1             #機を減らす
            if game.zanki == 0:
                print("残機が0になりました\nゲームオーバー")
                return game
            print("機が減った")
            game.show_life()
            play(game)                  #再度プレイ

def explanation():
    print("今からサイコロ当てゲームだ")
    print("1～6の数字を3つ選んでいいぞ")
    print("1つでも当たれば君の勝ちだ")