import matplotlib.pyplot as plt 
import os
import cv2

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
            f.write((chr(img_metrix[i][j])))
    f.close()

if __name__ == '__main__':
    dir_path = os.getcwd()
    print("\nread red chanel")
    red_chanel = get_metrixImage(dir_path + '/Image/SanFranPeak_red.pgm')
    print("\nread green chanel")
    green_chanel = get_metrixImage(dir_path + '/Image/SanFranPeak_green.pgm')
    print("\nread blue chanel")
    blue_chanel = get_metrixImage(dir_path + '/Image/SanFranPeak_blue.pgm')

    #excess green: 2g-r-b
    result = [[0]*len(red_chanel[0]) for i in range(len(red_chanel))]
    for i in range(len(red_chanel)):
        for j in range(len(red_chanel[0])):
            temp = (2 * green_chanel[i][j]) - red_chanel[i][j] - blue_chanel[i][j]
            if temp > 255:
                result[i][j] = 255
            elif temp < 0:
                result[i][j] = 0
            else:
                result[i][j] = temp
    save2pgm(result,dir_path + "/Image/SanFranPeak_excessGreen.pgm")
    
    #red-blue difference: r-b
    result = [[0]*len(red_chanel[0]) for i in range(len(red_chanel))]
    for i in range(len(red_chanel)):
        for j in range(len(red_chanel[0])):
            temp = red_chanel[i][j] - blue_chanel[i][j]
            if temp > 255:
                result[i][j] = 255
            elif temp < 0:
                result[i][j] = 0
            else:
                result[i][j] = temp
    save2pgm(result,dir_path + "/Image/SanFranPeak_red-blueDifference.pgm")

    #gray-level intensity: (g + r+ b)/3
    result = [[0]*len(red_chanel[0]) for i in range(len(red_chanel))]
    for i in range(len(red_chanel)):
        for j in range(len(red_chanel[0])):
            temp = round((green_chanel[i][j] + red_chanel[i][j] + blue_chanel[i][j]) / 3)
            if temp > 255:
                result[i][j] = 255
            elif temp < 0:
                result[i][j] = 0
            else:
                result[i][j] = temp
    save2pgm(result,dir_path + "/Image/SanFranPeak_gray-levelIntensity.pgm")

    image = cv2.imread(dir_path + "/Image/SanFranPeak_excessGreen.pgm",0)
    cv2.imshow('excessGreen',image)
    image = cv2.imread(dir_path + "/Image/SanFranPeak_red-blueDifference.pgm",0)
    cv2.imshow('red-blueDifference',image)
    image = cv2.imread(dir_path + "/Image/SanFranPeak_gray-levelIntensity.pgm",0)
    cv2.imshow('gray-levelIntensity',image)
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 