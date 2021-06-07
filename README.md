# proyecto-ASIR
# Gestión y control de medios audiovisuales en un aula de docencia. 
  Proyecto integrado para el curso 2020-2021 del ciclo Administración de Sistemas Informáticos en Red (ASIR) en el IES Francisco Romero Vargas. El objetivo básico de este proyecto consiste en la automatización del equipamiento audiovisual de un aula de docencia, de manera que ofrezca al profesor la mayor sencillez posible en el manejo de los equipos, así como que permita al administrador de los medios la consulta, supervisión y control de estos tanto en el sitio como de forma remota.
  
# Finalidad

  Es un hecho que hoy en día cualquier aula dedicada a la enseñanza suele contar con medios tecnológicos de apoyo, como la proyección de vídeo o la megafonía, que ayudan a los docentes en la impartición de sus clases. Estos medios requieren como es lógico de una puesta en marcha diaria y de un manejo para que se adecúen a las necesidades del profesor o la profesora en cada momento (encender los equipos, ajustar el micrófono, …). 
  A menudo estas tareas (como por ejemplo buscar el mando a distancia del videoproyector para encenderlo y encontrar el botón para que se vea el portátil, o encontrar el potenciómetro exacto del amplificador con el que se sube el volumen del micrófono), por elementales que parezcan, ocasionan molestias al docente que incluso provocan cierto hastío o falta de preocupación por el buen funcionamiento de los medios. Tal es así que en ocasiones éstos emiten quejas o plantean incidencias que se resuelven sin necesidad de apoyo técnico, tan solo sabiendo la operativa básica del equipamiento.
  En lo que respecta al vídeo, un aula de docencia básica cuenta normalmente con una pantalla de proyección, que queremos poder subir y bajar, y un videoproyector conectado por defecto al PC del aula que necesitamos poder apagar y encender, ambos de forma sincronizada con dos simples botones y sin tener que estar pendientes de un mando a distancia. También se desea la posibilidad de conectar un ordenador portátil que se disponga en el momento para proyectar su imagen. En cuanto al audio, se pretende poder controlar los niveles sonoros de micrófono y altavoces con pares de botones de subida y bajada. Con esto pretendemos simplificar el manejo lo máximo posible para que quien esté impartiendo la clase se libre de preocupaciones innecesarias con el equipamiento audiovisual, el cual realmente está para facilitar su labor. 
  Al tratarse de medios digitalizados con los que se puede interactuar, resulta interesante para alguien que tiene que mantener estos equipos la posibilidad de obtener datos de diagnóstico como estado, avería, consumo, etcétera, simplemente iniciando sesión desde una interfaz web, bien desde el PC del aula o desde fuera.

# Objetivos

  Dividiremos el proyecto en dos partes: control y gestión.
  
# Control

  La idea se centra en el PC miniaturizado Raspberry Pi, que hará de controlador del sistema. A este conectaremos por USB los siguientes elementos:
  
  •	Teclado personalizado de 10 botones desde el que se ejecutarán las órdenes básicas del equipamiento audiovisual.
   - Encendido y apagado general.    
   - Activación y desactivación del videoproyector.    
   - Subida y bajada del volumen del micrófono del docente.    
   - Subida y bajada del volumen los altavoces de la sala.
    
    
  •	Interfaces USB-RS232 para controlar:
   - Videoproyector.    
   - Amplificador-mezclador de audio.    
   - (Opcional) Conmutador de vídeo HDMI. Este recibe a su entrada tanto la señal de vídeo del PC de escritorio como la de un portátil que conectemos si es necesario. Sus salidas irán hacia el monitor de la mesa del docente y hacia el videoproyector.
    ![image](https://user-images.githubusercontent.com/55459327/121046195-39a4a980-c7b6-11eb-9d2d-30a4680147f2.png)


  Una pantalla de proyección común incorpora su propio panel de botones que accionan los relés de movimiento de subida y bajada. Para controlarlo conectaremos el puerto GPIO de la Raspberry a este panel mediante un optoacoplador (con el que aislamos nuestra Raspberry del circuito del motor la pantalla).
Mediante software se pretende programar la Raspberry para que, en función del botón pulsado, se comunique por puerto serie con los equipos que sea necesario. Por ejemplo, el botón de puesta en marcha realizaría lo siguiente:
  1.	Enviar una señal de encendido al proyector por el puerto serie.
  2.	Bajar la pantalla de proyección.
  3.	Enviar señal de encendido al amplificador de audio por su puerto serie correspondiente.
  4.	Reajusta los niveles de audio por si en la sesión anterior se hubieran dejado en un punto no deseado.
  5.	Enviar por serie la fuente de vídeo por defecto al conmutador de vídeo HDMI.
  6.	Enviar magic packet al PC del escritorio para que se encienda. Suponemos que ambos, controlador y PC se encuentran en la misma red.

# Gestión

  El controlador de los medios (RPi) albergará una interfaz web por medio de la que se podrá:
  
  •	Consultar el estado del equipamiento en el momento por si existe alguna incidencia o anomalía. Para ello el controlador enviaría las señales oportunas a los equipos vía RS-232.
  
  •	Controlar o reajustar parámetros del equipo del aula.
  
  •	Visualizar un histórico de operaciones, (encendido, selección, consulta…) para dar la posibilidad de un seguimiento de uso. Cada operación que haga el controlador deberá ser recogida en un archivo log.
  
  •	Enviar al controlador un archivo con los comandos de comunicación RS-232 actualizados en caso de que alguno de los equipos debiera ser sustituido por un modelo diferente. El controlador tendría una base de datos con diferentes modelos y los códigos correspondientes para cada operación.
  


# Medios necesarios

  Para la realización de este proyecto se necesita lo siguiente:
  
  •	Un ordenador PC de configuración media que hará de ordenador del aula.
  
  •	Un miniordenador Raspberry Pi 3B
  
  •	Un videoproyector con entrada HDMI y puerto serie RS-232.
  
  •	Cableado HDMI.
  
  •	Conmutador de vídeo con puerto serie RS-232.
  
  •	Amplificador-mezclador de audio con interfaz RS-232.
  
  •	Altavoces.
  
  •	Cableado de audio.
  
  •	Teclado pequeño de 10 teclas.
  
  •	Interfaces USB- RS232.
  
  •	Switch Ethernet
  
  •	Cableado de red para el PC de la mesa y la Raspberry.
  
