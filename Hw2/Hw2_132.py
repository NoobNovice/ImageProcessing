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

def bilinear_interpolation(img_metrix, x, y):
    px0 = math.trunc(x)
    py0 = math.trunc(y)
    xx = x - px0
    yy = y - py0
    f00 = img_metrix[py0][px0]
    f01 = img_metrix[py0][px0 + 1]
    f10 = img_metrix[py0 + 1][px0]
    f11 = img_metrix[py0 + 1][px0 + 1]
    point = [[f00],[f01],[f10],[f11]]
    cp = round((xx * (f10-f00)) + (yy * (f01-f00)) + (xx * yy * (f11+f00-f01-f10)) + f00)
    minimun = abs(point[0][0] - cp)
    index = [0,0]
    for i in range(len(point)):
        for k in range(len(point[0])):
            if abs(point[i][k] - cp) < minimun:
                minimun = abs(point[i][k] - cp)
                index[0] = i
                index[1] = k
    return px0+index[1], py0+index[0]

def rotate_img(img_metrix, radians):
    img = [[255]*len(img_metrix) for i in range(len(img_metrix))]
    point = [0] * 2
    for i in range(len(img_metrix)):
        for k in range(len(img_metrix)):
            if img_metrix[i][k] == 255:
                continue
            xp = k*round(math.cos(radians),2)+i*round(math.sin(radians),2)
            yp = -k*round(math.sin(radians),2)+i*round(math.cos(radians),2)
            x, y = bilinear_interpolation(img_metrix,xp,yp)
            img[y][x] = img_metrix[i][k]
    return img

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

if __name__ == '__main__':
    dir_path = os.getcwd()
    print("\nRead Image")
    cross_img = get_metrixImage(dir_path + "/Image/Cross.pgm")
    image = cv2.imread(dir_path + "/Image/Cross.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)

    print("\nRotate Image")
    img = rotate_img(cross_img, 30)
    img = restore_img(img)
    save2pgm(img,dir_path + "/Image/CrossRotate.pgm")
    image = cv2.imread(dir_path + "/Image/CrossRotate.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)

    print("\nFourier Transform cross image")
    f = np.fft.fft2(cross_img)
    fshift = np.fft.fftshift(f)
    Rf = np.fft.fft2(img)
    Rfshift = np.fft.fftshift(Rf)

    print("\nFind spectrum and save in to phase21.pgm")
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    save2pgm(magnitude_spectrum,dir_path + "/Image/spectrum23_original.pgm")
    Rmagnitude_spectrum = 20*np.log(np.abs(Rfshift))
    save2pgm(Rmagnitude_spectrum,dir_path + "/Image/spectrum23_rotate.pgm")

    image = cv2.imread(dir_path + "/Image/spectrum23_original.pgm",0)
    cv2.imshow('original',image)
    cv2.waitKey(0)
    image = cv2.imread(dir_path + "/Image/spectrum23_rotate.pgm",0)
    cv2.imshow('rotate',image)
    cv2.waitKey(0)

    cv2.destroyAllWindows() 