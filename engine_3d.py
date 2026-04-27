import pygame
import math
import numpy as np

pygame.init()

# These values should not be changed
SC_WIDTH = 800
SC_HEIGHT = 600

screen = pygame.display.set_mode((SC_WIDTH,SC_HEIGHT))
pygame.display.set_caption("The 3D ENGINE")

Fov = [120,75]

# ENTITIES
camera_pos = [0,-5,-8]

''' GEOMETRIES '''

cube_nodes = np.array([[-1,-1, 1],[-1,-1, -1],[-1,1, 1],[-1,1, -1],[1,-1, 1],[1,-1, -1],[1,1, 1],[1,1, -1]])
cube_lines = [[0,1],[0,2],[2,3],[1,3],[4,6],[4,5],[6,7],[5,7],[3,7],[2,6],[0,4],[1,5]]

pyramid_nodes = np.array([[0,1,0],[-1,-1,-1],[-1,-1,1],[1,-1,-1],[1,-1,1]])
pyramid_lines = [[0,1],[0,2],[0,3],[0,4],[1,2],[3,4],[1,3],[2,4]]

def generate_sphere(radius, lat_divisions, lon_divisions):
    nodes = []
    lines = []

    # 1. GENERATE NODES (Vertices)
    # We use lat_divisions + 1 to ensure we hit both the top and bottom poles
    for i in range(lat_divisions + 1):
        theta = (i * math.pi) / lat_divisions - (math.pi / 2)
        
        for j in range(lon_divisions):
            phi = (j * 2 * math.pi) / lon_divisions
            
            # Spherical to Cartesian coordinate conversion
            x = radius * math.cos(theta) * math.cos(phi)
            y = radius * math.sin(theta)
            z = radius * math.cos(theta) * math.sin(phi)
            
            nodes.append([x, y, z])

    # 2. GENERATE LINES (Edges connecting the vertices)
    for i in range(lat_divisions):
        for j in range(lon_divisions):
            # Calculate the 1D index of the current node
            current = i * lon_divisions + j
            
            # Find the next node horizontally (wrapping around the sphere using modulo %)
            next_lon = i * lon_divisions + ((j + 1) % lon_divisions)
            
            # Find the next node vertically (next latitude line)
            next_lat = (i + 1) * lon_divisions + j

            # Add horizontal line
            lines.append([current, next_lon])
            # Add vertical line
            lines.append([current, next_lat])

    # Return nodes as a NumPy array for fast matrix math, and lines as a standard list
    return np.array(nodes), lines

def get_object_from_file(filename):
    vertices = []
    faces = []
    unique_lines = set() # A Python 'set' automatically rejects duplicate entries

    with open(filename) as f:
        for line in f:
            if line.startswith('v '):
                # Grab only X, Y, Z. Removed the + [1] so it works with our 3x3 matrix
                parts = line.split()[1:4]
                vertices.append([float(i) for i in parts])
                
            elif line.startswith('f '):
                # Extract the vertex indices, subtracting 1 to make them 0-based
                faces_ = line.split()[1:]
                face = [int(p.split('/')[0]) - 1 for p in faces_]
                faces.append(face)

    # Convert faces into unique lines
    for face in faces:
        num_vertices = len(face)
        for i in range(num_vertices):
            # Connect current vertex to the next vertex
            # The modulo (%) wraps the last vertex back to the first vertex
            v1 = face[i]
            v2 = face[(i + 1) % num_vertices]
            
            # Sort the indices. This ensures that an edge from 5->7 is treated 
            # exactly the same as an edge from 7->5.
            edge = tuple(sorted((v1, v2)))
            
            # Add to our set. If it already exists, the set ignores it!
            unique_lines.add(edge)

    # Return vertices as a NumPy array (for fast math) and lines as a list
    return np.array(vertices), list(unique_lines)

''' TRANSFORMATIONS '''

def rotate(nodes, rx, ry, rz):

    rot_x = np.array([
        [1, 0, 0],
        [0, np.cos(rx), -np.sin(rx)],
        [0, np.sin(rx), np.cos(rx)]
    ])

    rot_y = np.array([
        [np.cos(ry), 0, np.sin(ry)],
        [0, 1, 0],
        [-np.sin(ry), 0, np.cos(ry)]
    ])

    rot_z = np.array([
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz), np.cos(rz), 0],
        [0, 0, 1]
    ])

    total_rot = rot_z @ rot_y @ rot_x
    
    return nodes @ total_rot

def scale(nodes, axis, scale):
    pass


def render_nodes(nodes): # updated renderer, this one provided by AI is far more efficient and creative, I mean this is interesting
    # 1. Shift the world based on camera position (Vectorized subtraction)
    shifted = nodes - camera_pos
    
    # 2. Extract X, Y, and Z columns into separate fast arrays
    x = shifted[:, 0]
    y = shifted[:, 1]
    z = shifted[:, 2]
    
    # 3. Safety Check: Prevent division by zero
    # If a Z value is exactly 0, nudge it to 0.0001
    z = np.where(z == 0, 0.0001, z)
    
    # 4. Standard Perspective Divide
    # We divide x and y by z, then scale by FOV, and center it on screen
    fov_factor = 400  # Increase this to zoom in, decrease to zoom out
    
    screen_x = (x / z) * fov_factor + (SC_WIDTH / 2)
    screen_y = (y / z) * fov_factor + (SC_HEIGHT / 2)
    
    # 5. Stack the separate X and Y arrays back into a list of [x, y] coordinates
    return np.column_stack((screen_x, screen_y))

clock = pygame.time.Clock()

''' Main Loop '''
running = True

# initial varibles
rot = 0

nodes, lines = get_object_from_file("plant.obj")
nodes = rotate(nodes, math.pi, 0, 0)
'''
nodes, lines = generate_sphere(1, 15, 30)
nodes2 = cube_nodes
'''

while running:

    #### EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    '''
    nodes2 = rotate(nodes2, 0, rot, 0)
    
    rendered_nodes2 = render_nodes(nodes2)
    for line in cube_lines:
        pygame.draw.line(screen,(0,0,255), rendered_nodes2[line[0]], rendered_nodes2[line[1]], 2)
    '''

    nodes = rotate(nodes, 0, rot, 0)

    rendered_nodes = render_nodes(nodes)

    for line in lines:
        pygame.draw.line(screen,(0,255,0), rendered_nodes[line[0]], rendered_nodes[line[1]])
        

    pygame.display.flip()
    clock.tick(60)

    rot = 0.1
    
pygame.quit()