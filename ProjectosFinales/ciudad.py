import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluSphere, gluDeleteQuadric
import sys
import math
import cv2
import mediapipe as mp
import random

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

def draw_sphere(radius=1.0, slices=16, stacks=16, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)


def draw_box(width=1.0, height=1.0, depth=1.0, color=(0.8, 0.5, 0.2)):
    """
    Dibuja un cubo o rectángulo 3D (paralelepípedo) centrado en el origen.
    
    Parámetros:
    - width: tamaño a lo largo del eje X
    - height: tamaño a lo largo del eje Y
    - depth: tamaño a lo largo del eje Z
    - color: tupla RGB para el color de las caras (por defecto marrón)
    """
    w = width / 2.0
    h = height
    d = depth / 2.0

    glBegin(GL_QUADS)
    glColor3f(*color)

    # Frente (z = +d)
    glVertex3f(-w, 0, d)
    glVertex3f(w, 0, d)
    glVertex3f(w, h, d)
    glVertex3f(-w, h, d)

    # Atrás (z = -d)
    glVertex3f(-w, 0, -d)
    glVertex3f(w, 0, -d)
    glVertex3f(w, h, -d)
    glVertex3f(-w, h, -d)

    # Izquierda (x = -w)
    glVertex3f(-w, 0, -d)
    glVertex3f(-w, 0, d)
    glVertex3f(-w, h, d)
    glVertex3f(-w, h, -d)

    # Derecha (x = w)
    glVertex3f(w, 0, -d)
    glVertex3f(w, 0, d)
    glVertex3f(w, h, d)
    glVertex3f(w, h, -d)

    # Arriba (y = h)
    glVertex3f(-w, h, -d)
    glVertex3f(w, h, -d)
    glVertex3f(w, h, d)
    glVertex3f(-w, h, d)

    # Abajo (y = 0)
    glVertex3f(-w, 0, -d)
    glVertex3f(w, 0, -d)
    glVertex3f(w, 0, d)
    glVertex3f(-w, 0, d)

    glEnd()

def draw_paloma(wing_angle=10.0, scale=1.0):
    """
    Paloma simple animable:
    - wing_angle: grados para rotar alas (positivo -> ala izquierda hacia arriba)
    - scale: escala uniforme
    """
    glPushMatrix()
    # Aplicar escala global para ajustar tamaño fácilmente
    glScalef(scale, scale, scale)

    # -------- CUERPO --------
    draw_sphere(radius=1.0, color=(0.95, 0.95, 0.95))  # gris/blanco

    # -------- ALA IZQUIERDA --------
    glPushMatrix()
    glTranslatef(-1.2, 0.3, 0.0)
    glRotatef(wing_angle, 0, 0, 1)
    draw_box(width=2.0, height=0.15, depth=1.2, color=(0.85, 0.85, 0.85))
    glPopMatrix()

    # -------- ALA DERECHA --------
    glPushMatrix()
    glTranslatef(1.2, 0.3, 0.0)
    glRotatef(-wing_angle, 0, 0, 1)
    draw_box(width=2.0, height=0.15, depth=1.2, color=(0.85, 0.85, 0.85))
    glPopMatrix()

    glPopMatrix()



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
    global cam_pos, cam_center, hand_control_enabled, palomas_initialized, num_palomas
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
    elif key == glfw.KEY_P:  # P para MÁS palomas
        num_palomas += 1
        palomas_initialized = False  # forzar reinicialización con nuevo tamaño
        print(f"num_palomas = {num_palomas}")
    elif key == glfw.KEY_O:  # O para MENOS palomas
        num_palomas = max(0, num_palomas - 1)
        palomas_initialized = False
        print(f"num_palomas = {num_palomas}")
    elif key == glfw.KEY_H:
        hand_control_enabled = not hand_control_enabled
        print(f"Hand control: {'ON' if hand_control_enabled else 'OFF'}")


# --- Control de cámara con manos ---
hand_control_enabled = True  # habilita/deshabilita control por manos
hand_control_speed = 0.6     # multiplicador de velocidad para control por manos (70%)

# --- Estado de los coches (multicoches) ---
# Cada coche es un dict: {'pos':[x,y,z], 'dir':[dx,dy,dz], 'speed':v, 'width':w, 'height':h, 'depth':d, 'color':(r,g,b)}
cars = []
cars_initialized = False
cars_time_prev = None        # tiempo anterior para calcular delta para todos los coches

# --- Palomas configurables ---
num_palomas = 30             # número inicial de palomas
palomas_initialized = False  # control de inicialización de palomas


def process_hands(results):
    """Procesa los resultados de MediaPipe Hands para controlar la cámara.
    - Mano derecha: controla yaw (rotación horizontal) y pitch (inclinación) usando la muñeca (landmark 0).
    - Mano izquierda: controla avance/retroceso (adelantar/retroceder a lo largo del eje cámara) usando la posición vertical de la muñeca.
    - Se ha eliminado el zoom por pellizco.
    """
    global cam_pos, cam_center, hand_control_enabled
    if not hand_control_enabled:
        return
    if not results or not results.multi_hand_landmarks:
        return

    # Direcciones comunes
    dir_vec = [cam_center[0]-cam_pos[0], cam_center[1]-cam_pos[1], cam_center[2]-cam_pos[2]]
    dir_norm = normalize(dir_vec)
    right = [ dir_norm[2]*cam_up[1] - dir_norm[1]*cam_up[2],
              dir_norm[0]*cam_up[2] - dir_norm[2]*cam_up[0],
              dir_norm[1]*cam_up[0] - dir_norm[0]*cam_up[1] ]
    r_norm = normalize(right)

    # Iterar por cada mano detectada junto con su 'handedness'
    for i, hand in enumerate(results.multi_hand_landmarks):
        # Obtener label seguro (Left/Right)
        label = 'Right'
        if results.multi_handedness and i < len(results.multi_handedness):
            label = results.multi_handedness[i].classification[0].label

        wrist = hand.landmark[0]

        if label == 'Right':
            # Rotación/pitch por posición de muñeca (como antes)
            pos_sens = 2.0 * hand_control_speed
            max_angle = math.radians(3.0)
            dx = wrist.x - 0.5
            dy = wrist.y - 0.5
            if abs(dx) > 0.02:
                # Invertimos la señal para que mover la mano a la izquierda gire la cámara a la izquierda
                angle_y = dx * pos_sens * max_angle
                cam_center = rotate_y_around_point(cam_pos, cam_center, angle_y)
            if abs(dy) > 0.02:
                angle_pitch = dy * pos_sens * max_angle
                cam_center = rotate_around_axis(cam_pos, cam_center, r_norm, angle_pitch)

        elif label == 'Left':
            # Avanzar/retroceder según la altura de la muñeca: mano arriba -> avanzar
            fb_sens = 3.0 * hand_control_speed       # sensibilidad del avance (escalada)
            dy = 0.5 - wrist.y  # positivo si la muñeca está por encima del centro de la imagen
            if abs(dy) > 0.05:
                dz = dy * fb_sens
                # limitar por fotograma
                dz = max(min(dz, 1.0), -1.0)
                for j in range(3):
                    cam_pos[j] += dir_norm[j] * dz
                    cam_center[j] += dir_norm[j] * dz
                # Limitar distancia mínima al centro
                dist = math.sqrt((cam_pos[0]-cam_center[0])**2 + (cam_pos[1]-cam_center[1])**2 + (cam_pos[2]-cam_center[2])**2)
                min_dist = 2.0
                if dist < min_dist:
                    for j in range(3):
                        cam_pos[j] = cam_center[j] + dir_norm[j] * min_dist


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
    # Palomas ahora son entidades animadas inicializadas y dibujadas más abajo
    # (se han quitado estas palomas estáticas para evitar conflicto con el sistema animado)


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

    # Actualizar y dibujar coches (soporte para múltiples coches)
    global cars, cars_initialized, cars_time_prev
    current_time = glfw.get_time()
    if cars_time_prev is None:
        cars_time_prev = current_time
    dt = current_time - cars_time_prev
    cars_time_prev = current_time


    if not cars_initialized:
        cars.clear()
        #donde circularán los coches
        max_x = num_bloques_x * (bloque_ancho * casa_dist + separacion_bloques)
        #carril
        for bz in range(num_bloques_z - 1):
            lane_z = (bz+1) * (bloque_profundidad * casa_dist + separacion_bloques) - separacion_bloques * 0.5
            dir_sign = 1 if (bz % 2 == 0) else -1
            cars_per_lane = 4
            for ci in range(cars_per_lane):
                x = random.uniform(0, max_x)
                car = {
                    'pos': [x, 0.0, lane_z-5.0],
                    'dir': [dir_sign, 0.0, 0.0],
                    'speed': random.uniform(3.0, 6.0),
                    'width': 4.0,
                    'height': 1.8,
                    'depth': 2.5,
                    'color': (0.2, 0.2, 0.9)
                }
                cars.append(car)
        cars_initialized = True

    # Actualizar cada coche y dibujarlo
    max_x = num_bloques_x * (bloque_ancho * casa_dist + separacion_bloques)
    margin = casa_dist
    for car in cars:
        # Mover
        car['pos'][0] += car['dir'][0] * car['speed'] * dt
        # Wrap-around simple en X
        if car['dir'][0] > 0 and car['pos'][0] > max_x + margin:
            car['pos'][0] = -margin
        if car['dir'][0] < 0 and car['pos'][0] < -margin:
            car['pos'][0] = max_x + margin

        # Dibujar coche
        glPushMatrix()
        glTranslatef(*car['pos'])
        draw_box(width=car['width'], height=car['height'], depth=car['depth'], color=car['color'])
        # Techo
        glTranslatef(0, car['height'], 0)
        draw_box(width=car['width']*0.6, height=car['height']*0.8, depth=car['depth'], color=car['color'])
        glPopMatrix()

    # --- Palomas animadas ---
    global palomas, palomas_initialized
    if 'palomas' not in globals():
        palomas = []
        palomas_initialized = False

    if not palomas_initialized:
        palomas.clear()
        max_x = num_bloques_x * (bloque_ancho * casa_dist + separacion_bloques)
        max_z = num_bloques_z * (bloque_profundidad * casa_dist + separacion_bloques)
        for i in range(num_palomas):
            # Velocidad principalmente en Z (avance/retroceso), X para ligera deriva
            palomas.append({
                'pos': [random.uniform(0, max_x), random.uniform(6.0, 12.0), random.uniform(0, max_z)],
                'vel': [random.uniform(-0.4, 0.4), 0.0, random.uniform(-1.5, 1.5)],
                'scale': random.uniform(0.6, 1.2),
                'phase': random.random() * math.pi * 2,
                'amp': random.uniform(15.0, 30.0),
                'freq': random.uniform(2.0, 4.0),
                # breathing (respiración): fractional amplitude and frequency in Hz
                'breath_amp': random.uniform(0.04, 0.18),
                'breath_freq': random.uniform(0.6, 1.6),
                'breath_phase': random.random() * math.pi * 2
            })
        palomas_initialized = True

    t = glfw.get_time()
    max_x = num_bloques_x * (bloque_ancho * casa_dist + separacion_bloques)
    max_z = num_bloques_z * (bloque_profundidad * casa_dist + separacion_bloques)

    for p in palomas:
        # movimiento (principalmente en Z)
        vx = p['vel'][0]
        vz = p['vel'][2]
        p['pos'][0] += vx * dt
        p['pos'][2] += vz * dt

        # wrap-around en los límites del mapa
        if p['pos'][0] < 0:
            p['pos'][0] = max_x
        if p['pos'][0] > max_x:
            p['pos'][0] = 0
        if p['pos'][2] < 0:
            p['pos'][2] = max_z
        if p['pos'][2] > max_z:
            p['pos'][2] = 0

        # calcular ángulo de ala
        wing_angle = math.sin(t * p['freq'] + p['phase']) * p['amp']
        # breathing (respiración): escalado oscilante
        breath = math.sin(t * p['breath_freq'] * (2 * math.pi) + p['breath_phase'])
        current_scale = p['scale'] * (1.0 + p['breath_amp'] * breath)
        current_scale = max(0.2, current_scale)  # evitar escalas negativas o demasiado pequeñas

        # orientación en Y: atan2(x, z) para obtener ángulo respecto al eje Z
        heading = math.degrees(math.atan2(vx, vz)) if (vx != 0 or vz != 0) else 0.0

        glPushMatrix()
        glTranslatef(*p['pos'])
        glRotatef(heading, 0, 1, 0)
        draw_paloma(wing_angle=wing_angle, scale=current_scale)
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
    print("H: alternar control por manos (mano izquierda: avanzar/retroceder; mano derecha: rotar/inclinar)")

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
        # Procesar control de cámara con las manos
        process_hands(results)
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