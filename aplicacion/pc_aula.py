#Métodos para controlar el PC del aula desde nuestro controlador RPi
#Se utiliza ssh con par de claves pública y privada para el apagado. Necesitamos la IP del PC
#Para el encendido lo haremos por WOL. Necesitaremos la MAC del PC

import paramiko
from wakeonlan import send_magic_packet

class device():
	
	status_dic = {
		'device_name' : "PC del aula 00 (RPi)",
		'power': "off",
		'ip' : "",
		'mac' : ""
		}

	def __init__(self, ip, mac):
		self.status_dic["ip"] = ip
		self.status_dic["mac"] = mac

	def get_status(self): #Devuelve el diccionario
		return self.status_dic
	def get_status_dic(self):
		return self.status_dic

	def set_power(self,on_off):
		if on_off == "off":
			#usamos ssh
			ssh_client = paramiko.SSHClient() #inicia el ciente
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Política por defecto para localizar la llave del host localmente
			ssh_client.connect(self.status_dic["ip"], 22, 'pi')
			ssh_client.exec_command('sudo poweroff')
			ssh_client.close()
		elif on_off == "on":
			#usamos WOL
			send_magic_packet(self.status_dic["mac"])



		return self.get_status()

