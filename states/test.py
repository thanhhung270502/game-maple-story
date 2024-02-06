import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vẽ 2 hình chữ nhật")

# Màu sắc
white = (255, 255, 255)
red = (255, 0, 0)

# Kích thước của hình chữ nhật 1
rect1_width = 400
rect1_height = 50
rect1_x = 20
rect1_y = 20

# Vẽ hình chữ nhật 1 (màu trắng)
pygame.draw.rect(screen, white, (rect1_x, rect1_y, rect1_width, rect1_height))

# Kích thước của hình chữ nhật 2
rect2_width = int(0.8 * rect1_width)
rect2_height = rect1_height
rect2_x = 20
rect2_y = 20

# Vẽ hình chữ nhật 2 (màu đỏ)
pygame.draw.rect(screen, red, (rect2_x, rect2_y, rect2_width, rect2_height))

# Hiển thị cửa sổ
pygame.display.flip()

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Xử lý các sự kiện khác và vẽ lại màn hình khi cần

# Kết thúc Pygame
pygame.quit()
sys.exit()
