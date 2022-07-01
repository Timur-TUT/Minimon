import random
import copy

LOSE = 0
WIN = 1

rili = []
def rireki(who,a,b,c):
    lis = [who,a,b,c]
    if who == "player":
        rili.append([lis])
    else:
        rili[-1].append(lis)

def show_rireki(li):
    output = ""
    for i in li:
        for j in i:
            output += f"{j[0]}: {j[1][0]}{j[1][1]}{j[1][2]} eat={j[2]},bite={j[3]}          "
        output += "\n"
    return output

def number_check(number, a):
    # ルール説明
    if number == ["r"]:
        print(explanation())
        return False
    
    # 3桁の数字かチェック
    elif not len(number) == 3:
        print('3桁で入力してください')
        return False

    # 同じ数字が入力されていないかチェック
    elif not len(set(number)) == 3:
        print("数字の重複をなくしてください")
        return False
    try:
        # 最初に指定する自分の数字
        if a == -1:
            print(f"あなたの数字は{int(number[0])}{int(number[1])}{int(number[2])}です")
            return True
        # 相手にコール数字
        else:
            print(f"あなたの聞いた数字は{int(number[0])}{int(number[1])}{int(number[2])}です")
            return True
    except ValueError:
        print("数字ではありません。")
        
def main(partner, a, count):
    #partner:プレイヤー、モンスターの数字
    #a:プレイヤーを0,モンスターを1に指定
    #count:ターン数
    while True:
        if a == 1:
            #print(count)
            count+=1
            # 0~9までの数字を生成
            number = list(str(i) for i in range(10))
            p = []
            # p:プレイヤーが指定した数字
            # number:プレイヤーが指定した数字以外の0~9の数字
            for n in partner:
                if n in number:
                    number.remove(n)
                    p.append(n)
                    
            # 3ターン以内の場合numberから2個、pから1個選択する
            if count <= 3:
                number1 = random.choice(number)
                number.remove(number1)
                #print(p, number)
                num = [number1, random.choice(p), random.choice(number)]
                random.shuffle(num)
                
            # 4,5ターンの場合numberから1個、pから1個選択する
            elif count <=5:
                number1 = random.choice(p)
                p.remove(number1)
                num = [number1, random.choice(p), random.choice(number)]
                random.shuffle(num)    
                
            # 6ターンでpから3個選択する
            elif count == 6:
                num = partner
            print(f"モンスターの聞いた数字は{int(num[0])}{int(num[1])}{int(num[2])}です")
            break
        else:
            num = list(input("モンスターの数字だと思うものを３桁で入力してください：（rを押すともう一度ルールを見ることができます）"))
            if number_check(num, 0) == True:
                break
                
    #eat,biteの計算
    eat = 0
    bite = 0
    if num[0] in partner:
        if num[0] == partner[0]:
            eat += 1
        else:
            bite += 1
    if num[1] in partner:
        if num[1] == partner[1]:
            eat += 1
        else:
            bite += 1
    if num[2] in partner:
        if num[2] == partner[2]:
            eat += 1
        else:
            bite += 1
    print(f"eat={eat},bite={bite}")
    if a == 0:
        rireki("player",num,eat,bite)
    else:
        rireki("monster",num,eat,bite)
    print(show_rireki(rili))
    return eat, count

def items(turn,who,partner,li, count):
    print(f"{turn}の番です")
    # アイテムを持ってない場合出力
    if not li:
        return None, count
    else:
        s = ""
        for i in li:
            if i != li[0]:
                s += "/"
            s += i
        if turn == "monster":
            return None
        
        while True:
            item = input(f"アイテムを使いますか？{s}/No:")
            item = item.lower()

            if item == "double":
                return Double(turn,partner, count,li)
            elif item == "target":
                return Target(partner, count, li)
            elif item == "shuffle":
                count -= 2
                return Shuffle(who, count, li)
            elif item == "change":
                count -= 2
                return Change(who, count, li)
            elif item == "no":
                print("アイテムを使用しません")
                return None,count
            else:
                print("指定のWordを入力してください")
        
def Double(turn,partner, count, li):
    li.remove("Double")
    a = main(partner, 0, count)
    if a == 3:
        return a, count
    return None, count
    
def Target(partner, count,li):
    num = input("数字を１つ入力してください:")
    if num in partner:
        if partner.index(num) == 0:
            print("100の位にあります")
        elif partner.index(num) == 1:
            print("10の位にあります")
        elif partner.index(num) == 2:
            print("1の位にあります")
    else:
        print("ありません")
    li.remove("Target")
    return None, count
        
def Shuffle(who, count,li):
    print("数字をシャッフルします。")
    random.shuffle(who)
    print(f"あなたの数字は{who[0]}{who[1]}{who[2]}です")
    li.remove("Shuffle")
    return who, count
    
def Change(who, count, li):
    while True:
        try:
            rank,num = input("どの桁をどの数字に変えますか？\n例）100の位を3に変更する場合：100-3").split("-")
            break
        except ValueError:
            print("正しく入力してください")
    if int(rank) == 100:
        while True:
            if (who[0]!=num) and (who[1]!=num) and (who[2]!=num):
                who[0] = num
                break
    elif int(rank) == 10:
        while True:
            if (who[0]!=num) and (who[1]!=num) and (who[2]!=num):
                who[1] = num
                break
    elif int(rank) == 1:
        while True:
            if (who[0]!=num) and (who[1]!=num) and (who[2]!=num):
                who[2] = num
                break
    print(f"あなたの数字は{who[0]}{who[1]}{who[2]}です")
    li.remove("Change")
    return who, count
    
def mos():
    ns = []
    while len(ns) < 3:
        n = str(random.randint(0, 9))
        if not n in ns:
            ns.append(n)
    return ns

def before_game():
    print('ヌメロンというゲームを始めます。\nルール説明は必要ですか？y or n')
    answer = input()
    if answer  == "y":
        return explanation()
    elif answer == "n":
        return ""
    else:
        print("yかnのみです")
        before_game()
    
def explanation():
    return """\nゲーム説明！
各プレイヤーは、0～9までの数字の中から3つ使って、3桁の番号を作成します。
0から始めても良いですが､｢550｣｢377｣といった同じ数字を2つ以上使用出来ません。
プレイヤーは、自身のターン時に相手が選んだと思われる３桁の番号を選択します。
数字と桁が合っていた場合は｢eat｣、数字は合っているが桁は合っていない場合は｢bite｣となります｡
[例]相手の番号が｢765｣で、自分が予測して入力した番号が｢746｣であった場合、｢7｣は数字と桁の位置が
合致しているためEAT。｢6｣は数字自体は合っているが桁の位置が違うためBITE。EATが1つ・BITEが1つなので､
結果は｢1EAT-1BITE｣となります｡先に3EATになったプレイヤーの勝利です！

アイテム説明!
・攻撃アイテム
<<Double>>続けて2度質問することができる
<<Target>>0～9の数字のうち1つを宣言し、その数字が相手の3桁に含まれているか知ることができる。
含まれている場合はその桁数まで知ることができる。
・防御アイテム
<<Shuffle>>自分の3桁をシャッフルすることができる。
<<Change>>Changeを宣言することで自分の3桁のうち1つを別の数字に変更することができる。
それではゲームスタート！！\n"""
    
def run(game):
    game.display_text(before_game())
    monster_number = mos()
    #print("ボスの数字（本来は出力しない）",monster_number,)
    Item_List = copy.copy(game.player_item)
    while True:
        player_number = list(input("あなたの数字を３桁で入力してください:"))
        if number_check(player_number, -1) == True:
            break
    count = 0
    while True:
        print("----------")
        a, count = items("player",player_number,monster_number,Item_List, count)
        if a == None:
            p, count = main(monster_number, 0, count)
        else:
            player_number = a
            p, count = main(monster_number, 0, count)
        if p == 3:
            print("You are win!")
            return WIN
        print("----------")
        print(f"monsterの番です")
        m, count = main(player_number, 1, count)
        if m == 3:
            print("You are lose...")
            return LOSE