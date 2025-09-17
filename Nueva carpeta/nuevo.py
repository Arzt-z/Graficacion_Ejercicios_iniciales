import cv2 as cv
import numpy as np 

img= np.ones((500,500),np.uint8)*150
cv.circle(img,(30,30),5,(23,43,144),4)
cv.rectangle(img,(10,10),(200,200),(34,56,100),-1)

cv.imshow("img",img)
cv.waitKey(0)
cv.destroyAllWindows()
