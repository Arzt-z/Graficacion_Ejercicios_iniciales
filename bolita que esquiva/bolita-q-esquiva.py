import cv2 as cv
import numpy as np 
import random

rng = np.random.default_rng()
tama=500
tamb=500
contador=0
#img= np.ones((tama,tamb),np.uint8)*150
background = np.zeros((tama, tamb, 3), dtype=np.uint8)

velocidadx=-4
velocidady=2

posicionx=4
posiciony=3

velocidadx2 = 1
velocidady2 = 2

posicionx2=250
posiciony2=250
rando = 1
radio=40


escapespeed = 6
distanciatrigger = 100 

while True:
    background = np.zeros((tama, tamb, 3), dtype=np.uint8)
    #cv.imshow("img",img)
    posicionx = posicionx + velocidadx
    posiciony = posiciony + velocidady
    posicionx2 = posicionx2 + velocidadx2
    posiciony2 = posiciony2 + velocidady2


    distanciax = posicionx2 - (posicionx + radio)
    distanciay = posiciony2 - (posiciony + radio)
    distancia = np.sqrt(distanciax**2 + distanciay**2)

    if distancia < distanciatrigger and distancia > 0:
        escapedirx = distanciax/distancia
        escapediry = distanciay/distancia
        velocidadx2 = escapedirx*escapespeed
        velocidady2 = escapediry*escapespeed

    if posicionx + radio*2 >= tamb:
        velocidadx = -velocidadx
        posicionx = tamb - radio*2
    if posicionx <= 0:
        velocidadx = -velocidadx
        posicionx = 0
    if posiciony + radio*2 >= tama:
        velocidady = -velocidady
        posiciony = tama - radio*2
    if posiciony <= 0:
        velocidady = -velocidady
        posiciony = 0
    buffer = 20 
    if posicionx2 <= radio/2 and velocidadx2 < 0:
        velocidady2 = velocidady2*1
        velocidadx2 = velocidady2*-1


    contador=contador+1
    if posicionx2 >= tamb - radio/2 and velocidadx2 > 0:
        velocidady2 = velocidady2*1
        velocidadx2 = velocidady2*-1
    
    if posiciony2 <=  radio/2 and velocidady2 < 0:
        velocidady2 = velocidady2*-1
        velocidadx2 = velocidady2*1
    
    if posiciony2 >= tama - radio/2 and velocidady2 > 0:
        velocidady2 = velocidady2*-1
        velocidadx2 = velocidady2*1
        
    if distancia < radio+30:
        posicionx2=250
        posiciony2=250

    posicionx2 = np.clip(posicionx2, radio/2, tamb-radio/2)
    posiciony2 = np.clip(posiciony2, radio/2, tama-radio/2)
    

        

    cv.circle(background, (int(posicionx+radio), int(posiciony+radio)), radio, (255,0,0), -1)
    cv.circle(background, (int(posicionx2), int(posiciony2)), int(radio/2), (0,255,255), -1)


    centro2 = (int(1), int(20))
    text = f"distancia: {distancia:.0f}"
    cv.putText(background, text, centro2, cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    
    cv.imshow("background", background)
    
    if cv.waitKey(5) & 0xFF == 27:
        break

cv.destroyAllWindows()
