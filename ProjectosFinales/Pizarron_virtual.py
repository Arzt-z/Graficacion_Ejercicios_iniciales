import cv2 
import numpy as np
import math



# Captura de video
cap = cv2.VideoCapture(1)

for _ in range(10):
    cap.read()


# Crear un lienzo para dibujar
ret, frame = cap.read()
canvas = np.zeros_like(frame)
canvas2 = np.zeros_like(frame) 
# Rango de color 
lower_color = np.array([50, 10, 10])
upper_color = np.array([85, 255, 255])

# Variable para guardar ultimo punto
prev_center = None
MIN_AREA = 300
modo=1  # Modo de dibujo activo
punto1 = None
punto2 = None

def limpiar_pantalla():
    global canvas
    global prev_center
    global punto1
    global punto2
    canvas = np.zeros_like(frame)  # Limpiar pantalla

    prev_center = None
    punto1 = None
    punto2 = None

def calcular_distancia(p1, p2):
    return int(math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2))

def mover_canvas(canvas, dx, dy):
    M = np.float32([[1, 0, dx],
                    [0, 1, dy]])
    return cv2.warpAffine(canvas, M, (canvas.shape[1], canvas.shape[0]))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 0)
    
    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Crear máscara
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Filtrar ruido
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((5,5), np.uint8))
    
    # Buscar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area > MIN_AREA:
            (x, y, w, h) = cv2.boundingRect(c)
            center = (x + w//2, y + h//2)

            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('1'):
                modo = 1  # Modo de dibujo

            elif key == ord('2'):
                modo = 2  # Modo de círculo

            elif key == ord('3'):
                modo = 3  # Modo de cuadrado

            elif key == ord('4') and modo !=4:
                modo = 4  # Modo de mover objeto
            elif key == ord('4') and modo ==4:
                modo = 0

            if key == ord('q'):
                punto1 = center
            if key == ord('w'):
                punto2 = center

            if key == ord('z'):
                limpiar_pantalla()

            if prev_center is not None and modo == 1 :
                cv2.line(canvas, prev_center, center, (0, 255, 0), 5)
            elif  punto1 is not None and (modo == 2 or modo ==3):
                
                if  punto2 is None:
                    distancia = calcular_distancia(punto1, center)
                    if modo ==2:
                        cv2.circle(frame, punto1, distancia , (200, 0, 50), -1)

                    elif modo ==3:
                        cv2.rectangle(frame, punto1, center, (200, 150, 50), -1)

                else:
                    distancia = calcular_distancia(punto1, punto2)
                    if modo ==2:
                        cv2.circle(canvas2, punto1, distancia, (200, 0, 50), -1)
                        punto1 = None
                        punto2 = None
                        prev_center = None
                    elif modo ==3:
                        cv2.rectangle(canvas2, punto1, punto2, (200, 150, 50), -1)
                        punto1 = None
                        punto2 = None
                        prev_center = None
            elif modo == 4 and prev_center is not None:
                dx = center[0] - prev_center[0]
                dy = center[1] - prev_center[1]

                canvas2 = mover_canvas(canvas2, dx, dy)


            prev_center = center
        else:
            prev_center = None

    
    # Combinar la cámara y el lienzo
    combined = cv2.add(frame, canvas)
    combined = cv2.add(combined, canvas2)

    # Mostrar resultados
    cv2.imshow("Dibujo", combined)
    cv2.imshow("Mascara", mask)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC para salir
        break
    elif key == ord('c'):  # 'c' para limpiar el lienzo
        canvas2 = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()