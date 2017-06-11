import cv2
import numpy as np
from matplotlib import pyplot as plt

def noise_average(n):
    cap = cv2.VideoCapture(0)
    _, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    av = np.array(img, dtype = int)
    total = 1
    cv2.imwrite(str(total) + ".jpg", img)
    while(total < n):
        _, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        av += np.array(img, dtype = int)
        total += 1
        cv2.imwrite(str(total) + ".jpg", img)
    av = av/n
    return av.astype(np.uint8)
    

#n bigger than 1
def noise_histogram(n, average):
    average = abs(np.array(average, dtype=int))
    img = cv2.imread("1.jpg", 0)
    noise = abs(np.array(img, dtype=int) - average)
    for i in range(2,n):
        img = cv2.imread(str(i) + ".jpg", 0)
        no = abs(np.array(img, dtype=int) - average)
        print no
        noise  += no
    average = average/n
    return average.astype(np.uint8)
    
def camera_noise(n):
    #noise = noise_histogram(n,noise_average(n))
    noise = noise_average(n)
    plt.hist(noise.ravel(),256,[0,256])
    plt.show()
    cv2.imshow("noise", noise)
    cv2.waitKey(0)

def gaussian_noise():
    img1 = cv2.imread("Gaussian-Noise.jpg")
    img2 = cv2.imread("No-Noise.jpg")
    plt.hist(img1.ravel(),256,[0,256])
    plt.show()
    cv2.imshow("noise", img1)
    cv2.waitKey(0)

gaussian_noise()






