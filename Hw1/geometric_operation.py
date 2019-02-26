import numpy as np
import os
import cv2
import math

def get_metrixImage(img_input):
    f = open(img_input,'rb')

    data = f.readline()
    img_type = data.decode('utf-8')
    #data = f.readline()  #delete commend image

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
    return

def checkEqual(elements):
    if len(elements) < 1 or len(elements) == elements.count(elements[0]):
        return True
    else:
        return False

def get_gridPoint(grid_metrix):
    result = []
    for i in range(0, len(grid_metrix)):
        for j in range(0, len(grid_metrix[0])):
            if i == 0 and j == 0:
                result.append([j,i])
            elif i == 0 and j == len(grid_metrix[0])-1:
                result.append([j,i])
            elif i == len(grid_metrix)-1 and j == 0:
                result.append([j,i])
            elif i == len(grid_metrix)-1 and j == len(grid_metrix[0])-1:
                result.append([j,i])
            elif grid_metrix[i][j] == 32:
                if i + 1 == len(grid_metrix) or i - 1 < 0 or j + 1 == len(grid_metrix[0]) or j - 1 < 0:
                    result.append([j,i])
                elif i + 1 < len(grid_metrix) or i - 1 >= 0 or j + 1 < len(grid_metrix[0]) or j - 1 >= 0:
                    adjacent = 0
                    left = [grid_metrix[i-1][j-1],grid_metrix[i][j-1],grid_metrix[i+1][j-1]]
                    right = [grid_metrix[i-1][j+1],grid_metrix[i][j+1],grid_metrix[i+1][j+1]]
                    up = [grid_metrix[i-1][j-1],grid_metrix[i-1][j],grid_metrix[i-1][j+1]]
                    down = [grid_metrix[i+1][j-1],grid_metrix[i+1][j],grid_metrix[i+1][j+1]]
                    if checkEqual(left) or checkEqual(right) or checkEqual(up) or checkEqual(down):
                        continue
                    for y in range(-1,2):
                        for x in range(-1,2):
                            if grid_metrix[i - y][j - x] == 32:
                                adjacent += 1
                    if adjacent == 5:
                        result.append([j,i])
            else:
                continue
    return result

def get_distGridPoint():                                                                            
    point = [[0, 0],[16, 0],[32, 0],[48, 0],[64, 0],[80, 0],[96, 0],[112, 0],[128, 0],[144, 0],[160, 0],[176, 0],[192, 0],[208, 0],[224, 0],[240, 0],[255, 0],
		    [0, 16],[16, 16],[32, 16],[48, 16],[64, 16],[80, 16],[97, 16],[115, 18],[130, 18],[146, 18],[161, 18],[176, 16],[192, 16],[208, 16],[224, 16],[240, 16],[255, 16],
		    [0, 32],[16, 32],[32, 32],[48, 32],[66, 33],[85, 35],[105, 38],[120, 40],[136, 42],[150, 43],[164, 42],[177, 38],[193, 34],[208, 32],[225, 32],[240, 32],[255, 32],
		    [0, 48],[16, 48],[32, 48],[51, 49],[71, 50],[93, 53],[112, 57],[128, 60],[141, 63],[155, 65],[165, 65],[178, 62],[192, 56],[207, 50],[224, 47],[240, 48],[255, 48],
		    [0, 64],[16, 64],[34, 64],[57, 66],[80, 66],[100, 67],[118, 72],[132, 77],[144, 80],[155, 84],[167, 85],[178, 83],[190, 80],[205, 74],[223, 66],[240, 64],[255, 64],
		    [0, 80],[16, 80],[38, 78],[62, 77],[84, 77],[103, 81],[119, 84],[132, 89],[144, 95],[155, 100],[165, 103],[177, 103],[188, 100],[203, 94],[221, 85],[239, 80],[255, 80],
		    [0, 96],[18, 95],[41, 92],[65, 90],[86, 89],[103, 91],[118, 95],[131, 102],[142, 109],[151, 114],[161, 117],[172, 119],[184, 117],[200, 112],[218, 104],[238, 97],[255, 96],
		    [0, 112],[18, 110],[42, 106],[65, 103],[84, 101],[100, 102],[114, 105],[127, 112],[136, 119],[145, 126],[154, 130],[167, 132],[180, 132],[196, 128],[215, 122],[238, 114],[255, 112],
		    [0, 128],[19, 125],[43, 119],[64, 114],[82, 111],[96, 111],[110, 114],[121, 120],[130, 128],[138, 135],[149, 140],[161, 143],[176, 143],[193, 141],[213, 136],[238, 130],[255, 128],
		    [0, 144],[19, 141],[41, 135],[61, 128],[77, 124],[92, 123],[103, 124],[112, 130],[122, 136],[133, 141],[142, 150],[156, 153],[172, 155],[190, 154],[213, 150],[236, 145],[255, 144],
		    [0, 160],[18, 158],[39, 151],[57, 143],[73, 139],[86, 137],[97, 137],[107, 141],[116, 147],[127, 154],[138, 160],[153, 164],[171, 166],[190, 165],[214, 163],[238, 161],[255, 160],
		    [0, 176],[16, 176],[36, 170],[54, 161],[69, 155],[82, 152],[93, 152],[103, 155],[113, 160],[125, 165],[138, 171],[153, 175],[172, 177],[193, 178],[218, 177],[239, 175],[255, 176],
		    [0, 192],[16, 192],[34, 189],[52, 182],[66, 175],[79, 170],[90, 169],[101, 172],[112, 174],[125, 179],[139, 183],[156, 187],[175, 189],[199, 191],[221, 191],[240, 192],[255, 192],
		    [0, 208],[16, 208],[32, 208],[50, 204],[65, 198],[78, 192],[90, 190],[102, 189],[114, 192],[128, 195],[143, 198],[161, 202],[182, 205],[204, 206],[224, 208],[240, 208],[255, 208],
		    [0, 224],[16, 224],[32, 224],[48, 223],[64, 220],[79, 215],[93, 213],[106, 212],[120, 212],[135, 214],[151, 217],[170, 220],[189, 222],[208, 224],[224, 224],[240, 224],[255, 224],
		    [0, 240],[16, 240],[32, 240],[48, 240],[64, 240],[80, 238],[96, 239],[111, 235],[125, 235],[142, 236],[159, 237],[175, 238],[192, 240],[208, 240],[224, 240],[240, 240],[255, 240],
		    [0, 255],[15, 255],[32, 255],[48, 255],[64, 255],[80, 255],[96, 255],[112, 255],[128, 255],[144, 255],[160, 255],[176, 255],[192, 255],[208, 255],[224, 255],[240, 255],[255, 255]]
    return point

def get_det(metrix,value):
    if value == 0:
        return 0
    elif math.sqrt(len(metrix)) == 2:
        return ((metrix[0]*metrix[3]) - (metrix[1]*metrix[2])) * value
    else:
        r = round(math.sqrt(len(metrix)))
        sum_metrix = 0
        toggle = 1
        for t in range(r):
            #cut metrix
            cut_metrix = []
            for i in range(r):
                if i == t:
                    continue
                else:
                    for j in range(1,r):  #row and col 0 is mark
                        cut_metrix.append(metrix[(r * i) + j])
            value_pass = toggle * metrix[r*t]
            toggle = toggle * -1
            sum_metrix += (value * get_det(cut_metrix,value_pass))
        return sum_metrix

def inverse_matrix(metrix):
    det_metrix = get_det(metrix,1)
    toggle = 1
    toggle_row = -1
    r = round(math.sqrt(len(metrix)))
    result = [[0]*r for i in range(r)]
    for i in range(r):
        for j in range(r):
            cut_metrix = []
            for k in range(r):
                if k == i:
                    continue
                else:
                    for l in range(r):
                        if l == j:
                            continue
                        else:
                            cut_metrix.append(metrix[(r * k) + l])
            result[j][i] = toggle*get_det(cut_metrix,1)/det_metrix
            toggle = toggle * -1
        toggle = toggle_row
        toggle_row = toggle_row * -1
    return result

def get_w(metrix_inverse,vector_b):
    result = []
    for i in range (4) :
        sum_w = 0
        for j in range (4) :
            sum_w += ( vector_b[j] * metrix_inverse[i][j] )
        result.append(sum_w)
    return result

def control_grid(grid_point,distgrid_point,img_metrix):
    x = [None]*4
    y = [None]*4
    x_prime = [None]*4
    y_prime = [None]*4
    result = [[0 for i in range(len(img_metrix))] for j in range(len(img_metrix[0]))]
    for i in range (16):
        for j in range (16):
            row = 17 * i
            x[0] = grid_point[row+j][0]
            x[1] = grid_point[row+j+1][0]
            x[2] = grid_point[row+17+j][0]
            x[3] = grid_point[row+17+j+1][0]
            y[0] = grid_point[row+j][1]
            y[1] = grid_point[row+j+1][1]
            y[2] = grid_point[row+17+j][1]
            y[3] = grid_point[row+17+j+1][1]

            x_prime[0] = distgrid_point[row+j][0]
            x_prime[1] = distgrid_point[row+j+1][0]
            x_prime[2] = distgrid_point[row+17+j][0]
            x_prime[3] = distgrid_point[row+17+j+1][0]
            vector_x = [x_prime[0],x_prime[1],x_prime[2],x_prime[3]]
            y_prime[0] = distgrid_point[row+j][1]
            y_prime[1] = distgrid_point[row+j+1][1]
            y_prime[2] = distgrid_point[row+17+j][1]
            y_prime[3] = distgrid_point[row+17+j+1][1]
            vector_y = [y_prime[0],y_prime[1],y_prime[2],y_prime[3]]

            # vector_w = metrix_inverse * vector_x or vector_y 
            metrix = [x[0],y[0],x[0]*y[0],1,
                      x[1],y[1],x[1]*y[1],1,
                      x[2],y[2],x[2]*y[2],1,
                      x[3],y[3],x[3]*y[3],1]
            metrix_inverse = inverse_matrix(metrix)

            #find w1,w2,w3,w4 in x
            wx = get_w(metrix_inverse,vector_x)
            #find w5,w6,w7,w8 in x
            wy = get_w(metrix_inverse,vector_y)

            for py in range(y[0],y[2]):
                for px in range(x[0],x[1]):
                    xx = int(round(wx[0]*px + wx[1]*py + wx[2]*px*py + wx[3]))
                    yy = int(round(wy[0]*px + wy[1]*py + wy[2]*px*py + wy[3]))
                    result[py][px] = img_metrix[yy][xx]
    return result

if __name__ == '__main__':
    dir_path = os.getcwd()
    # print("\nread image")
    # img = get_metrixImage(dir_path + "/Image/distlenna.pgm")
    # print("\nread grid")
    # grid = get_metrixImage(dir_path + "/Image/grid.pgm")
    # dis_grid = get_metrixImage(dir_path + "/Image/distgrid.pgm")
    # print("\nfind grid point")
    # grid_point = get_gridPoint(grid)
    # print("\ncontrol grid")
    # r = control_grid(grid_point,get_distGridPoint(),img)
    # save2pgm(r,dir_path + "/Image/grid_convert.pgm")

    # image1 = cv2.imread(dir_path + "/Image/grid_convert.pgm",0)
    # image2 = cv2.imread(dir_path + "/Image/lenna_re.pgm",0)
    # res = np.hstack((image1, image2))
    # cv2.imshow('image',res)
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 