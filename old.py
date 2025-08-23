import pygame
import math

pygame.init()

SC_WIDTH = 800
SC_HEIGHT = 600

screen = pygame.display.set_mode((SC_WIDTH,SC_HEIGHT))
pygame.display.set_caption("The 3D ENGINE")

running = True
Fov = [120,75]

# ENTITIES
camera_pos = [0,0,-5]

# CUBE
Nodes = [[-1,-1, 1],[-1,-1, -1],[-1,1, 1],[-1,1, -1],[1,-1, 1],[1,-1, -1],[1,1, 1],[1,1, -1]]
Lines = [[0,1],[0,2],[2,3],[1,3],[4,6],[4,5],[6,7],[5,7],[3,7],[2,6],[0,4],[1,5]]
# pyramid
Nodes2 = [[0,1,0],[-1,-1,-1],[-1,-1,1],[1,-1,-1],[1,-1,1]]
Lines2 = [[0,1],[0,2],[0,3],[0,4],[1,2],[3,4],[1,3],[2,4]]

def rotate_y(nodes, rot, center):
    nodes_2 = [[0,0,0]]*len(nodes)
    for n in nodes:
        r = math.sqrt((center[0]-n[0])**2+(center[2]-n[2])**2)
        if (n[0]-center[0]) > 0:
            ro = math.atan((n[2]-center[2])/(n[0]-center[0]))
        elif (n[0]-center[0]) < 0:
            ro = math.pi + math.atan((n[2]-center[2])/(n[0]-center[0]))
        else:
            if (n[2]-center[2]) > 0:
                ro = math.pi/2
            elif (n[0]-center[0]) < 0:
                ro = - math.pi/2
            else:
                ro = 0
        nodes_2[nodes.index(n)] = [r*math.cos(rot+ro)+center[0],
                                    n[1],
                                    r*math.sin(rot+ro)+center[2]]
    return nodes_2

def get_object_from_file(filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return vertex

def render_nodes(nodes):
    nodes_2 = [[0,0]]*len(nodes)
    for n in nodes:
        nodes_2[nodes.index(n)] = [(((math.atan((n[0]-camera_pos[0])/(n[2]-camera_pos[2]))*(180/3.1415) + 60) * 800) / 120),
                                   (((-math.atan((n[1]-camera_pos[1])/(n[2]-camera_pos[2]))*(180/3.1415) + 42) * 600) / 85)]

    return nodes_2
# nodesCar = get_object_from_file("Car Obj.obj")
clock = pygame.time.Clock()
rot = 0
while running:

    #### EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    '''
    RNodes = render_nodes(NodesC)
    for dot in RNodes:
        pygame.draw.circle(screen,(0,255,0), (dot[0],dot[1]),3)
    for j in range(50):
        for i in range(99):
            pygame.draw.line(screen,(0,255,0), RNodes[j*100+i], RNodes[j*100+i+1])
    '''
    
    
    RNodes = rotate_y(Nodes,rot,(0,0,0))
    RENodes = render_nodes(RNodes)

    for line in Lines:
        pygame.draw.line(screen,(0,255,0), RENodes[line[0]], RENodes[line[1]])
    
    '''

    RNodes = rotate_y(Nodes2,-rot,(0,0,0))
    RENodes = render_nodes(RNodes)

    for line in Lines2:
        pygame.draw.line(screen,(0,0,255), RENodes[line[0]], RENodes[line[1]])
    '''
    for i in range(15):
        theta = (i * math.pi)/15 - math.pi / 2
        theta_p = ((i+1) * math.pi)/15 - math.pi / 2
        for j in range(20):
            phi  = (j * math.pi * 2)/20
            phi_p = ((j + 1) * math.pi * 2)/20
            node1 = render_nodes(rotate_y([[math.cos(theta)*math.cos(phi),math.sin(theta),math.cos(theta)*math.sin(phi)]],-rot,(0,0,0)))
            node2 = render_nodes(rotate_y([[math.cos(theta)*math.cos(phi_p),math.sin(theta),math.cos(theta)*math.sin(phi_p)]],-rot,(0,0,0)))
            node3 = render_nodes(rotate_y([[math.cos(theta_p)*math.cos(phi),math.sin(theta_p),math.cos(theta_p)*math.sin(phi)]],-rot,(0,0,0)))
            pygame.draw.line(screen,(0,0,255), (node1[0][0], node1[0][1]),(node2[0][0], node2[0][1]))
            pygame.draw.line(screen,(0,0,255), (node1[0][0], node1[0][1]),(node3[0][0], node3[0][1]))
    '''
    rnodesCar = render_nodes(rotate_y(nodesCar,rot,(0,0,0)))
    for pos in rnodesCar:
        pygame.draw.circle(screen, (255,0,0), pos, 2)
    '''
    
    pygame.display.flip()
    clock.tick(30)
    rot += 0.1
    if rot >= 2*math.pi:
        rot = 0
    

pygame.quit()