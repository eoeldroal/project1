import pygame
import numpy as np

def getRegularPolygon(N, radius=1):
    v = np.zeros((N,2))
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v


def getRectangle(width, height, x=0, y=0):
    points = np.array([ [0, 0], 
                        [width, 0], 
                        [width, height], 
                        [0, height]], dtype='float')
    points = points + [x, y]
    return points
#

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([ [c, -s, 0], 
                   [s, c, 0], 
                   [0, 0, 1]], dtype='float')
    return R 
# 회전을 시킬 때 사용하는 행렬을 만들어주는 함수이다.

def Tmat(tx, ty):
    T = np.array([ [1, 0, tx], 
                   [0, 1, ty], 
                   [0, 0, 1]], dtype='float')
    return T 
# Rmat와 계산을 할 수 있도록 만들어주는 행렬을 생성하는 함수이다.

def draw(M, points, color=(0,0,0), p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = ( R @ points.T ).T + t 
    pygame.draw.polygon(screen, color, points_transformed)
    if p0 is not None:
        pygame.draw.line(screen, (0,0,0), p0, points_transformed[0])
        

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

BLACK = [0,0,0]
GRAY  = [200,200,200]
RED = [255,0,0]
YELLOW = [255,255,0]

pygame.init()  # 1! initialize the whole pygame system!
pygame.display.set_caption("20201082 박현빈")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

angle_sun = 0.
Sun = getRegularPolygon(40, 30)

angle_planet1 = 0.
dist_C_P1 = 100.
Planet1 = getRegularPolygon(40, 20)

angle_moon1 = 0.
dist_P1_M = 40.
Moon1 = getRegularPolygon(40, 10)

angle_planet2 = 0.
dist_C_P2 = 150.
Planet2 = getRegularPolygon(40, 25)

keys = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
}

m1 = None
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    screen.fill(GRAY)
    
    angle_sun += 3/10.
    angle_planet1 += 5/10.
    angle_planet2 += 6/10.
    angle_moon1 += 10/10.
    angle_m1 = 1
    
    CENTER = np.array([WINDOW_WIDTH/2. , WINDOW_HEIGHT/2.])
    P1_CENTER = np.array([WINDOW_WIDTH/2. + 2*dist_C_P1*np.cos(np.deg2rad(angle_planet1)) , WINDOW_HEIGHT/2. + dist_C_P1*np.sin(np.deg2rad(angle_planet1))])
    M1_CENTER = np.array([P1_CENTER[0] + 2*dist_P1_M*np.cos(np.deg2rad(angle_moon1)) , P1_CENTER[1] + dist_P1_M*np.sin(np.deg2rad(angle_moon1))])
    P2_CENTER = np.array([WINDOW_WIDTH/2. + 2.5*dist_C_P2*np.cos(np.deg2rad(angle_planet2)) , WINDOW_HEIGHT/2. + dist_C_P2*np.sin(np.deg2rad(angle_planet2))])
    
    Msun = Tmat(CENTER[0], CENTER[1]) @ Rmat(angle_sun)
    draw(Msun, Sun, (255, 255, 100), CENTER)
    
    # 첫 번째 행성의 궤도를 타원으로 나타낸다. 
    # 첫 번째 행성의 공전 중심은 태양이다.
    pygame.draw.ellipse(screen, (255,255,255), pygame.Rect(CENTER[0]-200,CENTER[1]-100, 400, 200),2)
    Mplanet1 = Tmat(P1_CENTER[0], P1_CENTER[1]) @ Rmat(angle_planet1)
    draw(Mplanet1, Planet1, (255, 255, 100), P1_CENTER)
    
    # 첫 번째 행성의 위성의 궤도를 타원으로 나타낸다.
    # 두 번째 행성의 공전 중심은 첫 번째 행성이다.
    pygame.draw.ellipse(screen, (255,255,255), pygame.Rect(P1_CENTER[0]-80,P1_CENTER[1]-40, 160, 80),2)
    Mmoon1 = Tmat(M1_CENTER[0], M1_CENTER[1]) @ Rmat(angle_moon1)
    draw(Mmoon1, Moon1, (255, 255, 100), M1_CENTER)
    
    pygame.draw.ellipse(screen, (255,255,255), pygame.Rect(CENTER[0]-375,CENTER[1]-150, 750, 300),2)
    Mplanet2 = Tmat(P2_CENTER[0], P2_CENTER[1]) @ Rmat(angle_planet2)
    draw(Mplanet2, Planet2, (255, 255, 100), P2_CENTER)
    
    sun_rect = pygame.Rect(CENTER[0] - 30, CENTER[1] - 30, 60, 60)
    planet1_rect = pygame.Rect(P1_CENTER[0] - 20, P1_CENTER[1] - 20, 40, 40)
    moon1_rect = pygame.Rect(M1_CENTER[0] - 10, M1_CENTER[1] - 10, 20, 20)
    planet2_rect = pygame.Rect(P2_CENTER[0] - 25, P2_CENTER[1] - 25, 50, 50)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

    
