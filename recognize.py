# -*- coding:utf-8 -*-  
import cv2
import os
import numpy as np
'''
用来识别特征
'''
def calc_feature(filename):
    img = cv2.imread(filename)
    height = img.shape[0]
    width = img.shape[1]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[255,0,0]

    xsum = 0.0
    ysum = 0.0
    counts = 0.0

    for i in range(0,height):
        for j in range(0,width):
            if img[i,j][0] == 255 and img[i,j][1] == 0 and img[i,j][2] == 0:
                xsum += i
                ysum += j
                counts += 1.0

    feature = np.array([xsum/counts, ysum/counts])
    return feature
    
if __name__ == '__main__':
    test_fea = calc_feature('CA.jpg')
    ChangAn_F = np.array([16.135315, 18.034494])
    Hyundai_F = np.array([14.053700, 24.397613])
    Chery_F = np.array([11.974086, 29.901463])
    Valks_F = np.array([26.971423, 25.067580])
    Gold_F = np.array([22.747977, 16.299428])
    JAC_F = np.array([21.000401, 74.030581])
    
    dis_CA = (test_fea[0]-ChangAn_F[0]) ** 2 + (test_fea[1]-ChangAn_F[1]) ** 2
    #print dis_CA
    dis_Ch = (test_fea[0]-Chery_F[0]) ** 2 + (test_fea[1]-Chery_F[1]) ** 2
    #print dis_Ch
    dis_Hd = (test_fea[0]-Hyundai_F[0]) ** 2 + (test_fea[1]-Hyundai_F[1]) ** 2
    #print dis_Hd
    dis_Vw = (test_fea[0]-Valks_F[0]) ** 2 + (test_fea[1]-Valks_F[1]) ** 2
    #print dis_Vw
    dis_G = (test_fea[0]-Gold_F[0]) ** 2 + (test_fea[1]-Gold_F[1]) ** 2
    #print dis_G
    
    cars = ['ChangAn', 'Chery', 'Hyundai', 'Valkswagen', 'Golden']
    distance = [dis_CA, dis_Ch, dis_Hd, dis_Vw, dis_G]
    Best_Fit = distance.index(min(distance))
    print 'This car might be %s' %cars[Best_Fit]
    