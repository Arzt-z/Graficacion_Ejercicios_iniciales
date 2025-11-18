import cv2 as cv
import numpy as np 
rng = np.random.default_rng()

img = np.ones((650,650,3), np.uint8) * 150

dispercion = 40
cantidad = 6
radio=15
puntos = [
 (250,300),
    (207,220), (312,157),
    (164,189), (206,170),
    (224,258), (163,242),
    (275,228), (259,175),
    (300,290), (310,235),
    (350,257),(340,268),
     (362,300),(400,168),
     (380,148),
    (362,296), (440,268),
    (497,226), (450,226)
]

for i in range(cantidad):
    for (x, y) in puntos:
        cx = x + rng.integers(0, dispercion)
        cy = y + rng.integers(0, dispercion)
        cv.circle(img, (cx, cy), radio, (23,255,100), radio*2)
        
#cv.rectangle(img,(10,10),(200,100),(34,56,100),-1)
cv.line(img, (244,480),(250,300),(51, 64, 94),4)
cv.line(img, (250,300),(207,220),(51, 64, 94),4)
cv.line(img, (250,300),(312,157),(51, 64, 94),4)
cv.line(img, (207,220),(164,189),(51, 64, 94),4)
cv.line(img, (207,220),(206,170),(51, 64, 94),4)
cv.line(img, (224,258),(163,242),(51, 64, 94),4)
cv.line(img, (275,228),(259,175),(51, 64, 94),4)

cv.line(img, (300,290),(310,235),(51, 64, 94),4)
cv.line(img, (300,290),(350,257),(51, 64, 94),4)

cv.line(img, (381,480),(362,300),(51, 64, 94),4)

cv.line(img, (362,296),(340,268),(51, 64, 94),4)
cv.line(img, (362,296),(440,268),(51, 64, 94),4)
cv.line(img, (362,296),(400,168),(51, 64, 94),4)
cv.line(img, (440,268),(497,226),(51, 64, 94),4)
cv.line(img, (440,268),(450,226),(51, 64, 94),4)

for i in range(cantidad):
    for (x, y) in puntos:
        cx = x + rng.integers(0, dispercion)
        cy = y + rng.integers(0, dispercion)
        cv.circle(img, (cx, cy), int(radio/4), (23,255,100), int(radio/2))



#cv.circle(img,(30,30),5,(23,43,144),4)
#for i in range(400):
    #img= np.ones((500,500),np.uint8)*150
    #cv.circle(img, (i,i),3,(255,0,0),-1)
    #cv.imshow("img",img)
    #cv.waitKey(30)
    



cv.imshow("img",img)
cv.waitKey(0)
cv.destroyAllWindows()
