import cv2

def save_threshold():
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (41, 41),0)
    ret,thresh = cv2.threshold(gray,230,255,cv2.THRESH_BINARY)
    cv2.imwrite("thresh.jpg", thresh)

def contours_live():
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (41, 41),0)
    ret,thresh = cv2.threshold(gray,230,255,cv2.THRESH_BINARY)

    cv2.imshow("1", thresh) 
    cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print contours

contours_live()
