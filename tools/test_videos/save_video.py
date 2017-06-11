import cv2
import freenect

def save_video(frames):
    
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter('lados_mov_test_75cm_big.avi',fourcc, 20.0, (640,480))
    
    while frames > 0:
        frame = freenect.sync_get_video()[0]
        #frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        #cv2.imshow('frame',frame)
        frames -= 1
        print frames

    out.release()
    cv2.destroyAllWindows()

save_video(600)