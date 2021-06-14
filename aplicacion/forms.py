from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DecimalField,IntegerField,TextAreaField,SelectField,PasswordField, HiddenField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField
from wtforms.validators import Required, NumberRange


class formCategoria(FlaskForm):                      
	nombre=StringField("Nombre:",validators=[Required("Tienes que introducir el dato")])
	submit = SubmitField('Enviar')


class formDispositivo(FlaskForm):                      
	nombre=StringField("Nombre:",validators=[Required("Tienes que introducir el dato")])
	CategoriaId=SelectField("Categoría:",coerce=int)
	puerto=StringField("Puerto:",default="/dev/ttyUSB0" ,validators=[Required("Tienes que introducir el dato")])
	ip=StringField("Dirección IP (si es requerido)")
	mac=StringField("Dirección MAC (si es requerida)")
	descripcion= TextAreaField("Descripción:")
	imagen = FileField('Selecciona imagen:')
	archivoHTML = FileField ('Sube la página del dispositivo')
	archivoPY = FileField ('Sube el archivo de código del dispositivo')
	submit = SubmitField('Enviar')
	
class formComando(FlaskForm):                      
	descripcion=StringField("Descripción:",validators=[Required("Tienes que introducir el dato")])
	codigo =StringField("Código:",validators=[Required("Tienes que escribir el código que corresponderá al comando")])
	DispositivoId=SelectField("Dispositivo:", coerce = int)
	submit = SubmitField('Enviar')

class formParametro(FlaskForm):                      
	descripcion=StringField("Descripción:",validators=[Required("Tienes que introducir una descripción")])
	valor =StringField("Valor:",validators=[Required("Tienes que especificar el código que corresponderá al parámetro")])
	ComandoId=SelectField("Comando:", coerce = int)
	submit = SubmitField('Enviar')

class formBotonera(FlaskForm):                      
	accion=StringField("Acción:",validators=[Required("Tienes que introducir el dato")])
	tecla =StringField("Tecla asignada:",validators=[Required("Tienes que especificar una tecla a la que asignar la acción")])
	ParametroId=SelectField("Parámetro:",coerce=int)
	submit = SubmitField('Enviar')

class formSINO(FlaskForm):      
	si = SubmitField('Si') 
	no = SubmitField('No') 

class LoginForm(FlaskForm):
	username = StringField('Login', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Entrar')

class formUsuario(FlaskForm):
	username = StringField('Login', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	nombre = StringField('Nombre completo')
	email = EmailField('Email')
	submit = SubmitField('Aceptar')	

class formChangePassword(FlaskForm):
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Aceptar')	
