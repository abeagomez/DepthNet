import depth_net
import cv2

def testing_camera():
    while True:
        frame = depth_net.get_video_frame()
        depth = depth_net.get_depth_map()
        #cv2.imshow("frame", frame)
        #cv2.imshow("depth", depth)
        centroid = depth_net.get_centroid(frame,depth)
        print centroid
        depth_net.show_scene(frame,depth,centroid)

        k = cv2.waitKey(10)
        if k == 27:
            break


testing_camera()
