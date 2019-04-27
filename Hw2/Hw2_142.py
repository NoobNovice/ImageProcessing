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

def restore_img(img_metrix):
    img = [[None]*len(img_metrix) for i in range(len(img_metrix))]
    for i in range(len(img_metrix)):
        for k in range(len(img_metrix)):
            f = img_metrix[i][k]
            try:
                f = img_metrix[i+1][k] * img_metrix[i-1][k] * img_metrix[i][k+1] * img_metrix[i][k-1]
                f = f ** (1/4)
            except IndexError:
                pass
            img[i][k] = f
    return img

def scaling_img(metrix_img, x_size, y_size):
    img = [[None]*x_size for i in range(y_size)]
    original_sizeX = len(metrix_img[0])
    original_sizeY = len(metrix_img)
    for i in range(len(img)):
        for k in range(len(img[0])):
            xp = round(k / x_size * original_sizeX)
            yp = round(i / y_size * original_sizeY)
            xp = min(xp,original_sizeX - 1)
            yp = min(yp,original_sizeY - 1)
            img[i][k] = metrix_img[yp][xp]
    return img

if __name__ == '__main__':
    #=================================================================
    # this code use fourier metrix algebraic (G=FgF and g=F^-1GF^-1).
    # on assumed width and length image is equal (N x N).
    #=================================================================
    dir_path = os.getcwd()
    print("\nRead Image")
    cross_img = get_metrixImage(dir_path + "/Image/Cross.pgm")
    image = cv2.imread(dir_path + "/Image/Cross.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)

    print("\nScaling Image")
    img = scaling_img(cross_img, 100, 100)
    img = restore_img(img)
    save2pgm(img,dir_path + "/Image/CrossScaling.pgm")
    image = cv2.imread(dir_path + "/Image/CrossScaling.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)

    print("\nFourier Transform cross image")
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    print("\nFind spectrum and save in to spectrum24.pgm")
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    save2pgm(magnitude_spectrum,dir_path + "/Image/spectrum24.pgm")
    image = cv2.imread(dir_path + "/Image/spectrum24.pgm",0)
    cv2.imshow('spectrum',image)
    cv2.waitKey(0)

    print("\nFind phase and save in to phase24.pgm")
    phase = 30*np.angle(fshift)
    save2pgm(phase,dir_path + "/Image/phase24.pgm")
    image = cv2.imread(dir_path + "/Image/phase24.pgm",0)
    cv2.imshow('phase',image)
    cv2.waitKey(0)

    cv2.destroyAllWindows() 