import cv2 as cv
import numpy as np 

img= np.ones((650,650),np.uint8)*150

#cv.rectangle(img,(10,10),(200,100),(34,56,100),-1)
cv.line(img, (244,480),(250,300),(23,244,144),4)
cv.line(img, (250,300),(207,220),(23,244,144),4)
cv.line(img, (250,300),(312,157),(23,244,144),4)
cv.line(img, (207,220),(164,189),(23,244,144),4)
cv.line(img, (207,220),(206,170),(23,244,144),4)
cv.line(img, (224,258),(163,242),(23,244,144),4)
cv.line(img, (275,228),(259,175),(23,244,144),4)

cv.line(img, (300,290),(310,235),(23,244,144),4)
cv.line(img, (300,290),(350,257),(23,244,144),4)

cv.line(img, (381,480),(362,300),(23,244,144),4)

cv.line(img, (362,296),(440,268),(23,244,144),4)
cv.line(img, (440,268),(497,226),(23,244,144),4)


#cv.circle(img,(30,30),5,(23,43,144),4)
#for i in range(400):
    #img= np.ones((500,500),np.uint8)*150
    #cv.circle(img, (i,i),3,(255,0,0),-1)
    #cv.imshow("img",img)
    #cv.waitKey(30)
    



cv.imshow("img",img)
cv.waitKey(0)
cv.destroyAllWindows()
