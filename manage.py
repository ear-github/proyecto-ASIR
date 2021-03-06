from flask_script import Manager
from aplicacion.app import app,db
from aplicacion.models import *
from getpass import getpass

manager = Manager(app)
app.config['DEBUG'] = True # Ensure debugger will load.

@manager.command
def create_tables():
    #"Create relational database tables."
    db.create_all()
    categoria=Categorias(id=0,nombre="Todos")
    db.session.add(categoria)
    db.session.commit()
    # dispositivo=Dispositivos(id=0,nombre="Ninguno", CategoriaId=0)
    # db.session.add(dispositivo)
    # db.session.commit()
    # comando=Comandos(id=0,descripcion="Ninguna", DispositivoId=0)
    # db.session.add(comando)
    # db.session.commit()
    # parametro=Parametros(id=0,descripcion="Ninguna", ComandoId=0)
    # db.session.add(parametro)
    # db.session.commit()

@manager.command
def drop_tables():
    # "Drop all project relational database tables. THIS DELETES DATA."
    db.drop_all()

@manager.command
def add_data_tables():
    db.create_all()

    categorias = ("Videoproyector","Mezclador","Pantalla", "PC")
    for cat in categorias:
        categoria=Categorias(nombre=cat)
        db.session.add(categoria)
        db.session.commit()

    dispositivos=[
    {"nombre":"Mitsubmshi EX320U","CategoriaId":1,"puerto":"/dev/ttyUSB0","ip" : "", "mac" : "","imagen":"mitsubishi_ex320u.jpg","descripcion":"Videoproyector DLP de la marca Mitsubishi", "archivoHTML":"vp_ex320u.html", "archivoPY":"vp_ex320u.py"},
    {"nombre":"Ecler CA-40","CategoriaId":2,"puerto":"/dev/ttyUSB1", "ip" : "", "mac" : "","imagen":"ecler_ca40.jpg","descripcion":"Mezclador compacto de una entrada de micro más una entrada de línea a escoger entre dos posibles. Incluye amplificador de 40 W y control por RS-232", "archivoHTML":"mx_ca40.html", "archivoPY":"mx_ca40.py"},
    {"nombre":"Pantalla simulada","CategoriaId":3,"puerto":"GPIO","ip" : "", "mac" : "","imagen":"pt_simulada.jpg","descripcion":"Motor DC que simula el movimiento de una pantalla de proyección real", "archivoHTML":"pt_simulada.html", "archivoPY":"pt_simulada.py"},
    {"nombre":"PC del aula 00 (RPi)","CategoriaId":4,"puerto":"ssh","ip" : "192.168.88.254", "mac" : "b8:27:eb:cb:1e:15","imagen":"pc_aula.jpeg","descripcion":"Se apaga por SSH y se enciende por WOL (no soportado en RPi).", "archivoHTML":"pc_aula.html", "archivoPY":"pc_aula.py"},    
    ]

    for disp in dispositivos:
        dispositivo=Dispositivos(**disp)
        db.session.add(dispositivo)
        db.session.commit()

    comandos=[
    # Videoproyector. Consultas
    {"descripcion":"EX320U-Estado general del videoproyector","codigo": "get_status", "DispositivoId":1},
    {"descripcion":"EX320U-Estado de encendido","codigo": "get_power", "DispositivoId":1},
    {"descripcion":"EX320U-Estado de mutado A/V","codigo": "get_avmute", "DispositivoId":1},
    {"descripcion":"EX320U-Fuente seleccionada","codigo": "get_source", "DispositivoId":1},
    {"descripcion":"EX320U-Volumen de altavoz","codigo": "get_volume", "DispositivoId":1},
    {"descripcion":"EX320U-Obtener preajuste de imagen","codigo": "get_picturesetting", "DispositivoId":1},
    {"descripcion":"EX320U-Obtener contraste","codigo": "get_contrast", "DispositivoId":1},
    {"descripcion":"EX320U-Obtener brillo","codigo": "get_brightness", "DispositivoId":1},
    {"descripcion":"EX320U-Obtener relación de aspecto","codigo": "get_aspect", "DispositivoId":1},
    {"descripcion":"EX320U-Obtener tiempo de lámpara","codigo": "get_lamptime", "DispositivoId":1},
    {"descripcion":"EX320U-Obtener modo de iluminación de lámpara","codigo": "get_lampmode", "DispositivoId":1},
    # Órdenes
    {"descripcion":"EX320U-Encender/Apagar","codigo": "set_power", "DispositivoId":1},
    {"descripcion":"EX320U-Mutear Audio y vídeo","codigo": "set_avmute", "DispositivoId":1},
    {"descripcion":"EX320U-Seleccionar fuente","codigo": "set_source", "DispositivoId":1},
    {"descripcion":"EX320U-Subir/Bajar volumen de altavoz","codigo": "set_volume", "DispositivoId":1},
    {"descripcion":"EX320U-Establecer preajuste de imagen","codigo": "set_picturesetting", "DispositivoId":1},
    {"descripcion":"EX320U-Ajustar contraste","codigo": "set_contrast", "DispositivoId":1},
    {"descripcion":"EX320U-Ajustar brillo","codigo": "set_brightness", "DispositivoId":1},
    {"descripcion":"EX320U-Establecer relación de aspecto","codigo": "set_aspect", "DispositivoId":1},
    {"descripcion":"EX320U-Establecer modo de iluminación de lámpara","codigo": "set_lampmode", "DispositivoId":1},
    # Mezclador. Consultas
    {"descripcion":"CA40-Obtener estado general del mezclador","codigo":"get_status","DispositivoId":2},
    {"descripcion":"CA40-Obtener silenciado del mezclador","codigo":"mute_status","DispositivoId":2},
    {"descripcion":"CA40-Obtener nivel maestro del mezclador","codigo":"master_status","DispositivoId":2},
    {"descripcion":"CA40-Obtener nivel de micrófono del mezclador","codigo":"mic_status","DispositivoId":2},
    {"descripcion":"CA40-Obtener nivel de línea del mezclador","codigo":"line1_status","DispositivoId":2},
    # Órdenes
    {"descripcion":"CA40-Poner/Quitar silencio en el mezclador","codigo":"set_mute","DispositivoId":2},
    {"descripcion":"CA40-Subir volumen maestro del mezclador","codigo":"master_vol_up","DispositivoId":2},
    {"descripcion":"CA40-Bajar volumen maestro del mezclador","codigo":"master_vol_down","DispositivoId":2},
    {"descripcion":"CA40-Subir volumen de micrófono del mezclador","codigo":"mic_vol_up","DispositivoId":2},
    {"descripcion":"CA40-Bajar volumen de micrófono del mezclador","codigo":"mic_vol_down","DispositivoId":2},
    {"descripcion":"CA40-Subir volumen de línea del mezclador","codigo":"line1_vol_up","DispositivoId":2},
    {"descripcion":"CA40-Bajar volumen de línea del mezclador","codigo":"line1_vol_down","DispositivoId":2},
    {"descripcion":"CA40-Ajustar a un nivel determinado el volumen maestro","codigo":"set_master_vol","DispositivoId":2},
    {"descripcion":"CA40-Ajustar a un nivel determinado el volumen de micrófono","codigo":"set_mic_vol","DispositivoId":2},
    {"descripcion":"CA40-Ajustar a un nivel determinado el volumen de línea","codigo":"set_line1_vol","DispositivoId":2},
    {"descripcion":"CA40-Subir/Bajar el volumen maestro del mezclador","codigo":"master_vol_up_down","DispositivoId":2},
    {"descripcion":"CA40-Subir/Bajar el volumen de micrófono del mezclador","codigo":"mic_vol_up_down","DispositivoId":2},
    {"descripcion":"CA40-Subir/Bajar el volumen de línea del mezclador","codigo":"line1_vol_up_down","DispositivoId":2},
    {"descripcion":"Pantalla-Mover (simulación)","codigo":"set_screen","DispositivoId":3},
    {"descripcion":"PC-Alimentación","codigo":"set_power","DispositivoId":4}
    ]
    for com in comandos:
        comando=Comandos(**com)
        db.session.add(comando)
        db.session.commit()

    #Algunos parámetros que serán de utilidad a la hora de asignar órdenes a cada botón
    parametros=[
    {"descripcion":"EX320U-Encender Videoproyector", "valor":"ON", "ComandoId":12},
    {"descripcion":"EX320U-Apagar Videoproyector", "valor":"OFF", "ComandoId":12},
    {"descripcion":"EX320U-Mutear A/V videoproyector", "valor":"ON", "ComandoId":13},
    {"descripcion":"EX320U-Desmutear A/V Videoproyector", "valor":"OFF", "ComandoId":13},
    {"descripcion":"EX320U-Fuente VGA Computer 1 de Videoproyector", "valor":"Computer 1", "ComandoId":14},
    {"descripcion":"EX320U-Fuente VGA Computer 2 de Videoproyector", "valor":"Computer 2", "ComandoId":14},
    {"descripcion":"EX320U-Fuente Video-1 de Videoproyector", "valor":"Video 1", "ComandoId":14},
    {"descripcion":"EX320U-Fuente S-Video de Videoproyector", "valor":"S-Video", "ComandoId":14},
    {"descripcion":"EX320U-Fuente HDMI de Videoproyector", "valor":"HDMI", "ComandoId":14},
    {"descripcion":"EX320U-Subir volumen Videoproyector", "valor":"up", "ComandoId":15},
    {"descripcion":"EX320U-Bajar volumen Videoproyector", "valor":"down", "ComandoId":15},
    {"descripcion":"EX320U-Preajuste de imagen Brightest", "valor":"Brightest", "ComandoId":16},
    {"descripcion":"EX320U-Preajuste de imagen Presentation", "valor":"Presentation", "ComandoId":16},
    {"descripcion":"EX320U-Preajuste de imagen Normal", "valor":"Normal", "ComandoId":16},
    {"descripcion":"EX320U-Preajuste de imagen Theather", "valor":"Theather", "ComandoId":16},
    {"descripcion":"EX320U-Preajuste de imagen User 1", "valor":"User 1", "ComandoId":16},
    {"descripcion":"EX320U-Preajuste de imagen User 2", "valor":"User 2", "ComandoId":16},
    {"descripcion":"EX320U-Restablecer contraste", "valor":"0", "ComandoId":17},
    {"descripcion":"EX320U-Restablecer brillo", "valor":"0", "ComandoId":18},
    {"descripcion":"EX320U-Relación de aspecto a Auto", "valor":"Auto", "ComandoId":19},
    {"descripcion":"EX320U-Relación de aspecto a Real", "valor":"Real", "ComandoId":19},
    {"descripcion":"EX320U-Relación de aspecto a 4:3", "valor":"4:3", "ComandoId":19},
    {"descripcion":"EX320U-Relación de aspecto a 16:9", "valor":"16:9", "ComandoId":19},
    {"descripcion":"EX320U-Modo de lámpara estándar", "valor":"Standard", "ComandoId":20},
    {"descripcion":"EX320U-Modo de lámpara económico", "valor":"Low", "ComandoId":20},
    {"descripcion":"CA40-Restablecer volumen maestro del mezclador", "valor":"60", "ComandoId":33},
    {"descripcion":"CA40-Restablecer volumen de micrófono del mezclador", "valor":"55", "ComandoId":34},
    {"descripcion":"CA40-Restablecer volumen de línea del mezclador", "valor":"50", "ComandoId":35},
    {"descripcion":"CA40-Silenciar mezclador", "valor":"ON", "ComandoId":26},
    {"descripcion":"CA40-Desactivar silencio del mezclador", "valor":"OFF", "ComandoId":26},
    {"descripcion":"CA40-Subir volumen maestro del mezclador", "valor":"up", "ComandoId":36},
    {"descripcion":"CA40-Bajar volumen maestro del mezclador", "valor":"down", "ComandoId":36},
    {"descripcion":"CA40-Subir volumen de micrófono del mezclador", "valor":"up", "ComandoId":37},
    {"descripcion":"CA40-Bajar volumen de micrófono del mezclador", "valor":"down", "ComandoId":37},
    {"descripcion":"CA40-Subir volumen de línea del mezclador", "valor":"up", "ComandoId":38},
    {"descripcion":"CA40-Bajar volumen de línea del mezclador", "valor":"down", "ComandoId":38},
    {"descripcion":"Pantalla-Bajar", "valor":"down", "ComandoId":39},
    {"descripcion":"Pantalla-Subir", "valor":"up", "ComandoId":39},
    {"descripcion":"Pantalla-Parar", "valor":"stop", "ComandoId":39},
    {"descripcion":"PC-Encender", "valor":"on", "ComandoId":40},
    {"descripcion":"PC-Apagar", "valor":"off", "ComandoId":40}
    ]
    for p in parametros:
        parametro=Parametros(**p)
        db.session.add(parametro)
        db.session.commit()

    botones=[
    {"accion":"Encendido de sistema","tecla": "1", "ParametroId":1},
    {"accion":"Encendido de sistema","tecla": "1", "ParametroId": 30},
    {"accion":"Apagado de sistema","tecla": "6", "ParametroId":2},
    {"accion":"Apagado de sistema","tecla": "6", "ParametroId":29},
    {"accion":"Subir pantalla y mutear proyector","tecla": "2", "ParametroId":3},
    {"accion":"Bajar pantalla y desmutear proyector","tecla": "7", "ParametroId":4},
    {"accion":"Subir altavoces","tecla": "3",  "ParametroId":31},
    {"accion":"Bajar altavoces","tecla": "8",  "ParametroId":32},
    {"accion":"Subir micrófono","tecla": "4",  "ParametroId":33},
    {"accion":"Bajar micrófono","tecla": "9",  "ParametroId":34},
    {"accion":"Pánico. Restablecer valores de proyector y mezclador","tecla": "0",  "ParametroId":26},
    {"accion":"Pánico. Restablecer valores de proyector y mezclador","tecla": "0",  "ParametroId":27},
    {"accion":"Pánico. Restablecer valores de proyector y mezclador","tecla": "0",  "ParametroId":28},
    {"accion":"Pánico. Restablecer valores de proyector y mezclador","tecla": "0",  "ParametroId":30},
    {"accion":"Pánico. Restablecer valores de proyector y mezclador","tecla": "0",  "ParametroId":4},
    {"accion":"Pánico. Restablecer valores de proyector y mezclador","tecla": "0",  "ParametroId":9},
    {"accion":"Pánico. Restablecer valores de proyector y mezclador","tecla": "0",  "ParametroId":39},
    {"accion":"Encendido del sistema","tecla": "1", "ParametroId":38},
    {"accion":"Apagado del sistema","tecla": "6", "ParametroId":37},
    {"accion":"Subir pantalla y mutear proyector","tecla": "2", "ParametroId":37},
    {"accion":"Bajar pantalla y desmutear proyector","tecla": "7", "ParametroId":38},
    {"accion":"Encendido del sistema","tecla": "1", "ParametroId":38},
    {"accion":"Encendido del sistema","tecla": "1", "ParametroId":40},
    {"accion":"Apagado del sistema","tecla": "1", "ParametroId":41},
    ]
    for b in botones:
        boton=Botones(**b)
        db.session.add(boton)
        db.session.commit()

@manager.command
def create_admin():
    usuario={"username":input("Usuario:"),
            "password":getpass("Password:"),
            "nombre":input("Nombre completo:"),
            "email":input("Email:"),
            "admin": True}
    usu=Usuarios(**usuario)
    db.session.add(usu)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
