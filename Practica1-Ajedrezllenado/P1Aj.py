import cv2 as cv
import numpy as np 

img= np.ones((600,600,3),np.uint8)*150

borde=10
tamanio=60
linea=6
contador=0

def teselas(cx,cy,giro):
    girooo=0
    global contador
    for y in range(2):
        for x in range(2):
            girooo +=1   
            if girooo != giro:
                cv.rectangle(img,(borde + (cx+x)*tamanio,borde+ (cy+y)*tamanio),(borde+tamanio+ (cx+x)*tamanio-linea,borde+tamanio+ (cy+y)*tamanio-linea),((255-200*(contador%2)),0+12*(contador),4*(contador)),-1)
    contador +=1    
    print(contador)

for x in range(8):
    for y in range(8):
        cv.rectangle(img,(borde + x*tamanio,borde+ y*tamanio),(borde+tamanio+ x*tamanio-linea,borde+tamanio+ y*tamanio-linea),(0,0,0),1)


teselas(0,0,4)
teselas(1,0,1)
teselas(3,0,2)
teselas(4,0,3)
teselas(6,0,4)
teselas(6,1,1)
teselas(6,3,3)
teselas(6,4,2)
teselas(6,6,1)
teselas(5,6,4)
teselas(3,6,1)
teselas(2,6,4)
teselas(0,6,1)
teselas(0,5,4)
teselas(0,3,2)
teselas(0,2,3)

teselas(2,2,4)
teselas(4,2,3)
teselas(2,4,2)
teselas(4,4,1)

teselas(3,3,1)

cv.imshow("img",img)
cv.waitKey(0)
cv.destroyAllWindows()