# -*- coding:utf-8 -*- 
import cv2
import numpy as np
from matplotlib import pyplot as plt
'''
未完成
harris角点轮子
'''
def Get_Harris(file_path):
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
    
    img_calc = np.float32(gaussian)
    height = img_calc.shape[0]
    width = img_calc.shape[1]
    k = 0.05
    hc_count = 0;
    hc_mat = np.matrix([]);
    for x in range(1, width-1):
        for y in range(1, height-1):
            Ix = (img_calc[x+1][y] - 2*img_calc[x][y] + img[x-1][y]) / 2.0
            Iy = (img_calc[x][y+1] - 2*img_calc[x][y]+img[x][y-1]) / 2.0
            MatM = np.array([[Ix**2, Ix*Iy], [Ix*Iy, Iy**2]])
            R = MatM[0][0]*MatM[1][1] - k*((MatM[0][0]+MatM[1][1]) ** 2)
            if R > 0:
                hc_count += 1
                hc_temp = [x,y]
                hc_mat = np.row_stack((hc_mat, hc_temp))
                
    return hc_mat

if __name__ == '__main__':
    img_path = '234_2.jpg'
    Get_Harris(img_path)