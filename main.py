import js
import random

# # HTML取得
# title = js.document.querySelector("#title")
# message = js.document.querySelector("#message")

# Canvas取得
canvas = js.document.querySelector("#canvas")
context = canvas.getContext("2d")

# サイズ定義
COL = 8
ROW = 10

TILE_SIZE = 40

# Canvasサイズ変更
canvas.width = COL * TILE_SIZE + 200
canvas.height = ROW * TILE_SIZE

# UI領域の始点
UI_x = COL*TILE_SIZE

# マウス変数
mouse_x = 0
mouse_y = 0

# game_over変数
game_over = False

# スコア変数
score = 0
combo = 0
high_score = 0

# 配列
neko = []
check = []

for y in range(ROW):
	row = []
	for x in range(COL):
		row.append(0)
	neko.append(row)
	check.append(row)

# 画像
img_neko = [None]

for i in range(1, 6):
	img = js.Image.new()
	img.src = f"./assets/neko{i}.png"
	img_neko.append(img)

# neko_niku
img_niku = js.Image.new()
img_niku.src = "./assets/neko_niku.png"

# cursor
img_cursor = js.Image.new()
img_cursor.src = "./assets/neko_cursor.png"


# 描画関数
def draw_board():

	# 背景描画
	# canvas.width は右側のUI領域も含めるため、改善の必要があるかも
	# context.fillStyle = "gray"
	# context.fillRect(0, 0, UI_x, canvas.height)

	# マウス位置をマス番号に変換
	cursor_x = mouse_x // TILE_SIZE
	cursor_y = mouse_y // TILE_SIZE

	# マス目の描画
	for y in range(ROW):
		for x in range(COL):
			
			# マス目の座標計算
			px = x * TILE_SIZE
			py = y * TILE_SIZE

			# カーソル位置に画像を描画
			if x == cursor_x and y == cursor_y:
				# context.fillStyle = "red"
				context.drawImage(
					img_cursor,
					px + 4,
					py + 4,
					TILE_SIZE - 8,
					TILE_SIZE - 8
				)

			# # 枠線を描画
			# context.strokeStyle = "black"
			# context.strokeRect(
			# 	px,
			# 	py,
			# 	TILE_SIZE,
			# 	TILE_SIZE
			# )

			# マス目をチェッカー柄に変更
			# 色変更時は参照 → https://www.colordic.org/
			if (x+y)%2 == 0:
				context.fillStyle = "pink"
			else:
				context.fillStyle = "mistyrose"
			
			context.fillRect(px, py, TILE_SIZE-1, TILE_SIZE-1)

			# マス番号を表示
			# context.fillStyle = "blue"
			# context.fillText(y*COL+x, px+TILE_SIZE//2, py+TILE_SIZE//2)

			# 配列値を取得
			n = neko[y][x]

			# 揃ったネコ
			if n == 9:
				context.drawImage(
					img_niku,
					px + 4,
					py + 4,
					TILE_SIZE - 8,
					TILE_SIZE - 8
				)
			# 通常ネコ
			elif n > 0:
				context.drawImage(
					img_neko[n],
					px + 4,
					py + 4,
					TILE_SIZE - 8,
					TILE_SIZE - 8
				)

	# UI領域の描画
	context.fillStyle = "paleturquoise"
	context.fillRect(UI_x+1, 0, 200, canvas.height)

	# スコアの描画
	context.fillStyle = "black"
	context.font = "20px Arial"
	context.textAlign = "left"
	context.fillText(f"SCORE : {score}", UI_x+10, 25)
	context.fillText(f"HIGH : {high_score}", UI_x+10, 50)
	context.fillText(f"COMBO : {combo}", UI_x+10, 75)

	# ゲームオーバー画面の描画
	# ゲームオーバーから復帰した後も、描画が残り続けるバグがある
	if game_over:
		context.fillStyle = "rgba(0,0,0,0.7)"
		context.fillRect(0, 0, canvas.width, canvas.height)
		context.fillStyle = "white"
		context.font = "bold 48px Arial"
		context.textAlign = "center"
		context.fillText("GAME OVER", canvas.width//2, canvas.height//2)


# 消去判定
def check_neko():

	# nekoをcheckにコピー
	for y in range(ROW):
		for x in range(COL):
			check[y][x] = neko[y][x]
	
	# マーク配列
	mark = []
	for y in range(ROW):
		row = []
		for x in range(COL):
			row.append(False)
		mark.append(row)
	
	# 横3つチェック
	for y in range(ROW):
		for x in range(COL - 2):
			n = check[y][x]
			if check[y][x]>0:
				if check[y][x+1] == n and check[y][x+2] == n:
					# 消去用値に変更
					mark[y][x] = True
					mark[y][x+1] = True
					mark[y][x+2] = True
	
	# 縦3つチェック
	for y in range(ROW - 2):
		for x in range(COL):
			n = check[y][x]
			if check[y][x]>0:
				if check[y+1][x] == n and check[y+2][x] == n:
					mark[y][x] = True
					mark[y+1][x] = True
					mark[y+2][x] = True
	
	# 斜め3つチェック
	for y in range(1, ROW-1):
		for x in range(1, COL-1):
			n = check[y][x]
			if check[y][x]>0:
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
	
	# 一括で変更
	for y in range(ROW):
		for x in range(COL):
			if mark[y][x]:
				neko[y][x] = 9

# 消去関数
def sweep_neko():
	global score, combo, high_score
	count = 0
	for y in range(ROW):
		for x in range(COL):
			# 揃ったネコを
			if neko[y][x] == 9:
				# 消す
				neko[y][x] = 0
				count += 1
	
	# スコア加算
	if count > 0:
		combo += 1
		add = count * 10 * combo
		score += add

		# ハイスコア更新
		if score > high_score:
			high_score = score
	else:
		combo = 0
	return count

def drop_neko():
	moved = False
	# 下から見る
	for y in range(ROW-2, -1, -1):
		for x in range(COL):
			if neko[y][x] != 0 and neko[y+1][x] == 0:
				neko[y+1][x] = neko[y][x]
				neko[y][x] = 0
				moved = True
	return moved

# ゲームオーバー判定
def over_neko():
	for x in range(COL):
		if neko[0][x] > 0:
			return True
	return False

# ネコを複数個降らせる
def set_neko():
	for x in range(COL):
		if neko[0][x] == 0:
			neko[0][x] = random.randint(1, 3)


# マウス移動イベント
def mouse_move(event):
	global mouse_x, mouse_y

	rect = canvas.getBoundingClientRect()

	mouse_x = int(event.clientX - rect.left)
	mouse_y = int(event.clientY - rect.top)

	draw_board()

# イベント登録
canvas.addEventListener("mousemove", mouse_move)

# 消去後に描画する関数
def erase_neko():
	sweep_neko()
	drop_loop()

# drop_neko()をループ
def drop_loop():
	moved = drop_neko()
	draw_board()

	# まだ落ちるネコがあるなら続行
	if moved:
		js.setTimeout(drop_loop, 100)
	else:
		# ゲームオーバー判定
		global game_over
		if over_neko():
			game_over = True
			draw_board()
			return
		
		# 落下後に再判定
		check_neko()
		draw_board()

		# 揃っているか確認
		found = False

		for y in range(ROW):
			for x in range(COL):
				if neko[y][x] == 9:
					found = True
		if found:
			js.setTimeout(erase_neko, 500)

# クリック処理
def canvas_click(event):
	global game_over, score, combo

	# ゲームオーバー時のクリック処理
	if game_over:
		# 盤面リセット
		for y in range(ROW):
			for x in range(COL):
				neko[y][x] = 0
		score = 0
		combo = 0
		game_over = False
		draw_board()
		return

	# canvasの位置情報を取得
	rect = canvas.getBoundingClientRect()

	# canvas内座標へ変換
	mouse_x = int(event.clientX - rect.left)
	mouse_y = int(event.clientY - rect.top)

	# マス番号へ変換
	x = mouse_x // TILE_SIZE
	y = mouse_y // TILE_SIZE

	# 範囲チェック
	if 0 <= x < COL and 0<= y < ROW:

		# ランダムなネコを配置
		if neko[y][x] == 0:
			neko[y][x] = random.randint(1, 3)
			set_neko()
		else:
			neko[y][x] = 0 

		# 再描画
		check_neko()
		draw_board()

		# 0.5秒後に消去
		js.setTimeout(erase_neko, 500)


# イベント登録
canvas.addEventListener("click", canvas_click)


# 初回描画
draw_board()
