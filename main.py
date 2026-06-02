import js
import random

win_w = js.window.innerWidth
win_h = js.window.innerHeight

# Canvas取得
canvas = js.document.querySelector("#canvas")
context = canvas.getContext("2d")

# 画像
def load_img(src):
	img = js.Image.new()
	img.src = src
	return img

img_niku = load_img("./assets/neko_niku.png")
img_cursor = load_img("./assets/neko_cursor.png")
img_bg = load_img("./assets/neko_bg.png")

img_neko = [None]
for i in range(1, 7):
	img = load_img(f"./assets/neko{i}.png")
	img_neko.append(img)

img_neko.append(load_img("./assets/neko_niku.png"))

# サイズ定義
COL = 8
ROW = 10
TILE_SIZE = min((win_w-30)//(COL+3), (win_h-30)//ROW)
UI_width = int(TILE_SIZE * 3)

# Canvasサイズ変更
canvas.width = TILE_SIZE * COL + UI_width
canvas.height = TILE_SIZE * ROW

# UI領域の始点
UI_x = COL*TILE_SIZE

# マウス変数
cursor_x = 0
cursor_y = 0
mouse_x = 0
mouse_y = 0
mouse_c = 0

# game_over変数
game_over = False

# スコア変数
score = 0
combo = 0
high_score = 0

index = 0
timer = 0
difficulty = 0
tsugi = 0

# 配列
neko = []
check = []
for y in range(ROW):
	row = []
	for x in range(COL):
		row.append(0)
	neko.append(row)
	check.append(row)

# 入力
def mouse_move(e):
	global mouse_x, mouse_y
	rect = canvas.getBoundingClientRect()
	mouse_x = int(e.clientX - rect.left)
	mouse_y = int(e.clientY - rect.top)

def mouse_press(e):
	global mouse_c
	mouse_c = 1

canvas.addEventListener("mousemove", mouse_move)
canvas.addEventListener("mousedown", mouse_press)

# 描画
def draw_neko():
	for y in range(ROW):
		for x in range(COL):
			if neko[y][x] > 0:
				context.drawImage(img_neko[neko[y][x]],
					  				x*TILE_SIZE, y*TILE_SIZE,
									TILE_SIZE, TILE_SIZE)

def draw_txt(txt, x, y, siz, col, tg):
	context.fillStyle = "black"
	context.font = f"bold {siz}px serif"
	context.fillText(txt, x+1, y+1)

	context.fillStyle = col
	context.fillText(txt, x, y)

# 判定
def check_neko():
	mark = []
	for y in range(ROW):
		row = []
		for x in range(COL):
			check[y][x] = neko[y][x]
			row.append(False)
		mark.append(row)
	
	# 縦3つチェック
	for y in range(1, ROW-1):
		for x in range(COL):
			n = check[y][x]
			if n > 0:
				if check[y-1][x] == n and check[y+1][x] == n:
					mark[y-1][x] = True
					mark[y][x] = True
					mark[y+1][x] = True
	
	# 横3つチェック
	for y in range(ROW):
		for x in range(1, COL-1):
			n = check[y][x]
			if n > 0:
				if check[y][x-1] == n and check[y][x+1] == n:
					mark[y][x-1] = True
					mark[y][x] = True
					mark[y][x+1] = True
	
	# 斜め3つチェック
	for y in range(1, ROW-1):
		for x in range(1, COL-1):
			n = check[y][x]
			if n > 0:
				# 左上、右下が同じ
				if check[y-1][x-1] == n and check[y+1][x+1] == n:
					mark[y-1][x-1] = True
					mark[y][x] = True
					mark[y+1][x+1] = True
				# 左下、右上が同じ
				if check[y+1][x-1] == n and check[y-1][x+1] == n:
					mark[y+1][x-1] = True
					mark[y][x] = True
					mark[y-1][x+1] = True
	
	for y in range(ROW):
		for x in range(COL):
			if mark[y][x]:
				neko[y][x] = 7

def sweep_neko():
	num = 0
	for y in range(ROW):
		for x in range(COL):
			# 揃ったネコを
			if neko[y][x] == 7:
				neko[y][x] = 0
				num += 1
	return num

def drop_neko():
	flg = False
	for y in range(ROW-2, -1, -1):
		for x in range(COL):
			if neko[y][x] != 0 and neko[y+1][x] == 0:
				neko[y+1][x] = neko[y][x]
				neko[y][x] = 0
				flg = True
	return flg

def over_neko():
	for x in range(COL):
		if neko[0][x] > 0:
			return True
	return False

def set_neko():
	for x in range(COL):
		neko[0][x] = random.randint(0, difficulty)

# メインループ
def game_main():
	global index, timer, score, high_score, difficulty, tsugi
	global cursor_x, cursor_y, mouse_c

	context.clearRect(0, 0, COL*TILE_SIZE, ROW*TILE_SIZE)
	# 背景描画
	context.fillStyle = "lightgray"
	context.fillRect(0, 0, canvas.width, canvas.height)
	for y in range(ROW):
		for x in range(COL):
			if (x+y)%2 == 0:
				context.fillStyle = "pink"
			else:
				context.fillStyle = "mistyrose"
			
			context.fillRect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE-1, TILE_SIZE-1)
	
	# ネコ描画
	draw_neko()

	if index == 0 or index == 1:
		draw_txt("Neko_Puzzle", TILE_SIZE, TILE_SIZE*3, TILE_SIZE, "violet", "TITLE")
		draw_txt("Easy", TILE_SIZE, TILE_SIZE*5, TILE_SIZE, "white", "TITLE")
		draw_txt("Normal", TILE_SIZE, TILE_SIZE*7, TILE_SIZE, "white", "TITLE")
		draw_txt("Hard", TILE_SIZE, TILE_SIZE*9, TILE_SIZE, "white", "TITLE")
		index = 1

		if mouse_c == 1:
			mouse_c = 0
			if TILE_SIZE*4 < mouse_y < TILE_SIZE*5:
				difficulty = 4
			if TILE_SIZE*6 < mouse_y < TILE_SIZE*7:
				difficulty = 5
			if TILE_SIZE*8 < mouse_y < TILE_SIZE*9:
				difficulty = 6
		
		if difficulty > 0:
			for y in range(ROW):
				for x in range(COL):
					neko[y][x] = 0
			mouse_c = 0
			score = 0
			tsugi = 0
			set_neko()
			index = 2
	
	elif index == 2:
		if not drop_neko():
			index = 3
	
	elif index == 3:
		check_neko()
		index = 4
	
	elif index == 4:
		sc = sweep_neko()
		score += sc * difficulty * 2
		if score > high_score:
			high_score = score
		
		if sc > 0:
			index = 2
		else:
			if not over_neko():
				tsugi = random.randint(1, difficulty)
				index = 5
			else:
				index = 6
				timer = 0
	
	elif index == 5:
		cursor_x = mouse_x // TILE_SIZE
		cursor_y = mouse_y // TILE_SIZE
		if 0 <= cursor_x < COL and 0<= cursor_y < ROW:
			if mouse_c == 1:
				mouse_c = 0
				set_neko()
				neko[cursor_y][cursor_x] = tsugi
				tsugi = 0
				index = 2
		
			# カーソル描画
			context.drawImage(
				img_cursor,
				cursor_x*TILE_SIZE + 4,
				cursor_y*TILE_SIZE + 4,
				TILE_SIZE - 8,
				TILE_SIZE - 8
			)
	
	elif index == 6:
		timer += 1
		if timer < 50:
			draw_txt("GAME OVER", 260, 348, 60, "red", "")
		if timer == 50:
			difficulty = 0
			index = 0
	
	

	
	# tile_sizeがどんな値でも崩れないようにする
	draw_txt(f"SCORE {score}", (COL+0.5)*TILE_SIZE, TILE_SIZE*1.5, TILE_SIZE*0.4, "blue", "")
	draw_txt(f"HISC {high_score}", (COL+0.5)*TILE_SIZE, TILE_SIZE*2.5, TILE_SIZE*0.4, "yellow", "")
	draw_txt("NEXT", (COL+0.5)*TILE_SIZE, TILE_SIZE*3.5, TILE_SIZE*0.4, "red", "")
	draw_txt(f"Win_w {win_w}", (COL+0.5)*TILE_SIZE, TILE_SIZE*4.5, TILE_SIZE*0.4, "orange", "")
	draw_txt(f"Win_h {win_h}", (COL+0.5)*TILE_SIZE, TILE_SIZE*5.5, TILE_SIZE*0.4, "orange", "")
	if win_w > win_h:
		draw_txt("PC用UI", (COL+0.5)*TILE_SIZE, TILE_SIZE*6.5, TILE_SIZE*0.4, "green", "")
	else:
		draw_txt("スマホ用UI", (COL+0.5)*TILE_SIZE, TILE_SIZE*6.5, TILE_SIZE*0.4, "green", "")

	if tsugi > 0:
		context.drawImage(img_neko[tsugi], (COL+2)*TILE_SIZE, TILE_SIZE*3, TILE_SIZE*0.5, TILE_SIZE*0.5)
	
	js.setTimeout(game_main, 100)

# 起動
game_main()
