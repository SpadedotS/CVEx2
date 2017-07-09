import cv2
import os
import numpy as np

def GetFileExt(filename):
    (filepath,tempfilename) = os.path.split(filename);
    (shotname,extension) = os.path.splitext(tempfilename);
    return extension
 
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
    all_feature = [0.0,0.0]
    logos = 30.0
    imgs = os.listdir(os.getcwd())
    for img in imgs:
        if GetFileExt(img) == '.jpg':
            all_feature += calc_feature(img)
    all_feature /= logos
    print all_feature
    
            
