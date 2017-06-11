import cv2
import depth_net

def analize(video):
    cap = cv2.VideoCapture(video)
    count = 0
    found = 0
    error = 0
    while(count < 600):
        ret, frame = cap.read()
        if ret:
            frame = depth_net.__gaussian_blur__(depth_net.__frame_to_gray__(frame))
            contours = depth_net.__get_contours__(frame, 5)
            count += 1
            print count
            if len(contours) == 1:
                found += 1
                print "found" 
            elif len(contours) > 1:
                error += 1
                print "error"

        
    print "total"
    print count
    print "found"
    print found
    cap.release()

analize("lados_mov_test_75cm_big.avi")