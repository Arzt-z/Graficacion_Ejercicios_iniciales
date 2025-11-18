import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


imagen = cv.imread('A.jpg')

factor_brillo = 50
factor_contraste = 1.2
min_val=0
max_val=100

imagen_float = imagen.astype(np.float32)
B = imagen_float[:,:,0]
G = imagen_float[:,:,1]
R = imagen_float[:,:,2]

gray = 0.0722*B + 0.7152*G + 0.2126*R
imagen_gris = np.clip(gray, 0, 255).astype(np.uint8)

cv.imwrite('imagen_original.jpg', imagen)
cv.imwrite('imagen_escalagrises.jpg', imagen_gris)

cv.imshow("imagen",imagen)
cv.imshow("brillo",imagen_gris)
cv.waitKey(0)
cv.destroyAllWindows()