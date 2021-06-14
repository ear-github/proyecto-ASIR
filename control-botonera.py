#!/usr/bin/env python3
import sqlite3, readchar, importlib, logging, re, paramiko
from wakeonlan import send_magic_packet

#Añadimos una ruta que apunta a donde tenemos guardados los módulos de nuestros dispositivos
import sys
sys.path.insert(1, '/home/pi/proyecto/')
sys.path.insert(1, '/home/pi/proyecto/aplicacion')

# Uso de un log de operaciones en archivo
logging.basicConfig(filename = "registro_botonera.log", level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

#Realizamos la conexión SQL
conexion = sqlite3.connect('/home/pi/proyecto/dbase.db')

#Creamos un cursor que tiene la última orden a la base de datos
cur = conexion.cursor()

#Realizamos la consulta de los comandos asignados en la botonera:
#Para cada tecla de la botonera se muestra el puerto del dispositivo, el/los comando/s y el/los parámetro/s asociado/s.
# [('1', '/dev/ttyUSB0', 'set_power', 'ON'),
#  ('1', '/dev/ttyUSB1', 'set_mute', 'OFF'),
#  ('6', '/dev/ttyUSB0', 'set_power', 'OFF'),
#  ('6', '/dev/ttyUSB1', 'set_mute', 'ON'),
#  ('2', '/dev/ttyUSB0', 'set_avmute', 'ON'),
#  ('7', '/dev/ttyUSB0', 'set_avmute', 'OFF'),
#  ('0', '/dev/ttyUSB1', 'set_line1_vol', '55')]
cur.execute("SELECT botones.tecla,dispositivos.puerto,dispositivos.ip,dispositivos.mac,dispositivos.archivoPY,comandos.codigo,parametros.valor,parametros.descripcion FROM botones JOIN parametros ON parametros.id = botones.ParametroId JOIN comandos ON comandos.id = parametros.ComandoId JOIN dispositivos ON dispositivos.id = comandos.DispositivoId")

#sacamos todos los datos de esta consulta y los guardamos en datos
datos = cur.fetchall()
lista_botones = [[],[],[],[],[],[],[],[],[],[]]

#Pasamos los datos que nos da la consulta a una lista en la que cada elemento contiene una lista de comandos asociados a un botón.
#Por ejemplo lista_botones[0] corresponde al botón 0 y contiene una lista de diccionarios, cada uno de los cuales contiene los datos necesarios para ejecutar un comando: puerto serie y orden, además de una pequeña descripción.
for linea in datos:
	lista_botones[int(linea[0])].append({"puerto" : linea[1], "ip" : linea[2],"mac" : linea[3], "modulo" : linea[4].rstrip(".py"), "orden" : linea[5] + "(\"" + linea[6] + "\")", "descripcion" : linea[7]})

opcion = ""
while opcion != "x":
	opcion = readchar.readkey()
	regex = '\d'
	if re.match(regex, opcion):
		i = int(opcion)
		lista_comandos = lista_botones[i]
		# try:
		for c in lista_comandos:
			nombre_modulo = c["modulo"].rstrip(".py")
			print("nombre módulo")
			modulo = importlib.import_module(nombre_modulo)
			print("módulo importado")
			print("puerto:" + c["puerto"])
			if c["puerto"] == "GPIO":
				dispositivo = modulo.device()
			elif c["puerto"] == "ssh":
				dispositivo = modulo.device(c["ip"],c["mac"])
			else:
				dispositivo = modulo.device(c["puerto"])
			print("dispositivo iniciado")
			eval("dispositivo." + c["orden"])
			print("orden lanzada")
			print(c["puerto"] + ", " + c["modulo"] + ", " + c["orden"] + ", " + c["descripcion"])
			logging.info("Puerto: '%s', dispositivo: '%s', comando: '%s', descripción: '%s'", c["puerto"], c["modulo"], c["orden"], c["descripcion"])
		# except:
		# 	print("Botón no asignado")
