import matplotlib.pyplot as plt 
import os
import cv2

def get_histogram(img_input):
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

    histogram = [0] * (Dmax + 1)  #init histogram
    for i in range(0, row * col):
        data = f.read(1)
        histogram[ord(data)] += 1
    return histogram

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

def peak_histogram(histogram, threshold):
    result = []
    for i in range(len(histogram)):
        if i != 255:
            if histogram[i] > threshold:
                result.append(i)
    return result

def binary_image(metrix_img, threshold):
    result = [[0]*len(metrix_img[0]) for i in range(len(metrix_img))]
    for y in range(len(metrix_img)):
        for x in range(len(metrix_img[0])):
            if metrix_img[y][x] == threshold:
                result[y][x] = 255
            else: result[y][x] = 0
    return result

def pq_moment(binary_img,p,q):
    result = 0
    for y in range(len(binary_img)):
        for x in range(len(binary_img[0])):
            result += (x**p)*(y**q)*binary_img[y][x]
    return result 

def central_moment(binary_img,p,q,x_hood,y_hood):
    result = 0
    for y in range(len(binary_img)):
        for x in range(len(binary_img[0])):
            result += ((x-x_hood)**p)*((y-y_hood)**q)*binary_img[y][x]  #x_hood = m10/m00 y_hood = m01/m00
    return result        

def normalize_moment(binary_image,p,q,x_hood,y_hood):
    u_pq = central_moment(binary_image,p,q,x_hood,y_hood)
    u_00 = central_moment(binary_image,0,0,x_hood,y_hood)
    return u_pq/(u_00**(((p+q)/2)+1))

def histogram_graph(histogram):
    y = histogram
    plt.title("Histogram")
    plt.xlabel("D")
    plt.ylabel("H(D)")
    plt.plot(y)
    plt.savefig("peak_histogram.png")
    return

if __name__ == '__main__':
    dir_path = os.getcwd()
    histogram = get_histogram(dir_path + '/Image/scaled_shapes.pgm')
    img_metrix = get_metrixImage(dir_path + '/Image/scaled_shapes.pgm')
    peak_histogram = peak_histogram(histogram, 1000)
    histogram_graph(histogram)
    print(peak_histogram)
    for i in range(5):
        p = 2
        q = 0
        bin_img = binary_image(img_metrix,peak_histogram[i])

        m00 = pq_moment(bin_img,0,0)
        m01 = pq_moment(bin_img,0,1)
        m10 = pq_moment(bin_img,1,0)
        x_hood = m10/m00
        y_hood = m01/m00

        u_pq = central_moment(bin_img,p,q,x_hood,y_hood)
        u_qp = central_moment(bin_img,q,p,x_hood,y_hood)
        n_pq = normalize_moment(bin_img,p,q,x_hood,y_hood)
        n_qp = normalize_moment(bin_img,q,p,x_hood,y_hood)
        quantity = n_pq + n_qp
        print(peak_histogram[i])
        print("center of mass:({},{})".format(x_hood,y_hood))
        print("central moment: u{}{} = {} ,u{}{} = {}".format(p,q,u_pq,q,p,u_qp))
        print("quantity:{}\n".format(quantity))
    image = cv2.imread(dir_path + "/Image/scaled_shapes.pgm",0)
    cv2.imshow('image',image)
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 