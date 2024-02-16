import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cấu hình màn hình
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drag and Drop Rectangle")

# Màu sắc
white = (255, 255, 255)
blue = (0, 0, 255)

# Tạo hình chữ nhật
rect_width, rect_height = 50, 50
rect = pygame.Rect((width - rect_width) // 2, (height - rect_height) // 2, rect_width, rect_height)

# Thiết lập trạng thái di chuyển
dragging = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    if dragging:
        rect.x, rect.y = pygame.mouse.get_pos()

    # Kiểm tra nếu hình chữ nhật ra khỏi màn hình
    if rect.left < 0:
        rect.left = 0
    elif rect.right > width:
        rect.right = width
    if rect.top < 0:
        rect.top = 0
    elif rect.bottom > height:
        rect.bottom = height

    # Vẽ màn hình
    screen.fill(white)
    pygame.draw.rect(screen, blue, rect)
    pygame.display.flip()
