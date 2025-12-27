from PyQt5.QtWidgets import *
from NewDronInterfaz import Ui_DronControl1
from Ventana2 import Ui_ventana_2

import time, cv2
from threading import Thread

from djitellopy import Tello
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer


import numpy as np
from ultralytics import YOLO

import sys


class CogniDronControl(QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.ui= Ui_DronControl1()
        self.ui.setupUi(self)
        self.ventana= Ventana2()
        #self.ui.grip= QSizeGrip(self.ui.lblgrid)
        self.keepRecording=False
        
          
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateDatos)
        self.timer.start(2000) 
        
        self.Dron=Tello()  #Instanciamos la clase Dron con la clase Tello.
        self.Dron.connect() #Realizamos la conexion del Dron.
        
        self.Dron.streamon()
        
        #self.Dron.send_keepalive()
              
    #Bonotes DronTello
      
        self.ui.Btn_Dron_Abajo.clicked.connect(self.Down)
        self.ui.Btn_Dron_Arriva.clicked.connect(self.Up)
        self.ui.Btn_Start.clicked.connect(self.TakeOff1)
        self.ui.Btn_Stop.clicked.connect(self.Land1)
        
        
    #Botones Control Camera
    
        self.ui.Btn_Video.clicked.connect(self.iniciar)
        
        self.ui.Btn_Camera.clicked.connect(lambda:self.ventana.mostrar())
        self.ventana.ventana2.btn_send.clicked.connect(lambda: self.setInformation())
        
        
    #Botones Fly Control
    
        self.ui.Btn_G_Izquierda.clicked.connect(self.Giro_Izquierda)
        self.ui.Btn_G_Derecha.clicked.connect(self.Giro_Derecha)
        self.ui.BtnArriva_2.clicked.connect(self.ForWard1)
        self.ui.BtnAbajo_2.clicked.connect(self.BackWard1)
        self.ui.BtnDerecha_2.clicked.connect(self.Right1)
        self.ui.BtnIzquierdo_2.clicked.connect(self.Left1)
        
        
        self.show()
        
        
        """
        DronTello:

        Take Off ----> Ctrl + Space
        Land     ----> Space
        
        Go up    ----> U
        Go down  ----> L
        
        Camera Control:
        
        Camera   ----> C
        Video    ----> V
        
        Fly Control:
        
        Up    ----> Flecha Arriva
        Donw  ----> Flecha abajo
        Right ----> Flecha derecha
        Left  ----> Flecha izquierda
        
        Rotate right ----> D
        Rotate left  ----> I

        """
    
        
#########################################################################    
    #Funciones DronTello
    
    def setInformation(self):
        
        #print(self.ventana.getDatos())
        pass
    
    def Up(self):
        
        #self.ui.lbl_pantalla.setText("Dron Arriva")
        self.Dron.move_up(100)
    
    def Down(self):
        
        #self.ui.lbl_pantalla.setText("Dron Abajo")
        self.Dron.move_down(50)
        
    def TakeOff1(self):           
        #self.ui.lbl_pantalla.setText("Despegar")
        self.Dron.takeoff()
        time.sleep(2)
    
    def Land1(self):           
        #self.ui.lbl_pantalla.setText("Aterrizar")
        self.Dron.land()

######################################################################### 
    
    #Funciones Control Camera
    
    
    def UpdateDatos(self):
                
        battery= self.Dron.get_battery()
        
        height= self.Dron.get_height()
        
        height = height / 100
        
        if battery is None:
            self.ui.lbl_battery.setText(" ")
            
        else:
            
            #percent= battery.percent
            self.ui.lbl_battery.setText(f'{battery}%')
            
        if height is None:
            self.ui.lbl_barometer_cm.setText(" ")
            
        else:
            
            #percent= barometer.percent
            self.ui.lbl_barometer_cm.setText(f'{height}m')
            
    def iniciar(self):
        
        if self.keepRecording:
            self.keepRecording=False
            self.recorder.join()
            
        else:
            
            self.keepRecording=True
            self.recorder = Thread(target=self.TomarVideo)
            self.recorder.start()
           
    
    def trackFace(self, info, w, pid, pError):

        area = info[1]

        x, y = info[0]

        fb = 0

        error = x - w // 2

        speed = pid[0] * error + pid[1] * (error - pError)

        speed = int(np.clip(speed, -100, 100))

        if area > 57000 and area < 58000:

            fb = 0

        elif area > 58000:

            fb = -20

        elif area < 57000 and area != 0:

            fb = 20

        if x == 0:

            speed = 0

            error = 0
        
        #Speed: Girar izquierda o derecha
        #fb: avanzar o retroceder

        print("speed=",speed,"fb=", fb)

        self.Dron.send_rc_control(0, fb, 0, speed)

        return error
    
    def detectObject(self,resultados):
        
        myFaceListC = []

        myFaceListArea = []
        
        num= self.ventana.getDatos()
        
        for r in resultados:
            
            for name in r.boxes.cls:
                
                #print("Encontre clase:",name)
                
                if name == 0:
                    
                    try:
                        
                        for id1 in r.boxes.id:
                            
                          #  print("encontre persona : ",id1)
                            
                            if id1 == num:
                                
                                for (x, y, w, h) in r.boxes.xywh:
                            
                                    cx = x + w // 2
                            
                                    cy = y + h // 2
                            
                                    area = w * h
                                    """
                                    myFaceListC.append([cx, cy])
    
                                    myFaceListArea.append(area)
    
                                if len(myFaceListArea) != 0:
    
                                    i = myFaceListArea.index(max(myFaceListArea))
    
                                    return [myFaceListC[i], myFaceListArea[i]]
    
                                else:
    
                                    return [[-1000,-1000],-1000]
                                    
                                    """
                                
                             
                                #print("cx=",cx,"cy=", cy)
                                #print("area:=",area)
                                
                                myFaceListC=[cx, cy]
                                
                               #myFaceLlistArea= [area]
                               #print("MyFacelistc=",myFaceListC,"MyFaceListArea:",myFaceListArea)
                               
                                info =[myFaceListC, area]
                                
                                return info
                        
                            #print(info)
                            #print("Center", info[0], "Area", info[1])
                        
                        else:
                            
                            print("****************id no encontrado***********************")
                            break
                                
                    except TypeError as e:
                    
                        print(f"Error id {e}")
                        return [[-1000,-1000],-1000]
                
                else:
                             
                    break
                
            return [[-1000,-1000],-1000]
        return [[-1000,-1000],-1000]
        
        
    
    def TomarVideo(self):
        
        
        #self.ui.lbl_pantalla.setText("Tomar Video")
        
        # cargar modelo
        modelo = YOLO('yolov8n.pt')
        
        pid = [0.1, 0.1, 0]
        pError = 0
        
        w , h= 640 ,380
        
        #height, width, _ = self.frame_read.frame.shape

        # Define el codec and crea el objeto VideoWriter para guardar un vídeo de salida.
        #video = cv2.VideoWriter("tracking.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 30, (w, h))
       # byTesperLine = 3 * w
        
        #ret = True # Cuando se convierte en falso se acabo el vídeo
        
        # Leer frames
        while self.keepRecording:
            
            frame= self.Dron.get_frame_read().frame
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            
            frame = cv2.resize(frame, (w, h))
            
            

            # detecta objetos
            # sigue objetos
            resultados = modelo.track(frame, persist=True)
            
            info= self.detectObject(resultados)
            
            #print(type(info))
            if info[0][0] !=-1000 and info[0][1] !=-1000 and info[1] !=-1000:
                
                pError= self.trackFace(info, w, pid, pError)
            

            #print("Center", info[0], "Area", info[1])
            

            # Dibuja los resultados
            # cv2.rectangle
            # cv2.putText
            frame_ = resultados[0].plot()

            # agregar frame al vídeo
            #video.write(frame_)
            
            rgb_image = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
            
            image = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], rgb_image.strides[0], QImage.Format_RGB888)    
         
            pixmap = QPixmap.fromImage(image)
            
            self.ui.lbl_pantalla.setPixmap(pixmap)
             
            #self.ui.lbl_pantalla.setPixmap(QPixmap(QImagen))

            time.sleep(1 / 30)
          
        print("Fin de lectura")
        
        


#########################################################################    
    

#Funciones Fly Control
    
    
    def ForWard1(self):
            
        #self.ui.lbl_pantalla.setText("Boton Adelante")
        self.Dron.move_forward(100)
        
    
    def BackWard1(self):
        
        #self.ui.lbl_pantalla.setText("Boton Atras")
        self.Dron.move_back(100)
        
    
    def Giro_Derecha(self):
        
        
        #self.ui.lbl_pantalla.setText("Giro derecha")
        self.Dron.rotate_clockwise(45)
    
        
    def Giro_Izquierda(self):    
            
        #self.ui.lbl_pantalla.setText("Giro izquierda")
        self.Dron.rotate_clockwise(-45)
    
        
    def Right1(self):     
              
        #self.ui.lbl_pantalla.setText("Boton derecha")
        self.Dron.move_right(100)
    
    def Left1(self): 
                  
        #self.ui.lbl_pantalla.setText("Boton izquierda")
        self.Dron.move_left(100)
        
        
    def closeEvent(self, event):
        # Este método se llama cuando se intenta cerrar la ventana
        respuesta = self.confirmarCerrarVentana()
        
        if respuesta:
            
            if self.keepRecording:
                 
                self.iniciar()
             
            self.close()
            
            self.Dron.end()
            
            event.accept()  # Acepta el evento de cierre
            
            
        else:
            event.ignore()  # Ignora el evento de cierre
    
    def confirmarCerrarVentana(self):
        # Muestra un cuadro de diálogo de confirmación
        mensaje = "¿Estás seguro de que quieres cerrar la aplicación?"
        
        respuesta = QMessageBox.question(self, 'Confirmar Cierre', mensaje, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
        return respuesta == QMessageBox.Yes
        
#########################################################################
        
class Ventana2(QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.ventana2= Ui_ventana_2()
        self.ventana2.setupUi(self)
        self.ventana2.lineEdit.setPlaceholderText("Enter a number:")
        
        self.datos= None
        
        # Conectar el evento de edición cambiada al método correspondiente
        self.ventana2.lineEdit.textChanged.connect(self.validar_numero)

        # Conectar el evento de clic del botón al método de enviar
        self.ventana2.btn_send.clicked.connect(self.getDatos)
         
    def validar_numero(self):
        
       # Obtener el texto del QLineEdit
       texto = self.ventana2.lineEdit.text()
       self.ventana2.lbl_info.setText(" ")

       try:
           # Intentar convertir el texto a un número entero
           numero = int(texto)
           
           self.datos = numero
           
       except ValueError:
           # Si no se puede convertir a un número entero, establecer la información como None
           self.datos = None
           
         
    def mostrar(self):
                
        self.show()
        
    def getDatos(self):
        
        if self.datos is not None:
            
            # Mostrar la información solo cuando se presiona el botón de enviar y es un número entero
            
            return self.datos
        
        else:
            
           #Si la información no es un número entero, mostrar un mensaje de error
           self.ventana2.lbl_info.setText("Error: Enter a valid number type")
        
    
if __name__ == '__main__':
    
    app=QApplication(sys.argv) 
    mi_aplication = CogniDronControl()
    mi_aplication.show()
    sys.exit(app.exec_())



    