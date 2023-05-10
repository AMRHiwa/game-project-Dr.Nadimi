import pygame

# تنظیمات بازی
WIDTH = 640
HEIGHT = 480
FPS = 30

# شروع کردن Pygame و تنظیم پنجره بازی
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morabaraba")
clock = pygame.time.Clock()

# ایجاد شکل‌های مورد نیاز
background = pygame.Surface(screen.get_size())
background.fill((255, 255, 255))

# حلقه بازی
running = True
while running:
    # فرایند ورودی کاربر
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ارسال شکل‌های جدید به پنجره بازی
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # تنظیم سرعت بازی
    clock.tick(FPS)

# پایان بازی
pygame.quit()

