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

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"x: {self.x}   y: {self.y}"

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __str__(self) -> str:
        return f"p1: {self.p1.x, self.p1.y}\np2: {self.p2.x, self.p2.y}\np3: {self.p3.x, self.p3.y}"


#seed point x_0 is just the first of this list
def rand_points(num_of_points):
    points = []
    for i in range(num_of_points):
        point = random.randint(100,900), random.randint(100,300)
        points.append(point)
    return points

def calc_dist(p1, p2):
    return sqrt(abs(p1[0]-p2[0])**2 + abs(p1[1]-p2[1])**2)

def calc_dist_point(p1, p2):
    return sqrt(abs(p1.x-p2.x)**2 + abs(p1.y-p2.y)**2)

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

def sort_for_s(s, target):
    sorted_s = [s[0]]
    for i in range(len(s)):
        for j in range(len(sorted_s)):
            if calc_dist_point(s[i], target) < calc_dist_point(sorted_s[j], target):
                sorted_s.insert(j, s[i])
                break
        if not sorted_s.__contains__(s[i]):
            sorted_s.append(s[i])
    return sorted_s

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

def ccw(p1, p2, p3):
    return (p3[1]-p1[1]) * (p2[0]-p1[0]) > (p2[1]-p1[1]) * (p3[0]-p1[0])

def check_line_intersect(line_1, line_2):
    try:
        return ccw(line_1[0], line_2[0], line_2[1]) != ccw(line_1[1], line_2[0], line_2[1]) and ccw(line_1[0], line_1[1], line_2[0]) != ccw(line_1[0], line_1[1], line_2[1])
    except:
        #co-linear
        return False
def main():
    lines = []
    x = rand_points(100)
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

    # CONVERT ALL TUPLE IN ARRAY TO POINTS
    x_0 = Point(x_0[0], x_0[1])
    x_j = Point(x_j[0], x_j[1])
    x_k = Point(x_k[0], x_k[1])
    for i in range(len(x)):
        temp = Point(x[i][0], x[i][1])
        x.pop(i)
        x.insert(i, temp)


    c = Point(c[0], c[1])
    print(c)
    seed_hull = Triangle(x_0, x_j, x_k)
    print(seed_hull)

    s = []
    for point in x[2:]:        
        if point != x_k:            
            s.append(point)
    print(s)
    s = sort_for_s(s, c)

    for point in s:
        #calculate facets to this point in the hull
        facets = []

        for i in range(len(hull)):
            for j in range(0,3):
                p = hull[i][j][0]
                for tri in hull:
                    for line in tri:
                        if not check_line_intersect(line, (p, point)):
                            hull.append()
                
    
    
    render(hull, x, x_k)

main()