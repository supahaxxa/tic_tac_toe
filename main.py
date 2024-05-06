from datetime import datetime
from warehouse import *
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 550, 550

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

font = pygame.font.SysFont("Arial", 40)


def draw_gridlines(top, left, color):
	for i in range(2):
		pygame.draw.rect(screen, color, pygame.Rect(left + (150 * (i + 1)) + (25 * i), top, 25, 500))    # vertical
		pygame.draw.rect(screen, color, pygame.Rect(left, top + (150 * (i + 1)) + (25 * i), 500, 25))    # horizontal

	del i


def draw_cross(left, top, color):
	s = 100
	half = s / 2
	root = s / (2 ** 0.5) / 4
	points = ((left + root, top), (left + half, top + (half - root)), (left + (s - root), top),
		(left + s, top + root), (left + half + root, top + half), (left + s, top + (s - root)),
		(left + (s - root), top + s), (left + half, top + half + root), (left + root, top + s),
		(left, top + (s - root)), (left + (half - root), top + half), (left, top + root))
	pygame.draw.polygon(screen, color, points)


def draw_circle(left, top, color):
	pygame.draw.circle(screen, color, (left + 50, top + 50), 50)
	pygame.draw.circle(screen, BLACK, (left + 50, top + 50), 25)


def check_completion(grid):
	# check horizontals
	for i in range(3):
		if grid[3 * i] == grid[(3 * i) + 1] and grid[(3 * i)] == grid[(3 * i) + 2]:
			return grid[3 * i]
	del i
	# check verticals
	for i in range(3):
		if grid[i] == grid[i + 3] and grid[i] == grid[i + 6]:
			return grid[i]
	del i
	# check major diagonal
	if grid[0] == grid[4] and grid[0] == grid[8]:
		return grid[4]

	# check minor diagonal
	if grid[2] == grid[4] and grid[6] == grid[4]:
		return grid[4]

	return None


move = 0
mark = 0

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			for i in range(9):
				if slots_range[i][0][0] <= pygame.mouse.get_pos()[0] <= slots_range[i][0][1] and slots_range[i][1][0] <= pygame.mouse.get_pos()[1] <= slots_range[i][1][1] and states[i] is None:
					states[i] = move
					move = (move + 1) % 2

	screen.fill(BLACK)

	draw_gridlines(25, 25, WHITE)

	for i in range(9):
		if states[i] == 1:
			draw_circle(slots[i][0], slots[i][1], WHITE)
		elif states[i] == 0:
			draw_cross(slots[i][0], slots[i][1], WHITE)

	# checking whether the game is completed
	if check_completion(states) == 0 or check_completion(states) == 1:
		pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, 550, 550))

		if check_completion(states) == 0:
			message = font.render("Player X won.", True, WHITE)
		else:
			message = font.render("Player O won.", True, WHITE)
		message_rect = message.get_rect()
		message_rect.center = (275, 275)
		screen.blit(message, message_rect)

		if mark == 0:
			mark = datetime.now()
		else:
			if (datetime.now() - mark).seconds >= 2:
				quit()
	elif check_completion(states) is None and None not in states:
		pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, 550, 550))

		message = font.render("It was a draw.", True, WHITE)
		message_rect = message.get_rect()
		message_rect.center = (275, 275)
		screen.blit(message, message_rect)

		if mark == 0:
			mark = datetime.now()
		else:
			if (datetime.now() - mark).seconds >= 2:
				quit()

	pygame.display.update()
