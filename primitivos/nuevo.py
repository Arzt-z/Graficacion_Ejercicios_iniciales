import cv2 as cv
import numpy as np 

img= np.ones((500,500),np.uint8)*150

cv.rectangle(img,(10,10),(200,100),(34,56,100),-1)
cv.line(img, (255,255),(200,100),(23,244,144),4)
cv.circle(img,(30,30),5,(23,43,144),4)
for i in range(400):
    #img= np.ones((500,500),np.uint8)*150
    cv.circle(img, (i,i),3,(255,0,0),-1)
    cv.imshow("img",img)
    cv.waitKey(30)
    



cv.imshow("img",img)
cv.waitKey(0)
cv.destroyAllWindows()
