import cv2
import freenect
from matplotlib import pyplot as plt
import numpy as np

def take_shot_rgb():
    cap = cv2.VideoCapture(0)
    _, img = cap.read()

    #img = get_kinect_video()
    cv2.imwrite("img_rgb.jpg", img)

def take_shot_ir():
    cap = cv2.VideoCapture(0)
    _, img = cap.read()

    #img = get_kinect_video()
    cv2.imwrite("img_ir.jpg", img)

def threshold():
    cap = cv2.VideoCapture(0)
    _, img = cap.read()

    #img = get_kinect_video()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (41, 41),0)
    ret,thresh1 = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    cv2.imwrite("thresh.jpg", thresh1)
    plt.hist(thresh1.ravel(),256,[0,256]); plt.show()

def otsu():
        img = freenect.sync_get_video()[0]

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # global thresholding
        blur1 = cv2.GaussianBlur(img,(55,55),0)
        ret1,th1 = cv2.threshold(blur1,20,255,cv2.THRESH_BINARY)
        
        # Otsu's thresholding
        ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # Otsu's thresholding after Gaussian filtering
        blur2 = cv2.GaussianBlur(img,(25,25),0)
        ret3,th3 = cv2.threshold(blur1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # Global Thresholding after Gaussian filtering
        blur3 = cv2.GaussianBlur(img,(55,55),0)
        ret4, th4 = cv2.threshold(blur1, 240, 255, cv2.THRESH_BINARY)

        # plot all the images and their histograms
        images = [blur1, 0, th1,
                #blur, 0, th2,
                blur1, 0, th3,
                blur1, 0, th4]
        titles = ['Filtro Gaussiano (kernel = 55)','Histograma','Filtro de umbral global (v=20)',
                'Filtro Gaussiano (kernel = 55)','Histograma',"Filtro de umbral con Otsu",
                #'Gaussian filtered Image','Histogram',"Otsu's Thresholding",
                'Filtro Gaussiano (kernel = 55)', 'Histograma', 'Filtro de umbral global (v=240)']
        
        for i in xrange(3):
            plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
            plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
            plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
            plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
            plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
            plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
        
        plt.show()
        #k = cv2.waitKey(10)
        #if k == 27:
        #    break

def threshold_examples():
    img = freenect.sync_get_video()[0]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img,(141,141),0)
    _,th1 = cv2.threshold(img,0,255,cv2.THRESH_BINARY)
    _,th2 = cv2.threshold(img,5,255,cv2.THRESH_BINARY)
    _,th3 = cv2.threshold(img,15,255,cv2.THRESH_BINARY)
    _,th4 = cv2.threshold(img,35,255,cv2.THRESH_BINARY)
    _,th5 = cv2.threshold(img,100,255,cv2.THRESH_BINARY)
    cv2.imwrite("th1b.jpg", th1)
    cv2.imwrite("th2b.jpg", th2)
    cv2.imwrite("th3b.jpg", th3)

    cv2.imwrite("th4b.jpg", th4)
    cv2.imwrite("th5b.jpg", th5)

def blur_examples():
    img = freenect.sync_get_video()[0]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(img,(5,5),0)
    blur2 = cv2.GaussianBlur(img,(25,25),0)
    blur3 = cv2.GaussianBlur(img,(41,41),0)
    blur4 = cv2.GaussianBlur(img,(101,101),0)
    blur5 = cv2.GaussianBlur(img,(141,141),0)
    blur6 = cv2.GaussianBlur(img,(199,199),0)
    cv2.imwrite("gb.jpg", blur1)
    cv2.imwrite("g2b.jpg", blur2)
    cv2.imwrite("g3b.jpg", blur3)

    cv2.imwrite("g4b.jpg", blur4)
    cv2.imwrite("g5b.jpg", blur5)
    cv2.imwrite("g6b.jpg", blur6)

def ir_3led():
    img = freenect.sync_get_video()[0]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img,(41,41),0)
    _,th = cv2.threshold(blur,15,255,cv2.THRESH_BINARY)
    cv2.imwrite("3led.jpg", th)

ir_3led()