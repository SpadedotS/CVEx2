# -*- coding:utf-8 -*-  
import numpy
import cv2
from matplotlib import pyplot as plt
'''
获取车牌和车标的位置
'''
file_path = '231_2.jpg'
img = cv2.imread(file_path)
height = img.shape[0]
width = img.shape[1]
img = img[100:height,0:width]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gaussian = cv2.GaussianBlur(gray, (1, 1), 0, 0, cv2.BORDER_DEFAULT)
median = cv2.medianBlur(gaussian, 5)

sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0,  ksize = 5)
canny = cv2.Canny(median,50,100)

ret, binaryC = cv2.threshold(canny, 100, 255, cv2.THRESH_BINARY)

element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 2))
element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 3))
element3 = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 4))

dilation_C = cv2.dilate(binaryC, element1, iterations = 2)
erosion_C = cv2.erode(dilation_C, element2, iterations = 5)
dilation2_C = cv2.dilate(erosion_C, element3,iterations = 2)

nlx = 0
nly = 0
nlw = 0
nlh = 0

image, contours, hierarchy = cv2.findContours(dilation2_C,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for con in contours:
    x,y,w,h = cv2.boundingRect(con)
    area = w*h
    ratio = float(w)/float(h)
    if area > 3000 and area <10000 and ratio > 3.2 and ratio < 6:
        nlx = x
        nly = y
        nlw = w
        nlh = h
        print area, ratio, nlw, nlh, nlx, nly
        cv2.drawContours(img, [con], 0, (0,255,0), 3)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 4)
        cv2.rectangle(img, (x+10, y-150), (x+w-10, y), (255,0,0),3)
        
for con in contours:
    x,y,w,h = cv2.boundingRect(con)
    area = w*h
    ratio = float(w)/float(h)
    if x > nlx and x < nlx+nlw and y > nly-150 and y < nly and area > 1000 and ratio >1 and ratio < 10:
        print area, ratio, w, h, x, y
        #cv2.drawContours(img, [con], 0, (0,255,0), 3)
        #cv2.rectangle(img, (x+10, y), (x+w-10, y+h), (255,0,255), 3)
        logo_location = img[y-5:y+h, x+5:x+w-10]
write_path = 'D:\\Code\\Python\\CVEx2\\get_logo\\' + file_path + '_logo.jpg'
cv2.imwrite(write_path, logo_location)
plt.subplot(2,4,5),plt.imshow(dilation2_C),plt.title('Mea')
plt.xticks([]),plt.yticks([])
plt.subplot(2,4,6),plt.imshow(img),plt.title('Original')
plt.xticks([]),plt.yticks([])

plt.subplot(2,4,7),plt.imshow(logo_location),plt.title('logo')
plt.xticks([]),plt.yticks([])
plt.subplot(2,4,1),plt.imshow(binaryC,'gray'),plt.title('binaryC')
plt.xticks([]),plt.yticks([])

plt.subplot(2,4,3),plt.imshow(gaussian,'gray'),plt.title('Gaussian')
plt.xticks([]),plt.yticks([])
plt.subplot(2,4,4),plt.imshow(median,'gray'),plt.title('median')
plt.xticks([]),plt.yticks([])
plt.show()