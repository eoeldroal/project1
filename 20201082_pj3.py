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

def Tmat(tx, ty):
    T = np.array([ [1, 0, tx], 
                   [0, 1, ty], 
                   [0, 0, 1]], dtype='float')
    return T 

def draw(M, points, color=(0,0,0), p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = ( R @ points.T ).T + t 
    pygame.draw.polygon(screen, color, points_transformed)
    if p0 is not None:
        pygame.draw.line(screen, (0,0,0), p0, points_transformed[0])
        
def draw_robot(x, y, width, height):
    # Draw the body
    body_height = height * 0.6
    body_width = width * 0.6
    body_x = x + width * 0.2
    body_y = y + height * 0.4
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(body_x, body_y, body_width, body_height))

    # Draw the head
    head_radius = width * 0.2
    head_x = x + width / 2
    head_y = y + height * 0.2
    pygame.draw.circle(screen, (0, 0, 0), (int(head_x), int(head_y)), int(head_radius))

    # Draw the arms
    arm_length = height * 0.3
    arm_y = y + height * 0.5
    left_arm_x = x
    right_arm_x = x + width
    pygame.draw.line(screen, (0, 0, 0), (int(left_arm_x), int(arm_y)), (int(body_x), int(arm_y)), 3)
    pygame.draw.line(screen, (0, 0, 0), (int(right_arm_x), int(arm_y)), (int(body_x + body_width), int(arm_y)), 3)

    # Draw the legs
    leg_length = height * 0.3
    leg_y = y + height
    left_leg_x = x + width * 0.3
    right_leg_x = x + width * 0.7
    pygame.draw.line(screen, (0, 0, 0), (int(left_leg_x), int(body_y + body_height)), (int(left_leg_x), int(leg_y)), 3)
    pygame.draw.line(screen, (0, 0, 0), (int(right_leg_x), int(body_y + body_height)), (int(right_leg_x), int(leg_y)), 3)


pygame.init()
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

pygame.init()
pygame.display.set_caption("Mouse")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

angle1 = 20
width1 = 100
height1 = 50
rect1 = getRectangle(width1, height1)

gap = 30
angle2 = 0

Arm_ang = -50

arms = [[getRectangle(width1, height1) for _ in range(3)] for _ in range(3)]

centers = [[WINDOW_WIDTH/2. - 350., WINDOW_HEIGHT/2.], [WINDOW_WIDTH/2., WINDOW_HEIGHT/2.], [WINDOW_WIDTH/2. + 350., WINDOW_HEIGHT/2.],]

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                angle1 += 5
            elif event.key == pygame.K_a:
                angle1 -= 5   
            elif event.key == pygame.K_w:
                angle2 += 5
            elif event.key == pygame.K_s:
                angle2 -= 5
            elif event.key == pygame.K_UP:
                Arm_ang += 5
            elif event.key == pygame.K_DOWN:
                Arm_ang -= 5
                
    screen.fill((255,255,255))
    draw_robot(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 100, 200)
    
    i = 0
    for center1, arm in zip(centers, arms):
        M = np.eye(3) @ Tmat(center1[0], center1[1]) @ Rmat(angle1) @ Tmat(0, -height1/2.)

        for segment in arm:
            draw(M, segment, (255, 0, 0))
            M2 = M @ Tmat(width1, 0) @ Tmat(0, height1/2.)
            pygame.draw.circle(screen, (0,0,0), M2[0:2, 2],10)
            M = M @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Tmat(gap, 0) @ Rmat(angle2) @ Tmat(0, -height1/2.)
            M3 = M2 @ Tmat(gap, 0)
            pygame.draw.line(screen, (0,0,0), M2[0:2, 2], M3[0:2, 2], 10)
            pygame.draw.circle(screen, (0,0,0), M2[0:2, 2],10)
            pygame.draw.circle(screen, (0,0,0), M3[0:2, 2],10)
            
        M_U = M3 @ Rmat(90+Arm_ang) @ Tmat(gap, 0) 
        M_D = M3 @ Rmat(-Arm_ang-90) @ Tmat(gap, 0)     
        M_U_2 = M_U @ Rmat(-Arm_ang-90) @ Tmat(gap, 0)
        M_D_2 = M_D @ Rmat(90+Arm_ang) @ Tmat(gap, 0) 
        
        pygame.draw.line(screen, (0,0,0), M3[0:2, 2], M_U[0:2, 2], 10)
        pygame.draw.line(screen, (0,0,0), M3[0:2, 2], M_D[0:2, 2], 10)
        pygame.draw.line(screen, (0,0,0), M_U[0:2, 2], M_U_2[0:2, 2], 10)
        pygame.draw.line(screen, (0,0,0), M_D[0:2, 2], M_D_2[0:2, 2], 10)

        i += 1
            
    # update screen
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()

# 게임 종료
pygame.quit()