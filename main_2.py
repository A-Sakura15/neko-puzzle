import js
import random

# # HTML取得
# title = js.document.querySelector("#title")
# message = js.document.querySelector("#message")

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
TILE_SIZE = 72

# Canvasサイズ変更
canvas.width = COL * TILE_SIZE + 200
canvas.height = ROW * TILE_SIZE

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
	context.fillText(txt, x+2, y+2)

	context.fillStyle = col
	context.fillText(txt, x, y)

# 判定
def check_neko():
	for y in range(ROW):
		for x in range(COL):
			check[y][x] = neko[y][x]
	
	# 縦3つチェック
	for y in range(1, ROW-1):
		for x in range(COL):
			n = check[y][x]
			if check[y][x]>0:
				if check[y-1][x] == n and check[y+1][x] == n:
					neko[y-1][x] = 7
					neko[y][x] = 7
					neko[y+1][x] = 7
	
	# 横3つチェック
	for y in range(ROW):
		for x in range(1, COL-1):
			n = check[y][x]
			if check[y][x]>0:
				if check[y][x-1] == n and check[y][x+1] == n:
					neko[y][x-1] = 7
					neko[y][x] = 7
					neko[y][x+1] = 7
	
	# 斜め3つチェック
	for y in range(1, ROW-1):
		for x in range(1, COL-1):
			n = check[y][x]
			if check[y][x]>0:
				# 左上、右下が同じ
				if check[y-1][x-1] == n and check[y+1][x+1] == n:
					neko[y-1][x-1] = 7
					neko[y][x] = 7
					neko[y+1][x+1] = 7
				# 左下、右上が同じ
				if check[y+1][x-1] == n and check[y-1][x+1] == n:
					neko[y+1][x-1] = 7
					neko[y][x] = 7
					neko[y-1][x+1] = 7

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
	context.drawImage(img_bg, 0, 0, COL*TILE_SIZE, ROW*TILE_SIZE)

	if index == 0 or index == 1:
		draw_txt("ねこねこ", 250, 240, 80, "violet", "TITLE")
		draw_txt("Easy", 280, 400, 40, "white", "TITLE")
		draw_txt("Normal", 260, 500, 40, "white", "TITLE")
		draw_txt("Hard", 280, 600, 40, "white", "TITLE")
		index = 1

		if mouse_c == 1:
			mouse_c = 0
			if 350 < mouse_y < 450:
				difficulty = 4
			if 450 < mouse_y < 550:
				difficulty = 5
			if 550 < mouse_y < 650:
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

	
	# elif index == 1:
	# 	difficulty = 0
	# 	if mouse_c == 1:
	# 		if 350 < mouse_y < 450:
	# 			difficulty = 4
	# 		if 450 < mouse_y < 550:
	# 			difficulty = 5
	# 		if 550 < mouse_y < 650:
	# 			difficulty = 6
		
	# 	if difficulty > 0:
	# 		for y in range(ROW):
	# 			for x in range(COL):
	# 				neko[y][x] = 0
	# 		mouse_c = 0
	# 		score = 0
	# 		tsugi = 0
	# 		set_neko()
	# 		index = 2
	
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
		if 24 <= mouse_x < 24+72*8 and 24 <= mouse_y < 24+72*10:
			cursor_x = mouse_x // TILE_SIZE
			cursor_y = mouse_y // TILE_SIZE
			if 0 <= cursor_x < COL and 0<= cursor_y < ROW:
				if mouse_c == 1:
					mouse_c = 0
					set_neko()
					neko[cursor_y][cursor_x] = tsugi
					tsugi = 0
					index = 2
	
	elif index == 6:
		timer += 1
		if timer == 1:
			draw_txt("GAME OVER", 260, 348, 60, "red", "")
		if timer == 50:
			index = 0
	
	draw_neko()

	draw_txt(f"SCORE {score}", 120, 50, 30, "blue", "")
	draw_txt(f"HISC {high_score}", 450, 50, 30, "yellow", "")

	if tsugi > 0:
		context.drawImage(img_neko[tsugi], 700, 100, TILE_SIZE, TILE_SIZE)
	
	js.setTimeout(game_main, 100)

# 起動
game_main()











# # 描画関数
# def draw_board():

# 	# 背景描画
# 	# canvas.width は右側のUI領域も含めるため、改善の必要があるかも
# 	# context.fillStyle = "gray"
# 	# context.fillRect(0, 0, UI_x, canvas.height)

# 	# マウス位置をマス番号に変換
# 	cursor_x = mouse_x // TILE_SIZE
# 	cursor_y = mouse_y // TILE_SIZE

# 	# マス目の描画
# 	for y in range(ROW):
# 		for x in range(COL):
			
# 			# マス目の座標計算
# 			px = x * TILE_SIZE
# 			py = y * TILE_SIZE

# 			# # 枠線を描画
# 			# context.strokeStyle = "black"
# 			# context.strokeRect(
# 			# 	px,
# 			# 	py,
# 			# 	TILE_SIZE,
# 			# 	TILE_SIZE
# 			# )

# 			# マス目をチェッカー柄に変更
# 			# 色変更時は参照 → https://www.colordic.org/
# 			if (x+y)%2 == 0:
# 				context.fillStyle = "pink"
# 			else:
# 				context.fillStyle = "mistyrose"
			
# 			context.fillRect(px, py, TILE_SIZE-1, TILE_SIZE-1)

# 			# マス番号を表示
# 			# context.fillStyle = "blue"
# 			# context.fillText(y*COL+x, px+TILE_SIZE//2, py+TILE_SIZE//2)

# 			# カーソル位置に画像を描画
# 			if x == cursor_x and y == cursor_y:
# 				# context.fillStyle = "red"
# 				context.drawImage(
# 					img_cursor,
# 					px + 4,
# 					py + 4,
# 					TILE_SIZE - 8,
# 					TILE_SIZE - 8
# 				)

# 			# 配列値を取得
# 			n = neko[y][x]

# 			# 揃ったネコ
# 			if n == 7:
# 				context.drawImage(
# 					img_niku,
# 					px + 4,
# 					py + 4,
# 					TILE_SIZE - 8,
# 					TILE_SIZE - 8
# 				)
# 			# 通常ネコ
# 			elif n > 0:
# 				context.drawImage(
# 					img_neko[n],
# 					px + 4,
# 					py + 4,
# 					TILE_SIZE - 8,
# 					TILE_SIZE - 8
# 				)

# 	# UI領域の描画
# 	context.fillStyle = "paleturquoise"
# 	context.fillRect(UI_x+1, 0, 200, canvas.height)

# 	# スコアの描画
# 	context.fillStyle = "black"
# 	context.font = "20px Arial"
# 	context.textAlign = "left"
# 	context.fillText(f"SCORE : {score}", UI_x+10, 25)
# 	context.fillText(f"HIGH : {high_score}", UI_x+10, 50)
# 	context.fillText(f"COMBO : {combo}", UI_x+10, 75)

# 	# ゲームオーバー画面の描画
# 	# ゲームオーバーから復帰した後も、描画が残り続けるバグがある
# 	if game_over:
# 		context.fillStyle = "rgba(0,0,0,0.7)"
# 		context.fillRect(0, 0, canvas.width, canvas.height)
# 		context.fillStyle = "white"
# 		context.font = "bold 48px Arial"
# 		context.textAlign = "center"
# 		context.fillText("GAME OVER", canvas.width//2, canvas.height//2)





# # 消去後に描画する関数
# def erase_neko():
# 	sweep_neko()
# 	drop_loop()

# # drop_neko()をループ
# def drop_loop():
# 	moved = drop_neko()
# 	draw_board()

# 	# まだ落ちるネコがあるなら続行
# 	if moved:
# 		js.setTimeout(drop_loop, 100)
# 	else:
# 		# ゲームオーバー判定
# 		global game_over
# 		if over_neko():
# 			game_over = True
# 			draw_board()
# 			return
		
# 		# 落下後に再判定
# 		check_neko()
# 		draw_board()

# 		# 揃っているか確認
# 		found = False

# 		for y in range(ROW):
# 			for x in range(COL):
# 				if neko[y][x] == 9:
# 					found = True
# 		if found:
# 			js.setTimeout(erase_neko, 500)

# # クリック処理
# def canvas_click(event):
# 	global game_over, score, combo

# 	# ゲームオーバー時のクリック処理
# 	if game_over:
# 		# 盤面リセット
# 		for y in range(ROW):
# 			for x in range(COL):
# 				neko[y][x] = 0
# 		score = 0
# 		combo = 0
# 		game_over = False
# 		draw_board()
# 		return

# 	# canvasの位置情報を取得
# 	rect = canvas.getBoundingClientRect()

# 	# canvas内座標へ変換
# 	mouse_x = int(event.clientX - rect.left)
# 	mouse_y = int(event.clientY - rect.top)

# 	# マス番号へ変換
# 	x = mouse_x // TILE_SIZE
# 	y = mouse_y // TILE_SIZE

# 	# 範囲チェック
# 	if 0 <= x < COL and 0<= y < ROW:

# 		# ランダムなネコを配置
# 		if neko[y][x] == 0:
# 			neko[y][x] = random.randint(1, 3)
# 			set_neko()
# 		else:
# 			neko[y][x] = 0 

# 		# 再描画
# 		check_neko()
# 		draw_board()

# 		# 0.5秒後に消去
# 		js.setTimeout(erase_neko, 500)


# # イベント登録
# canvas.addEventListener("click", canvas_click)


# # 初回描画
# draw_board()
