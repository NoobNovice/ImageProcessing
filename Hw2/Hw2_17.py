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

# origin kernel is center and size 3 x 3 only 
def blur_img(metrix_img, kernel):
    add_size = 1
    img = [[0] * (len(metrix_img) - (add_size * 2)) for i in range((len(metrix_img) - (add_size * 2)))]
    for i in range(len(img)):
        for k in range(len(img)):
            img[i][k] = metrix_img[i][k] * kernel[0][0]
            img[i][k]  += metrix_img[i][k+1] * kernel[0][1]
            img[i][k]  += metrix_img[i][k+2] * kernel[0][2]

            img[i][k]  += metrix_img[i+1][k] * kernel[1][0] 
            img[i][k]  += metrix_img[i+1][k+1] * kernel[1][1]
            img[i][k]  += metrix_img[i+1][k+2] * kernel[1][2]

            img[i][k]  += metrix_img[i+2][k] * kernel[2][0] 
            img[i][k]  += metrix_img[i+2][k+1] * kernel[2][1]
            img[i][k]  += metrix_img[i+2][k+2] * kernel[2][2]
            img[i][k] = round(img[i][k])
    return img

def padboth_img(metrix_img, add_size):
    img = [[0] * (len(metrix_img) + (add_size * 2)) for i in range((len(metrix_img) + (add_size * 2)))]
    for i in range(len(metrix_img)):
        for k in range(len(metrix_img)):
            img[add_size + i][add_size + k] = metrix_img[i][k]
    return img

def re_padboth(metrix_img, re_size):
    img = [[0] * (len(metrix_img) - (re_size * 2)) for i in range((len(metrix_img) - (re_size * 2)))]
    for i in range(len(img)):
        for k in range(len(img)):
            img[i][k] = metrix_img[i + re_size][k + re_size]
    return img

def padpost_img(metrix_img, add_size):
    img = [[0] * (len(metrix_img) + add_size) for i in range((len(metrix_img) + add_size))]
    for i in range(len(metrix_img)):
        for k in range(len(metrix_img)):
            img[i][k] = metrix_img[i][k]
    return img

if __name__ == '__main__':
    #=================================================================
    # this code use fourier metrix algebraic (G=FgF and g=F^-1GF^-1).
    # on assumed width and length image is equal (N x N).
    #=================================================================
    dir_path = os.getcwd()

    print("\nRead Image")
    chess_img = get_metrixImage(dir_path + "/Image/Chess.pgm")
    image = cv2.imread(dir_path + "/Image/Chess.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)

    print("\n Blur Image")
    # # Gaussian Blur kernel 3 x 3
    # k = [[1/16, 1/8, 1/16], 
    #      [1/8, 1/4, 1/8], 
    #      [1/16, 1/8, 1/16]]
    k = [[1/9, 1/9, 1/9], 
         [1/9, 1/9, 1/9], 
         [1/9, 1/9, 1/9]]
    pad_chess = padboth_img(chess_img, 1)
    blur_image = blur_img(pad_chess, k)
    save2pgm(blur_image, dir_path + "/Image/ChessBlur.pgm")
    image = cv2.imread(dir_path + "/Image/ChessBlur.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)

    print("\nFourier Transform chess image and kernel image")
    Ng = len(chess_img)
    Fg = get_F(Ng)
    g_center = get_gCenter(chess_img)
    G = fourier_transform(chess_img,Fg)

    pad_k = padpost_img(k, 253)
    Nk = len(pad_k)
    Fk = get_F(Nk)
    k_center = get_gCenter(pad_k)
    K = fourier_transform(pad_k,Fk)
    
    # G multiple K ==> g convolution k
    print("\nMultiple chess_fourier and kernel_fourier")
    K = np.matrix(K)
    G = np.matrix(G)
    G_blur = np.matmul(G,K)
    G_blur = G_blur.getA()

    print(G_blur)

    print("\nInvert Fourier")
    Fg_invert = np.matrix(Fg).T
    g = invert_fourier(G_blur,Fg_invert)
    save2pgm(g,dir_path + "/Image/ChessBlur2.pgm")
    image = cv2.imread(dir_path + "/Image/ChessBlur2.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)

    cv2.destroyAllWindows() 