import cv2
import freenect
import numpy as np
import math

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
        return (-1,-1)

def __get_contours__(frame, thresh_index = 20):
        #cv2.imshow("contour", __binary_threshold__(frame, thresh_index))
        contours, _ = cv2.findContours(__binary_threshold__(frame, thresh_index), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return contours

#Cambiar nombre a get_marker_coordinates
def get_centroid(frame, depth, thresh_index = 20, kernel = 41):
        frame = __gaussian_blur__(__frame_to_gray__(frame), kernel)
        contours = __get_contours__(frame, thresh_index)
        default_response = (-1,-1,-1)
        if len(contours) > 1 or len(contours) == 0:
            print "No se detecto nada"
            return default_response
        else:
            c = contours[0]
            extLeft = tuple(c[c[:, :, 0].argmin()][0])
            extRight = tuple(c[c[:, :, 0].argmax()][0])
            extTop = tuple(c[c[:, :, 1].argmin()][0])
            extBot = tuple(c[c[:, :, 1].argmax()][0])

            left_top = (extLeft[0], extTop[1])
            right_bo = (extRight[0], extBot[1])

            depth_r, _ = freenect.sync_get_depth(0, freenect.DEPTH_REGISTERED)
            depth_p = []
            for x in range(extLeft[0], extRight[0]):
                for y in range(extTop[1], extBot[1]):
                    if depth_r[y][x] != 0:
                        depth_p.append(depth_r[y][x])
            x, y = __get_contour_centroid__(c)
            if (x,y) == (-1,-1):
                return default_response
            z = np.average(depth_p)
            if math.isnan(float(z)):
                return default_response
            return (x, y, z)

def show_scene(frame, depth, centroid = (-1,-1,-1)):
    filtered_frame = __binary_threshold__(__gaussian_blur__(__frame_to_gray__(frame), 41), 20)
    filtered_frame = cv2.cvtColor(filtered_frame, cv2.COLOR_GRAY2BGR)
    #filtered_frame = __binary_threshold__(frame, 20)
    #filtered_frame = cv2.cvtColor(filtered_frame, cv2.COLOR_GRAY2BGR)
    if centroid != (-1,-1,-1):
        cv2.circle(filtered_frame,(centroid[0],centroid[1]),3,(0,0,255),3)
    cv2.putText(filtered_frame,"({:.0f}, {:.0f}) {:.2f}mm".format(*centroid),(centroid[0], centroid[1]-10),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0))
    cv2.imshow("contour", filtered_frame)
    cv2.imshow("frame", frame)
    cv2.imshow("depth", depth)



def __frame_to_gray__(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray

def __gaussian_blur__(frame, kernel = 41):
    blur = cv2.GaussianBlur(frame, (kernel, kernel),0)
    return blur

def __binary_threshold__(frame, threshold = 20):
    ret,thresh = cv2.threshold(frame,threshold,255,cv2.THRESH_BINARY)
    return thresh

def compute_matrix(detected_points, calibration_points):
    x = np.array(detected_points)
    y = np.array(calibration_points)
    mc, resid, rank, sigma = lstsq(x,y)
    m, c = mc[0:3], mc[-1]
    return m, c

def build_a(x_data):
    return np.column_stack((x_data, np.ones(len(x_data))))

def lstsq(x_data, y_data):
    return np.linalg.lstsq(build_a(x_data), y_data)

def test_camera():
    while True:
        frame = get_video_frame()
        cv2.imshow("frame", frame)

        k = cv2.waitKey(10)
        if k == 27:
            break
