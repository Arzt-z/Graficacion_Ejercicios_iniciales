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

radio=20
while True:
    background = np.zeros((tama, tamb, 3), dtype=np.uint8)
    #cv.imshow("img",img)
    
    posicionx = posicionx + velocidadx
    posiciony = posiciony + velocidady
    cv.circle(background, (posicionx,posiciony),radio,(255,0,0),-1)
    cv.imshow("background",background)

    if posicionx+radio >= tama:
        velocidadx = -velocidadx
    if posicionx <= 0:
        velocidadx = -velocidadx
    if posiciony+radio >= tamb:
        velocidady = -velocidady
    if posiciony <= 0:
        velocidady = -velocidady

    if cv.waitKey(5) & 0xFF==27:
        break


