import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser #esta libreria ya la tiene python
import datetime #esta libreria ya la tiene python
import wikipedia #esta libreria ya la tiene python

'''Funcion para escuchar nuestro microfono y devolver audio como texto'''
def transformar_audio_en_texto():

    #almacernar el recognizer en una variable
    r = sr.Recognizer()

    #configurar el microfono
    with sr.Microphone() as origen:
        #tiempo de espera desde que se active el microfono para que empiece a escuchar
        r.pause_threshold = 0.8

        #informar que comenzo la grabacion
        print('ya puedes hablar')

        #guardar lo que escuche como audio en una variable
        audio = r.listen(origen)

        try:
            # buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language='es-es')

            #prueba de que pudo ingresar y transformar nuestra voz en un texto
            print('Dijiste: '+ pedido)

            #devolver a pedido
            return pedido
        #en caso de que no comprenda el audio
        except sr.UnknownValueError:

            #prueba de que no comprendio el audio
            print('ups, no entendi')

            #devolver error
            return 'sigo esperando'

        #en caso de no resolver el pedido, es decir, que grabo el audio pero no lo puede transformar
        except sr.RequestError:
            # prueba de que no comprendio el audio
            print('ups, no hay servicio')

            # devolver error
            return 'sigo esperando'

        #en caso de error inesperado
        except:
            # prueba de que no comprendio el audio
            print('ups, algo ha salido mal')

            # devolver error
            return 'sigo esperando'

'''#El siguiente codigo es para saber que tipos de voz tengo instalados en mi computador'''
#engine = pyttsx3.init()
#for voz in engine.getProperty('voices'):
    #print(voz)

id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

'''Funcion para que el asistente puede ser escuchado'''
def hablar(mensaje):

    # encender el motor de pyttsx3, se le colocla engine por convencion
    engine = pyttsx3.init()
    #como abajo se que tipos de voz tengo en mi laptop ahora puedo definir cual usar
    engine.setProperty('voice', id1)
    # pronunciar un mensaje
    engine.say(mensaje)
    engine.runAndWait()


'''Funcion para informar el dia de la semana'''
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    #crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    # Decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


'''Funcion para informar que hora es'''
def pedir_hora():

    #crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    #decir la hora
    hablar(hora)


'''Funcion saludo inicial'''
def saludo_inicial():


    #crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = ' Buenas noches'
    elif hora.hour >= 6 and hora.hour< 13:
        momento = 'Buen dia'
    else:
        momento = 'Buenas tardes'

     #decir el saludo
    hablar(f'{momento}, soy Helena, tu asistente personal, por favor, dime en que te puedo ayudar')

'''#Funcion central del asistente'''
def pedir_cosas():

    #activar saludo inicial
    saludo_inicial()

    #para que esta funcion no se detenga y sigan funcionando hasta que le indiquemos algo hacemos un loop
    # while, primero debemos asignar una variable de corte
    comenzar = True

    #loop centra

    while comenzar:

        '''Activar el micro y guardar el pedido en un string, en una variable que llamamos pedido
        la igualamos a la funcion transformar audio en texto y le ponemos lower para que me trasnforme
        todo a minuscula'''
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar("Con gusto, estoy abriendo youtube")
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'que dia es hoy' in pedido:
            pedir_dia()
            continue
        elif 'que hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            #en este caso reigualo pedido con un replace para que no busque la palabra busca en wikipedia
            pedido = pedido.replace('busca en wikipedia','')
            #con set_lang estoy configurando el lenguaje que es espanol
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido) #playonyt es reproducir en youtube
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es')) #para un chiste- get joke como argumento el idioma
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()

            '''#crear un diccionario donde se asignara algunas acciones de la bolsa y como las puede identificar en la bolsa
            por ejemplo apple en la bolsa es APPL'''
            cartera = {'apple':'APPL',
                       'amazon': 'AMZN',
                       'google':'GOOGL'}

            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontre, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdon, pero no la he encontrado')
                continue
        elif 'adiós' in pedido:
            hablar('Me voy a descanar, cualquier cosa me avisas')
            break

pedir_cosas()


