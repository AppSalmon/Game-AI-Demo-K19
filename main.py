import cv2
import pygame
from pygame.locals import *
from random import randint
import mediapipe as mp
import math
import time
from login import Login
import json


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_hands = mp.solutions.hands

current_control = 'up'
new_control = ''
speed = 1

data = Login()
pygame.quit()


# Khởi tạo Pygame
pygame.init()

# Cài đặt kích thước cửa sổ

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 700
CAM_WIDTH = 300
CAM_HEIGHT = int(0.7*CAM_WIDTH)
PLAY_SIZE = 700
FOOD_SIZE = 20

BACKGROUND = (214, 214, 214) # Màu background
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)
BROWN = (150, 75, 0)


def create_text(x, color, size): # Tạo chữ
	font = pygame.font.SysFont('sans', size)
	return font.render(x, True, color)


score = 0
# land = randint(1, 3)
land = PLAY_SIZE//2
food_y = 0
food_x = randint(0, PLAY_SIZE - FOOD_SIZE*2)
food_drop = 9
score = 0
x_dom = [0, 0, 0]
y_dom = [0, 0, 0]
result1 = ""
result2 = ""

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game of AI club IUH")
icon = pygame.image.load('AiClub.jpg')
pygame.display.set_icon(icon) # Set logo


# Load hình ảnh nền
background_image = pygame.image.load("backgr.jpg")
background_image = pygame.transform.scale(background_image, (PLAY_SIZE, PLAY_SIZE))

# Load hình ảnh nền
background_control = pygame.image.load("backgr_control.png")
background_control = pygame.transform.scale(background_control, (PLAY_SIZE - CAM_HEIGHT - 50, PLAY_SIZE - CAM_HEIGHT - 30))

# Trái cây
food_image = "food.png"
food_image = pygame.image.load(food_image)
food_image = pygame.transform.scale(food_image, (50, 50))

# Đom đóm
dom_image = "FireFly.png"
dom_image = pygame.image.load(dom_image)
dom_image = pygame.transform.scale(dom_image, (100, 100))

# Cup
cup_image = "cup.png"
cup_image = pygame.image.load(cup_image)
cup_image = pygame.transform.scale(cup_image, (100, 120))

# Player
player_image = "player.png"
player_image = pygame.image.load(player_image)
player_image = pygame.transform.scale(player_image, (100, 120))

# Load nhạc
pygame.mixer.init()
background_music = pygame.mixer.Sound("backgr.mp3")
background_music.play(-1)

start_music = pygame.mixer.Sound("start.mp3")
end_music = pygame.mixer.Sound("gameover.mp3")
get_music = pygame.mixer.Sound("get.mp3")

# Khởi tạo OpenCV cho camera
cap = cv2.VideoCapture(0)  # Sử dụng camera mặc định (thay đổi số để chọn camera khác)

# Vòng lặp chính
running = True
clock = pygame.time.Clock() # Tạo FPS
pausing = False
cnt = 0

with mp_hands.Hands(
	model_complexity=0,
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5) as hands:
	while running and cap.isOpened():
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False

		# ======= Camera ======== #
				
		# Đọc khung hình từ camera
		ret, frame = cap.read()
		
		if not ret:
			print("Ignoring empty camera frame.")
			# Nếu đang tải video, hãy sử dụng 'ngắt' thay vì 'tiếp tục'.
			continue
		
		if ret:
			# Xoay khung hình 90 độ
			frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
			frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
			frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

			# Chuyển đổi khung hình từ OpenCV sang Pygame
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			frame = cv2.resize(frame, (CAM_HEIGHT, CAM_WIDTH))
			# frame_py = pygame.surfarray.make_surface(frame)

			# # # Hiển thị khung hình từ camera trong cửa sổ Pygame   
			# screen.blit(frame_py, (SCREEN_WIDTH - CAM_WIDTH - 10, SCREEN_HEIGHT - CAM_HEIGHT - 15))
			# pygame.display.update()

		# To improve performance, optionally mark the frame as not writeable to
		# pass by reference.
		frame.flags.writeable = False
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		results = hands.process(frame)

		# Draw the hand annotations on the frame.
		frame.flags.writeable = True
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

		height, width, _ = frame.shape # Lấy chiều cao và bề ngang của frame

		hand_centers = []
		if results.multi_hand_landmarks: # Detect được bàn tay
			
			for hand_landmarks in results.multi_hand_landmarks:

				hand_centers.append([int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)])
				# hand_centers.append([int(hand_landmarks.landmark[8].x * width), int(hand_landmarks.landmark[8].y * height)])
				# mp_drawing.draw_landmarks(
				# 	frame,
				# 	hand_landmarks,
				# 	mp_hands.HAND_CONNECTIONS,
				# 	mp_drawing_styles.get_default_hand_landmarks_style(),
				# 	mp_drawing_styles.get_default_hand_connections_style())
		# cv2.circle(frame, (0, 0), 2, RED, 2) # Hình, tọa độ tâm, bán kính, màu, dày 
		if len(hand_centers) >= 1:
			x_hand = hand_centers[0][0]
			y_hand = hand_centers[0][1]

			# print(x_hand, y_hand)
			cv2.circle(frame, (x_hand, y_hand), randint(1, 9), (0, 255, 0), 2)

			land = int(y_hand / 300 * PLAY_SIZE)

			# Cũ
			# if y_hand <= 75:
			# 	land = 1
			# elif y_hand <= 75 * 2:
			# 	land = 2
			# elif y_hand <= 75 * 3:
			# 	land = 3
			# else:
			# 	land = 4

		# elif len(hand_centers) > 1:

		# print(land)

		# (y, x)

		
		# Cũ
		# Vẽ gianh giới trên camera
		# cv2.line(frame, (0, 0), (height, 0), RED, 1)
		# cv2.line(frame, (0, height//4), (height, height//4), RED, 1)
		# cv2.line(frame, (0, height//4 * 2), (height, height//4 * 2), RED, 1)
		# cv2.line(frame, (0, height//4 * 3), (height, height//4 * 3), RED, 1)
		# cv2.line(frame, (0, height), (height, height), RED, 1)

		frame_py = pygame.surfarray.make_surface(frame)

		# Hiển thị khung hình từ camera trong cửa sổ Pygame   
		screen.blit(frame_py, (SCREEN_WIDTH - CAM_WIDTH - 10, SCREEN_HEIGHT - CAM_HEIGHT - 20))
		pygame.display.update()


		# cv2.imshow('Salmon control', cv2.flip(frame, 0)) # Chọn 1 nếu muốn lật camera
		if cv2.waitKey(10) & 0xFF == 27:
			break
		
		# ======= Draw interface ========== #
		# Vẽ nền chơi & nền bảng điều khiển
		# pygame.draw.rect(screen, WHITE, (0, 0, PLAY_SIZE, PLAY_SIZE)) # Tọa độ bắt đầu, size
		screen.blit(background_image, (0, 0))

		# Vẽ đom đóm
		# cnt += 1
		# if cnt % 50 == 0:
		# 	x_dom[0] = randint(0, 500)
		# 	y_dom[0] = randint(0, 100)
		# if cnt % 30 == 0:
		# 	x_dom[1] = randint(0, 500)
		# 	y_dom[1] = randint(0, 100)
		# if cnt % 70 == 0:
		# 	x_dom[2] = randint(0, 500)
		# 	y_dom[2] = randint(0, 100)

		# if cnt > 100:
		# 	cnt = 0
		# screen.blit(dom_image, (x_dom[0], y_dom[0]))
		# screen.blit(dom_image, (x_dom[1], y_dom[1]))
		# screen.blit(dom_image, (x_dom[2], y_dom[2]))

		# pygame.draw.rect(screen, GRASS, (PLAY_SIZE, 0, PLAY_SIZE - CAM_HEIGHT, PLAY_SIZE - CAM_HEIGHT - 20)) # Tọa độ bắt đầu, size
		screen.blit(background_control, (PLAY_SIZE, 0))
		# pygame.draw.rect(screen, BLACK, (PLAY_SIZE, PLAY_SIZE - CAM_HEIGHT - 20, CAM_WIDTH + 20, CAM_HEIGHT + 20), 10) # x, y, dày cao, dày rộng
		pygame.draw.line(screen, BLACK, (PLAY_SIZE + 6, PLAY_SIZE - CAM_HEIGHT - 30), (PLAY_SIZE + 6, PLAY_SIZE), 13)  # Vẽ đường chia giữa cam và khu vực chơi


		# Cũ
		# Vẽ gianh giới con đường
		# pygame.draw.line(screen, RED, (0, 0), (0, PLAY_SIZE), 2)
		# pygame.draw.line(screen, RED, (PLAY_SIZE//4, 0), (PLAY_SIZE//4, PLAY_SIZE), 2)
		# pygame.draw.line(screen, RED, (PLAY_SIZE//4 * 2, 0), (PLAY_SIZE//4 * 2, PLAY_SIZE), 2)
		# pygame.draw.line(screen, RED, (PLAY_SIZE//4 * 3, 0), (PLAY_SIZE//4 * 3, PLAY_SIZE), 2)
		# pygame.draw.line(screen, RED, (PLAY_SIZE, 0), (PLAY_SIZE, PLAY_SIZE), 2)

		# Vẽ player
		# player = pygame.draw.rect(screen, RED, (PLAY_SIZE//4 * (land-1), PLAY_SIZE-40, PLAY_SIZE//4, 20))
		player = pygame.draw.rect(screen, BROWN, (land, PLAY_SIZE-40, PLAY_SIZE//4, 20))
		screen.blit(player_image, (land + 50, PLAY_SIZE-150))

		# Vẽ food
		food = pygame.draw.rect(screen, GREEN, (food_x, food_y, FOOD_SIZE, FOOD_SIZE))
		screen.blit(food_image, (food_x-10, food_y-25))

		# Vẽ đất
		ground = pygame.draw.rect(screen, BLACK, (0, PLAY_SIZE-20, PLAY_SIZE, 50))

		# Vẽ điểm
		screen.blit(create_text('Score A+: ' + str(score), WHITE, 50), (PLAY_SIZE + 20, 100))

		# Rớt liên tục
		food_y += food_drop
		
		# Reset rớt
		if food_y > PLAY_SIZE+30:
			food_y = 0
			food_x = randint(100, PLAY_SIZE - FOOD_SIZE * 2)

		if food.colliderect(player):
			score += 1
			get_music.play()
			food_y = 0
			food_x = randint(100, PLAY_SIZE - FOOD_SIZE * 2)
			if food_drop <= 20:
				food_drop += 1

			# music_sucess.play()
		
		if food.colliderect(ground):
			food_drop = 0
			if pausing == False:
				end_music.play()
				try:
					with open('data.json', 'a') as f:
						data['score'] = score
						json.dump(data, f)
						f.write('\n')
				except:
					pass

				""" Bảng xếp hạng """
				numbers = []
				with open('ranking.txt', 'r') as file:
					for line in file:
						number = int(line.strip())
						numbers.append(number)
				# print(numbers)
				numbers.append(score)
				numbers.sort(reverse=True)  # Sắp xếp từ lớn đến bé
				numbers_sort = numbers[:5]
				if score in numbers_sort:
					result1 = "Top: " + str(numbers.index(score)+1)

				with open('ranking.txt', 'w') as file:
					for number in numbers_sort:
						file.write(str(number) + '\n')
				result2 = "BXH: " + str(numbers_sort)

			pausing = True
			# music_fail.play()
			# screen.blit(image_fruit_die, (food_x-10, food_y-25))
		if pausing == True:
			pygame.draw.rect(screen, BLACK, (50, 50, PLAY_SIZE - 100, PLAY_SIZE - 100)) # Tọa độ bắt đầu, size
			screen.blit(create_text('Game over', RED, 100), (150, 200))
			screen.blit(create_text('Score A+: ' + str(score), RED, 50), (200, 300))
			screen.blit(cup_image, (PLAY_SIZE//2-50, 400))

			screen.blit(create_text(result1, RED, 40), (300, 580))
			screen.blit(create_text(result2, RED, 40), (190, 530))


		for event in pygame.event.get():  # bat su kien, neu khong bat su kien window se nghi chuong trinh ko phan hoi.
			if event.type == pygame.QUIT:  # bat su kien exit
				pygame.quit()
				running = False
			elif event.type == pygame.KEYDOWN:
				if pausing == True:
					if event.key == pygame.K_SPACE:
						start_music.play()
						score = 0
						land = randint(1, 3)
						food_y = 0
						food_x = randint(100, PLAY_SIZE - FOOD_SIZE * 2)
						food_drop = 9
						score = 0
						pausing = False
						
		# print(food_drop)
		# pygame.display.flip() # Show chương trình

# Đóng camera và thoát
cap.release()
pygame.quit()
cv2.destroyAllWindows()

