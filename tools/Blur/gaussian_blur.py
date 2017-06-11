import cv2
import numpy as np

img = cv2.imread("blur.jpg", 1)

cv2.imshow("original", img)

img1 = cv2.GaussianBlur(img, (41, 41),0)
cv2.imshow("41", img1)
cv2.imwrite("blur41.jpg", img1)

img2 = cv2.GaussianBlur(img, (101, 101),0)
cv2.imshow("100", img2)
cv2.imwrite("blur100.jpg", img2)

img3 = cv2.GaussianBlur(img, (201, 201),0)
cv2.imwrite("blur200.jpg", img3)
cv2.imshow("200", img3)

cv2.waitKey(0)