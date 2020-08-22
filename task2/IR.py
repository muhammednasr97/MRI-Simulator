import numpy as np
import math


def IR(t1_array,t2_array,Ti):
      
     #Create_array_of_magnetic_field_in_z_direction
    [h,w] = np.shape(t1_array)
    Phantom = np.zeros([h,w,3])
    Phantom[:,:,2] = 1
    
    RF1 = np.array([[1,0,0],[0,math.cos(math.pi),math.sin(math.pi)],[0,-math.sin(math.pi),math.cos(math.pi)]])     # Rotate around x-axis with angle 180
    
    
    for i in range (h):
        for j in range (w):

            IR = np.array([[np.exp(-Ti/t2_array[i,j]),0,0],[0,np.exp(-Ti/t2_array[i,j]),0],[0,0,1-np.exp(-Ti/t1_array[i,j])]])

            Phantom[i, j, :] = np.dot(RF1, Phantom[i, j, :])  # Phantom after rotation around 180 around x-axis

            Phantom[i, j, :] = np.dot(IR , Phantom[i, j, :]) + np.array([0, 0, 1-np.exp(-Ti/t1_array[i,j])])  # Phantom after decay at x-y plane (on y-axis)

                    
    return Phantom[:,:,2]

