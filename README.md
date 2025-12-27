# DJI-TELLO-YOLOv8
Sistema de detección y seguimiento autónomo de personas y objetos para drones DJI Tello usando YOLOv8 y Python.

Este proyecto implementa un sistema de visión artificial avanzado para vehículos aéreos no tripulados (UAV). Utiliza el modelo **YOLOv8** para identificar objetos y personas en tiempo real, permitiendo que el dron (DJI Tello) realice un seguimiento inteligente basado en la retroalimentación de la cámara.

##Características principales
* **Detección en tiempo real:** Identificación de múltiples clases de objetos (personas, vehículos, etc.) con alta precisión.
* **Seguimiento Autónomo:** Algoritmos de control para mantener al objetivo centrado en el frame.
* **Interfaz de Control:** Visualización del flujo de video procesado con anotaciones de IA.
* **Optimización:** Configuración ligera (YOLOv8 Nano) para procesamiento en tiempo real en laptops.

##Stack Tecnológico
* **Lenguaje:** Python 3.11
* **IA/Deep Learning:** Ultralytics YOLOv8, PyTorch
* **Visión Artificial:** OpenCV (cv2)
* **Hardware:** DJI Tello SDK (DJITelloPy)
* **Entorno:** Anaconda / Spyder

##Requisitos Previos
Antes de ejecutar el proyecto, asegúrate de tener instalado:
- Python 3.11
- Drivers de video actualizados (especialmente si usas GPU NVIDIA)
- Conexión WiFi al dron DJI Tello
