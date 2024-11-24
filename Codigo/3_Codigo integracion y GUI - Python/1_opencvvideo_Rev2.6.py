import cv2
import numpy as np
import serial
import time
#Interfaz grafica
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
letra = None
import os
global frame_redimensionado
R10K1=0
R10K2=0
R4K71=0
R4K72=0
R4K73=0
R22K1=0
R1501=0
R391=0
T1=0
D1=0
D2=0
D3=0
D4=0
D5=0
fplaca1=0
fplaca2=0
fplaca3=0
fplaca4=0
fplaca5=0
command = 0 # variable que hace girar la placa o el ascensor
#Comunicacion con el arduino Mega
arduino = serial.Serial('COM5', 9600)
time.sleep(2)  # Espera un poco para la inicialización del Arduino
esp32 = serial.Serial('COM3', 9600)
time.sleep(2)
#frame_redimensionado=0
lista_deteccion = [None]
n=0
letra = 0
# Acceder a la cámara
captura_video = cv2.VideoCapture(2)  # Usa 0 para la cámara predeterminada.
lista_placa_5 = ['5R4K71.jpg', '5R4K72.jpg', '5R4K73.jpg','5R10K1.jpg', '5R10K2.jpg','5R22K1.jpg','5R391.jpg','5R1501.jpg','5T1.jpg','5D1.jpg', '5D2.jpg', '5D3.jpg', '5D4.jpg', '5D5.jpg']
lista_placa_4 = ['4R4K71.jpg', '4R4K72.jpg', '4R4K73.jpg','4R10K1.jpg', '4R10K2.jpg','4R22K1.jpg','4R391.jpg','4R1501.jpg','4T1.jpg','4D1.jpg', '4D2.jpg', '4D3.jpg', '4D4.jpg', '4D5.jpg']
lista_placa_3 = ['3R4K71.jpg', '3R4K72.jpg', '3R4K73.jpg','3R10K1.jpg', '3R10K2.jpg','3R22K1.jpg','3R391.jpg','3R1501.jpg','3T1.jpg','3D1.jpg', '3D2.jpg', '3D3.jpg', '3D4.jpg', '3D5.jpg']
lista_placa_2 = ['2R4K71.jpg', '2R4K72.jpg', '2R4K73.jpg','2R10K1.jpg', '2R10K2.jpg','2R22K1.jpg','2R391.jpg','2R1501.jpg','2T1.jpg','2D1.jpg', '2D2.jpg', '2D3.jpg', '2D4.jpg', '2D5.jpg']
lista_placa_1 = ['1R4K71.jpg', '1R4K72.jpg', '1R4K73.jpg','1R10K1.jpg', '1R10K2.jpg','1R22K1.jpg','1R391.jpg','1R1501.jpg','1T1.jpg','1D1.jpg', '1D2.jpg', '1D3.jpg', '1D4.jpg', '1D5.jpg']
#lista_placa_4_sold = ['4sold1.jpg','4sold2.jpg','4sold3.jpg','4sold5.jpg',]
listas = { #transformo en un diccionario las listas anteriorres para usarlas en la funcion Video
    1: lista_placa_1, # y elegir con la variable n la lista correspondiente. De esta manera
    2: lista_placa_2, # evito hacer un if por cada lista, solo utilizo lista[n]
    3: lista_placa_3,
    4: lista_placa_4,
    5: lista_placa_5,
    #6: lista_placa_4_sold,
}
placas = {
    'placa_1': ['1F1.jpg'],
    'placa_2': ['2F1.jpg'],
    'placa_3': ['3F1.jpg'],
    'placa_4': ['4F1.jpg'],
    'placa_5': ['5F1.jpg'],
}
comp_1 = {
    '1R4K7': ['1R4K71.jpg', '1R4K72.jpg', '1R4K73.jpg'],
    '1R10K': ['1R10K1.jpg', '1R10K2.jpg'],
    '1R22K': ['1R22K1.jpg'],
    '1R39': ['1R391.jpg'],
    '1R150': ['1R1501.jpg'],
    '1T': ['1T1.jpg'],
    '1D': ['1D1.jpg', '1D2.jpg', '1D3.jpg', '1D4.jpg', '1D5.jpg'],
}
comp_2 = {
    '2R4K7': ['2R4K71.jpg', '2R4K72.jpg', '2R4K73.jpg'],
    '2R10K': ['2R10K1.jpg', '2R10K2.jpg'],
    '2R22K': ['2R22K1.jpg'],
    '2R39': ['2R391.jpg'],
    '2R150': ['2R1501.jpg'],
    '2T': ['2T1.jpg'],
    '2D': ['2D1.jpg', '2D2.jpg', '2D3.jpg', '2D4.jpg', '2D5.jpg'],
}
comp_3 = {
    '3R4K7': ['3R4K71.jpg', '3R4K72.jpg', '3R4K73.jpg'],
    '3R10K': ['3R10K1.jpg', '3R10K2.jpg'],
    '3R22K': ['3R22K1.jpg'],
    '3R39': ['3R391.jpg'],
    '3R150': ['3R1501.jpg'],
    '3T': ['3T1.jpg'],
    '3D': ['3D1.jpg', '3D2.jpg', '3D3.jpg', '3D4.jpg', '3D5.jpg'],
}
comp_4 = {
    '4R4K7': ['4R4K71.jpg', '4R4K72.jpg', '4R4K73.jpg'],
    '4R10K': ['4R10K1.jpg', '4R10K2.jpg'],
    '4R22K': ['4R22K1.jpg'],
    '4R39': ['4R391.jpg'],
    '4R150': ['4R1501.jpg'],
    '4T': ['4T1.jpg'],
    '4D': ['4D1.jpg', '4D2.jpg', '4D3.jpg', '4D4.jpg', '4D5.jpg'],
}
comp_5 = {
    '5R4K7': ['5R4K71.jpg', '5R4K72.jpg', '5R4K73.jpg'],
    '5R10K': ['5R10K1.jpg', '5R10K2.jpg'],
    '5R22K': ['5R22K1.jpg'],
    '5R39': ['5R391.jpg'],
    '5R150': ['5R1501.jpg'],
    '5T': ['5T1.jpg'],
    '5D': ['5D1.jpg', '5D2.jpg', '5D3.jpg', '5D4.jpg', '5D5.jpg'],
}
sold_4 = {
    '4sold1': ['4sold1.jpg'],
    '4sold2': ['4sold2.jpg'],
    '4sold3': ['4sold3.jpg'],
    '4sold4': ['4sold5.jpg'],
}
sold_1 = {
    '1sold1': ['1sold1.jpg'],
    '1sold2': ['1sold2.jpg'],
}
sold_2 = {
}
sold_3 = {
}
sold_5 = {
}
# Lista de plantillas para resistencias, diodos, capacitores
# componentes = {
#     '4k7': ['1R4K71.jpg', '1R4K72.jpg', '1R4K73.jpg', '2R4K71.jpg', '2R4K72.jpg', '2R4K73.jpg', '3R4K71.jpg',
#             '3R4K72.jpg', '3R4K73.jpg', '4R4K71.jpg', '4R4K72.jpg', '4R4K73.jpg', '5R4K71.jpg', '5R4K72.jpg',
#             '5R4K73.jpg'],
#     '10k': ['1R10K1.jpg', '1R10K2.jpg', '2R10K1.jpg', '2R10K2.jpg', '3R10K1.jpg', '3R10K2.jpg', '4R10K1.jpg',
#             '4R10K2.jpg', '5R10K1.jpg', '5R10K2.jpg'],
#     '22k': ['1R22K1.jpg', '2R22K1.jpg', '3R22K1.jpg', '4R22K1.jpg', '5R22K1.jpg'],
#     '39': ['1R391.jpg', '2R391.jpg', '3R391.jpg', '4R391.jpg', '5R391.jpg'],
#     '150': ['1R1501.jpg', '2R1501.jpg', '3R1501.jpg', '4R1501.jpg', '5R1501.jpg'],
#     'T': ['1T1.jpg', '2T1.jpg', '3T1.jpg', '4T1.jpg', '5T1.jpg'],
#     'D': ['1D1.jpg', '1D2.jpg', '1D3.jpg', '1D4.jpg', '1D5.jpg', '2D1.jpg', '2D2.jpg', '2D3.jpg', '2D4.jpg', '2D5.jpg',
#           '3D1.jpg', '3D2.jpg', '3D3.jpg', '3D4.jpg', '3D5.jpg', '4D1.jpg', '4D2.jpg', '4D3.jpg', '4D4.jpg', '4D5.jpg',
#           '5D1.jpg', '5D2.jpg', '5D3.jpg', '5D4.jpg', '5D5.jpg'],
# }


# Función para detectar componentes y obtener la ubicación del centro
def detectar_componentes(gray_imagen, componentes, umbral,frame_redimensionado):
    ubicaciones = []  # Lista para almacenar las ubicaciones de los componentes
    for componente, plantillas in componentes.items():
        for ruta_plantilla in plantillas:
            plantilla = cv2.imread(ruta_plantilla, 0)
            if plantilla is None:
                print(f"Error: No se pudo cargar la plantilla {ruta_plantilla}. Verifica la ruta.")
                continue

            w, h = plantilla.shape[::-1]  # Ancho y alto de la plantilla
            resultado = cv2.matchTemplate(gray_imagen, plantilla, cv2.TM_CCOEFF_NORMED)
            loc = np.where(resultado >= umbral)

            for pt in zip(*loc[::-1]):
                # Dibujar el rectángulo en la imagen para visualización
                cv2.rectangle(frame_redimensionado, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

                # Calcular el centro del componente detectado
                centro_x = pt[0] + w // 2
                centro_y = pt[1] + h // 2

                # Almacenar las coordenadas del centro
                ubicacion = {
                    'componente': componente,
                    #'centro': (centro_x, centro_y),
                    'uni': ruta_plantilla,
                }
                ubicaciones.append(ubicacion)

                # Cambiar el tipo de fuente, tamaño, grosor y color del texto
                font = cv2.FONT_HERSHEY_COMPLEX  # Fuente más clara
                font_size = 0.8
                font_thickness = 1
                text_color = (0, 0, 255)  # Color rojo

                # Dibujar el texto del componente detectado en el centro
                cv2.putText(frame_redimensionado, componente, (centro_x - 10, centro_y - 10), font, font_size,
                            text_color, font_thickness, cv2.LINE_AA)


    return ubicaciones

#################################################
#################################################
# funcion para iniciar video luego se utiliza la funcion para detectar componentes
def video(objetos,umbral, n):
    global ubicaciones_componentes
    ret, frame = captura_video.read()

    # Verificar si se ha capturado correctamente el frame
    if ret:
        # Redimensionar el frame (si es necesario)
        global frame_redimensionado
        frame_redimensionado= frame

        # Convertir el frame a escala de grises
        gray_imagen = cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2GRAY)

        # Aplicar la detección de componentes en el frame
        ubicaciones_componentes = detectar_componentes(gray_imagen, objetos, umbral,frame_redimensionado)
        #cv2.imshow('Componentes Detectados', frame_redimensionado)
        # Mostrar el frame con los componentes detectados
        #print(objetos)
        if n == 6 or n == 5 or n == 4 or n == 3 or n == 2 or n == 1:

            #cv2.imshow('Componentes Detectados', frame_redimensionado)
            if (objetos==comp_1 or objetos==comp_2 or objetos==comp_3 or objetos==comp_4 or objetos==comp_5):
                cv2.imwrite("impl.png", frame_redimensionado)
            else:
                cv2.imwrite("imsold.png", frame_redimensionado)
            #///////////////////////////////////////////////////////////////////////////


            #///////////////////////////////////////////////////////////////////////////
            for ubicacion in ubicaciones_componentes:
                # componente = ubicacion['componente']  # Nombre del componente detectado
                # centro = ubicacion['centro']  # Coordenadas del centro del componente
                comp_unitario = ubicacion['uni']
                lista_deteccion.append(comp_unitario)
                # Imprimir el nombre del componente y sus coordenadas
                # print(f"Componente: {comp_unitario}, Centro: {centro}")
            #elementos_faltantes = list(set(lista_placa_5) - set(lista_deteccion))
            if n <= 5:
                global elementos_faltantes
                elementos_faltantes = list(set(listas[n]) - set(lista_deteccion))
                print("Elementos faltantes:", elementos_faltantes)
                with open("faltantes_componentes.txt", "w") as file:
                    # Convertir la lista en una cadena de texto separada por saltos de línea
                    for elemento in elementos_faltantes:
                        file.write(f"{elemento}\n")
            elif n >= 6:
                elementos_faltantes = list(set(lista_deteccion)) # error de soldadura
                print("Errores de soldadura:", elementos_faltantes)
                with open("faltantes_soldadura.txt", "w") as file:
                    # Convertir la lista en una cadena de texto separada por saltos de línea
                    for elemento in elementos_faltantes:
                        file.write(f"{elemento}\n")
            lista_deteccion.clear()
            #n=0

            #cv2.waitKey(0)  # Espera indefinidamente a que se presione una tecla
            cv2.destroyAllWindows()
            #cv2.waitKey(0)
    else:
        print("Error en la captura de video.")
    #captura_video.release()
    #cv2.destroyAllWindows()

    return ubicaciones_componentes

#Funcion para girar placa o ascensor arduino
def send_command(command):
    """Envía un comando al Arduino y espera la respuesta."""
    arduino.write(command.encode())  # Enviar el comando
    time.sleep(0.2)  # Breve espera para la transmisión

def send_com_esp(command):
    """Envía un comando a la ESP32 y espera la respuesta."""
    esp32.write(command.encode())  # Enviar el comando
    time.sleep(0.1)
# def discri_comp (comp_placa):
#     for ubicacion in comp_placa:
#         # componente = ubicacion['componente']  # Nombre del componente detectado
#         # centro = ubicacion['centro']  # Coordenadas del centro del componente
#         comp_unitario = ubicacion['uni']
#         lista_deteccion.append(comp_unitario)
#         # Imprimir el nombre del componente y sus coordenadas
#         # print(f"Componente: {comp_unitario}, Centro: {centro}")
#     elementos_faltantes = list(set(lista_placa_5) - set(lista_deteccion))
#     print("Elementos faltantes:", elementos_faltantes)
def seccuencia ():
    com = 'h'
    send_com_esp(com)
    time.sleep(25)
    com = 'p'
    send_com_esp(com)
    time.sleep(18)
    com = 'o'
    send_com_esp(com)
    # medir puntas
    time.sleep(28)
    com = 'p'
    send_com_esp(com)
    time.sleep(35)
    com = 'h'
    send_com_esp(com)
    time.sleep(35)
    # letra = 0

#////////////////////////////////////////////////////////////////////////////////////////////
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Interfaz Gráfica")
        self.setFixedSize(1100, 550)

        # Crear botón "Siguiente"
        boton_siguiente = QPushButton("Siguiente", self)
        boton_siguiente.clicked.connect(self.guardar_letra)  # Conectar el botón a la función
        boton_siguiente.setFixedSize(int(3 * 37.8), int(1 * 37.8))


        # Crear cuadro de imagen 1 de 6x6 cm en píxeles
        self.cuadro_imagen1 = QLabel(self)
        self.cuadro_imagen1.setFixedSize(350, 350)  # 6 cm x 6 cm en píxeles
        self.cuadro_imagen1.setStyleSheet("border: 1px solid black;")
        self.cuadro_imagen1.setAlignment(Qt.AlignCenter)

        # Crear título para el cuadro de imagen 1
        titulo1 = QLabel("Componentes", self)
        titulo1.setAlignment(Qt.AlignCenter)
        #elementos_faltantes= 'holis'
        #texto1 = QLabel(", ".join(elementos_faltantes), self)
        titulo3 = QLabel("Componentes faltantes:", self)
        titulo3.setAlignment(Qt.AlignCenter)
        titulo4 = QLabel("Errores de soldadura:", self)
        titulo4.setAlignment(Qt.AlignCenter)

        # Crear un cuadro para el texto debajo de la imagen 1 (QFrame o QLabel)
        self.texto1 = QLabel(self)
        self.texto1.setFixedSize(350, 100)  # Tamaño del texto, mismo ancho que la imagen
        self.texto1.setAlignment(Qt.AlignCenter)
        self.texto1.setStyleSheet("border: 1px solid black;")  # Borde para simular un cuadro

        # Crear layout vertical para cuadro de imagen 1, su título y el texto
        #layout_texto1 = QVBoxLayout()
        #layout_texto1.addWidget(titulo3)
        #layout_texto1.addWidget(self.texto1)
        #layout_texto1.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))  # Espacio de 3 cm
        #layout_texto1.addWidget(self.texto1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mostrar_elementos_faltantes)  # Conectar la señal de timeout al método
        self.timer.start(3000)  # Establecer el intervalo en 3000 milisegundos (3 segundos)

        # Crear layout vertical para cuadro de imagen 1, su título y el texto
        layout_imagen1 = QVBoxLayout()
        layout_imagen1.addWidget(titulo1)
        layout_imagen1.addWidget(self.cuadro_imagen1)
        layout_imagen1.addSpacerItem(QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))  # Espacio de 3 cm
        layout_imagen1.addWidget(titulo3)
        layout_imagen1.addWidget(self.texto1)

        # Crear cuadro de imagen 2 de 6x6 cm en píxeles
        self.cuadro_imagen2 = QLabel(self)
        self.cuadro_imagen2.setFixedSize(350, 350)  # 6 cm x 6 cm en píxeles
        self.cuadro_imagen2.setStyleSheet("border: 1px solid black;")
        self.cuadro_imagen2.setAlignment(Qt.AlignCenter)

        # Crear título para el cuadro de imagen 2
        titulo2 = QLabel("Soldadura", self)
        titulo2.setAlignment(Qt.AlignCenter)

        # Crear un cuadro para el texto debajo de la imagen 2 (QFrame o QLabel)
        self.texto2 = QLabel(self)
        self.texto2.setFixedSize(350, 100)  # Tamaño del texto, mismo ancho que la imagen
        self.texto2.setAlignment(Qt.AlignCenter)
        self.texto2.setStyleSheet("border: 1px solid black;")  # Borde para simular un cuadro

        # Crear layout vertical para cuadro de imagen 2, su título y el texto
        layout_imagen2 = QVBoxLayout()
        layout_imagen2.addWidget(titulo2)
        layout_imagen2.addWidget(self.cuadro_imagen2)
        layout_imagen2.addSpacerItem(QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))  # Espacio de 3 cm
        layout_imagen2.addWidget(titulo4)
        layout_imagen2.addWidget(self.texto2)

        # Crear un layout horizontal principal
        h_layout = QHBoxLayout()

        # Agregar el botón al layout principal
        h_layout.addWidget(boton_siguiente)

        # Agregar un espaciador de 3 cm (aproximadamente 113 píxeles) entre el botón y el primer cuadro de imagen
        h_layout.addSpacerItem(QSpacerItem(113, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # Agregar el layout vertical del primer cuadro de imagen al layout principal
        h_layout.addLayout(layout_imagen1)

        # Agregar un espaciador de 3 cm (aproximadamente 113 píxeles) entre los cuadros de imagen
        h_layout.addSpacerItem(QSpacerItem(70, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # Agregar el layout vertical del segundo cuadro de imagen al layout principal
        h_layout.addLayout(layout_imagen2)

        # Establecer el layout principal en la ventana
        self.setLayout(h_layout)


        self.timer = self.startTimer(3000)
        #self.mostrar_imagen('impl.jpg')
    def timerEvent(self, event):
        """Actualizar las imágenes mostradas cada vez que se activa el temporizador."""
        self.mostrar_imagen('impl.png', self.cuadro_imagen1)
        self.mostrar_imagen('imsold.png', self.cuadro_imagen2)
        #texto1 = QLabel(", ".join(str(elemento) for elemento in elementos_faltantes), self)
        #texto1 = QLabel(elementos_faltantes, self)

    def guardar_letra(self):
        """Guardar la letra 'd' en la variable global 'letra'."""
        global letra
        letra = 'd'
        #print(f"Letra guardada: {letra}")  # Confirmación en consola

    def mostrar_imagen(self, imagen_path, cuadro_imagen):
        print(f"Ruta proporcionada: {imagen_path}")
        # Verificar existencia de la ruta
        if not os.path.exists(imagen_path):
            print("Error: La ruta no existe.")
            return
        #imagen_path = r"C:/1_Leandro-EBMPAPST/100_Leandro/7_Facu/2_2024/3_Materias de cursada/1_Proyecto/8_Deteccion openCV/1_Imagenes raiz/4/5F1.jpg"

        # Intentar cargar la imagen
        pixmap = QPixmap(imagen_path)
        if pixmap.isNull():
            print("Error: No se pudo cargar la imagen con QPixmap.")
            return

        # Mostrar la imagen
        cuadro_imagen.setPixmap(pixmap.scaled(cuadro_imagen.size(), Qt.KeepAspectRatio))
        print("Imagen cargada correctamente.")

    def mostrar_elementos_faltantes(self):
        """Leer el archivo de texto y actualizar el QLabel con los elementos faltantes."""
        try:
            with open("faltantes_componentes.txt", "r") as file:
                contenido_comp = file.read()  # Leer todo el contenido del archivo

            # Actualizar el texto del QLabel
            self.texto1.setText(contenido_comp)

        except FileNotFoundError:
            self.texto1.setText("Archivo no encontrado.")

        try:
            with open("faltantes_soldadura.txt", "r") as file:
                #contenido_sold = file.read()  # Leer todo el contenido del archivo
                lineas = file.readlines()  # Leer todas las líneas del archivo
                lineas = [linea for linea in lineas if linea.strip()]
                cant_sold = len(lineas)
                #print(f'Cantidad errores soldadura {cant_sold}')
            # Actualizar el texto del QLabel
            self.texto2.setText(f'{cant_sold}')
            #self.texto2.setText(contenido_sold)
        except FileNotFoundError:
            self.texto2.setText("Archivo no encontrado.")


# Función para la lógica de detección
def main_logic():
    global letra
    while True:
        print('el valor de letra es' )
        print(letra)
        # cv2.waitKey(0)
        #letra = input("Ingrese la letra 'd' para iniciar la detección: ").strip().lower()
        # num = input("Ingrese el numero 8 para iniciar la detección: ")
        if letra == 'd':
            n = 0
            # letra = 0
            letra = ''
            command = 'g'  # con la letra g hago que el gira placas muestre los componentes a la camara
            send_command(command)
            time.sleep(5)
            command = 'l'
            send_command(command)
            time.sleep(9)

            num_placa = video(placas, 0.85, n)

            for ubicacion in num_placa:
                componente = ubicacion['componente']
                print(f"Componente: {componente}")
                if componente == 'placa_5':
                    n = 5
                    video(comp_5, 0.8, n)
                    command = 's'  # con la letra s hago que el gira placas muestre las soldaduras a la camara
                    n = 6
                    send_command(command)
                    time.sleep(7)
                    video(sold_5, 0.8, n)
                    #/////////////////////


                    #/////////////////////
                    time.sleep(2)
                    command = 'w'
                    send_command(command)
                    time.sleep(7)
                    seccuencia()
                    # command_esp = 'p'
                    # send_command_esp(command_esp)
                    # time.sleep(7)
                    # command_esp = 'o'
                    # send_command_esp(command_esp)
                    # #medir puntas
                    # time.sleep(7)
                    # command_esp = 'p'
                    # send_command_esp(command_esp)
                    # time.sleep(7)
                    # command_esp = 'h'
                    # send_command_esp(command_esp)
                    # time.sleep(7)
                    # letra = 0
                    # discri_comp(comp_placa)
                    # cv2.imshow('Componentes Detectados', frame_redimensionado)
                if componente == 'placa_4':
                    n = 4
                    video(comp_4, 0.8, n)
                    command = 's'  # con la letra s hago que el gira placas muestre las soldaduras a la camara
                    n = 6
                    send_command(command)
                    time.sleep(7)
                    video(sold_4, 0.8, n)
                    time.sleep(2)
                    command = 'w'
                    send_command(command)
                    time.sleep(7)
                    seccuencia()
                    # letra = 0
                    # discri_comp(comp_placa)
                if componente == 'placa_3':
                    n = 3
                    video(comp_3, 0.8, n)
                    command = 's'  # con la letra s hago que el gira placas muestre las soldaduras a la camara
                    n = 6
                    send_command(command)
                    time.sleep(7)
                    video(sold_3, 0.8, n)
                    time.sleep(2)
                    command = 'w'
                    send_command(command)
                    time.sleep(7)
                    seccuencia()
                    # letra = 0
                if componente == 'placa_2':
                    n = 2
                    video(comp_2, 0.8, n)
                    command = 's'  # con la letra s hago que el gira placas muestre las soldaduras a la camara
                    n = 6
                    send_command(command)
                    time.sleep(7)
                    video(sold_2, 0.8, n)
                    time.sleep(2)
                    command = 'w'
                    send_command(command)
                    time.sleep(7)
                    seccuencia()
                    # com = 'h'
                    # send_com_esp(com)
                    # time.sleep(25)
                    # com = 'p'
                    # send_com_esp(com)
                    # time.sleep(18)
                    # com = 'o'
                    # send_com_esp(com)
                    # # medir puntas
                    # time.sleep(28)
                    # com = 'p'
                    # send_com_esp(com)
                    # time.sleep(35)
                    # com = 'h'
                    # send_com_esp(com)
                    # time.sleep(35)
                    # #letra = 0
                if componente == 'placa_1':
                    n = 1
                    video(comp_1, 0.8, n)
                    command = 's'  # con la letra s hago que el gira placas muestre las soldaduras a la camara
                    n = 6
                    send_command(command)
                    time.sleep(7)
                    video(sold_1, 0.8, n)
                    time.sleep(2)
                    command = 'w'
                    send_command(command)
                    time.sleep(7)
                    seccuencia()
                    # letra = 0
                command = 'g'  # break
                send_command(command)
                letra = ''
                break
            # break  # Salimos del bucle después de iniciar la detección
        else:
            print("Letra incorrecta. Inténtelo de nuevo.")


# Función principal para iniciar la interfaz gráfica
def iniciar_aplicacion():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()

    # Iniciar la lógica en un hilo independiente
    logic_thread = threading.Thread(target=main_logic, daemon=True)
    logic_thread.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    iniciar_aplicacion()



#///////////////////////////////////////////////////////////////////////////////////////////





    # for ubicacion in ubicaciones_componentes:
    #     componente = ubicacion['componente']  # Nombre del componente detectado
    #     #centro = ubicacion['centro']  # Coordenadas del centro del componente
    #
    #     # Imprimir el nombre del componente y sus coordenadas
    #     print(f"Componente: {componente}")#, Centro: {centro}")
    #     if componente == 'placa_5':
    #         # Leer un solo frame de la cámara
    #         ret, frame = captura_video.read()
    #
    #         # Verificar si se ha capturado correctamente el frame
    #         if ret:
    #             # Redimensionar el frame (si es necesario)
    #             frame_redimensionado = frame
    #
    #             # Convertir el frame a escala de grises
    #             gray_imagen = cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2GRAY)
    #
    #             # Aplicar la detección de componentes en el frame
    #             comp_placas = detectar_componentes(gray_imagen, comp_5, umbral = 0.85)
    #             # Mostrar el frame con los componentes detectados
    #             cv2.imshow('Componentes Detectados', frame_redimensionado)
    #             for ubicacion in comp_placas:
    #                 #componente = ubicacion['componente']  # Nombre del componente detectado
    #                 #centro = ubicacion['centro']  # Coordenadas del centro del componente
    #                 comp_unitario = ubicacion['uni']
    #                 lista_deteccion.append(comp_unitario)
    #                 # Imprimir el nombre del componente y sus coordenadas
    #                 #print(f"Componente: {comp_unitario}, Centro: {centro}")
    #
    #             #print(type(comp_placas))
    #             #print(comp_placas)
    #     elementos_faltantes = list(set(lista_placa_5) - set(lista_deteccion))
    #     print("Elementos faltantes:", elementos_faltantes)
    #             #print(ubicacion)
    #     if componente == 'placa_4':
    #         # Leer un solo frame de la cámara
    #         ret, frame = captura_video.read()
    #
    #         # Verificar si se ha capturado correctamente el frame
    #         if ret:
    #             # Redimensionar el frame (si es necesario)
    #             frame_redimensionado = frame
    #
    #             # Convertir el frame a escala de grises
    #             gray_imagen = cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2GRAY)
    #
    #             # Aplicar la detección de componentes en el frame
    #             comp_placas = detectar_componentes(gray_imagen, comp_4, umbral = 0.75)
    #
    #             # Mostrar el frame con los componentes detectados
    #             cv2.imshow('Componentes Detectados', frame_redimensionado)
    #             for ubicacion in comp_placas:
    #                 #componente = ubicacion['componente']  # Nombre del componente detectado
    #                 #centro = ubicacion['centro']  # Coordenadas del centro del componente
    #
    #                 # Imprimir el nombre del componente y sus coordenadas
    #                 #print(f"Componente: {componente}, Centro: {centro}")
    #                 comp_unitario = ubicacion['uni']
    #                 lista_deteccion.append(comp_unitario)
    #                 # Imprimir el nombre del componente y sus coordenadas
    #                 # print(f"Componente: {comp_unitario}, Centro: {centro}")
    #
    #                 # print(type(comp_placas))
    #                 # print(comp_placas)
    #             elementos_faltantes = list(set(lista_placa_4) - set(lista_deteccion))
    #             print("Elementos faltantes:", elementos_faltantes)
    #     if componente == 'placa_3':
    #         # Leer un solo frame de la cámara
    #         ret, frame = captura_video.read()
    #
    #         # Verificar si se ha capturado correctamente el frame
    #         if ret:
    #             # Redimensionar el frame (si es necesario)
    #             frame_redimensionado = frame
    #
    #             # Convertir el frame a escala de grises
    #             gray_imagen = cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2GRAY)
    #
    #             # Aplicar la detección de componentes en el frame
    #             comp_placas = detectar_componentes(gray_imagen, comp_3, umbral = 0.87)
    #
    #             # Mostrar el frame con los componentes detectados
    #             cv2.imshow('Componentes Detectados', frame_redimensionado)
    #             for ubicacion in comp_placas:
    #                 #componente = ubicacion['componente']  # Nombre del componente detectado
    #                 #centro = ubicacion['centro']  # Coordenadas del centro del componente
    #
    #                 # Imprimir el nombre del componente y sus coordenadas
    #                 #print(f"Componente: {componente}, Centro: {centro}")
    #                 comp_unitario = ubicacion['uni']
    #                 lista_deteccion.append(comp_unitario)
    #                 # Imprimir el nombre del componente y sus coordenadas
    #                 # print(f"Componente: {comp_unitario}, Centro: {centro}")
    #
    #                 # print(type(comp_placas))
    #                 # print(comp_placas)
    #             elementos_faltantes = list(set(lista_placa_3) - set(lista_deteccion))
    #             print("Elementos faltantes:", elementos_faltantes)
    #     if componente == 'placa_2':
    #         # Leer un solo frame de la cámara
    #         ret, frame = captura_video.read()
    #
    #         # Verificar si se ha capturado correctamente el frame
    #         if ret:
    #             # Redimensionar el frame (si es necesario)
    #             frame_redimensionado = frame
    #
    #             # Convertir el frame a escala de grises
    #             gray_imagen = cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2GRAY)
    #
    #             # Aplicar la detección de componentes en el frame
    #             comp_placas = detectar_componentes(gray_imagen, comp_2, umbral = 0.87)
    #
    #             # Mostrar el frame con los componentes detectados
    #             cv2.imshow('Componentes Detectados', frame_redimensionado)
    #             for ubicacion in comp_placas:
    #                 #componente = ubicacion['componente']  # Nombre del componente detectado
    #                 #centro = ubicacion['centro']  # Coordenadas del centro del componente
    #
    #                 # Imprimir el nombre del componente y sus coordenadas
    #                 #print(f"Componente: {componente}, Centro: {centro}")
    #                 comp_unitario = ubicacion['uni']
    #                 lista_deteccion.append(comp_unitario)
    #                 # Imprimir el nombre del componente y sus coordenadas
    #                 # print(f"Componente: {comp_unitario}, Centro: {centro}")
    #
    #                 # print(type(comp_placas))
    #                 # print(comp_placas)
    #             elementos_faltantes = list(set(lista_placa_2) - set(lista_deteccion))
    #             print("Elementos faltantes:", elementos_faltantes)
    #     if componente == 'placa_1':
    #         # Leer un solo frame de la cámara
    #         ret, frame = captura_video.read()
    #
    #         # Verificar si se ha capturado correctamente el frame
    #         if ret:
    #             # Redimensionar el frame (si es necesario)
    #             frame_redimensionado = frame
    #
    #             # Convertir el frame a escala de grises
    #             gray_imagen = cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2GRAY)
    #
    #             # Aplicar la detección de componentes en el frame
    #             comp_placas = detectar_componentes(gray_imagen, comp_1, umbral = 0.87)
    #
    #             # Mostrar el frame con los componentes detectados
    #             cv2.imshow('Componentes Detectados', frame_redimensionado)
    #             for ubicacion in comp_placas:
    #                 #componente = ubicacion['componente']  # Nombre del componente detectado
    #                 #centro = ubicacion['centro']  # Coordenadas del centro del componente
    #
    #                 # Imprimir el nombre del componente y sus coordenadas
    #                 #print(f"Componente: {componente}, Centro: {centro}")
    #                 comp_unitario = ubicacion['uni']
    #                 lista_deteccion.append(comp_unitario)
    #                 # Imprimir el nombre del componente y sus coordenadas
    #                 # print(f"Componente: {comp_unitario}, Centro: {centro}")
    #
    #                 # print(type(comp_placas))
    #                 # print(comp_placas)
    #             elementos_faltantes = list(set(lista_placa_5) - set(lista_deteccion))
    #             print("Elementos faltantes:", elementos_faltantes)
    #     if 360 <= centro[0] <= 373 and 118 <= centro[1] <= 135 and componente == '10k':
    #         print('componente ok')
    #         R10K1 = 1
    #     if 350 <= centro[0] <= 370 and 140 <= centro[1] <= 159 and componente == '10k':
    #         #print('componente ok')
    #         R10K2 = 1
    #     if 300 <= centro[0] <= 320 and 158 <= centro[1] <= 170 and componente == '4k7':
    #         #print('componente ok')
    #         R4K71 = 1
    #     if 310 <= centro[0] <= 325 and 178 <= centro[1] <= 192 and componente == '4k7':
    #         # print('componente ok')
    #         R4K72 = 1
    #     if 155 <= centro[0] <= 170 and 237 <= centro[1] <= 252 and componente == '4k7':
    #         # print('componente ok')
    #         R4K73 = 1
    #     if 305 <= centro[0] <= 327 and 275 <= centro[1] <= 288 and componente == '22k':
    #         # print('componente ok')
    #         R22K1 = 1
    #     if 214 <= centro[0] <= 224 and 316 <= centro[1] <= 329 and componente == '150':
    #         # print('componente ok')
    #         R1501 = 1
    #     if 200 <= centro[0] <= 225 and 332 <= centro[1] <= 347 and componente == '39':
    #         # print('componente ok')
    #         R391 = 1
    #     if 230 <= centro[0] <= 245 and 232 <= centro[1] <= 245 and componente == 'T1':
    #         # print('componente ok')
    #         T1=1
    #     if 309 <= centro[0] <= 325 and 193 <= centro[1] <= 205 and componente == 'D1':
    #         # print('componente ok')
    #         D1 = 1
    #     if 158 <= centro[0] <= 172 and 156 <= centro[1] <= 170 and componente == 'D2':
    #         # print('componente ok')
    #         D2 = 1
    #     if 154 <= centro[0] <= 174 and 175 <= centro[1] <= 185 and componente == 'D3':
    #         # print('componente ok')
    #         D3 = 1
    #     if 155 <= centro[0] <= 172 and 192 <= centro[1] <= 203 and componente == 'D4':
    #         # print('componente ok')
    #         D4 = 1
    #     if 154 <= centro[0] <= 172 and 209 <= centro[1] <= 221 and componente == 'D5':
    #         # print('componente ok')
    #         D5 = 1
    # if R10K1 == 0:
    #     print('R10K1 NO ESTA')
    # if R10K2 == 0:
    #     print('R10K2 NO ESTA')
    # if R4K71 == 0:
    #     print('R4K71 NO ESTA')
    # if R4K72 == 0:
    #     print('R4K72 NO ESTA')
    # if R4K73 == 0:
    #     print('R4K73 NO ESTA')
    # if R22K1 == 0:
    #     print('R22K1 NO ESTA')
    # if R1501 == 0:
    #     print('R1501 NO ESTA')
    # if R391 == 0:
    #     print('R391 NO ESTA')
    # if T1 == 0:
    #     print('T1 NO ESTA')
    # if D1 == 0:
    #     print('D1 NO ESTA')
    # if D2 == 0:
    #     print('D2 NO ESTA')
    # if D3 == 0:
    #     print('D3 NO ESTA')
    # if D4 == 0:
    #     print('D4 NO ESTA')
    # if D5 == 0:
    #     print('D5 NO ESTA')


    # Esperar a que se presione una tecla para cerrar la ventana



    #cv2.waitKey(0)
# Liberar recursos
# captura_video.release()
# cv2.destroyAllWindows()
