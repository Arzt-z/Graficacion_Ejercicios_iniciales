import cv2 as cv
import numpy as np 

img= np.ones((600,600),np.uint8)*150
borde=10
tamanio=60
linea=4
for x in range(8):
    for y in range(8):
        cv.rectangle(img,(borde + x*tamanio,borde+ y*tamanio),(borde+tamanio+ x*tamanio-linea,borde+tamanio+ y*tamanio-linea),(34,56,100),-1)







cv.imshow("img",img)
cv.waitKey(0)
cv.destroyAllWindows()