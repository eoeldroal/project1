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
# 위에서 생성한 정다각형 도형과 여러 행렬을 응용하여 도형을 그려주는 함수이다.
        
# class planet() :
#     def __init__(self, center, angle_planet, dist, shape)  :
#         self.center = center
#         self.angle_planet = angle_planet
#         self.dist = dist
#         self.shape = shape
#         self.angle = 0
        
#     def update(self, returncen = False) :
#         self.angle += self.angle_planet
#         self.center = np.array([self.center[0] + 2*self.dist*np.cos(np.deg2rad(self.angle)) , self.center[1] + self.dist*np.sin(np.deg2rad(self.angle))])
#         if returncen == True :
#             return self.center
#         self.Msun = Tmat(self.center[0], self.center[1]) @ Rmat(self.angle)
    
#     def draw(self,) :
#         pygame.draw.ellipse(screen, (255,255,255), pygame.Rect(self.center[0]-2*self.dist, self.center[1]-self.dist, 4*self.dist, 2*self.dist),2)
#         draw(self.Msun, self.shape, (255, 255, 100), self.center)
        


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

loc1 = 100
loc2 = WINDOW_WIDTH/2
sq_size = 20
SPEED = 5

R = []

m1 = None
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                keys["up"] = True
            elif event.key == pygame.K_DOWN:
                keys["down"] = True
            elif event.key == pygame.K_LEFT:
                keys["left"] = True
            elif event.key == pygame.K_RIGHT:
                keys["right"] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                keys["up"] = False
            elif event.key == pygame.K_DOWN:
                keys["down"] = False
            elif event.key == pygame.K_LEFT:
                keys["left"] = False
            elif event.key == pygame.K_RIGHT:
                keys["right"] = False
                
    if keys["up"]:
        loc2 -= SPEED
    if keys["down"]:
        loc2 += SPEED
    if keys["left"]:
        loc1 -= SPEED
    if keys["right"]:
        loc1 += SPEED
        
    Iscollide = False
            
    screen.fill(GRAY)
    
    rocket = pygame.Rect(loc1, loc2, sq_size, sq_size)
    
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

    if rocket.colliderect(sun_rect):
        Iscollide = True
        sq_size += 20
        
    if rocket.colliderect(planet1_rect) or rocket.colliderect(moon1_rect) or rocket.colliderect(planet2_rect):
        sq_size /= 2
        Iscollide = True
        loc1_s = loc1
        loc2_s = loc2
        piece1 = pygame.Rect(loc1_s, loc2_s, sq_size // 3, sq_size // 3)
        piece2 = pygame.Rect(loc1_s + sq_size // 3, loc2_s, sq_size // 3, sq_size // 3)
        piece3 = pygame.Rect(loc1_s + 2 * sq_size // 3, loc2_s, sq_size // 3, sq_size // 3)
        
        velocities = [np.random.uniform(-5, 5, size=2) for _ in range(3)]
        
        R+=list(zip([piece1, piece2, piece3],velocities))

    if Iscollide == True : 
        loc1 = 100
        loc2 = WINDOW_WIDTH/2
        Iscollide = False  
    
    pygame.draw.rect(screen, BLACK, rocket)
    
    for p, v in R:
        p.x += v[0]
        p.y += v[1]
        pygame.draw.rect(screen, BLACK, p)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

    