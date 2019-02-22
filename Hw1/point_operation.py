import cv2
import numpy as np
from matplotlib import pyplot as plt 
import os
def histogram_equalization(img_input,img_output):
    image = cv2.imread(img_input,0)
    cv2.imshow('image',image)
    plt.hist(image.flatten(),256,[0,256])
    plt.show()

    equalize = cv2.equalizeHist(image)
    res = np.hstack((image, equalize))  # open new window
    cv2.imshow('image',res)
    plt.hist(equalize.flatten(),256,[0,256])
    plt.show()
    
    cv2.imwrite(img_output,equalize)
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    dir_path = os.getcwd()
    histogram_equalization(dir_path + '/image/SEM256_256.pgm',dir_path + '/image/SEM256_256_edit.pgm')
    histogram_equalization(dir_path + '/image/Cameraman.pgm',dir_path + '/image/CameraBoy_edit.pgm')
