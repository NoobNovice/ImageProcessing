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

def get_F(N):
    F = [[0]*N for i in range(N)]
    for i in range(N):
        for k in range(N):
            F[i][k]=(1/math.sqrt(N)) * cmath.exp((-2j*cmath.pi*i*k)/N)
    return F

def fourier_transform(metrix_img,F):
    mF = np.matrix(F)
    mg = np.matrix(metrix_img)
    mFg = np.matmul(mF,mg)
    G = np.matmul(mFg,mF)
    return G.getA()

def invert_fourier(metrix_fourier,F_invert):
    mF_invert = np.matrix(F_invert)
    mG = np.matrix(metrix_fourier)
    mF_invertG = np.matmul(mF_invert,mG)
    g = np.matmul(mF_invertG,mF_invert)
    real_g = []
    g = g.getA()
    for i in range(len(g)):
        temp = []
        for k in range(len(g)):
            temp.append(abs(round(g[i][k].real)))
        real_g.append(temp)
    return real_g

def get_gCenter(metrix_img):
    g_center = [[0]*len(metrix_img) for i in range(len(metrix_img))]
    for i in range(len(metrix_img)):
        for k in range(len(metrix_img)):
            g_center[i][k] = metrix_img[i][k]*((-1) ** (i+k)) 
    return g_center

def shift_fourier(feqc_metrix,x,y):
    result = []
    for i in range(len(feqc_metrix)):
        temp = []
        for k in range(len(feqc_metrix)):
            temp.append(feqc_metrix[i][k] * cmath.exp(-2j*cmath.pi*((x*k+y*i)/len(feqc_metrix))))
        result.append(temp)
    return result

if __name__ == '__main__':
    #=================================================================
    # this code use fourier metrix algebraic (G=FgF and g=F^-1GF^-1).
    # on assumed width and length image is equal (N x N).
    #=================================================================
    dir_path = os.getcwd()
    print("\nRead Image")
    cross_img = get_metrixImage(dir_path + "/Image/Cross.pgm")

    print("\nFourier Transform cross image")
    N = len(cross_img)
    F = get_F(N)
    g_center = get_gCenter(cross_img)
    G = fourier_transform(g_center,F)

    G_shitf = shift_fourier(G,20,30) #  shitf g with e^(-2jPi(20x/200+30y/200))

    print("\nInvert Fourier")
    F_invert = np.matrix(F).T
    g = invert_fourier(G_shitf,F_invert)
    print(g)
    save2pgm(g,dir_path + "/Image/Cross20_30.pgm")
    image = cv2.imread(dir_path + "/Image/Cross20_30.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)

    cv2.destroyAllWindows() 
