#Métodos para controlar la pantalla simulada con motor DC conectado al GPIO

import RPi.GPIO as GPIO
from time import sleep
import threading

class device():
	
	status_dic = {
		'device_name' : "Pantalla simulada",
		'screen': "stop"
		}

	MotorIN1 = 15 # MotorIN1 y MotorIN2 establecen el sentido de giro
	MotorIN2 = 14 #Asignación de variables a pines del GPIO
	MotorE1 = 18 # activa el motor cuando está en alto (HIGH)
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	# def __init__(self):
	# 	# super().__init__()
	# 	#Configuración inicial de los pines GPIO
	# 	GPIO.cleanup()
	# 	GPIO.setmode(GPIO.BCM)
	# 	MotorIN1 = 15 # MotorIN1 y MotorIN2 establecen el sentido de giro
	# 	MotorIN2 = 14 #Asignación de variables a pines del GPIO
	# 	MotorE1 = 18 # activa el motor cuando está en alto (HIGH)

	# 	GPIO.setup(MotorIN1,GPIO.OUT) # Configura los pines en modo salida
	# 	GPIO.setup(MotorIN2,GPIO.OUT) # porque se dirigen hacia el controlador de motor DC '293D'
	# 	GPIO.setup(MotorE1,GPIO.OUT)

	def get_status(self): #Devuelve la última acción 
		return self.status_dic
	def get_status_dic(self): #Devuelve la última acción 
		return self.status_dic

	


	def __move_screen(self, up_down_stop):
		# GPIO.cleanup()
		# GPIO.setmode(GPIO.BCM)
		# MotorIN1 = 15 # MotorIN1 y MotorIN2 establecen el sentido de giro
		# MotorIN2 = 14 #Asignación de variables a pines del GPIO
		# MotorE1 = 18 # activa el motor cuando está en alto (HIGH)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.MotorIN1,GPIO.OUT) # Configura los pines en modo salida
		GPIO.setup(self.MotorIN2,GPIO.OUT) # porque se dirigen hacia el controlador de motor DC '293D'
		GPIO.setup(self.MotorE1,GPIO.OUT)
		if up_down_stop == "up":
			GPIO.output(self.MotorIN1,GPIO.HIGH) # MotorIN1 y MotorIN2 establecen el sentido de giro  
			GPIO.output(self.MotorIN2,GPIO.LOW)  
			GPIO.output(self.MotorE1,GPIO.HIGH)  # activa el motor cuando está en alto (HIGH)
			self.status_dic["screen"] = "up"
			sleep(5) # Al tratarse de una simulación lo tendremos funcionando solo unos segundos
		elif up_down_stop == "down":
			GPIO.output(self.MotorIN1,GPIO.LOW)   # MotorIN1 y MotorIN2 establecen el sentido de giro contrario 
			GPIO.output(self.MotorIN2,GPIO.HIGH)  
			GPIO.output(self.MotorE1,GPIO.HIGH)   # Activa el motor
			self.status_dic["screen"] = "down"
			sleep(5)
		elif up_down_stop == "stop":
			GPIO.output(self.MotorE1,GPIO.LOW)    # Desactiva el motor
			self.status_dic["screen"] = "stop"
		GPIO.cleanup()
		
		return self.get_status()


	def set_screen(self,up_down_stop):
		t = threading.Thread(target = self.__move_screen, args =(up_down_stop, ))
		t.start()



