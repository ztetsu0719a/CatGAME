
##モジュールの引用
import sys
import pygame
import random

##画像読み込み
icon_kappa = pygame.image.load('C:/Users/ztets/Pictures/Screenshots/スクリーンショット 2024-06-18 151208.png')
img_bg = pygame.image.load('C:/Users/ztets/Downloads/image0 (11).jpeg')
img_player = pygame.image.load('img_fuku.png')
img_water = pygame.image.load('C:/Users/ztets/Downloads/image2 (1).jpeg')
img_flour = pygame.image.load('C:/Users/ztets/Downloads/image1 (1).jpeg')
txt_gameover = pygame.image.load('txt_gameover.png')

##サウンド準備
voice_up = None
voice_down = None

##固定値

# ストップウォッチの時間 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
STOPWATCH_MAX = 60  # 60フレーム = 1秒

#ゲームのステップの定義
STEP_READY = 0
STEP_PLAY= 1
STEP_GAMEOVER = 2

#surfaceの定義
SURFACE_WIDTH = 920
SURFACE_HEIGHT = 630

img_bg = pygame.transform.scale(img_bg,(SURFACE_WIDTH,SURFACE_HEIGHT))

#アイテムの定義
ITEM_TYPE_NUM = 2
ITEM_WIDTH = 100
ITEM_HEIGHT = 100
ITEM_MAX = 30 #最大個数

img_water = pygame.transform.scale(img_water, (ITEM_WIDTH, ITEM_HEIGHT))
img_flour = pygame.transform.scale(img_flour, (ITEM_WIDTH, ITEM_HEIGHT))

#プレイヤーの定義
PLAYER_WIDTH = 320
PLAYER_HEIGHT = 340
PLAYER_Y = 540 #Y座標(画面の中央)

img_player = pygame.transform.scale(img_player, (PLAYER_WIDTH, PLAYER_HEIGHT))

#水分の設定
MOISTURE_MAX = 150

# ストップウォッチの時間 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
stopwatch_timer = 0

##初期値の設定
step = STEP_READY
timer = 0
px = SURFACE_WIDTH / 2 #px = player_x(プレイヤーのx座標)
#アイテムの状態
moisture = MOISTURE_MAX
item_hit = [False] * ITEM_MAX
item_x = [0] * ITEM_MAX
item_y = [0] * ITEM_MAX 
item_type = [''] * ITEM_MAX
item_num = 10
#反転フラグの設定
flg_turn = False
#最後に←が押されたとする
lust_key = pygame.K_LEFT

##プレイヤーの移動
def move_player(key) :
    global px,lust_key,flg_turn

    if key[pygame.K_LEFT] == 1 :
        px -= 20
        #一番左端
        if px < - 50 + int(PLAYER_WIDTH / 2) :
            px = - 50 + int(PLAYER_WIDTH / 2)
        if lust_key == pygame.K_RIGHT :
            flg_turn = True #左押した後に「→」押されたら右向きにする
            lust_key = pygame.K_LEFT #戻す

    elif key[pygame.K_RIGHT] :
        px += 20
        #一番右端
        if px > SURFACE_WIDTH + 50 - int(PLAYER_WIDTH / 2) :
            px = SURFACE_WIDTH + 50 - int(PLAYER_WIDTH / 2 )
        if lust_key == pygame.K_LEFT :
            flg_turn = True#右押した後に「←」押されたら左向きにする
            lust_key = pygame.K_RIGHT
            
##アイテムのタイムと初期座標の設定
def locate_item() :
    global item_y
    for i in range(ITEM_MAX) :#最大個数回繰り返す
        #アイテムの落ちる範囲
        item_x[i] = random.randint(50, (SURFACE_WIDTH) - 50 - int((ITEM_WIDTH) / 2))
        item_y[i] = random.randint(-500,0)
        #アイテムの種類が均一に落ちてくるようにする
        if i % ITEM_TYPE_NUM == 0 :
            item_type[i] = 'w'#水に変更
        else :
            item_type[i] = 'f'#粉

##アイテム落下と当たり判定
def move_item() :
    for i in range(item_num) :
        #落下速度
        item_y[i] += 6 + ( i / 5 )
        if item_y[i] > SURFACE_HEIGHT :
            item_hit[i] = False
            item_x[i] = random.randint(50,SURFACE_WIDTH - 50 - int(ITEM_WIDTH / 2))
            item_y[i] = random.randint(-500,0)

        #当たり判定
        if item_hit[i] == False :
            if is_hit(px,PLAYER_Y,item_x[i],item_y[i]) == True :
                item_hit[i] = True
                get_item(item_type[i])

##当たり判定
def is_hit(x1,y1,x2,y2) :
    #当たり
    if (abs(x1-x2) <= int(ITEM_WIDTH / 2) + int(PLAYER_WIDTH / 2) -110
        and abs(y1-y2) <= int(ITEM_HEIGHT / 2) + int(PLAYER_HEIGHT / 2) - 130):
        #当たったことを通知
        return True
    #当たらなかったことを通知
    return False

def get_item(category) :
    global moisture
    #水に当たったとき
    if category == 'w' :
        moisture += 10
        if moisture > MOISTURE_MAX :
            moisture = MOISTURE_MAX

    #粉に当たったとき
    elif category == 'f' :
        moisture -= 10
        if moisture < 0 :
            moisture = 0

##アイテムの描画
def show_item(surface) :
    for i in range(item_num) :
        #粉のとき
        if item_hit[i] == False and item_type[i] == 'w' :
            surface.blit(img_water,[item_x[i] - int(ITEM_WIDTH / 2),item_y[i] - int(ITEM_HEIGHT / 2)])
        #水のとき
        elif item_hit[i] == False and item_type[i] == 'f' :
            surface.blit(img_flour,[item_x[i] - int(ITEM_WIDTH / 2),item_y[i] - int(ITEM_HEIGHT / 2)])

##main関数
def main() :
    global step , timer , moisture , px , voice_up , voice_down
    global item_num , img_player , flg_turn
    global stopwatch_timer  # ストップウォッチの時間を追加 \\\\\\\\\\\\\\\\\\\

    #ウィンドウ作成
    pygame.init()
    #タイトル
    pygame.display.set_caption('ネコを守れ')
    #アイコン
    pygame.display.set_icon(icon_kappa)
    surface = pygame.display.set_mode((SURFACE_WIDTH,SURFACE_HEIGHT))
    clock = pygame.time.Clock()
    #サウンド


    while True :
        timer += 1

        #やめる
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

        #プレイステップへ
        if step == STEP_READY :
            stopwatch_timer = 0  # ストップウォッチの時間をリセット \\\\\\\\\\
            step = STEP_PLAY
            #水分をMAXに設定
            moisture = MOISTURE_MAX
            #プレイヤー位置
            px = int(SURFACE_WIDTH / 2)
            #アイテム数
            item_num = 10
            #アイテム配置
            locate_item()
 
        elif step == STEP_PLAY :
            #GAMEOVERの演出
            if moisture <= 0 :
                step = STEP_GAMEOVER
                timer = 0

            #アイテムがMAXではなく、時間が100で割り切れるとき
            if item_num != ITEM_MAX and timer % 100 == 0 :
                item_num += 5

            moisture -= 0.5
            move_player(pygame.key.get_pressed())
            move_item()

        #時間経過でゲームリセット
        elif step == STEP_GAMEOVER :
            if timer == 50 :
                step = STEP_READY
                timer = 0

        # ストップウォッチをカウントアップ
        if step == STEP_PLAY:  # プレイ中のみカウントアップ
            stopwatch_timer += 1

        #描画設定
        surface.blit(img_bg,[0,0])

        # 水分ゲージの文字を描画
        font_path = "C:/Windows/Fonts/arial.ttf"
        font = pygame.font.Font(font_path, 24)  # フォントとサイズを設定
        text = font.render("life", True, (255, 0, 0))  # テキストをレンダリング
        surface.blit(text, (50, 5))  # 画面上の適切な場所にテキストを描画

        # ストップウォッチの表示
        font = pygame.font.Font(None, 36)
        text = font.render("Time: " + str(stopwatch_timer // 10), True, (0, 0, 0))  # 黒色のストップウォッチを表示
        surface.blit(text, (400, 10))

        #逆を向いたら画像をひっくり返す
        if flg_turn == True :
            img_player = pygame.transform.flip(img_player,True,False)
            flg_turn = False

        #カッパの描画
        surface.blit(img_player,[px - int(PLAYER_WIDTH / 2),PLAYER_Y - int(PLAYER_HEIGHT / 2)])
        #アイテムの描画
        show_item(surface)
        #水分ゲージの下
        surface.fill((250,237,240),(50,30,MOISTURE_MAX,40))
        #水分ゲージの上
        surface.fill((236,37,90),(50,30,moisture,40))

        if step == STEP_GAMEOVER :
            sub_surface = pygame.Surface((SURFACE_WIDTH,SURFACE_HEIGHT),pygame.SRCALPHA)
            sub_surface.fill((0,0,0,100))
            surface.blit(sub_surface,[0,0])
            #GAMEOVER
            surface.blit(txt_gameover,[100,220])

        #画面更新
        pygame.display.update()
        clock.tick(20)

#実行
main()
