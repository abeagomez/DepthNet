import cv2
import numpy as np
from matplotlib import pyplot as plt

def testing_light():
    cap = cv2.VideoCapture(0)
    while( cap.isOpened() ) :
        ret,img = cap.read()
        orig = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (41, 41),0)
        
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        #cv2.circle(img, maxLoc, 20, (255,0,0), 3)
        brightest_area_center = maxLoc
        
        ret,thresh1 = cv2.threshold(gray,230,255,cv2.THRESH_BINARY)
        cv2.imshow("Binary", thresh1)

        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0,255,0), 3)

        for contour in contours:
            img = get_contour_centroid(contour, img)

        cv2.imshow('output',img)
        #cv2.imshow("gray", gray)

        k = cv2.waitKey(10)
        if k == 27:
            break
def get_contour_centroid(contour, img):
    M = cv2.moments(contour)
    if int(M['m00']) != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        img = circle_contour(contour,(cx,cy),img)
        #cv2.circle(img, (cx,cy), 10, (0,0,255), 3)
    return img

def image_to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img, kernel):
    cv2.GaussianBlur(gray, (kernel, kernel),0)

def brightest_area_center(img):
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(image_to_grayscale(image))
    return maxLoc

def circle_contour(contour, centroid, img):
    x,y = contour[0][0][0], contour[0][0][1]
    min_x, min_y, max_x, max_y = x, y, x, y
    for contour_list in contour:
        for c in contour_list:
            if c[0] < min_x:
                min_x = c[0]
            elif c[0] > max_x:
                max_x = c[0]
            if c[1] < min_y:
                min_y = c[1]
            elif c[1] > max_y:
                max_y = c[1]
    radius = contour_max_radius(centroid, min_x, max_x, min_y,  max_y)
    cv2.circle(img,centroid,radius,(255,0,0),3)
    return img

def contour_max_radius(centroid, min_x, max_x, min_y, max_y):
    return max(centroid[0] - min_x, max_x - centroid[0],centroid[1] - min_y, max_y - centroid[1] )
    

def otsu():
    cap = cv2.VideoCapture(0)
    while True:
        ret,img = cap.read()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # global thresholding
        ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        
        # Otsu's thresholding
        ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(img,(5,5),0)
        ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # plot all the images and their histograms
        images = [img, 0, th1,
                img, 0, th2,
                blur, 0, th3]
        titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
                'Original Noisy Image','Histogram',"Otsu's Thresholding",
                'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]
        
        for i in xrange(3):
            plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
            plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
            plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
            plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
            plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
            plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
        
        plt.show()
        k = cv2.waitKey(10)
        if k == 27:
            break

