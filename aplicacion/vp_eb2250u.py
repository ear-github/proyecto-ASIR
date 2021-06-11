#Métodos para controlar el videoproyector
#Epson EB 2250U.

from serial import Serial
# from serial.serialutil import SerialBase


class device(Serial):

	status_dic = {
			'device_name' : "Epson EB-2250U",
			'power_status' : "",
			'av_mute': "",
			'source' : "",
			'volume' : 0,
			'lamp_hours' : 0,
			'lamp_minutes' : 0,
			'picturesetting': "",
			'contrast': 0,
			'brightness':0,
			'lampmode': "",
			'aspect': ""
		}


	def __init__(self,ex320_port):
		super().__init__(ex320_port, timeout = 1)
		# Serial(ex320_port, timeout = 1)

	# def class_name(self):
	# 	return self.__class__.__name__

############################## CONSULTAS ############################################
	
	def get_serialnumber(self):
		self.flush()
		self.write(b'SNO?\r')
		lee = self.read_until("\r")
		sno = str(lee).lstrip("b'SNO=").rstrip("\\r:'")
		return sno
	
	
	def get_power(self):
		self.flush()
		self.write(b'PWR?\r')
		lee = self.read_until("\r")
		status = {
		b'PWR=00\r:': "Standby Mode (Network OFF)",
		b'PWR=01\r:': "ON",
		b'PWR=02\r:': "Warm up",
		b'PWR=03\r:': "Cool down",
		b'PWR=04\r:': "Standby Mode (Network ON)",
		b'PWR=05\r:': "Abnormality Standby",
		b'PWR=06\r:': "A/V Stanby"
		}
		self.status_dic['power_status'] = status.get(lee, "?")
		return self.status_dic['power_status']

	def get_avmute(self):
		self.flush()
		self.write(b'MUTE?\r')
		lee = self.read_until("\r")
		status = {
		b'MUTE=ON\r:': "ON",
		b'MUTE=OFF\r:': "OFF"
		}
		self.status_dic['av_mute'] = status.get(lee, "?")
		return self.status_dic['av_mute']

	def get_source(self):
		self.flush()
		self.write(b'SOURCE?\r')
		lee = self.readline()
		sources ={
			b'SOURCE=30\r:': "HDMI 1",
			b'SOURCE=A0\r:': "HDMI 2",
			b'SOURCE=40\r:': "Video",
			b'SOURCE=41\r:': "Video (RCA)",
			b'SOURCE=42\r:': "S-Video",
			b'SOURCE=11\r:': "Computer 1 (VGA)",
			b'SOURCE=21\r:': "Computer 2 (VGA)"
		}
		self.status_dic['source'] = sources.get(lee, "?")
		return self.status_dic['source']

	# ~ def get_volume(self):
		# ~ self.flush()
		# ~ self.write(b'00VL\r')
		# ~ lee = self.readline()
		# ~ vol = str(lee).split("00VL")[1].rstrip("\\r'")
		# ~ if vol == ":N":
			# ~ return "0"
		# ~ else:
			# ~ return str(int(vol))

	def get_lamptime(self):
		self.flush()
		self.write(b'LAMP?\r')
		lee = self.readline()
		hours = str(lee).split("'bLAMP=").rstrip("\\r:'")
		self.status_dic['lamp_hours'] = hours
		return hours

	# ~ def get_picturesetting(self):
		# ~ self.flush()
		# ~ self.write(b'00CE\r')
		# ~ lee = self.readline()
		# ~ setting = {
			# ~ b'00CE0\r': "Brightest",
			# ~ b'00CE1\r': "Presentation",
			# ~ b'00CE2\r': "Normal",
			# ~ b'00CE3\r': "Theather",
			# ~ b'00CE4\r': "User 1",
			# ~ b'00CE5\r': "User 2"
		# ~ }
		# ~ ps = setting.get(lee, "?")
		# ~ return ps
	    
	def get_contrast(self):
		self.flush()
		self.write(b'CONTRAST?\r')
		lee = self.readline()
		contrast = str(lee).lstrip("b'CONTRAST=").rstrip("\\r:'")
		return contrast

	def get_brightness(self):
		self.flush()
		self.write(b'00QQ\r')
		lee = self.readline()
		brightness = str(lee).split("00QQ")[1].rstrip("\\r'")
		if brightness == ":N":
			return "0"
		else:
			return str(int(brightness))

	def get_lampmode(self):
		self.flush()
		self.write(b'00LM\r')
		lee = self.readline()
		mode ={
			b'00LM0\r': "Standard",
			b'00LM1\r': "Low"
		}
		lampmode = mode.get(lee, "?")
		return lampmode

	def get_aspect(self):
		self.flush()
		self.write(b'00SC\r')
		lee = self.readline()
		aspect_ratio ={
			b'ASPECT=00 30\r:': "Normal - Auto",
			b'ASPECT=00\r:': "Normal",
			b'ASPECT=20\r:': "16:9",
			b'ASPECT=30\r:': "Auto",
			b'ASPECT=40\r:': "Full",
			b'ASPECT=50\r:': "Zoom",
			b'ASPECT=60\r:': "Native"
		}
		aspect = aspect_ratio.get(lee, "?")
		return aspect


	def get_status(self):
		self.status_dic['power_status'] = self.get_power()
		self.status_dic['av_status'] = self.get_avmute()
		self.status_dic['source'] = self.get_source()
		self.status_dic['vol'] = self.get_volume()
		self.status_dic['lamp_hours'] = self.get_lamptime()["hours"]
		self.status_dic['lamp_minutes'] = self.get_lamptime()["minutes"]
		self.status_dic['lampmode'] = self.get_lampmode()
		self.status_dic['picturesetting'] = self.get_picturesetting()
		self.status_dic['contrast'] = self.get_contrast()
		self.status_dic['brightness'] = self.get_brightness()
		self.status_dic['aspect'] = self.get_aspect()
		return self.status_dic

	def get_status_dic(self):
		return self.status_dic

########### Menú de opciones

	def menu(self):
		print("----------------------------------------")
		print("Control de selfector Mitsubishi EX320")
		print("----------------------------------------")
		print("-----------------------")
		print(" Estado encendido: " + get_power_status())
		lamp = lamptime()
		print(" Horas de lámpara: " + lamp[0] + " horas, " + lamp[1] +" minutos.")
		print(" Fuente de vídeo: " + get_source())
		print(" Volumen altavoz: " + get_vol())
		print(" Configuración de imagen: " + get_picturesetting())
		print(" Contraste: " + get_contrast())
		print(" Brillo: " + get_brightness())
		print(" Modo de lámpara: " + get_lampmode())
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



######################## OPERACIONES BÁSICAS ################################

	def set_power(self, ON_OFF):
		self.flush()
		power ={
			"ON": b'PWR ON\r',
			"OFF": b'PWR OFF"\r'
		}
		envio = power.get(ON_OFF)
		try:
			self.write(envio)
			self.status_dic["power_status"] = ON_OFF
			return True
		except:
			return False

	def set_avmute(self, ON_OFF):
		self.flush()
		mute ={
			"ON": b'00MUTE1\r',
			"OFF": b'00MUTE0\r'
		}
		envio = mute.get(ON_OFF)
		try:
			self.write(envio)
			self.status_dic["av_mute"] = ON_OFF
			return True
		except:
			return False



	def set_source(self, source):
		self.flush()
		sources ={
			"HDMI 1": b'SOURCE 30\r',
			"HDMI 2": b'SOURCE A0\r'
			"Computer 1": b'SOURCE 11\r',
			"Computer 2": b'SOURCE 21\r',
			"Video": b'SOURCE 40\r',
			"S-Video": b'SOURCE 42\r',
			"Video (RCA)": b'SOURCE 41\r'
		}
		sources ={
			b'SOURCE=30\r:': "HDMI 1",
			b'SOURCE=A0\r:': "HDMI 2",
			b'SOURCE=40\r:': "Video",
			b'SOURCE=41\r:': "Video (RCA)",
			b'SOURCE=42\r:': "S-Video",
			b'SOURCE=11\r:': "Computer 1 (VGA)",
			b'SOURCE=21\r:': "Computer 2 (VGA)"
		}
		envio = sources.get(source)
		try:
			self.write(envio)
			self.status_dic["source"] = source
			return True
		except:
			return False

######### Ajuste de imagen
	# ~ def set_picturesetting(self, mode):
		# ~ self.flush()
		# ~ setting ={
			# ~ "Brightest": b'00CE0\r',
			# ~ "Presentation": b'00CE1\r', 
			# ~ "Normal": b'00CE2\r',
			# ~ "Theather": b'00CE3\r', 
			# ~ "User1": b'00CE4\r',
			# ~ "User2": b'00CE5\r' 
		# ~ }
		# ~ envio = setting.get(mode)
		# ~ try:
			# ~ self.write(envio)
			# ~ self.status_dic["picturesetting"] = mode
			# ~ return True
		# ~ except:
			# ~ return False

	def set_contrast(self, value):
		self.flush()
		envio = "CONTRAST "+ value + "\r"
		try:
			self.write(envio.encode())
			self.status_dic["contrast"] = value
			return True
		except:
			return False


	def set_brightness(self, value):
		self.flush()
		envio = "00QQ" + value.zfill(3) + "\r"
		try:
			self.write(envio.encode())
			self.status_dic["brightness"] = value
			return True
		except:
			return False


	def set_lampmode(self, mode):
		self.flush()
		self.write(b'00LM\r')
		lee = self.readline()
		modes ={
			"Standard": b'00LM0\r',
			"Low": b'00LM1\r'
		}
		envio = modes.get(mode)
		try:
			self.write(envio)
			self.status_dic["lampmode"] = mode
			return True
		except:
			return False

	def set_aspect(self, mode):
		self.flush()
		aspect ={
			"Auto": b'00SC0\r',
			"Real": b'00SC1\r',
			"4:3": b'00SC2\r',
			"16:9": b'00SC3\r'
		}
		envio = aspect.get(mode)
		try:
			self.write(envio)
			self.status_dic["aspect"] = mode
			return True
		except:
			return False

########## Ajuste de audio

	def set_volume(self,up_down):
		self.flush()
		if up_down == "up":
			self.write(b'00r06\r')
			lee = self.readline()
			vol = str(lee).split("00r06")[1].rstrip("\\r'")
		else:
			self.write(b'00r07\r')
			lee = self.readline()
			vol = str(lee).split("00r07")[1].rstrip("\\r'")
		
		
		# if vol == ":N":
		# 	output = "0"
		# else:
		# 	output = str(int(vol))
		self.status_dic['volume'] = vol
		return vol

	# def set_vol_down():
	# 	self.flush()
	# 	self.write(b'00r07\r')
	# 	return self.get_volume()
