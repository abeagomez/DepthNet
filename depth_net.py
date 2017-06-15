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

#Cambiar nombre a get_marker_coordinates
def get_centroid(frame, depth, thresh_index = 20, kernel = 41):
        frame = __gaussian_blur__(__frame_to_gray__(frame), kernel)
        contours = __get_contours__(frame, thresh_index)
        if len(contours) > 1 or len(contours) == 0:
            print "No se detecto nada"
            return (-1,-1,-1)
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
            return (x, y, np.average(depth_p))

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
