#!/usr/bin/env python3
#control-ex320.py
import serial,readchar,os
proy = serial.Serial('/dev/ttyUSB0', timeout=1) 

# Peticiones de datos 
def get_power_status():
	proy.write(b'00vP\r')
	lee = proy.read_until("\r")
	status = {
		b'00vP0\r': "OFF",
		b'00vP1\r': "ON"
	}
	return status.get(lee, "?")

def get_source():
	proy.write(b'00vI\r')
	lee = proy.read_until("\r")
	sources ={
		b'00vIr1\r': "Computer 1",
		b'00vIr2\r': "Computer 2",
		b'00vIv1\r': "Video 1",
		b'00vIv2\r': "S-Video",
		b'00vId1\r': "HDMI"
	}
	return sources.get(lee, "ERROR")

def get_vol():
	proy.write(b'00VL\r')
	lee = proy.read_until("\r")
	print(lee)
	vol = str(lee).split("00VL")[1].rstrip("\\r'")
	return vol

def lamp_time():
	proy.write(b'00vLE\r')
	lee = proy.read_until("\r")
	hours = str(lee).split("00vLE")[1].rstrip("\\r'")[:4]
	minutes = str(lee).split("00vLE")[1].rstrip("\\r'")[4:]
	return hours, minutes

def get_picture_setting():
	proy.write(b'00CE\r')
	lee = proy.read_until("\r")
	setting ={
		b'00CE0\r': "Brightest",
		b'00CE1\r': "Presentation",
		b'00CE2\r': "Normal",
		b'00CE3\r': "Theather",
		b'00CE4\r': "User 1",
		b'00CE5\r': "User 2"
	}
	return setting.get(lee, "?")
    
def get_contrast():
	proy.write(b'00PP\r')
	lee = proy.read_until("\r")
	print(lee)
	contrast = str(lee).split("00PP")[1].rstrip("\\r'")
	return contrast

def get_brightness():
	proy.write(b'00QQ\r')
	lee = proy.read_until("\r")
	print(lee)
	brightness = str(lee).split("00QQ")[1].rstrip("\\r'")
	return brightness

def get_lamp_mode():
	proy.write(b'00LM\r')
	lee = proy.read_until("\r")
	mode ={
		b'00LM0\r': "Standard",
		b'00LM1\r': "Low"
	}
	return mode.get(lee, "?")

def get_aspect():
	proy.write(b'00SC\r')
	lee = proy.read_until("\r")
	aspect ={
		b'00SC0\r': "Auto",
		b'00SC1\r': "Real",
		b'00SC2\r': "4:3",
		b'00SC3\r': "16:9"
	}
	return aspect.get(lee, "?")

# Menú de opciones

def menu():
	print("----------------------------------------")
	print("Control de proyector Mitsubishi EX320")
	print("----------------------------------------")
	print("-----------------------")
	print(" Estado encendido: " + get_power_status())
	lamp = lamp_time()
	print(" Horas de lámpara: " + lamp[0] + " horas, " + lamp[1] +" minutos.")
	print(" Fuente de vídeo: " + get_source())
	print(" Volumen altavoz: " + get_vol())
	print(" Configuración de imagen: " + get_picture_setting())
	print(" Contraste: " + get_contrast())
	print(" Brillo: " + get_brightness())
	print(" Modo de lámpara: " + get_lamp_mode())
	print(" Relación de aspecto: " + get_aspect())
	print("-----------------------")
	print("1.Enciende")
	print("2.Apaga")
	print("3.AV Mute ON")
	print("4.AV Mute OFF")
	print("5.Source Computer 1")
	print("6.Source Computer 2")
	print("7.Source video 1")
	print("8.Source S-Video")
	print("9.Source HDMI")
	print("q.Vol +")
	print("w.Vol -")
	print("x.Salir")

# Operaciones básicas
def power_on():
	proy.write(b'00!\r')
	proy.flush()
	print("power_on")

def power_off():
	proy.write(b'00"\r')
	lee = proy.read_until("\r")
	print(lee)
	proy.flush()
	print("power_off")

	
def av_mute_on():
	proy.flush()
	proy.write(b'00MUTE1\r')
	lee = proy.read_until("\r")
	print(lee)

def av_mute_off():
	proy.write(b'00MUTE0\r')
	lee = proy.read_until("\r")
	print(lee)
	proy.flush()
	print("av_mute_off")

def source_computer1():
	proy.write(b'00_r1\r')
	lee = proy.read_until("\r")
	print(lee)
	proy.flush()
	print("Computer 1")

def source_computer2():
	proy.write(b'00_r2\r')
	lee = proy.read_until("\r")
	print(lee)
	proy.flush()
	print("Computer 2")

def source_video1():
	proy.write(b'00_v1\r')
	lee = proy.read_until("\r")
	print(lee)
	proy.flush()
	print("video1")

def source_svideo():
	proy.write(b'00_v2\r')
	lee = proy.read_until("\r")
	print(lee)
	proy.flush()
	print("S-Video")

def source_hdmi():
	proy.write(b'00_d1\r')
	lee = proy.read_until("\r")
	print(lee)
	proy.flush()
	print("HDMI")
# Ajuste de imagen
def picture_settings(option):
	proy.write(b'00CE\r')
	lee = proy.read_until("\r")
	sources ={
		b'00vIr1\r': "Computer 1",
		b'00vIr2\r': "Computer 2",
		b'00vIv1\r': "Video 1",
		b'00vIv2\r': "S-Video",
		b'00vId1\r': "HDMI"
	}
	return sources.get(lee, "ERROR")

# Ajuste de audio

def vol_up():
	proy.write(b'00r06\r')
	lee = proy.read_until("\r")
	print(lee)
	proy.flush()
	print(get_vol())

def vol_down():
	proy.write(b'00r07\r')
	lee = proy.read_until("\r")
	print(lee)
	proy.flush()
	print(get_vol())

def default():
	print("")

def set_picture_setting(mode):
	setting ={
		"Brightest": b'00CE0\r',
		"Presentation": b'00CE1\r', 
		"Normal": b'00CE2\r',
		"Theather": b'00CE3\r', 
		"User1": b'00CE4\r',
		"User2": b'00CE5\r' 
	}
	envio = setting.get(mode)
	proy.write(envio)

def set_contrast(value):
	envio = "00PP" + "+" + value + "\r"
	print(envio.encode)
	proy.write(envio.encode())


def set_brightness(value):
	envio = "00QQ" + "+" + value + "\r"
	print(envio.encode)
	proy.write(envio.encode())

def set_lamp_mode(mode):
	proy.write(b'00LM\r')
	lee = proy.read_until("\r")
	modes ={
		"Standard": b'00LM0\r',
		"Low": b'00LM1\r'
	}
	envio = modes.get(mode)
	proy.write(envio)

def set_aspect(aspect):
	aspect ={
		"Auto": b'00SC0\r',
		"Real": b'00SC1\r',
		"4:3": b'00SC2\r',
		"16:9": b'00SC3\r'
	}
	envio = aspect.get(mode)
	proy.write(envio)

print(proy.port)

opcion = ""
while opcion != "x":
	#os.system("clear")
	menu()
	opcion = readchar.readkey()
	sw = {
		"1": power_on,
		"2": power_off,
		"3": av_mute_on,
		"4": av_mute_off,
		"5": source_computer1,
		"6": source_computer2,
		"7": source_video1,
		"8": source_svideo,
		"9": source_hdmi,
		"q": vol_up,
		"w": vol_down
	}

	sw.get(opcion, default)()

proy.close()
