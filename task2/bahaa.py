import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
  
# Load an image in grayscale
img = cv2.imread('Phantom32.jpg', 0)
TE = 20
TR = 1900

arr = np.asarray(img)
row, col = arr.shape
t1_array = np.ones((row, col))  
t2_array = np.ones((row, col))

for i in range(row):
    for j in range(col):
        if(arr[i][j] >= 0) & (arr[i][j] < 50):
            t1_array[i][j] = 250     
            t2_array[i][j] = 70
            
        elif (arr[i][j] >= 50) & (arr[i][j] < 220):
            t1_array[i][j] = 400    
            t2_array[i][j] = 120
        
        elif (arr[i][j] >= 220):
            t1_array[i][j] = 320    
            t2_array[i][j] = 90
        
        

theta = 0.50*np.pi   
spinVector = np.array([[0], [0], [1]])
phSize = 64
total_theta = 0
sum = 0

phantom=np.zeros((row,col,3))            # Creating phantom as a 3D array, each pixel has a vector
KSpace = np.zeros((row, col), dtype=np.complex) # creating K-space


for i in range(row):                     # All vectors are [0]
    for j in range(col):                 #                 [0]
        phantom[i,j,2]=1                 #                 [1]

# rotation matrix around y-axis
RF=([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta),0,np.cos(theta)]]) 

for r in range(row):  # k-space row
    for i in range(row): 
        for j in range(col):
            dec = np.exp(-TE/t2_array[i,j])   #Decay equation 
            phantom[i,j,:] = np.dot(RF,phantom[i,j,:]) # Phantom after rotation around y-axis
            phantom[i,j,:] = np.dot(dec,phantom[i,j,:]) # Phantom after decay at x-y plane (on x-axis)
    
    for c in range(col):
        Gx_step=((2*math.pi)/row)*r     #Frequency encodind
        Gy_step=((2*math.pi)/col)*c     #Phase encodind
        for ph_row in range(row): 
            for ph_col in range(col):
                Toltal_theta=(Gx_step*ph_row)+(Gy_step*ph_col)        
                
                Mag=math.sqrt(((phantom[ph_row,ph_col,0])*(phantom[ph_row,ph_col,0]))+((phantom[ph_row,ph_col,1])*(phantom[ph_row,ph_col,1])))
                
                KSpace[r,c] = KSpace[r,c]+(Mag*np.exp(-1j*Toltal_theta))
       
        
    for ph_rowtr in range(row):                # each pixel in phantom
        for ph_coltr in range(col):            
            phantom[ph_rowtr,ph_coltr,0]=0     # zero component at x-axis
            phantom[ph_rowtr,ph_coltr,1]=0     # zero component at y-axis
            # recovery on z-axis
            phantom[ph_rowtr,ph_coltr,2]=((phantom[ph_rowtr,ph_coltr,2])*np.exp(-TR/t1_array[i,j])) + (1-np.exp(-TR/t1_array[ph_rowtr,ph_coltr]))

output = np.absolute(np.fft.ifft2(KSpace))    # simple ifft2 to bring back the image.
fshift = np.fft.fftshift(KSpace)
KSpaceOutput = 20*np.log(np.abs(fshift))
plt.subplot(121),plt.imshow(KSpaceOutput, cmap = 'gray')
plt.title('K-space'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(output, cmap = 'gray')
plt.title('Reconstructed image'), plt.xticks([]), plt.yticks([])
plt.show()