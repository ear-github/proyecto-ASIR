#Métodos para controlar el mezclador amplificador 
#Ecler CA40. Serán llamadas desde la aplicación principal

from serial import Serial
# from serial.serialutil import SerialBase

# class ca40(serial.Serial,SerialBase):
class device(Serial):

	status_dic = { 'device_name' : "Ecler CA-40", 'mute_status' : 0, 'master_status' : 0, 'mic_status' : 0, 'line1_status' : 0 }
	

	def __init__(self,ca40_port):
		super().__init__(ca40_port, timeout = 0.5)
		# Serial(ca40_port, timeout=0.5)

	# def get_status(self):
	# 	for key in self.status_dic:
	# 		orden = getattr(self,key)
	# 		self.status_dic[key] = orden()
	# 	return self.status_dic

	def get_status(self):
		self.status_dic['mute_status'] = self.mute_status()
		self.status_dic['master_status'] = self.master_status()
		self.status_dic['mic_status'] = self.mic_status()
		self.status_dic['line1_status'] = self.line1_status()
		return self.status_dic

	def mute_status(self):
		self.write(b'GET MUTE\n')
		lee = self.readline()
		mute = str(lee,'utf-8').split(" ")[2].rstrip("\r\n")
		self.status_dic['mute_status'] = mute
		return mute
	
	def mic_status(self):
		self.flush()
		self.write(b'GET MICRO_VOL\n')
		lee = self.read_until()
		micro_vol = str(lee,'utf-8').split(" ")[2].rstrip("\r\n")
		self.status_dic['mic_status'] = micro_vol
		return int(micro_vol)
    
	def master_status(self):
		self.flush()
		self.write(b'GET MASTER_VOL\n')
		lee = self.read_until()
		master_vol = str(lee,'utf-8').split(" ")[2].rstrip("\r\n")
		self.status_dic['master_status'] = master_vol
		return int(master_vol)

	def line1_status(self):
		self.flush()
		self.write(b'GET LINE1_VOL\n')
		lee = self.read_until()
		line1_vol = str(lee,'utf-8').split(" ")[2].rstrip("\r\n")
		self.status_dic['line1_status'] = line1_vol
		return int(line1_vol)
    
	def menu(self):
		print("----------------------------------------")
		print(" Control de ampliicador Ecler CA-40")
		print("----------------------------------------")
		print("-----------------------")
		print(" Volumen general ", self.mute_status())
		print(" Volumen general ", self.master_status())
		print(" Volumen micro ", self.mic_status())
		print(" Volumen línea ", self.line1_status())
		print("-----------------------")
		print("1.Silencio SÍ")
		print("6.Silencio NO")
		print("2.VOL general ^")
		print("7.VOL general v")
		print("3.VOL micro ^")
		print("8.VOL micro v")
		print("4.VOL línea ^")
		print("9.VOL línea v")
		
	def mute_on(self):
		self.write(b'SET MUTE ON\n')
		return self.get_status()

	def mute_off(self):
		self.write(b'SET MUTE OFF\n')
		return self.get_status()

	def set_mute(self, ON_OFF):
		if ON_OFF == "ON":
			self.write(b'SET MUTE ON\n')
		elif ON_OFF == "OFF":
			self.write(b'SET MUTE OFF\n')
		return self.get_status()


	def master_vol_up(self):
		if self.master_status() < 64:
			vol = self.master_status() + 1
			envio = "SET MASTER_VOL " + str(vol) + "\n"
			self.write(envio.encode())
			self.flush()
		return self.master_status()

	def master_vol_down(self):
		if self.master_status() > 0:
			vol = self.master_status() - 1
			envio = "SET MASTER_VOL " + str(vol) + "\n"
			self.write(envio.encode())
			self.flush()
		return self.master_status()

	def master_vol_up_down(self, up_down):
		if up_down == "up":
			if self.master_status() < 64:
				vol = self.master_status() + 1
				envio = "SET MASTER_VOL " + str(vol) + "\n"
				self.write(envio.encode())
				self.flush()
			return self.master_status()
		elif up_down == "down":
			if self.master_status() > 0:
				vol = self.master_status() - 1
				envio = "SET MASTER_VOL " + str(vol) + "\n"
				self.write(envio.encode())
				self.flush()
			return self.master_status()


	def set_master_vol(self, vol):
		if int(vol) >= 0 & int(vol) <= 64:
			envio = "SET MASTER_VOL " + str(vol) + "\n"
			self.write(envio.encode())
			self.flush()
		return self.master_status()

		
	def mic_vol_up(self):
		if self.mic_status() < 64:
			vol = self.mic_status() + 1
			envio = "SET MICRO_VOL " + str(vol) + "\n"
			self.write(envio.encode())
			self.flush()
		return self.mic_status()


	def mic_vol_down(self):
		if self.mic_status() > 0:
			vol = self.mic_status() - 1
			envio = "SET MICRO_VOL " + str(vol) + "\n"
			self.write(envio.encode())
			self.flush()
		return self.mic_status()

	def mic_vol_up_down(self, up_down):
		if up_down == "up":
			if self.mic_status() < 64:
				vol = self.mic_status() + 1
				envio = "SET MICRO_VOL " + str(vol) + "\n"
				self.write(envio.encode())
				self.flush()
			return self.mic_status()
		elif up_down == "down":
			if self.mic_status() > 0:
				vol = self.mic_status() - 1
				envio = "SET MICRO_VOL " + str(vol) + "\n"
				self.write(envio.encode())
				self.flush()
			return self.mic_status()

	def set_mic_vol(self, vol):
		if int(vol) >= 0 & int(vol) <= 64:
			envio = "SET MICRO_VOL " + str(vol) + "\n"
			self.write(envio.encode())
			self.flush()
		return self.mic_status()
	
	def line1_vol_up(self):
		if self.line1_status() < 64:
			vol = self.line1_status() + 1
			envio = "SET LINE1_VOL " + str(vol) + "\n"
			self.write(envio.encode())
			self.flush()
		return self.line1_status()


	def line1_vol_down(self):
		if self.line1_status() > 0:
			vol = self.line1_status() - 1
			envio = "SET LINE1_VOL " + str(vol) + "\n"
			self.write(envio.encode())
			self.flush()
		return self.line1_status()

	def line1_vol_up_down(self, up_down):
		if up_down == "up":
			if self.line1_status() < 64:
				vol = self.line1_status() + 1
				envio = "SET LINE1_VOL " + str(vol) + "\n"
				self.write(envio.encode())
				self.flush()
			return self.line1_status()
		elif up_down == "down":
			if self.line1_status() > 0:
				vol = self.line1_status() - 1
				envio = "SET LINE1_VOL " + str(vol) + "\n"
				self.write(envio.encode())
				self.flush()
			return self.line1_status()

	def set_line1_vol(self, vol):
		if int(vol) >= 0 & int(vol) <= 64:
			envio = "SET LINE1_VOL " + str(vol) + "\n"
			self.write(envio.encode())
			self.flush()
		return self.line1_status()

			



