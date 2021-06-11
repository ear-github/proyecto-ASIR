from flask import Flask, render_template,redirect,url_for,request,abort,session
from flask import make_response, jsonify, copy_current_request_context, current_app
from flask import send_file
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from aplicacion.forms import formCategoria,formDispositivo,formSINO,LoginForm,formUsuario,formChangePassword, formBotonera
from werkzeug.utils import secure_filename
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
import os, sys
import json
import serial, readchar
import importlib # para importar módulos desde una cadena almacenada en una variable
import logging #Uso de logs

#Para poder importar módulos que se guarden en el directorio de la aplicación
#p.ej.: los archivos .py que se suban manualmente desde la web.
sys.path.insert(1, '/home/pi/proyecto/aplicacion')

app = Flask(__name__)
app.config.from_object(config)
Bootstrap(app)	
db = SQLAlchemy(app)

# Uso de un log de operaciones en archivo
# logging.basicConfig(filename = "registro.log", level=logging.DEBUG)
logging.basicConfig(filename = "registro_web.log", level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

# Manejo de usuarios

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


from aplicacion.models import Categorias, Dispositivos, Comandos, Parametros, Botones, Usuarios

##################################################################################

@app.route('/categorias')
def categorias():
	categorias=Categorias.query.all()	
	logging.debug("/categorias")
	return render_template("categorias.html",categorias=categorias)

@app.route('/categorias/new', methods=["get","post"])
@login_required
def categorias_new():
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	form=formCategoria(request.form)
	if form.validate_on_submit():
		cat=Categorias(nombre=form.nombre.data)
		db.session.add(cat)
		db.session.commit()
		return redirect(url_for("categorias"))
		logging.info("/categorias Categoría '%s' creada.", form.nombre.data)
	else:
		logging.info("/categorias_new.html")
		return render_template("categorias_new.html",form=form)

@app.route('/categorias/<id>/edit', methods=["get","post"])
@login_required
def categorias_edit(id):
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	cat=Categorias.query.get(id)
	if cat is None:
		abort(404)

	form=formCategoria(request.form,obj=cat)
		
	if form.validate_on_submit():
		form.populate_obj(cat)
		db.session.commit()
		logging.info("/categorias_new.html Categría %s editada.", cat.nombre)
		return redirect(url_for("categorias"))

	
	return render_template("categorias_new.html",form=form)

@app.route('/categorias/<id>/delete', methods=["get","post"])
@login_required
def categorias_delete(id):
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	cat=Categorias.query.get(id)
	if cat is None:
		abort(404)
	form=formSINO()
	if form.validate_on_submit():
		if form.si.data:
			db.session.delete(cat)
			db.session.commit()
			logging.info("/categorias_new.html Categría %s borrada.", cat.nombre)
		return redirect(url_for("categorias"))
	return render_template("categorias_delete.html",form=form,cat=cat)

################################################################################
# @app.route('/articulos/new', methods=["get","post"])
# @login_required
# def articulos_new():

# 	# Control de permisos
# 	if not current_user.is_admin():
# 		abort(404)
# 	form=formArticulo()
# 	categorias=[(c.id, c.nombre) for c in Categorias.query.all()[1:]]
# 	form.CategoriaId.choices = categorias
# 	if form.validate_on_submit():
# 		try:
# 			f = form.photo.data
# 			nombre_fichero=secure_filename(f.filename)
# 			f.save(app.root_path+"/static/upload/"+nombre_fichero)
# 		except:
# 			nombre_fichero=""
# 		art=Articulos()
# 		form.populate_obj(art)
# 		art.image=nombre_fichero
# 		db.session.add(art)
# 		db.session.commit()
# 		return redirect(url_for("inicio"))
# 	else:
# 		return render_template("articulos_new.html",form=form)

# @app.route('/articulos/<id>/edit', methods=["get","post"])
# @login_required
# def articulos_edit(id):
# 	# Control de permisos
# 	if not current_user.is_admin():
# 		abort(404)

# 	art=Articulos.query.get(id)
# 	if art is None:
# 		abort(404)

# 	form=formArticulo(obj=art)
# 	categorias=[(c.id, c.nombre) for c in Categorias.query.all()[1:]]
# 	form.CategoriaId.choices = categorias
	
# 	if form.validate_on_submit():
# 		#Borramos la imagen anterior si hemos subido una nueva
# 		if  form.photo.data:
# 			os.remove(app.root_path+"/static/upload/"+art.image)
# 			try:
# 				f = form.photo.data
# 				nombre_fichero=secure_filename(f.filename)
# 				f.save(app.root_path+"/static/upload/"+nombre_fichero)
# 			except:
# 				nombre_fichero=""
# 		else:
# 			nombre_fichero=art.image
			
# 		form.populate_obj(art)
# 		art.image=nombre_fichero
# 		db.session.commit()
# 		return redirect(url_for("inicio"))
# 	return render_template("articulos_new.html",form=form)

# @app.route('/articulos/<id>/delete', methods=["get","post"])
# @login_required
# def articulos_delete(id):
# 		# Control de permisos
# 	if not current_user.is_admin():
# 		abort(404)

# 	art=Articulos.query.get(id)
# 	if art is None:
# 		abort(404)

# 	form=formSINO()
# 	if form.validate_on_submit():
# 		if form.si.data:
# 			if art.image!="":
# 				os.remove(app.root_path+"/static/upload/"+art.image)
# 			db.session.delete(art)
# 			db.session.commit()
# 		return redirect(url_for("inicio"))
# 	return render_template("articulos_delete.html",form=form,art=art)
##################################################################################

@app.route('/login', methods=['get', 'post'])
def login():
	# Control de permisos
	if current_user.is_authenticated:
		return redirect(url_for("inicio"))

	form = LoginForm()
	if form.validate_on_submit():
		user=Usuarios.query.filter_by(username=form.username.data).first()
		if user!=None and user.verify_password(form.password.data):
			login_user(user)
			next = request.args.get('next')
			return redirect(next or url_for('inicio'))
		form.username.errors.append("Usuario o contraseña incorrectas.")
	return render_template('login.html', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route("/registro",methods=["get","post"])
def registro():
	# Control de permisos
	if current_user.is_authenticated:
		return redirect(url_for("inicio"))

	form=formUsuario()
	if form.validate_on_submit():
		existe_usuario=Usuarios.query.filter_by(username=form.username.data).first()
		if existe_usuario==None:
			user=Usuarios()
			form.populate_obj(user)
			user.admin=False
			db.session.add(user)
			db.session.commit()
			return redirect(url_for("inicio"))
		form.username.errors.append("Nombre de usuario ya existe.")
	return render_template("usuarios_new.html",form=form)

@app.route('/perfil/<username>', methods=["get","post"])
@login_required
def perfil(username):
	user=Usuarios.query.filter_by(username=username).first()
	if user is None:
		abort(404)

	form=formUsuario(request.form,obj=user)
	del form.password	
	if form.validate_on_submit():
		form.populate_obj(user)
		db.session.commit()
		return redirect(url_for("inicio"))

	return render_template("usuarios_new.html",form=form,perfil=True)

@app.route('/changepassword/<username>', methods=["get","post"])
@login_required
def changepassword(username):
	user=Usuarios.query.filter_by(username=username).first()
	if user is None:
		abort(404)

	form=formChangePassword()
	if form.validate_on_submit():
		form.populate_obj(user)
		db.session.commit()
		return redirect(url_for("inicio"))

	return render_template("changepassword.html",form=form)

@login_manager.user_loader
def load_user(user_id):
	return Usuarios.query.get(int(user_id))

# ##############################################################################
# @app.route('/carrito/add/<id>',methods=["get","post"])
# @login_required
# def carrito_add(id):

# 	art=Articulos.query.get(id)	
# 	form=formCarrito()
# 	form.id.data=id
# 	if form.validate_on_submit():
# 		if art.stock>=int(form.cantidad.data):
# 			try:
# 				datos = json.loads(request.cookies.get(str(current_user.id)))
# 			except:
# 				datos = []
# 			actualizar= False
# 			for dato in datos:
# 				if dato["id"]==id:
# 					dato["cantidad"]=form.cantidad.data
# 					actualizar = True
# 			if not actualizar:
# 				datos.append({"id":form.id.data,"cantidad":form.cantidad.data})
# 			resp = make_response(redirect(url_for('inicio')))
# 			resp.set_cookie(str(current_user.id),json.dumps(datos))
# 			return resp
# 		form.cantidad.errors.append("No hay artículos suficientes.")
# 	return render_template("carrito_add.html",form=form,art=art)

# @app.route('/carrito')
# @login_required
# def carrito():
# 	try:
# 		datos = json.loads(request.cookies.get(str(current_user.id)))
# 	except:
# 		datos = []
# 	articulos=[]
# 	cantidades=[]
# 	total=0
# 	for articulo in datos:
# 		articulos.append(Articulos.query.get(articulo["id"]))
# 		cantidades.append(articulo["cantidad"])
# 		total=total+Articulos.query.get(articulo["id"]).precio_final()*articulo["cantidad"]
# 	articulos=zip(articulos,cantidades)
# 	return render_template("carrito.html",articulos=articulos,total=total)

# @app.route('/carrito_delete/<id>')
# @login_required
# def carrito_delete(id):
# 	try:
# 		datos = json.loads(request.cookies.get(str(current_user.id)))
# 	except:
# 		datos = []
# 	new_datos=[]
# 	for dato in datos:
# 		if dato["id"]!=id:
# 			new_datos.append(dato)
# 	resp = make_response(redirect(url_for('carrito')))
# 	resp.set_cookie(str(current_user.id),json.dumps(new_datos))
# 	return resp

# @app.context_processor
# def contar_carrito():
# 	if not current_user.is_authenticated:
# 		return {'num_articulos':0}
# 	if request.cookies.get(str(current_user.id))==None:
# 		return {'num_articulos':0}
# 	else:
# 		datos = json.loads(request.cookies.get(str(current_user.id)))
# 		return {'num_articulos':len(datos)}

# @app.route('/pedido')
# @login_required
# def pedido():
# 	try:
# 		datos = json.loads(request.cookies.get(str(current_user.id)))
# 	except:
# 		datos = []
# 	total=0
# 	for articulo in datos:
# 		total=total+Articulos.query.get(articulo["id"]).precio_final()*articulo["cantidad"]
# 		Articulos.query.get(articulo["id"]).stock-=articulo["cantidad"]
# 		db.session.commit()
# 	resp = make_response(render_template("pedido.html",total=total))
# 	resp.set_cookie(str(current_user.id),"",expires=0)
# 	return resp
#######################################################################

################# PÁGINA PRINCIPAL ###################

@app.route('/')
@app.route('/categoria/<id>')
def inicio(id='0'):
	categoria=Categorias.query.get(id)
	if id=='0':
		dispositivos=Dispositivos.query.all()
	else:
		dispositivos=Dispositivos.query.filter_by(CategoriaId=id)
	categorias=Categorias.query.all()
	pagina = "inicio.html"
	print(pagina, sys.stdout)
	logging.info("/inicio.html Llamada a página principal")
	return render_template(pagina, dispositivos = dispositivos, categorias=categorias,categoria=categoria)


#################### COMANDOS #################################

@app.route('/comandos')
def comandos(id='0'):
	categoria=Categorias.query.get(id)
	if id=='0':
		dispositivos=Dispositivos.query.all()
	else:
		dispositivos=Dispositivos.query.filter_by(CategoriaId=id)
	categorias=Categorias.query.all()
	logging.info("/comandos.html Llamada a página de comandos disponibles")
	comandos = Comandos.query.all()
	listadispositivos = [[]]
	dispositivos = Dispositivos.query.all()
	# ~ print(comandos, sys.stdout)
	for d in dispositivos:
		listadispositivos.append({"nombre": d.nombre, "descripcion": d.descripcion})
		print(d, sys.stdout)
	return render_template("comandos.html", dispositivos = dispositivos, categorias=categorias,categoria=categoria, comandos = comandos, listadispositivos = listadispositivos)

@app.route('/comandos/new', methods=["get","post"])
@login_required
def comandos_new():
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	form=formComandos()
	dispositivos=[(d.id, d.descripcion, d.codigo) for d in Dispositivos.query.all()]
	form.DispositivoId.choices = dispositivos
	
	if form.validate_on_submit():
		cmd = Comandos()
		form.populate_obj(cmd)
		db.session.add(cmd)
		db.session.commit()
		logging.info("Creado comando con id = '%s': '%s', asignado al dispositivo con id = '%s'.", cmd.id, cmd.accion, cmd.DispositivoId)
		return redirect(url_for("comandos"))
	# Si se llega a la página sin haber enviado formulario (con GET) nos vamos a la página en blanco
	return render_template("comandos_new.html",form=form)

@app.route('/comandos/<id>/edit', methods=["get","post"])
@login_required
def comandos_edit(id):
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	cmd=Comandos.query.get(id)
	if cmd is None:
		abort(404)

	form=formComandos()
	dispositivos=[(d.id, d.descripcion, d.codigo) for d in Dispositivos.query.all()]
	form.DispositivoId.choices = dispositivos
	
	if form.validate_on_submit():		
		form.populate_obj(cmd)
		db.session.commit()
		logging.info("Editado comando con id = '%s': '%s', asignado a dispositivo '%s'.", cmd.id, cmd.codigo, cmd.DispositivoId)
		return redirect(url_for("comandos"))
	return render_template("parametros.html",form=form)

@app.route('/parametros/<id>/delete', methods=["get","post"])
@login_required
def comandos_delete(id):
		# Control de permisos
	if not current_user.is_admin():
		abort(404)

	cmd=Comandos.query.get(id)
	if cmd is None:
		abort(404)

	form=formSINO()
	if form.validate_on_submit():
		if form.si.data:
			cmd_descripcion = cmd.descripcion
			cmd_id = cmd.id
			cmd_codigo = cmd.codigo
			db.session.delete(cmd)
			db.session.commit()
			logging.info("Borrado comando con id = '%s' y valor '%s'.  '%s'.", cmd_id, cmd_codigo, cmd_descripcion)
		return redirect(url_for("comandos"))
	return render_template("comandos_delete.html",form=form,cmd=cmd)


#################### PARÁMETROS #################################

@app.route('/parametros')
def parametros(id='0'):
	categoria=Categorias.query.get(id)
	if id=='0':
		dispositivos=Dispositivos.query.all()
	else:
		dispositivos=Dispositivos.query.filter_by(CategoriaId=id)
	categorias=Categorias.query.all()
	logging.info("/parametros.html Llamada a página de parámetros")
	parametros = Parametros.query.all()
	listacomandos = [[]]
	comandos = Comandos.query.all()
	# ~ print(comandos, sys.stdout)
	for c in comandos:
		listacomandos.append({"codigo": c.codigo, "descripcion": c.descripcion})
		print(c, sys.stdout)
	return render_template("parametros.html", dispositivos = dispositivos, categorias=categorias,categoria=categoria, parametros = parametros, listacomandos = listacomandos)

@app.route('/parametros/new', methods=["get","post"])
@login_required
def parametros_new():
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	form=formParametros()
	comandos=[(c.id, c.descripcion, c.codigo) for c in Comandos.query.all()]
	form.ComandoId.choices = comandos
	
	if form.validate_on_submit():
		par = Parametros()
		form.populate_obj(par)
		db.session.add(par)
		db.session.commit()
		logging.info("Creado parámetro con id = '%s': '%s', asignado al comando con id = '%s'.", par.id, par.accion, par.ComandoId)
		return redirect(url_for("parametros"))
	# Si se llega a la página sin haber enviado formulario (con GET) nos vamos a la página en blanco
	return render_template("parametros_new.html",form=form)

@app.route('/parametros/<id>/edit', methods=["get","post"])
@login_required
def parametros_edit(id):
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	par=Parametros.query.get(id)
	if par is None:
		abort(404)

	form=formParametro(obj=par)
	comandos=[(c.id, c.descripcion, c.codigo) for c in Comandos.query.all()]
	form.ComandoId.choices = comandos
	
	if form.validate_on_submit():		
		form.populate_obj(par)
		db.session.commit()
		logging.info("Editada acción con id = '%s': '%s', asignada a tecla '%s'.", par.id, par.accion, par.tecla)
		return redirect(url_for("parametros"))
	return render_template("parametros.html",form=form)

@app.route('/parametros/<id>/delete', methods=["get","post"])
@login_required
def parametros_delete(id):
		# Control de permisos
	if not current_user.is_admin():
		abort(404)

	par=Parametros.query.get(id)
	if par is None:
		abort(404)

	form=formSINO()
	if form.validate_on_submit():
		if form.si.data:
			par_descripcion = par.descripcion
			par_id = par.id
			par_valor = par.valor
			db.session.delete(par)
			db.session.commit()
			logging.info("Borrado parámetro con id = '%s' y valor '%s'.  '%s'.", par_id, par_valor, par_descripcion)
		return redirect(url_for("parametros"))
	return render_template("parametros_delete.html",form=form,par=par)

##################### BOTONERA ###################
@app.route('/botonera')
def botonera(id = '0'):
	categorias=Categorias.query.all()
	categoria=Categorias.query.get(id)
	consulta = db.engine.execute("SELECT botones.tecla,botones.accion,dispositivos.puerto,dispositivos.archivoPY,comandos.codigo,parametros.valor,parametros.descripcion FROM botones JOIN parametros ON parametros.id = botones.ParametroId JOIN comandos ON comandos.id = parametros.ComandoId JOIN dispositivos ON dispositivos.id = comandos.DispositivoId")
	nombres_botones = ["No asignado","No asignado","No asignado","No asignado","No asignado","No asignado","No asignado","No asignado","No asignado","No asignado"]
	lista_botonera = Botones.query.all()
	for l in consulta:
		nombres_botones[int(l[0])] = l[1]
	
	for n in nombres_botones:
		print(n,sys.stdout)
		
		# print(nombres_botones[i], sys.stdout)

	#Realizamos la consulta de los comandos asignados en la botonera:
	#Para cada tecla de la botonera se muestra el puerto del dispositivo, el/los comando/s y el/los parámetro/s asociado/s.
	# [('1', '/dev/ttyUSB0', 'set_power', 'ON'),
	#  ('1', '/dev/ttyUSB1', 'set_mute', 'OFF'),
	#  ('6', '/dev/ttyUSB0', 'set_power', 'OFF'),
	#  ('6', '/dev/ttyUSB1', 'set_mute', 'ON'),
	#  ('2', '/dev/ttyUSB0', 'set_avmute', 'ON'),
	#  ('7', '/dev/ttyUSB0', 'set_avmute', 'OFF'),
	#  ('0', '/dev/ttyUSB1', 'set_line1_vol', '55')]

	#sacamos todos los datos de esta consulta y los guardamos en datos
	lista_acciones = [[],[],[],[],[],[],[],[],[],[]]

	#Pasamos los datos que nos da la consulta a una lista en la que cada elemento contiene una lista de comandos asociados a un botón.
	#Por ejemplo lista_botones[0] corresponde al botón 0 y contiene una lista de diccionarios, cada uno de los cuales contiene los datos necesarios para ejecutar un comando: puerto serie y orden, además de una pequeña descripción.
	for linea in consulta:
		lista_acciones[int(linea[0])].append({"puerto" : linea[2], "modulo" : linea[3].rstrip(".py"), "orden" : linea[4] + "(\"" + linea[5] + "\")", "descripcion" : linea[6]})
	# print(lista_accioness[0][0]["orden"])
	return render_template("botonera.html", categorias = categorias, categoria = categoria, nombres_botones = nombres_botones, lista_acciones = lista_acciones)

@app.route('/pulsar_boton/', methods = ['POST'])
def pulsar_boton():
	lista_acciones = [[],[],[],[],[],[],[],[],[],[]]
	consulta = db.engine.execute("SELECT botones.tecla,botones.accion,dispositivos.puerto,dispositivos.archivoPY,comandos.codigo,parametros.valor,parametros.descripcion FROM botones JOIN parametros ON parametros.id = botones.ParametroId JOIN comandos ON comandos.id = parametros.ComandoId JOIN dispositivos ON dispositivos.id = comandos.DispositivoId")
	
	#Pasamos los datos que nos da la consulta a una lista en la que cada elemento contiene una lista de comandos asociados a un botón.
	#Por ejemplo lista_botones[0] corresponde al botón 0 y contiene una lista de diccionarios, cada uno de los cuales contiene los datos necesarios para ejecutar un comando: puerto serie y orden, además de una pequeña descripción.
	for linea in consulta:
		lista_acciones[int(linea[0])].append({"puerto" : linea[2], "modulo" : linea[3].rstrip(".py"), "orden" : linea[4] + "(\"" + linea[5] + "\")", "descripcion" : linea[6]})
	
	i = int(request.form["boton"])
	lista_comandos = lista_acciones[i]
	for c in lista_comandos:
		nombre_modulo = c["modulo"].rstrip(".py")
		print("nombre módulo", sys.stdout)
		try:
			modulo = importlib.import_module(nombre_modulo)
			print("modulo " + nombre_modulo + " importado", sys.stdout)
		except:
			print("módulo no importado", sys.stdout)
		dispositivo = modulo.device(c["puerto"])
		print("dispositivo iniciado", sys.stdout)
		eval("dispositivo." + c["orden"])
		print("orden lanzada", sys.stdout)
		print(c["puerto"] + ", " + c["modulo"] + ", " + c["orden"] + ", " + c["descripcion"], sys.stdout)
		logging.info("Puerto: '%s', dispositivo: '%s', comando: '%s', descripción: '%s'", c["puerto"], c["modulo"], c["orden"], c["descripcion"])
	return ""

##################### ACCIONES ASIGNADAS A BOTONERA ####################
@app.route('/acciones_botonera')
def acciones_botonera(id='0'):
	categoria=Categorias.query.get(id)
	if id=='0':
		dispositivos=Dispositivos.query.all()
	else:
		dispositivos=Dispositivos.query.filter_by(CategoriaId=id)
	categorias=Categorias.query.all()
	logging.info("/botonera_ok.html Llamada a página de la botonera")
	botones = Botones.query.all()
	listaparametros = []
	parametros = Parametros.query.all()
	# ~ print(parametros, sys.stdout)
	for p in parametros:
		listaparametros.append(p.descripcion)
		print(p, sys.stdout)
	return render_template("acciones_botonera.html", dispositivos = dispositivos, categorias=categorias,categoria=categoria, botones = botones, listaparametros = listaparametros)

@app.route('/accion_boton/new', methods=["get","post"])
@login_required
def accion_boton_new():
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	form=formBotonera()
	parametros=[(p.id, p.descripcion) for p in Parametros.query.all()]
	form.ParametroId.choices = parametros
	
	if form.validate_on_submit():
		bot = Botones()
		form.populate_obj(bot)
		db.session.add(bot)
		db.session.commit()
		logging.info("Creada acción con id = '%s': '%s', asignada a tecla '%s'.", bot.id, bot.accion, bot.tecla)
		return redirect(url_for("botonera"))
	# Si se llega a la página sin haber enviado formulario (con GET) nos vamos a la página en blanco
	return render_template("accion_boton_new.html",form=form)

@app.route('/accion_boton/<id>/edit', methods=["get","post"])
@login_required
def accion_boton_edit(id):
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	bot=Botones.query.get(id)
	if bot is None:
		abort(404)

	form=formBotonera(obj=bot)
	parametros=[(p.id, p.descripcion) for p in Parametros.query.all()]
	form.ParametroId.choices = parametros
	
	if form.validate_on_submit():		
		form.populate_obj(bot)
		# bot.ParametroId = form.ParametroId.data
		db.session.commit()
		logging.info("Editada acción con id = '%s': '%s', asignada a tecla '%s'.", bot.id, bot.accion, bot.tecla)
		return redirect(url_for("botonera"))
	return render_template("accion_boton_new.html",form=form)

@app.route('/accion_boton/<id>/delete', methods=["get","post"])
@login_required
def accion_boton_delete(id):
		# Control de permisos
	if not current_user.is_admin():
		abort(404)

	bot=Botones.query.get(id)
	if bot is None:
		abort(404)

	form=formSINO()
	if form.validate_on_submit():
		if form.si.data:
			bot_accion = bot.accion
			bot_id = bot.id
			bot_tecla = bot.tecla
			db.session.delete(bot)
			db.session.commit()
			logging.info("Borrada acción con id = '%s': '%s', asignada a tecla '%s'.", bot_id, bot_accion, bot_tecla)
		return redirect(url_for("botonera"))
	return render_template("accion_boton_delete.html",form=form,bot=bot)

##################################
@app.route('/dispositivo/<id>')
@login_required
def dispositivo(id='0'):
	if id=='0':
		# Si se indica categoría 0 nos dirigimos a la página principal
		logging.info("/inicio.html. No existe Dispositivo con id = 0.")
		return redirect(url_for("inicio"))
	else:
		db_device = Dispositivos.query.get(id)

		#importamos el archivo con la clase y los métodos del dispositivo según el su nombre de archivo
		nombre_modulo = db_device.archivoPY.rstrip(".py")
		print(nombre_modulo, sys.stdout)
		try:
			modulo = importlib.import_module(nombre_modulo)
			print("modulo " + nombre_modulo + " importado", sys.stdout)
		except:
			print("módulo no importado", sys.stdout)

		# print(nombre_modulo +".device(db_device.puerto)")
		puerto = db_device.puerto
		print(puerto)
		# print(eval(modulo +".device(eval(puerto))"))
		dispositivo = modulo.device(puerto)
		status = dispositivo.get_status()
		pagina = db_device.archivoHTML
		nombre = db_device.nombre
		device_id = db_device.id
		logging.info("/%s Dispositivo '%s'  con id = %s.", pagina, nombre, id)
		return render_template(pagina, device_id = device_id, **status, port = puerto)

@app.route('/orden/<device_id>', methods = ['POST'])
def proj_command(device_id = None):
	if request.method == "POST":
		if device_id=='0':
			# Si se indica categoría 0 nos dirigimos a la página principal
			logging.info("/inicio.html desde una orden con id = 0.")
			return redirect(url_for("inicio"))
		else:
			db_device = Dispositivos.query.get(device_id)
			nombre_modulo = db_device.archivoPY.rstrip(".py")
			print(nombre_modulo, sys.stdout)
			try:
				modulo = importlib.import_module(nombre_modulo)
				print("modulo " + nombre_modulo + " importado", sys.stdout)
			except:
				print("módulo no importado", sys.stdout)
			puerto = db_device.puerto
			dispositivo = modulo.device(puerto)
			cmd = request.form["command"]
			param = request.form["parameter"]
			orden = getattr(dispositivo,cmd) # busca en el objeto el método con el nombre que viene en cmd
			orden(param)
			status = dispositivo.get_status_dic()
			logging.info("/%s Orden: '%s', parámetro: '%s', puerto: '%s', id Dispositivo: %s.", db_device.archivoHTML, cmd, param, puerto, device_id)
			return jsonify(status)		
			# return render_template('proyector.html', **status, device_name = proj.device_name)

@app.route('/dispositivo/new', methods=["get","post"])
@login_required
def dispositivo_new():
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	form=formDispositivo()
	categorias=[(c.id, c.nombre) for c in Categorias.query.all()[1:]]
	form.CategoriaId.choices = categorias
	
	if form.validate_on_submit():
		try:
			puerto = form.puerto.data
		except:
			puerto = "/dev/ttyUSB0"

		try:
			f = form.imagen.data
			nombre_imagen=secure_filename(f.filename)
			f.save(app.root_path+"/static/img/"+nombre_imagen)
		except:
			nombre_imagen=""

		try:
			f = form.archivoHTML.data
			nombre_archivoHTML=secure_filename(f.filename)
			f.save(app.root_path+"/templates/"+nombre_archivoHTML)
		except:
			nombre_archivoHTML=""

		try:
			f = form.archivoPY.data
			nombre_archivoPY=secure_filename(f.filename)
			f.save(app.root_path+"/"+nombre_archivoPY)
		except:
			nombre_archivoPY=""
		disp = Dispositivos()
		form.populate_obj(disp)
		disp.puerto = puerto
		disp.imagen = nombre_imagen
		disp.archivoHTML = nombre_archivoHTML
		disp.archivoPY = nombre_archivoPY
		db.session.add(disp)
		db.session.commit()
		logging.info("/%s Puerto: '%s', imagen: '%s', archivoPY: '%s'.", nombre_archivoHTML, puerto, nombre_imagen, nombre_archivoPY)
		return redirect(url_for("inicio"))
	# Si se llega a la página sin haber enviado formulario (con GET) nos vamos a la página en blanco
	return render_template("dispositivo_new.html",form=form)


@app.route('/dispositivo/<id>/delete', methods=["get","post"])
@login_required
def dispositivo_delete(id):
		# Control de permisos
	if not current_user.is_admin():
		abort(404)

	disp=Dispositivos.query.get(id)
	if disp is None:
		abort(404)

	form=formSINO()
	if form.validate_on_submit():
		if form.si.data:
			if disp.imagen != "":
				os.remove(app.root_path + "/static/img/" + disp.imagen)
			disp_nombre = disp.nombre
			disp_id = disp.id
			disp_puerto = disp.puerto
			db.session.delete(disp)
			db.session.commit()
			logging.info("/dispositivo_delete.html Dispositivo '%s' con id = '%s' en puerto: '%s' borrado.", disp_nombre, disp_id, disp_puerto)
		return redirect(url_for("inicio"))
	return render_template("dispositivo_delete.html",form=form,disp=disp)


@app.route('/dispositivo/<id>/edit', methods=["get","post"])
@login_required
def dispositivo_edit(id):
	# Control de permisos
	if not current_user.is_admin():
		abort(404)

	disp=Dispositivos.query.get(id)
	if disp is None:
		abort(404)

	form=formDispositivo(obj=disp)
	categorias=[(c.id, c.nombre) for c in Categorias.query.all()[1:]]
	form.CategoriaId.choices = categorias
	
	if form.validate_on_submit():
		#Borramos la imagen anterior si hemos subido una nueva
		if  form.puerto.data:
			puerto = form.puerto.data
		else:
			puerto = "/dev/ttyUSB0"

		if  form.imagen.data:
			try:
				os.remove(app.root_path + "/static/img/" + disp.imagen)
			except:
				print("ERROR: No se encuentra la imagen especificada para borrar", sys.stdout)
			try:
				f = form.imagen.data
				nombre_imagen=secure_filename(f.filename)
				f.save(app.root_path + "/static/img/" + nombre_imagen)
			except:
				nombre_imagen = ""
		else:
			nombre_imagen = disp.imagen

		if  form.archivoHTML.data:
			try:
				os.remove(app.root_path+"/templates/"+disp.archivoHTML)
			except:
				print("ERROR: No se encuentra el archivo HTML especificado para borrar", sys.stdout)
			try:
				f = form.archivoHTML.data
				nombre_archivoHTML=secure_filename(f.filename)
				f.save(app.root_path+"/templates/"+nombre_archivoHTML)
			except:
				nombre_archivoHTML=""
		else:
			nombre_archivoHTML=disp.archivoHTML

		if  form.archivoPY.data:
			try:
				os.remove(app.root_path+"/"+disp.archivoPY)
			except:
				print("ERROR: No se encuentra el archivo .py para borrar", sys.stdout)
			try:
				f = form.archivoPY.data
				nombre_archivoPY=secure_filename(f.filename)
				f.save(app.root_path+"/"+nombre_archivoPY)
			except:
				nombre_archivoPY=""
		else:
			nombre_archivoPY=disp.archivoPY
			
		form.populate_obj(disp)
		disp.puerto = puerto
		disp.imagen = nombre_imagen
		disp.archivoHTML = nombre_archivoHTML
		disp.archivoPY = nombre_archivoPY
		db.session.commit()
		logging.info("/%s Dispositivo con id = '%s'. Editados puerto: '%s', imagen: '%s', archivoPY: '%s'.", nombre_archivoHTML, disp.id, puerto, nombre_imagen, nombre_archivoPY)
		return redirect(url_for("inicio"))
	return render_template("dispositivo_new.html",form=form)

#Descargar archivo de log
@app.route("/descargar_log_web")
@login_required
def descargar_log_web():
	# Control de permisos
	if not current_user.is_admin():
		abort(403)
	return send_file("../registro_web.log", as_attachment=True)

@app.route("/descargar_log_botonera")
@login_required
def descargar_log_botonera():
	# Control de permisos
	if not current_user.is_admin():
		abort(403)
	return send_file("../registro_botonera.log", as_attachment=True)


# Acceso no permitido
@app.errorhandler(403)
def no_permitido(error):
	return render_template("error.html",error="Acceso no permitido."), 403

# Página no encontrada
@app.errorhandler(404)
def page_not_found(error):
	return render_template("error.html",error="Página no encontrada..."), 404

# @app.route('/puerto/<device_id>', methods = ['POST'])
# def proj_port_edit(device_id = None):
# 	if request.method == "POST":
# 		if id=='0':
# 			# Si se indica categoría 0 nos dirigimos a la página principal
# 			return render_template("/categoria/0")
# 		else:
# 			# No tenemos que crear el objeto del dispositivo como antes
# 			# Tan solo cambiamos el puerto y lo almacenamos en la BDD
# 			port = request.form["port_name"]
# 			db_device = Dispositivos.query.get(device_id)
# 			db_device.port = port
# 			status = dispositivo.get_status()
# 			return jsonify(port)




# @app.route('/mezclador')
# @login_required
# def mixer():
# 	mixer = mezclador("/dev/ttyUSB1")
# 	name = mixer.device_name
# 	status = mixer.get_status()
# 	return render_template('mezclador.html', **status, device_name=name)

# @app.route('/mezclador/<cmd>')
# def mixer_command(cmd=None):
# 	mixer = mezclador("/dev/ttyUSB1")
# 	orden = getattr(mixer,cmd) # capta el nombre del comando
# 	status = orden() # Función con el mismo nombre del comando que devuelve el estado del mezclador
# 	return jsonify(status)

# @app.route('/mezclador/status')
# def mixer_status():
# 	mixer=mezclador("/dev/ttyUSB1")
# 	status = mixer.get_status()
# 	return jsonify(status)


# @app.route('/proyector')
# def projector():
# 	proj = proyector("/dev/ttyUSB0")
# 	name = proj.device_name
# 	status = proj.get_status()
# 	return render_template('proyector.html', **status, device_name=name)



# @app.route('/proyector/status')
# def proj_status():
# 	proj = proyector("/dev/ttyUSB0")
# 	status = proj.get_status_dic()
# 	return jsonify(status)
