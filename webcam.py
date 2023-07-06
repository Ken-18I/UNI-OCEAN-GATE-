from threading import Thread
import cv2
import platform
    
class Webcam:
    def __init__(self):
        self.stopped = False
        self.stream = None
        self.lastFrame = None
        self.os_name = platform.system()

    def start(self):
        t = Thread(target=self.update, args=())  # Iniciamos un hilo para actualizar el streaming
        t.daemon = True
        t.start()
        return self

    def update(self):
        if self.stream is None:  # Si no se ha inicializado el streaming
            if self.os_name == "Windows":  # Si el sistema operativo es Windows
                self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Inicializamos el streaming usando CAP_DSHOW
            elif self.os_name == "Darwin":  # Si el sistema operativo es macOS
                self.stream = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Inicializamos el streaming usando CAP_AVFOUNDATION
            else:  # Si el sistema operativo es Linux
                self.stream = cv2.VideoCapture(0, cv2.CAP_V4L)  # Inicializamos el streaming usando CAP_V4L
        while True:  # Bucle principal para actualizar el streaming
            if self.stopped:  # Si se ha detenido la webcam
                return
            (result, image) = self.stream.read()  # Leemos un fotograma del streaming
            if not result:  # Si no se ha obtenido un fotograma válido
                self.stop()  # Detenemos la webcam
                return
            self.lastFrame = image  # Guardamos el ultimo fotograma

    def read(self):
        return self.lastFrame  # Devolvemos el ultimo fotograma leído

    def stop(self):
        self.stopped = True  # Marcamos la webcam como detenida

    def width(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)  # Devolvemos el ancho del streaming

    def height(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)  # Devolvemos el alto del streaming
    
    def ready(self):
        return self.lastFrame is not None  # Devolvemos si hay un fotograma disponible
