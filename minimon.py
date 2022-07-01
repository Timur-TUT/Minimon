import random
import dice
import blackjack
import yubi_match
import rps
import numelon
import game_explanation
import ascii
from time import sleep

#初期数値設定
BOARD_SIZE = 5
ZANKI = 3

#ヌメロンの勝敗
LOSE = 0
WIN = 1

#表示用
RED = '\033[91m'
CYAN = '\033[36m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
END = '\033[0m'

#部屋の種類
START_ROOM = "S"
GOAL_ROOM = "G"
ENEMY_ROOM = f"{RED}E{END}"
PIT_ROOM = f"{CYAN}P{END}"
WARP_ROOM = f"{CYAN}W{END}"
TREASURE_ROOM = f"{YELLOW}T{END}"
NOTHING_ROOM = "N"

#部屋の状態
FOUND = 0
NOT_FOUND = 1

#POINT OF VIEW  (マップ表示モードの指定に使う)
PLAYER = 0
GOD = 1

#真ん中の3列
middle_rand = [ENEMY_ROOM]*4
middle_rand += [PIT_ROOM]*3
middle_rand += [WARP_ROOM]*2
middle_rand += [TREASURE_ROOM]*3
middle_rand += [NOTHING_ROOM]*3

#上下の2列
edge_rand = [ENEMY_ROOM]*2
edge_rand += [TREASURE_ROOM]*2
edge_rand += [NOTHING_ROOM]*4

#部屋クラス
class Room:
    def __init__(self, type, status):
        self.type = type        #部屋の種類
        self.status = status    #訪問済かどうか
        self.spec = None        #ワープやモンスタールームの番号付けに使用

#ゲームクラス
class Game:
    def __init__(self):
        self.game_flag = None
        self.map = self.generate_map()  #ゲームマップ
        self.det_specification()        #場合分け
        self.position = [0,0]           #プレイヤーの現在地
        self.zanki = ZANKI              #残機
        self.minigame_defeat = 0
        self.minigame_win = 0
        self.player_item = []
        self.boss_item = ["Double","Target","Shuffle","Change"]
        self.hint = ["「ボスはとっても強いんだってね。アイテムは早めに使った方がいいよ。」",
        "「一度倒したモンスター達は再び生き返ることはない。」",
        "「一度開けた宝箱は空になってしまう。当たり前だけどね。解錠を失敗しても二度と開かなくなるみたいだよ？」",
        "「モンスター達は全員で６体いるんだ。」",
        "「落とし穴は全部で３か所ある。落ちると残機が減るから注意しないとね。」",
        "NEXT", "NEXT"]

        #self.display_text(game_explanation.show())   #ゲーム説明
        self.start_room()
            
    #マップの初期化
    def generate_map(self):
        game_map = []
        for i in range(5):
            line = []
            for j in range(5):
                if (i,j) == (0,0):      #スタート部屋
                    line.append(Room(START_ROOM, FOUND))
                    continue
                elif (i,j) == (4,4):    #ゴール部屋
                    line.append(Room(GOAL_ROOM, FOUND))
                    continue

                if i == 0 or i == 4:    #上下、端の行
                    line.append(Room(edge_rand.pop(random.randint(0,len(edge_rand)-1)), NOT_FOUND))
                else:                   #真ん中の3行
                    line.append(Room(middle_rand.pop(random.randint(0,len(middle_rand)-1)), NOT_FOUND))

            game_map.append(line)
        
        return game_map

    #マップの表示
    def show_map(self, pov):
        for i,line in enumerate(self.map):
            output_row = ""
            for j,room in enumerate(line):
                if [i,j] == self.position:  #現在地には"●"を表示
                    output_row += "●" + "  "
                    continue
                if pov == PLAYER:   #表示モードが"PLAYER"なら
                    if room.status == NOT_FOUND:    #未訪問の部屋を隠す
                        output_row += "?" + "  "
                        continue
                output_row += room.type + "  "
            print(output_row)

    def display_text(self, text):
        for i in range(0, len(text)):
            print(text[i], end="")
            sleep(0.07)

    #ワープや敵の場合分け
    def det_specification(self):
        wr_destination = [(BOARD_SIZE-1,0), (0,BOARD_SIZE-1)]   #ワープ用の座標

        minigame_list = [dice, blackjack, yubi_match, rps]      #ミニゲームのモジュールリスト
        #ランダムに2つを追加
        while len(minigame_list) < 6:
            extra_game = random.choice(minigame_list)
            if extra_game != yubi_match and minigame_list.count(extra_game) == 1:
                minigame_list.append(extra_game)

        for line in self.map:
            for room in line:
                #マップの左上から順に
                if room.type == WARP_ROOM:
                    room.spec = wr_destination.pop(random.randint(0,len(wr_destination)-1))

                elif room.type == ENEMY_ROOM:
                    room.spec = minigame_list.pop(random.randint(0,len(minigame_list)-1))

                elif room.type == GOAL_ROOM:
                    room.spec = numelon

    #進む方向を入力するための関数
    def input_direction(self):
        x, y = self.position[1], self.position[0]
        output = "方向選択をしてください:"
        dir = "r"

        #進める方向を判定
        if 0 < y:
            dir += "w"
        if y < BOARD_SIZE-1:
            dir += "s"
        if 0 < x:
            dir += "a"
        if x < BOARD_SIZE-1:
            dir += "d"
            
        print(output+dir[1:])
        print("r を入力するとルールをもう一度表示します")
        
        input_txt = input()
        while len(input_txt) < 1:
            input_txt = input("入力してください")

        #進める方向が入力されるまで無限ループ
        while input_txt[0] not in dir:
            print(f"選べる方向は {dir[1:]} のみです")
            input_txt = input()

        print()
        self.move(input_txt[0])    #ループ抜けたら実際の移動を行う

    #実際の移動を行う関数
    def move(self, txt):
        if txt == "w":
            self.position[0] -= 1
        elif txt == "s":
            self.position[0] += 1
        elif txt == "a":
            self.position[1] -= 1
        elif txt == "d":
            self.position[1] += 1
        elif txt == "r":
            print(game_explanation.show(True))
            return
            
        self.check_event()

    #自分がいる部屋のイベントを確認する関数
    def check_event(self):
        current_room = self.map[self.position[0]][self.position[1]]
        if current_room.type == START_ROOM:
            self.start_room()

        elif current_room.type == GOAL_ROOM:
            self.goal_room()

        elif current_room.type == ENEMY_ROOM:
            if current_room.status == FOUND:
                print("このモンスターは既に倒されました")
            else:
                self.enemy_room()
                self.minigame_win += 1
                if self.minigame_win > 4:
                    print("残機ゲット")
                    self.zanki += 1

        elif current_room.type == PIT_ROOM:
            current_room.status = FOUND #訪問済にする
            self.pit_room()

        elif current_room.type == WARP_ROOM:
            current_room.status = FOUND #訪問済にする
            self.warp_room(current_room.spec)
            
        elif current_room.type == TREASURE_ROOM:
            if current_room.status == FOUND:
                print("この宝箱はもう回収出来ません")
            else:
                self.treasure_room()

        elif current_room.type == NOTHING_ROOM:
            if current_room.status == NOT_FOUND:
                self.nothing_room()
            else:
                print("何もありません")

        self.map[self.position[0]][self.position[1]].status = FOUND #訪問済にする

    #残機の表示
    def show_life(self):
        print("残機："+f"{RED}♥{END}"*self.zanki)

    #所持品の表示
    def show_load(self):
        if not self.player_item:
            print("所持品：なし")
        else:
            s = ""
            for i in self.player_item:
                if i != self.player_item[0]:
                    s += ","
                s += i
            print("所持品："+ s)

    #スタート
    def start_room(self):
        print("startの部屋です")
        
    #ゴール
    def goal_room(self):
        print(f"{RED}ボス{END}が出現しました")
        mini_game = self.map[self.position[0]][self.position[1]].spec
        self.game_flag = mini_game.run(self)
        if self.game_flag == LOSE:
            print("ゲームオーバー")
        elif self.game_flag == WIN:
            print("おめでとう！")
            print("脱出")
        
    #敵
    def enemy_room(self):        
        print(f"{RED}敵{END}です")
        print("-------------------------")
        mini_game = self.map[self.position[0]][self.position[1]].spec
        self.minigame_defeat = 0
        self = mini_game.run(self)
        
    #落とし穴
    def pit_room(self):
        print(f"{CYAN}落とし穴{END}に落ちました")
        print()
        sleep(1)
        self.zanki -= 1
        if self.zanki == 0:
            print("残機が0になりました\nゲームオーバー")
            return
        self.position = [0,0]
        self.check_event()

    #ワープ
    def warp_room(self, spec):
        print(f"{CYAN}ワープ{END}の部屋です")
        self.position = list(spec)
        print(f"{self.position}にワープしました")
        print()
        sleep(1)
        self.check_event()

    #宝箱
    def treasure_room(self):
        #数値や演算子の決定
        num1 = random.randint(1,30)
        num2 = random.randint(1,30)
        symbols = ["+", "-", "*", "/"]
        symbol = random.choice(symbols)
        correct_ans = 0

        #正解を計算
        if symbol == "+":
            correct_ans = num1 + num2
        elif symbol == "-":
            correct_ans = num1 - num2
        elif symbol == "*":
            correct_ans = num1 * num2
        elif symbol == "/":
            while num1 % num2 != 0: #割り切れる数字になるまで行う
                num1 = random.randint(2,30)
                num2 = random.randint(2,30)
            correct_ans = num1 / num2

        #出力
        print(f"{YELLOW}宝箱{END}があります")
        print("計算問題を解くと開けられます")
        print(f"{num1} {symbol} {num2} = ?")
        while True:
            try:
                player_ans = int(input())   #入力
                break
            except ValueError:
                print("数字を入力してください。")
        if player_ans == int(correct_ans):   #正解
            print("宝箱が開きました")
            print("残機ゲット")
            self.zanki += 1
        else:   #不正解
            print("宝箱は開きませんでした")

    #何も無い部屋
    def nothing_room(self):        
        ascii.run()
        result = self.hint.pop(random.randint(0,len(self.hint)-1))
        if result == "NEXT":
            self.next_room()
        else:
            self.display_text(result)

        print()

    def next_room(self):
        x, y = self.position[1], self.position[0]
        rooms = []

        #進める方向を判定
        if 0 < y:
            rooms.append([[self.map[y-1][x]],["上"]])
        if y < BOARD_SIZE-1:
            rooms.append([[self.map[y+1][x]],["下"]])
        if 0 < x:
            rooms.append([[self.map[y][x-1]],["左"]])
        if x < BOARD_SIZE-1:
            rooms.append([[self.map[y][x+1]],["右"]])

        while len(rooms) > 0:
            room = rooms.pop(random.randint(0,len(rooms)-1))
            if room[0][0].status == NOT_FOUND:
                break
        else:
            room = None

        if room:
            self.display_text(f"{room[1][0]}の部屋は{room[0][0].type}だよ")
        else:
            self.display_text(self.hint.pop(0))

    #ゲームのループ
    def main_loop(self):
        while True:
            self.show_life()
            self.show_load()
            #self.show_map(GOD)     #マップをすべて表示
            self.show_map(PLAYER)
            self.input_direction()
            if self.game_flag != None or self.zanki == 0:
                break
            print("-------------------------")

game = Game()
game.main_loop()
