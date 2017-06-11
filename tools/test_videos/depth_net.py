import cv2
import freenect
import numpy as np

def get_video_frame():
    return(freenect.sync_get_video()[0])

def get_depth_map():
    depth, timestamp = freenect.sync_get_depth(0, freenect.DEPTH_REGISTERED)
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

def get_original_depth():
    depth, _ = freenect.sync_get_depth(0, freenect.DEPTH_REGISTERED)
    return depth

def __get_point_depth__(depth, x, y):
    return depth[y][x]

def __get_contour_centroid__(contour):
    M = cv2.moments(contour)
    if int(M['m00']) != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return cx,cy
    else:
        raise exception("centroid division by zero")

def __get_contours__(frame, thresh_index = 20):
        contours, _ = cv2.findContours(__binary_threshold__(frame, thresh_index), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return contours

def get_centroid(frame, depth, thresh_index = 20):
        frame = __gaussian_blur__(__frame_to_gray__(frame))
        contours = __get_contours__(frame, thresh_index)
        if len(contours) > 1:
            raise exception("More than one light recieved")
        if len(contours) == 0:
            return (-1,-1,-1)
        else:
            cx, cy = __get_contour_centroid__(contours[0])
            return (cx,cy,__get_point_depth__(depth, cx, cy))

def __frame_to_gray__(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray

def __gaussian_blur__(frame, kernel = 41):
    blur = cv2.GaussianBlur(frame, (kernel, kernel),0)
    return blur

def __binary_threshold__(frame, threshold = 20):
    ret,thresh = cv2.threshold(frame,threshold,255,cv2.THRESH_BINARY)
    return thresh
