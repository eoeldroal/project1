import pygame
import time
import numpy as np

pygame.init()

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

BLACK = [0,0,0]
GRAY  = [200,200,200]
RED = [255,0,0]
YELLOW = [255,255,0]

CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
LENGTH_HOUR = 100.
LENGTH_MINUTE = 150.
LENGTH_SECOND = 200.

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class Rocket():
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\eoeld\\Downloads\\rocket_im.png")  # Load an image
        self.image = pygame.transform.scale(self.image, (20, 40))  # Scale it to the desired size

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = WINDOW_HEIGHT
        self.speed = 3

    def update(self):
        self.rect.y -= self.speed
            
        
rockets = []

running = True

launch = False
launch_sound = pygame.mixer.Sound("C:\\Users\\eoeld\\Downloads\\MP_MissleLaunch.mp3")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                launch = True
                
    screen.blit(pygame.transform.scale(pygame.image.load("C:\\Users\\eoeld\\Downloads\\map.png"), (WINDOW_WIDTH, WINDOW_HEIGHT)),(0,0))
    
    now = time.localtime()
    hour, minute, second = now.tm_hour, now.tm_min, now.tm_sec
    
    if (minute == 0 and second == 0) or launch == True:
        for i in range(4):
            rockets.append(Rocket(np.random.randint(1, WINDOW_WIDTH)))
        launch = False  # Reset the launch flag
        launch_sound.play()
        
    for r in rockets:
        r.update()
        screen.blit(r.image, r.rect)
        
    pygame.draw.circle(screen, [255,255,255], CENTER, 210)
    pygame.draw.circle(screen, BLACK, CENTER, 210, 2)
    

    # 시침
    end = (CENTER[0] + LENGTH_HOUR * np.sin(hour / 12.0 * 2 * np.pi),
            CENTER[1] - LENGTH_HOUR * np.cos(hour / 12.0 * 2 * np.pi))
    pygame.draw.line(screen, BLACK, CENTER, end, 6)

    # 분침
    end = (CENTER[0] + LENGTH_MINUTE * np.sin(minute / 60.0 * 2 * np.pi),
            CENTER[1] - LENGTH_MINUTE * np.cos(minute / 60.0 * 2 * np.pi))
    pygame.draw.line(screen, GRAY, CENTER, end, 4)

    # 초침
    end = (CENTER[0] + LENGTH_SECOND * np.sin(second / 60.0 * 2 * np.pi),
            CENTER[1] - LENGTH_SECOND * np.cos(second / 60.0 * 2 * np.pi))
    pygame.draw.line(screen, RED, CENTER, end, 2)

        
    pygame.display.flip()
        
        

pygame.quit()
