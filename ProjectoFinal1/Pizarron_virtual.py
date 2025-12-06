import cv2 
import numpy as np

# Captura de video
cap = cv2.VideoCapture(0)

# Crear un lienzo para dibujar
ret, frame = cap.read()
canvas = np.zeros_like(frame)

# Rango de color 
lower_color = np.array([40, 0, 0])
upper_color = np.array([80, 255, 255])

# Variable para guardar último punto
prev_center = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
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
        # Contorno más grande
        c = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        center = (x + w//2, y + h//2)
        
        # Dibujar círculo en la cámara
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
        # Dibujar línea en el lienzo
        if prev_center is not None:
            cv2.line(canvas, prev_center, center, (0, 255, 0), 5)
        
        prev_center = center
    else:
        prev_center = None
    
    # Combinar la cámara y el lienzo
    combined = cv2.add(frame, canvas)
    
    # Mostrar resultados
    cv2.imshow("Dibujo", combined)
    cv2.imshow("Mascara", mask)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC para salir
        break
    elif key == ord('c'):  # 'c' para limpiar el lienzo
        canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()