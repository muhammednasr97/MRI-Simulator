from random import randint
import time
import sys
import math
import numpy as np
import cv2
from PIL.ImageQt import ImageQt
import pyqtgraph as pg
from PIL import ImageEnhance,Image
from qimage2ndarray import gray2qimage  
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog,QVBoxLayout,QMainWindow,QMessageBox,QInputDialog,QGraphicsView
from PyQt5.QtGui import QPixmap,QPen,QPainter,QBrush,QColor

def rotate(theta,phantom):
        RF=([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta),0,np.cos(theta)]]) 
        phantom=np.dot(RF,phantom) 
        return phantom
        
def decay(phantom,TE,T2):
        dec=np.exp(-TE/T2)
        phantom=np.dot(dec,phantom)
        return phantom
    
def recovery(phantom,row,col,TR,T1):
        for ph_rowtr in range(row): 
            for ph_coltr in range(col):
                phantom[ph_rowtr,ph_coltr,0]=0
                phantom[ph_rowtr,ph_coltr,1]=0
                phantom[ph_rowtr,ph_coltr,2]=((phantom[ph_rowtr,ph_coltr,2])*np.exp(-TR/T1[ph_rowtr,ph_coltr]))+(1-np.exp(-TR/T1[ph_rowtr,ph_coltr]))
        return phantom 
    
def rotate_decay(phantom,theta,TE,T2,row,col):
        for i in range(row): 
            for j in range(col):
                phantom[i,j,:]=rotate(theta,phantom[i,j,:]) 
                phantom[i,j,:]=decay(phantom[i,j,:],TE,T2[i,j]) 
        return phantom  
    
def startup_cycle(phantom,theta,TE,TR,T2,T1,row,col,n):
        for r in range(n):  #rows
            phantom=rotate_decay(phantom,theta,TE,T2,row,col)
            phantom=recovery(phantom,row,col,TR,T1)  
        return phantom

def spin_Echo(row,col,te,tr,image_shape0,image_shape1,T2,T1,phantom,Gy,Start_up):

        theta=np.radians(90) 

        Kspace_SE=np.zeros((image_shape0,image_shape1),dtype=np.complex_)
        if (Start_up==True):
            phantom=startup_cycle(phantom,theta,te,tr,T2,T1,row,col,15)

        for r in range(Kspace_SE.shape[0]):  #rows
            phantom=rotate_decay(phantom,np.radians(90),te/2,T2,row,col)
            phantom=recovery(phantom,row,col,te/2,T1)
            phantom=rotate_decay(phantom,np.radians(180),te/2,T2,row,col)
            for c in range(Kspace_SE.shape[1]):
  
                Gx_step=((2*math.pi)/row)*r
                Gy_step=(Gy/col)*c
                for ph_row in range(row): 
                    for ph_col in range(col):
                        Toltal_theta=(Gx_step*ph_row)+(Gy_step*ph_col)
                        Mag=math.sqrt(((phantom[ph_row,ph_col,0])*(phantom[ph_row,ph_col,0]))+((phantom[ph_row,ph_col,1])*(phantom[ph_row,ph_col,1])))
                        
                        
                        Kspace_SE[r,c]=Kspace_SE[r,c]+(Mag*np.exp(-1j*Toltal_theta))
                        QApplication.processEvents()
                       
                QApplication.processEvents()
                
            phantom=recovery(phantom,row,col,tr,T1)  
            
            QApplication.processEvents()
           
        
        iff= np.fft.ifft2(Kspace_SE)

        inverse_array=np.abs(iff)
        inverse_array = (inverse_array - np.amin(inverse_array)) * 255/ (np.amax(inverse_array) - np.amin(inverse_array))
        inverse_img=gray2qimage(inverse_array)
        imgreconstruction = inverse_img#piexel of image
        
        return imgreconstruction
        
def GRE(theta,row,col,te,tr,image_shape0,image_shape1,T2,T1,phantom,Gy,Start_up):
        
        Kspace=np.zeros((image_shape0,image_shape1),dtype=np.complex_) 
        
        if (Start_up==True):
            phantom=startup_cycle(phantom,theta,te,tr,T2,T1,row,col,15)

        
        for r in range(Kspace.shape[0]):  #rows
            phantom=rotate_decay(phantom,theta,te,T2,row,col)
            
            for c in range(Kspace.shape[1]): #columns
                Gx_step=((2*math.pi)/row)*r
                Gy_step=((Gy)/col)*c
                for ph_row in range(row): 
                    for ph_col in range(col):
                        Toltal_theta=(Gx_step*ph_row)+(Gy_step*ph_col)
                        Mag=math.sqrt(((phantom[ph_row,ph_col,0])*(phantom[ph_row,ph_col,0]))+((phantom[ph_row,ph_col,1])*(phantom[ph_row,ph_col,1])))

                        Kspace[r,c]=Kspace[r,c]+(Mag*np.exp(-1j*Toltal_theta))
                        QApplication.processEvents()
                QApplication.processEvents()
            phantom=recovery(phantom,row,col,tr,T1)        
            QApplication.processEvents()
        
        iff= np.fft.ifft2(Kspace)
        
        inverse_array=np.abs(iff)
        inverse_array = (inverse_array - np.amin(inverse_array)) * 255/ (np.amax(inverse_array) - np.amin(inverse_array))
        inverse_img=gray2qimage(inverse_array)
        imgreconstruction = inverse_img
        return imgreconstruction
def SSFP(theta,row,col,te,tr,image_shape0,image_shape1,T2,T1,phantom,Gy,Start_up):
        
        Kspace_ssfp=np.zeros((image_shape0,image_shape1),dtype=np.complex_) 
        
        if (Start_up==True):
            phantom=startup_cycle(phantom,theta/2,te,tr,T2,T1,row,col,1)

        phantom=startup_cycle(phantom,theta,te,tr,T2,T1,row,col,15)
        
        for r in range(Kspace_ssfp.shape[0]):  #rows
            theta=-theta
            phantom=rotate_decay(phantom,theta,te,T2,row,col)
            for c in range(Kspace_ssfp.shape[1]):
                Gx_step=((2*math.pi)/row)*r
                Gy_step=(Gy/col)*c
                for ph_row in range(row): 
                    for ph_col in range(col):
                        Toltal_theta=(Gx_step*ph_row)+(Gy_step*ph_col)
                        Mag=math.sqrt(((phantom[ph_row,ph_col,0])*(phantom[ph_row,ph_col,0]))+((phantom[ph_row,ph_col,1])*(phantom[ph_row,ph_col,1])))

                        Kspace_ssfp[r,c]=Kspace_ssfp[r,c]+(Mag*np.exp(-1j*Toltal_theta))
                        QApplication.processEvents()

                QApplication.processEvents()
              
            print(theta)
            phantom=recovery(phantom,row,col,tr,T1)
            
            QApplication.processEvents()
        iff= np.fft.ifft2(Kspace_ssfp)

        #print(iff)
        inverse_array=np.abs(iff)
        inverse_array = (inverse_array - np.amin(inverse_array)) * 255/ (np.amax(inverse_array) - np.amin(inverse_array))
        inverse_img=gray2qimage(inverse_array)
        imgreconstruction = inverse_img
        return imgreconstruction

