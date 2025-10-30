import cv2 as cv
import numpy as np 

tama=500
tamb=500

#img= np.ones((tama,tamb),np.uint8)*150
background = np.zeros((tama, tamb, 3), dtype=np.uint8)

velocidadx=4
velocidady=2

posicionx=0
posiciony=0

posicionx2=350
posiciony2=250

radio=20
while True:
    background = np.zeros((tama, tamb, 3), dtype=np.uint8)
    #cv.imshow("img",img)
    
    posicionx = posicionx + velocidadx
    posiciony = posiciony + velocidady
    cv.circle(background, (posicionx,posiciony),radio,(255,0,0),-1)
    cv.circle(background, (posicionx2,posiciony2),radio,(0,255,255),-1)
    cv.imshow("background",background)

    if posicionx+radio >= tama:
        velocidadx = -velocidadx
    if posicionx <= 0:
        velocidadx = -velocidadx
    if posiciony+radio >= tamb:
        velocidady = -velocidady
    if posiciony <= 0:
        velocidady = -velocidady

    distanciax= posicionx2 - posicionx
    distanciay= posiciony2 - posiciony
    if distanciax < 0:
        direccionx = -1
    else:
        direccionx = 1
    if distanciay < 0:
        direcciony = -1
    else:
        direcciony = 1

    contador=contador+1
    if np.sqrt(distanciax**2) <= 30 and np.sqrt(distanciay**2) <= 30:
        if contador <= 30:
            posicionx2=posicionx2+10 





    if cv.waitKey(5) & 0xFF==27:
        break


