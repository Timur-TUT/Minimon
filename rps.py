import random

#実行関数
def run(game):
    explanation()
    play(game)

#ゲームを行う関数
def play(game):
    print()
    hands = ["グー", "チョキ", "パー"]
    judge = ["あいこ", "負け", "勝ち"]

    my_hand = random.randint(0,2)
    while True:
        try:
            player_hand = int(input("じゃんけん・・・")) - 1
            if player_hand not in [0,1,2]:
                print("指定の数字から選んでください")
                continue
            break
        except ValueError:
            print("指定の選択肢から入力してください")

    print(f'あなた：{hands[player_hand]}　敵：{hands[my_hand]}')

    # 勝敗判定
    i = (player_hand - my_hand + 3) % 3
    print(judge[i])

    if i == 0:  #引き分け
        print("もう一回！")
        play(game)
    elif i == 1:  #負け
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
    elif i == 2:  #勝利
        if game.boss_item:  #アイテムがあれば追加
            new_item = game.boss_item.pop(random.randint(0,len(game.boss_item)-1))
            game.player_item.append(new_item)
            print(f"アイテムをゲットしました：{new_item}")
        
        return game

#説明用の関数
def explanation():
    print("今からじゃんけんだ")
    print("勝てばモンスターを倒すことが出来るぞ")
    print(f'1:グー　2:チョキ　3:パー')