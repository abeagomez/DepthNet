import depth_net
import cv2

def testing_camera():
    while True:
        frame = depth_net.get_video_frame()
        depth = depth_net.get_depth_map()
        cv2.imshow("frame", frame)
        cv2.imshow("depth", depth)
        print depth_net.get_centroid(frame,depth)

        k = cv2.waitKey(10)
        if k == 27:
            break

testing_camera()
