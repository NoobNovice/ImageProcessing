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

def re_padpost(metrix_img, re_size):
    img = [[0] * (len(metrix_img) - re_size) for i in range((len(metrix_img) - re_size))]
    for i in range(len(img)):
        for k in range(len(img)):
            img[i][k] = metrix_img[i + re_size][k + re_size]
    return img

def mult_point(metrix_fourier, kernal):
    img = [[0] * len(metrix_fourier) for i in range(len(metrix_fourier))]
    for i in range(len(img)):
        for j in range(len(img[0])):
            img[i][j] = metrix_fourier[i][j]*kernal[i][j]
    return img

if __name__ == '__main__':
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
    blur_image = re_padboth(blur_image, 1)
    save2pgm(blur_image, dir_path + "/Image/ChessBlur.pgm")
    image = cv2.imread(dir_path + "/Image/ChessBlur.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0)

    print("\nFourier Transform cross image")
    f = np.fft.fft2(chess_img)
    fshift = np.fft.fftshift(f)
    k = padpost_img(k, 253)
    K = np.fft.fft2(k)
    Kshift = np.fft.fftshift(K)

    # G multiple K ==> g convolution k
    print("\nMultiple chess_fourier and kernel_fourier")
    G_blur = mult_point(fshift, Kshift)

    print("\nInvert Fourier")
    f_ishift = np.fft.ifftshift(G_blur)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    img_back = re_padpost(img_back, 1)
    save2pgm(img_back,dir_path + "/Image/CrossBlur_fourier.pgm")

    image = cv2.imread(dir_path + "/Image/CrossBlur_fourier.pgm",0)
    cv2.imshow('img_back',image)
    cv2.waitKey(0)

    cv2.destroyAllWindows()