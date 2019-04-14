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

def get_amplitude(fourier_metrix):
    amp = []
    for i in range(len(fourier_metrix)):
        temp = []
        for k in range(len(fourier_metrix)):
            a = round(math.sqrt(fourier_metrix[i][k].real ** 2 + fourier_metrix[i][k].imag ** 2))
            if a > 255:
                a = 255
            temp.append(a)
        amp.append(temp)
    return amp

def get_phase(fourier_metrix):
    phase = []
    for i in range(len(fourier_metrix)):
        temp = []
        for k in range(len(fourier_metrix)):
            p = round(cmath.phase(fourier_metrix[i][k]))
            if p < 0:
                temp.append(0)
            elif p > 255:
                temp.append(255)
            else:
                temp.append(p)
        phase.append(temp)
    return phase

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
    #=================================================================
    # this code use fourier metrix algebraic (G=FgF and g=F^-1GF^-1).
    # on assumed width and length image is equal (N x N).
    #=================================================================
    dir_path = os.getcwd()
    
    print("\nFourier Transform cross image")
    cross_img = get_metrixImage(dir_path + "/Image/Cross.pgm")
    N = len(cross_img)
    F = get_F(N)
    F_invert = np.matrix(F).T
    G = fourier_transform(cross_img,F)

    print("\n#################### Point 2.1.5.1 ####################")
    print("\nFind amplitude")
    amp = get_amplitude(G)

    print("\nInvert Fourier\n")
    re_amp = invert_fourier(amp,F_invert)
    re_amp = restore_img(re_amp)
    save2pgm(re_amp,dir_path + "/Image/restoreAmplitude21.pgm")
    image = cv2.imread(dir_path + "/Image/restoreAmplitude21.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    print("#######################################################")


    print("\n\n#################### Point 2.1.5.2 ####################")
    print("\nFind phase spectra")
    phase = get_phase(G)

    print("\nInvert Fourier\n")
    re_phase = invert_fourier(phase,F_invert)
    re_phase = restore_img(re_phase)
    for i in range(len(re_phase)):
        for k in range(len(re_phase)):
            re_phase[i][k] *= 50
    save2pgm(re_phase,dir_path + "/Image/restorePhase21.pgm")
    image = cv2.imread(dir_path + "/Image/restorePhase21.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    print("#######################################################")

    cv2.destroyAllWindows() 
