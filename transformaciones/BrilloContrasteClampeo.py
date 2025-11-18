import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


imagen = cv.imread('A.jpg')

factor_brillo = 50
factor_contraste = 1.2
min_val=0
max_val=100

imagen_float = imagen.astype(np.float32)
imagen_transformada = imagen_float + factor_brillo
imagen_transformada = np.clip(imagen_transformada, 0, 255)
imagen_brillo = imagen_transformada.astype(np.uint8)

imagen_float = imagen.astype(np.float32)
imagen_transformada = imagen_float * factor_contraste
imagen_transformada = np.clip(imagen_transformada, 0, 255)
imagen_contraste = imagen_transformada.astype(np.uint8)

imagen_clampeada = np.clip(imagen, min_val, max_val)
imagen_clampeo =imagen_clampeada.astype(np.uint8)

cv.imwrite('imagen_original.jpg', imagen)
cv.imwrite('imagen_brillo.jpg', imagen_brillo)
cv.imwrite('imagen_contraste.jpg', imagen_contraste)
cv.imwrite('imagen_clampeo.jpg', imagen_clampeo)

cv.imshow("imagen",imagen)
cv.imshow("brillo",imagen_brillo)
cv.imshow("contraste",imagen_contraste)
cv.imshow("clampeo",imagen_clampeo)
cv.waitKey(0)
cv.destroyAllWindows()