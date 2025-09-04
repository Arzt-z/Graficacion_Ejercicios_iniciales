import numpy as np   # Importa la librería NumPy, útil para trabajar con arreglos y operaciones numéricas.
import cv2 as cv     # Importa la librería OpenCV, que se utiliza para procesamiento de imágenes.
import time
# Crea una imagen de 500x500 píxeles, todos con valor 240 (gris claro). 
# La imagen tiene solo un canal (escala de grises) y está inicializada con valores de tipo uint8 (enteros sin signo de 8 bits).
img = np.ones((500, 500), dtype=np.uint8) * 240

# Modifica algunos píxeles específicos en las coordenadas (30, 30) a (30, 35) para que tengan un valor de 1 (casi negro).
# Esto creará una pequeña línea vertical de 6 píxeles en la imagen de color casi negro.

offsetx=50
offsety=50
grosor=10
for i in range(50):
	for o in range(grosor):
		img[i+offsetx, offsety+o]=i*3


for i in range(30):
	for o in range(grosor):
		img[o+offsetx, offsety+i]=i*3


for i in range(50):
	for o in range(grosor):
		img[i+offsetx, offsety+o+30]=i*3


for i in range(30):
	for o in range(grosor):
		img[o+offsetx+20, offsety+i]=i*3

#////////////////////////////////////////////
offsetx2=50
offsety2=50*2
#ver
for i in range(50):
	for o in range(grosor):
		img[i+offsetx2, offsety2+o]=i*3





for i in range(30):
	for o in range(grosor):
		img[o+offsetx2+40, offsety2+i]=100

#////////////////////////////////////////////
offsetx3=50
offsety3=50*3
#ver
for i in range(50):
	for o in range(grosor):
		img[i+offsetx3, offsety3+o]=i*3


for i in range(30):
	for o in range(grosor):
		img[o+offsetx3, offsety3+i]=i*3




for i in range(30):
	for o in range(grosor):
		img[o+offsetx3+20, offsety3+i]=i*3

for i in range(30):
	for o in range(grosor):
		img[o+offsetx3+40, offsety3+i]=100



#////////////////////////////////////////////
offsetx4=50
offsety4=50*4
#ver
for i in range(50):
	for o in range(grosor):
		img[i+offsetx4, offsety4+o+i]=i*3

#ver
for i in range(50):
	for o in range(15):
		img[-i+offsetx4+50, offsety4+o+i]=i*3

for i in range(50):
	for o in range(grosor):
		img[i+offsetx4, offsety4+o+i]=i*3



#////////////////////////////////////////////
offsetx5=50
offsety5=50*5+20
#ver
for i in range(50):
	for o in range(grosor):

		img[i+offsetx5, offsety5+o]=i*3


#////////////////////////////////////////////
offsetx5=50
offsety5=50*6
#ver
for i in range(20):
	for o in range(grosor):
		img[i+offsetx5, offsety5+o]=i*3


for i in range(40):
	for o in range(grosor):
		img[o+offsetx5, offsety5+i]=i*3

#ver
for i in range(30):
	for o in range(grosor):
		img[i+offsetx5+20, offsety5+o+30]=i*3


for i in range(30):
	for o in range(grosor):
		img[o+offsetx5+20, offsety5+i]=i*3

for i in range(30):
	for o in range(grosor):
		img[o+offsetx5+40, offsety5+i]=100



# img[30, 30] = 1
# img[30, 31] = 1
# img[30, 32] = 1
# img[30, 33] = 1
# img[30, 34] = 1
# img[30, 35] = 1

# Muestra la imagen en una ventana con el título 'img'. 
cv.imshow('img', img)
# time.sleep(5)
# Espera a que el usuario presione cualquier tecla para continuar.
cv.waitKey()

# Cierra todas las ventanas creadas por OpenCV.
cv.destroyAllWindows()


