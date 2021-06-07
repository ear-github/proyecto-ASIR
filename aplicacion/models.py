from sqlalchemy import Boolean, Column , ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from aplicacion.app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Categorias(db.Model):
	"""Categorías de los dipositivos"""
	__tablename__ = 'categorias'
	id = Column(Integer, primary_key=True)
	nombre = Column(String(100))
	# modelo = relationship("Modelos", cascade="all, delete-orphan", backref="Categorias",lazy='dynamic', back_populates="parent")
	modelo = relationship("Dispositivos", cascade="all, delete-orphan", backref="Categorias",lazy='dynamic')


	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


class Dispositivos(db.Model):
	"""Modelo tipo de dispositivo"""
	__tablename__ = 'dispositivos'
	id = Column(Integer, primary_key=True)
	nombre = Column(String(100),nullable=False)
	descripcion = Column(String(255))
	imagen = Column(String(255))
	puerto = Column(String(100))
	archivoHTML = Column(String(255))
	archivoPY = Column(String(255))
	# stock = Column(Integer,default=0)
	CategoriaId=Column(Integer,ForeignKey('categorias.id'), nullable=False)
	categoria = relationship("Categorias", backref="Dispositivos")
	comando = relationship("Comandos", cascade="all, delete-orphan",backref = "Dispositivos",lazy='dynamic')

	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Comandos(db.Model):
	"""comandos asociados a un modelo"""
	__tablename__ = 'comandos'
	id = Column(Integer, primary_key=True)
	descripcion = Column(String(100))
	codigo = Column(String(255))
	DispositivoId = Column(Integer,ForeignKey('dispositivos.id'), nullable=False)
	parametro = relationship("Parametros", backref = "Comandos")

	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
	

class Parametros(db.Model):
	"""parámetro asociado a un comando"""
	__tablename__ = 'parametros'
	id = Column(Integer, primary_key=True)
	descripcion = Column(String(100))
	valor = Column(String(255))
	ComandoId = Column(Integer,ForeignKey('comandos.id'), nullable=False)
	boton = relationship("Botones", backref="Parametros")

	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Botones(db.Model):
	"""Botones asociados a comandos de dispositivos"""
	__tablename__ = 'botones'
	id = Column(Integer, primary_key=True)
	accion = Column(String(100))
	tecla = Column(String(255))
	ParametroId = Column(Integer,ForeignKey('parametros.id'), nullable=False)
	

	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Usuarios(db.Model):
	"""Usuarios"""
	__tablename__ = 'usuarios'
	id = Column(Integer, primary_key=True)
	username = Column(String(100),nullable=False)
	password_hash = Column(String(128),nullable=False)
	nombre = Column(String(200),nullable=False)
	email = Column(String(200),nullable=False)
	admin = Column(Boolean, default=False)
	
	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

 	
# Flask-Login integration
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def is_admin(self):
		return self.admin
