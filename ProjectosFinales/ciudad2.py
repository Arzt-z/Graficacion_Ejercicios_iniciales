import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys
import math
import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(1)
# Camera state
cam_pos = [9.0, 10.0, 15.0]     # Eye
cam_center = [0.0, 0.0, 0.0]    # Center point the camera looks at
cam_up = [0.0, 1.0, 0.0]        # Up vector
move_speed = 0.5
rot_angle = math.radians(5)    # rotation per key press


def normalize(v):
    l = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
    if l == 0:
        return [0,0,0]
    return [v[0]/l, v[1]/l, v[2]/l]


def rotate_y_around_point(point, center, angle):
    # rotate 'center' around 'point' along Y axis by 'angle' radians
    x = center[0] - point[0]
    z = center[2] - point[2]
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    rx = x * cos_a - z * sin_a
    rz = x * sin_a + z * cos_a
    return [point[0] + rx, center[1], point[2] + rz]


def rotate_around_axis(point, center, axis, angle):
    """Rotate `center` around `point` along arbitrary normalized `axis` by `angle` radians.
    Uses Rodrigues' rotation formula."""
    vx = center[0] - point[0]
    vy = center[1] - point[1]
    vz = center[2] - point[2]
    ux, uy, uz = axis
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    # cross(axis, v)
    cx = uy * vz - uz * vy
    cy = uz * vx - ux * vz
    cz = ux * vy - uy * vx
    dot = ux * vx + uy * vy + uz * vz
    rx = vx * cos_a + cx * sin_a + ux * dot * (1 - cos_a)
    ry = vy * cos_a + cy * sin_a + uy * dot * (1 - cos_a)
    rz = vz * cos_a + cz * sin_a + uz * dot * (1 - cos_a)
    return [point[0] + rx, point[1] + ry, point[2] + rz]


def key_callback(window, key, scancode, action, mods):
    global cam_pos, cam_center
    if action not in (glfw.PRESS, glfw.REPEAT):
        return
    # Direction vector from eye to center
    dir_vec = [cam_center[0]-cam_pos[0], cam_center[1]-cam_pos[1], cam_center[2]-cam_pos[2]]
    dir_norm = normalize(dir_vec)
    # Right vector = cross(dir, up)
    right = [ dir_norm[2]*cam_up[1] - dir_norm[1]*cam_up[2],
              dir_norm[0]*cam_up[2] - dir_norm[2]*cam_up[0],
              dir_norm[1]*cam_up[0] - dir_norm[0]*cam_up[1] ]
    r_norm = normalize(right)
    if key == glfw.KEY_W:
        for i in range(3):
            cam_pos[i] += dir_norm[i]*move_speed
            cam_center[i] += dir_norm[i]*move_speed
    elif key == glfw.KEY_S:
        for i in range(3):
            cam_pos[i] -= dir_norm[i]*move_speed
            cam_center[i] -= dir_norm[i]*move_speed
    elif key == glfw.KEY_A:
        for i in range(3):
            cam_pos[i] -= r_norm[i]*move_speed
            cam_center[i] -= r_norm[i]*move_speed
    elif key == glfw.KEY_D:
        for i in range(3):
            cam_pos[i] += r_norm[i]*move_speed
            cam_center[i] += r_norm[i]*move_speed
    elif key == glfw.KEY_LEFT:
        cam_center = rotate_y_around_point(cam_pos, cam_center, rot_angle)
    elif key == glfw.KEY_RIGHT:
        cam_center = rotate_y_around_point(cam_pos, cam_center, -rot_angle)
    elif key == glfw.KEY_Q:
        # Inclina la cámara hacia arriba (pitch up) alrededor del eje 'right'
        cam_center = rotate_around_axis(cam_pos, cam_center, r_norm, rot_angle)
    elif key == glfw.KEY_E:
        # Inclina la cámara hacia abajo (pitch down) alrededor del eje 'right'
        cam_center = rotate_around_axis(cam_pos, cam_center, r_norm, -rot_angle)
    elif key == glfw.KEY_UP:
        cam_pos[1] += move_speed
        cam_center[1] += move_speed
    elif key == glfw.KEY_DOWN:
        cam_pos[1] -= move_speed
        cam_center[1] -= move_speed


def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1, 6, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    """Dibuja el cubo (base cuadrada de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.5, 0.2)  # Marrón para todas las caras

    # Frente (z = 1.5)
    glVertex3f(-1.5, 0, 1.5)
    glVertex3f(1.5, 0, 1.5)
    glVertex3f(1.5, 5, 1.5)
    glVertex3f(-1.5, 5, 1.5)

    # Atrás     X  Y   Z (z = -1.5)
    glVertex3f(-1.5, 0, -1.5)
    glVertex3f(1.5, 0, -1.5)
    glVertex3f(1.5, 5, -1.5)
    glVertex3f(-1.5, 5, -1.5)

    # Izquierda (x = -1.5)
    glVertex3f(-1.5, 0, -1.5)
    glVertex3f(-1.5, 0, 1.5)
    glVertex3f(-1.5, 5, 1.5)
    glVertex3f(-1.5, 5, -1.5)

    # Derecha (x = 1.5)
    glVertex3f(1.5, 0, -1.5)
    glVertex3f(1.5, 0, 1.5)
    glVertex3f(1.5, 5, 1.5)
    glVertex3f(1.5, 5, -1.5)

    # Arriba (techo de la base)
    glColor3f(0.9, 0.6, 0.3)  # Color diferente para la parte superior
    glVertex3f(-1.5, 5, -1.5)
    glVertex3f(1.5, 5, -1.5)
    glVertex3f(1.5, 5, 1.5)
    glVertex3f(-1.5, 5, 1.5)

    # Abajo (suelo de la casa)
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1.5,0 , -1.5)
    glVertex3f(1.5, 0, -1.5)
    glVertex3f(1.5, 0, 1.5)
    glVertex3f(-1.5, 0, 1.5)
    glEnd()

def draw_roof():
    """Dibuja el techo (pirámide que encaja en la base cuadrada)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.9, 0.1, 0.1)  # Rojo brillante

    # Frente (z = 1.5)
    glVertex3f(-1.5, 5, 1.5)
    glVertex3f(1.5, 5, 1.5)
    glVertex3f(0, 9, 0)

    # Atrás     x  y   z (z = -1.5)
    glVertex3f(-1.5, 5, -1.5)
    glVertex3f(1.5, 5, -1.5)
    glVertex3f(0, 9, 0)

    # Izquierda
    glVertex3f(-1.5, 5, -1.5)
    glVertex3f(-1.5, 5, 1.5)
    glVertex3f(0, 9, 0)

    # Derecha
    glVertex3f(1.5, 5, -1.5)
    glVertex3f(1.5, 5, 1.5)
    glVertex3f(0, 9, 0)
    glEnd()

def draw_ground():
    """Dibuja un plano para representar el suelo o calle"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-200, 0, 200)
    glVertex3f(200, 0, 200)
    glVertex3f(200, 0, -200)
    glVertex3f(-200, 0, -200)
    glEnd()


def draw_pasto(size=6.0, y=0.01):
    """Dibuja un parche de pasto cuadrado centrado en el origen.
    - size: longitud del lado del parche
    - y: altura sobre el suelo para evitar z-fighting
    """
    half = size / 2.0
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.8, 0.2)  # Verde
    glVertex3f(-half, y, -half)
    glVertex3f(half, y, -half)
    glVertex3f(half, y, half)
    glVertex3f(-half, y, half)
    glEnd()

def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()  # Base de la casa
    draw_roof()  # Techo

def draw_scene():
    """Dibuja toda la escena con 4 casas"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara (controlada por teclado)
    gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],  # Posición de la cámara
              cam_center[0], cam_center[1], cam_center[2],    # Punto al que mira
              cam_up[0], cam_up[1], cam_up[2])    # Vector hacia arriba

    # Dibujar el suelo
    draw_ground()


    # Dibujar las casas en diferentes posiciones
    positions = [
        (0, 0, 0),   # Casa 1



    ]
    num_bloques_x = 6        # bloques a lo largo de X
    num_bloques_z = 8        # bloques a lo largo de Z
    bloque_ancho = 10        # casas por bloque en X
    bloque_profundidad = 2   # casas por bloque en Z
    casa_dist = 10           # separación entre casas
    separacion_bloques = 10  # separación entre bloques

    for bz in range(num_bloques_z):       # bucle para filas de bloques en Z
        offset_z = bz * (bloque_profundidad * casa_dist + separacion_bloques)
        for bx in range(num_bloques_x):   # bucle para bloques a lo largo de X
            offset_x = bx * (bloque_ancho * casa_dist + separacion_bloques)
            for x in range(bloque_ancho):
                for z in range(bloque_profundidad):
                    positions.append((x*casa_dist + offset_x, 0, z*casa_dist + offset_z))


    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual
        # Dibujar parche de pasto centrado en la casa. Se usa 0.9*casa_dist para
        # evitar que los parches de casas adyacentes se solapen.
        draw_pasto(size=casa_dist * 0.99)
        draw_house()        # Dibujar la casa
        glPopMatrix()

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Escena con 4 casas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Registrar callback de teclado para mover la cámara
    glfw.set_key_callback(window, key_callback)
    print("Controles: W/S adelante/atrás, A/D izquierda/derecha, flechas Izq/Dcha rotan, Flecha Arriba/Abajo elevan/bajan la cámara, Q/E inclinan la cámara arriba/abajo")

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()
        ret, frame = cap.read()
        frame = cv2.flip(frame, 0)
        if not ret:
            break

        # Convertir imagen a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detectar manos
        results = hands.process(frame_rgb)
        print(results.multi_hand_landmarks)
        # Dibujar los puntos clave y conexiones
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Mostrar la imagen
        cv2.imshow("Salida", frame)

    cap.release()
    cv2.destroyAllWindows()
    glfw.terminate()

if __name__ == "__main__":
    main()