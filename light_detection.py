import cv2
import numpy as np
import freenect
import depth_net as dn
from matplotlib import pyplot as plt


class FrameProcessor:
    def __init__(self, frame):
        self.frame = frame

    def get_frame_with_blur(self):
        return cv2.GaussianBlur(cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY), (41, 41),0)

    def binary_thresh(self, index):
        gray = self.get_frame_with_blur()
        _ , thresh =  cv2.threshold(gray,index,255,cv2.THRESH_BINARY)
        return thresh

    def draw_contours_and_centroids(self, thresh_index = 200, window_identifier = 'output'):
        contours, hierarchy = self.get_contours(thresh_index)
        cv2.drawContours(self.frame, contours, -1, (0,255,0), 3)
        for contour in contours:
            M = cv2.moments(contour)
            if int(M['m00']) != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(self.frame, (cx,cy), 10, (0,0,255), 3)

        cv2.imshow(window_identifier,self.frame)

    def get_centroid(self, thresh_index = 200, window_identifier = 'output'):
        contours, _ = self.get_contours(thresh_index)
        if len(contours) > 1:
            raise exception("More than one light recieved")
        if len(contours) == 0:
            return 0
        else:
            M = cv2.moments(contours[0])
            if int(M['m00']) != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(self.frame, (cx,cy), 10, (0,0,255), 3)
                return((cx,cy))

    def get_contours(self, thresh_index):
        contours, hierarchy = cv2.findContours(self.binary_thresh(thresh_index), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return((contours, hierarchy))


class KinectManager:
    def get_rgb_video(self):
        return cv2.cvtColor(freenect.sync_get_video()[0] , cv2.COLOR_RGB2BGR)

    def get_depth(self):
        depth, timestamp = freenect.sync_get_depth(0, freenect.DEPTH_REGISTERED)
        np.clip(depth, 0, 2**10 - 1, depth)
        depth >>= 2
        depth = depth.astype(np.uint8)
        return depth




def get_kinect_video():
    return(freenect.sync_get_video()[0])

def testing_freenct():
    while True:
        cv2.imshow("kinnect", get_video())
        if cv2.waitKey(10) == 27:
            break

def testing_light_kinect(): 
    while(True) :
        img = get_kinect_video()
        orig = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (41, 41),0)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        cv2.circle(img, maxLoc, 20, (255,0,0), 3)
        cv2.imshow('video', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        cv2.imshow("gray", gray)
        k = cv2.waitKey(10)
        if k == 27:
            break

def get_depth():
    depth, timestamp = freenect.sync_get_depth(0, freenect.DEPTH_REGISTERED)
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

def show_depth():
    while True:
        depth = get_depth()
        blur = cv2.GaussianBlur(depth, (5, 5), 0)
        cv2.imshow('image', depth)
        k = cv2.waitKey(10)
        if k == 27:
            break

def testing_image_and_depth():
    while True:
        img = get_kinect_video()
        depth = get_depth()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (55, 55),0)
        ret,thresh1 = cv2.threshold(gray,15,255,cv2.THRESH_BINARY)
        cv2.imshow("Binary", thresh1)

        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0,255,0), 3)

        for contour in contours:
            M = cv2.moments(contour)
            if int(M['m00']) != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(img, (cx,cy), 10, (0,0,255), 3)
                cv2.circle(depth, (cx,cy), 10, (0,0,255), 3)
                #print len(depth[0])
                depth_r, _ = freenect.sync_get_depth(0, freenect.DEPTH_REGISTERED)
                
                #print depth[cy][cx]
                print depth_r[cy][cx]

        cv2.imshow('output',cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        cv2.imshow("depth", depth)

        k = cv2.waitKey(10)
        if k == 27:
            break
    
def test_dn():
    c = 0
    while True:
        print c
        c += 1
        print dn.get_centroid(dn.get_video_frame(),dn.get_original_depth())

def otsu():
        img = get_kinect_video()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # global thresholding
        ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        
        # Otsu's thresholding
        ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(img,(5,5),0)
        ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # Global Thresholding after Gaussian filtering
        ret4, th4 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

        # plot all the images and their histograms
        images = [img, 0, th1,
                img, 0, th2,
                #blur, 0, th3,
                blur, 0, th4]
        titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
                'Original Noisy Image','Histogram',"Otsu's Thresholding",
                #'Gaussian filtered Image','Histogram',"Otsu's Thresholding",
                'Gaussian filtered Image', 'Histogram', 'Global Thresholfing (v=127)']
        
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


def contour_rectangle():
    while True:
        img = get_kinect_video()
        depth = get_depth()
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (55, 55),0)
        ret,thresh = cv2.threshold(blur,15,255,cv2.THRESH_BINARY)
        cv2.imshow("Binary", thresh)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0,255,0), 3)

        if len(contours) == 0 or len(contours) > 1:
            print "More than one contour found"
        else:
            c = contours[0]
            extLeft = tuple(c[c[:, :, 0].argmin()][0])
            extRight = tuple(c[c[:, :, 0].argmax()][0])
            extTop = tuple(c[c[:, :, 1].argmin()][0])
            extBot = tuple(c[c[:, :, 1].argmax()][0])
            
            left_top = (extLeft[0], extTop[1])
            right_bo = (extRight[0], extBot[1])

            cv2.rectangle(img, left_top, right_bo, (0,0,255), 3)
            
            depth_r, _ = freenect.sync_get_depth(0, freenect.DEPTH_REGISTERED)
            depth_p = []
            for x in range(extLeft[0], extRight[0]):
                for y in range(extTop[1], extBot[1]):
                    if depth_r[y][x] != 0:
                        depth_p.append(depth_r[y][x])
            print np.average(depth_p)
        
        cv2.imshow('output',cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        cv2.imshow("depth", depth)

        k = cv2.waitKey(10)
        if k == 27:
            break

contour_rectangle()