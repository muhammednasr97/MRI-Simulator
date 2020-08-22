import cv2
import numpy as np
from matplotlib import pyplot as plt

def box(cwidth,rwidth,img,imgwidth,imgheight) :
    img[0:rwidth,0:] = 0 
    img[imgheight-rwidth:imgheight,0:] = 0
    img[0:,0:cwidth] = 0
    img[0:,imgwidth-cwidth:imgwidth] = 0
    return img

img = cv2.imread('128A.png',0)
rows, cols = img.shape

for i in range(int(cols/2)):
    crow,ccol = rows/2 , cols/2
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    fshift[int(crow-i):int(crow+i),int(ccol-i):int(ccol+i)] = 0
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    magnitude_spectrum = np.asarray(magnitude_spectrum,dtype=np.uint8)
    cv2.imshow('magnitude_spectrum', magnitude_spectrum)
    cv2.waitKey(250)
    cv2.destroyAllWindows()
#plt.subplot(121),plt.imshow(img, cmap = 'gray')
#plt.title('Input Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
#plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
#plt.show()
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    img_back = np.asarray(img_back,dtype=np.uint8)
    cv2.imshow('img_back', img_back)
    cv2.waitKey(250)
    cv2.destroyAllWindows()
#    image = box(10+i,10+i,img_back,128,128)
#    cv2.imshow('img', image)
#    cv2.waitKey(250)
#    cv2.destroyAllWindows()    

#plt.subplot(131),plt.imshow(img, cmap = 'gray')
#plt.title('Input Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(132),plt.imshow(img_back, cmap = 'gray')
#plt.title('Image after HPF'), plt.xticks([]), plt.yticks([])
#plt.subplot(133),plt.imshow(img_back)
#plt.title('Result in JET'), plt.xticks([]), plt.yticks([])

#plt.show()