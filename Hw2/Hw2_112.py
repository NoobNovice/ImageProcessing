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

if __name__ == '__main__':
    dir_path = os.getcwd()

    print("\nRead Image")
    img = cv2.imread(dir_path + '/Image/Cross.pgm',0)

    print("\nFourier Transform cross image")
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    print("\nFind spectrum and save in to phase21.pgm")
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    save2pgm(magnitude_spectrum,dir_path + "/Image/spectrum21.pgm")
    image = cv2.imread(dir_path + "/Image/spectrum21.pgm",0)
    cv2.imshow('spectrum',image)
    cv2.waitKey(0)

    print("\nFind phase and save in to amplitude21.pgm")
    phase = 30*np.angle(fshift)
    save2pgm(phase,dir_path + "/Image/amplitude21.pgm")
    image = cv2.imread(dir_path + "/Image/amplitude21.pgm",0)
    cv2.imshow('phase',image)
    cv2.waitKey(0)

    print("\nInvert Fourier")
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    save2pgm(img_back,dir_path + "/Image/restoreCross.pgm")
    image = cv2.imread(dir_path + "/Image/restoreCross.pgm",0)
    cv2.imshow('img_back',image)
    cv2.waitKey(0)

    cv2.destroyAllWindows() 