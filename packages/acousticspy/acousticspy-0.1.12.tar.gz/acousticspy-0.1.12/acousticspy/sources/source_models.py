import numpy as np
import scipy.linalg as la
import scipy.special as sp

def baffled_circular_piston_directivity(radius,frequency,theta):
    c = 343
    k = 2*np.pi*frequency/c
    return 2*sp.jv(1,k*radius*np.sin(theta)) / (k*radius*np.sin(theta))

def get_circle_elements(total_area,num_elements):
    
    radius = np.sqrt(total_area/np.pi)
    
    diameter = 2*radius

    square_positions, square_areas = get_square_elements(diameter**2,num_elements*4/np.pi)
    
    areas = np.zeros(1)
    positions = np.zeros([1,3])
    
    # Cut out points that aren't in the circle
    for i in range(len(square_areas)):
        
        if la.norm(square_positions[i,:]) <= radius:
            areas = np.append(areas,square_areas[i])
            positions = np.append(positions,[square_positions[i,:]],axis = 0)
        
    # Removing the zeros at the top of the arrays
    areas = areas[1:]
    positions = positions[1:]
        
    return positions, areas

def get_square_elements(total_area,num_elements):
    
    length = np.sqrt(total_area)
    
    elements_length = int(np.sqrt(num_elements))
    
    dy = length/elements_length
    dz = dy
    
    areas = np.zeros(1)
    positions = np.zeros([1,3])
    
    for i in range(elements_length):
        for j in range(elements_length):
            y = (dy*i - length/2) + dy/2
            z = (dz*j - length/2) + dz/2
            areas = np.append(areas,dy*dz)
            positions = np.append(positions,[[0,y,z]],axis = 0)
            
    # Removing the zeros at the top of the arrays
    areas = areas[1:]
    positions = positions[1:]

    return positions, areas