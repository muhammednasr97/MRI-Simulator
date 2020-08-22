# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt


img = cv2.imread('128A.png',0)
rows, cols = img.shape
for i in range(int(cols/2)):
    crow,ccol = rows/2 , cols/2
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    fshift[int(i):int(2*crow-i-1),int(i):int(2*ccol-i-1)] = 0
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    magnitude_spectrum = np.asarray(magnitude_spectrum,dtype=np.uint8)
    cv2.imshow('magnitude_spectrum', magnitude_spectrum)
    cv2.waitKey(250)
    cv2.destroyAllWindows()
































#import cv2
#import numpy as np
#from matplotlib import pyplot as plt
#
#img = cv2.imread('128A.png',0)
#f = np.fft.fft2(img)
#fshift = np.fft.fftshift(f)
#magnitude_spectrum = 20*np.log(np.abs(fshift))
#
#plt.subplot(121),plt.imshow(img, cmap = 'gray')
#plt.title('Input Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
#plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
#plt.show()
#
#rows, cols = img.shape
#crow,ccol = rows/2 , cols/2
#fshift[int(crow-30):int(crow+30), int(ccol-30):int(ccol+30)] = 0
#f_ishift = np.fft.ifftshift(fshift)
#img_back = np.fft.ifft2(f_ishift)
#img_back = np.abs(img_back)
#
#plt.subplot(131),plt.imshow(img, cmap = 'gray')
#plt.title('Input Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(132),plt.imshow(img_back, cmap = 'gray')
#plt.title('Image after HPF'), plt.xticks([]), plt.yticks([])
#plt.subplot(133),plt.imshow(img_back)
#plt.title('Result in JET'), plt.xticks([]), plt.yticks([])

