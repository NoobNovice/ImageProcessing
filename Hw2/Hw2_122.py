import os
import cv2
import math
import cmath
import numpy as np

def get_metrixImage(img_input):
    f = open(img_input,'rb')

    data = f.readline()
    img_type = data.decode('utf-8')

    data = f.readline()  #delete commend image

    data = f.readline()
    size = data.decode('utf-8')
    row,col = size.split(" ")
    row = int(row)
    col = int(col)

    data = f.readline()
    Dmax = int(data.decode('utf-8'))

    metrix = []  #init histogram
    for y in range(0, row):
        temp = []
        for x in range(0,col):
            data = f.read(1)
            temp.append(ord(data))
        metrix.append(temp)
    return metrix

def save2pgm(img_metrix,file_name):
    row = len(img_metrix)
    col = len(img_metrix[0])
    f = open(file_name,'w',encoding="ISO-8859-1")
    f.write("P5\r")
    f.write("#\r")
    f.write(str(row)+" "+str(col)+"\r")
    f.write("255\r")
    for i in range(row):
        for j in range(col):
            if img_metrix[i][j] < 0:
                f.write(chr(0))
            elif img_metrix[i][j] > 255:
                f.write((chr(255)))
            else:
                f.write(chr(int(img_metrix[i][j])))
    f.close()
    return

def shift_fourier(feqc_metrix,x,y):
    result = []
    for i in range(len(feqc_metrix)):
        temp = []
        for k in range(len(feqc_metrix)):
            temp.append(feqc_metrix[i][k] * cmath.exp(-2j*cmath.pi*((x*k+y*i)/len(feqc_metrix))))
        result.append(temp)
    return result

if __name__ == '__main__':
    dir_path = os.getcwd()

    print("\nRead Image")
    img = cv2.imread(dir_path + '/Image/Cross.pgm',0)

    print("\nFourier Transform cross image")
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    fshitf_20_30 = shift_fourier(fshift,20,30) #  shitf g with e^(-2jPi(20x/200+30y/200))

    print("\nInvert Fourier")
    f_ishift = np.fft.ifftshift(fshitf_20_30)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    save2pgm(img_back,dir_path + "/Image/CrossShitf.pgm")

    image = cv2.imread(dir_path + "/Image/Cross.pgm",0)
    cv2.imshow('before',image)
    cv2.waitKey(0)
    image_shitf = cv2.imread(dir_path + "/Image/CrossShitf.pgm",0)
    cv2.imshow('after',image_shitf)
    cv2.waitKey(0)

    cv2.destroyAllWindows()