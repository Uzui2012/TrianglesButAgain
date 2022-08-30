from math import sqrt
import sys, pygame
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

def render(lines, points):
    screen=pygame.display.set_mode((width,height))
    screen.fill(screen_color)
    
    for i in points:
        pygame.draw.circle(screen, dots_color, i, 1)
    
    pygame.draw.circle(screen, c_color, points[-1], calc_dist(points[-1], points[0]))
    pygame.draw.circle(screen, dot_color, points[0], 2)
    pygame.draw.circle(screen, dot_color, points[1], 2)
    pygame.draw.circle(screen, dot_color, points[2], 2)

    for line in lines:
        pygame.draw.lines(screen, dot_color, line.p1, line.p2)

    pygame.display.flip()
    
    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)

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
        print([a, b, c])

def main():
    lines = []
    x = rand_points(500)
    x = sort_points(x)
    x_0 = x[0]
    x_j = x[1]
    x_k = x[2]
    for i in x[2:]:
        if calc_dist(calc_circum_circle_centre(x_0, x_j, i), x_0) < calc_dist(calc_circum_circle_centre(x_0, x_j, x_k), x_0):
            x_k = i
    c = calc_circum_circle_centre(x_0, x_j, x_k)
    x.append(c)
    
    
    render(lines, x)
main()