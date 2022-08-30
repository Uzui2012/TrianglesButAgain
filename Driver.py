from math import sqrt
import sys, pygame
from time import sleep
import random
from pygame.locals import*

width = 1000
height = 500
screen_color = (0, 0, 0)
line_color = (255, 0, 0)
c_color = (200, 200, 0)
dot_color = (0, 0, 255)
dots_color = (255, 0, 0)

#seed point x_0 is just the first of this list
def rand_points(num_of_points):
    points = []
    for i in range(num_of_points):
        point = random.randint(100,900), random.randint(100,300)
        points.append(point)
    return points

def calc_dist(p1, p2):
    return sqrt(abs(p1[0]-p2[0])**2 + abs(p1[1]-p2[1])**2)

def sort_points(x):
    x_0 = x[0]
    sorted_x = []
    sorted_x.append(x_0)
    for i in range(len(x)):
        for j in range(len(sorted_x)):
            #print(f" {calc_dist(x[i], x_0)} ,  {calc_dist(sorted_x[j], x_0)}  ")
            if calc_dist(x[i], x_0) < calc_dist(sorted_x[j], x_0):
                sorted_x.insert(j, x[i])
                break
        if not sorted_x.__contains__(x[i]):
            sorted_x.append(x[i])
    return sorted_x

def render(hull, points, x_k):
    screen=pygame.display.set_mode((width,height))
    screen.fill(screen_color)
    
    for i in points:
        pygame.draw.circle(screen, dots_color, i, 1)
    
    #pygame.draw.circle(screen, c_color, points[-1], calc_dist(points[-1], points[0]))
    pygame.draw.circle(screen, dot_color, points[0], 2)
    pygame.draw.circle(screen, dot_color, points[1], 2)
    pygame.draw.circle(screen, dot_color, x_k, 2)

    for tri in hull:
        for line in tri:
            pygame.draw.lines(screen, dot_color, line, line)

    pygame.display.flip()
    
    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
            sleep(5)
            main()

def calc_circum_circle_centre(a, b, c):
    try:
        d = 2*( (a[0])*(b[1]-c[1]) + 
                (b[0])*(c[1]-a[1]) + 
                (c[0])*(a[1]-b[1])   )
        r_x = ( (a[0]*a[0]+a[1]*a[1])*(b[1]-c[1]) + 
                (b[0]*b[0]+b[1]*b[1])*(c[1]-a[1]) + 
                (c[0]*c[0]+c[1]*c[1])*(a[1]-b[1])   ) /d

        r_y = ( (a[0]*a[0]+a[1]*a[1])*(c[0]-b[0]) + 
                (b[0]*b[0]+b[1]*b[1])*(a[0]-c[0]) + 
                (c[0]*c[0]+c[1]*c[1])*(b[0]-a[0])   ) /d

        return (r_x, r_y)
    except:
        pass

def main():
    lines = []
    x = rand_points(25)
    x = sort_points(x)
    x_0 = x[0] #just always the first point
    x_j = x[1] #conversly always the 2nd point
    x_k = x[2]
    for i in x[2:]:
        try:
            if calc_dist(calc_circum_circle_centre(x_0, x_j, i), x_0) < calc_dist(calc_circum_circle_centre(x_0, x_j, x_k), x_0):
                x_k = i
        except:
            pass
    c = calc_circum_circle_centre(x_0, x_j, x_k)
    #x.append(c)

    hull = [ [ (x_0, x_j), (x_j, x_k), (x_k, x_0)] ]




    
    render(hull, x, x_k)

main()