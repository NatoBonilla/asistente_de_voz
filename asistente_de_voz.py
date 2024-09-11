import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
from datetime import datetime
import wikipedia


# opciones de voz / idioma
id_1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
id_2 = "KEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
id_3 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"

# escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():
    
    # almacenar recognizer en variable
    r = sr.Recognizer()
    
    # configurar el microfono
    with sr.Microphone() as origen:
        # tiempo de espera
        r.pause_threshold = 0.8
        
        # Informar que comenzo la grabacion
        print("Ya puedes hablar")
        
        # guardar lo que escuche como audio
        audio = r.listen(origen)
        
        try:
            # uso API reconocimiento de voz de google
            pedido = r.recognize_google(audio, language="es-CO")
            
            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)
            
            # devolver pedido
            return pedido
        
        # en caso de que no comprenda audio
        except sr.UnknownValueError:
            #prueba de que no comprendio el audio
            print("Ups, no entendi")
            
            #devolver error
            return "Sigo esperando"
        
        # en caso de que no comprenda audio
        except sr.RequestError:
            #prueba de que no comprendio el audio
            print("Ups, no hay servicio")
            
            #devolver error
            return "Sigo esperando"
        
        # error inesperado
        except:
            #prueba de que no comprendio el audio
            print("Ups, Algo ha salido mal")
            
            #devolver error
            return "Sigo esperando"
        
        

# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id_3)
    
    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()



# informar el dia de la semana
def pedir_dia():
    
    # crear variable con datos de hoy
    dia = datetime.today().date()
    
    #crear variable para el dia de la semana
    dia_semana = dia.weekday()
    
    # diccionario con nombres de dias
    calendario = {0: "lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "jueves",
                  4: "Viernes", 
                  5: "Sábado",
                  6: "Domingo"}
    
    # decir el dia de la semana
    hablar(f"Hoy es {calendario[dia_semana]}")
    


# informar hora
def pedir_hora():
    
    # crear una variable con datos de la hora
    hora = datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    
    # decir la hora
    hablar(hora)



# funcion saludo inicial
def saludo_inicial():
    
    # crear variable con datos de hora
    hora = datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
        
    elif hora.hour >= 6 and hora.hour < 13:
        momento = "Buen día"
        
    else:
        momento = "Buenas tardes"
    
    
    # decir el saludo
    hablar(f"{momento}, soy Tomoe, Tu asistente personal. Dime en que puedo ayudarte")
    


#funcion central asistente
def pedir_cosas():
    
    #activar sonido inicial
    saludo_inicial()
    
    #variable de corte
    comenzar = True
    
    #loop central
    while comenzar:
        
        #activar el micro y guardar pedido en un string
        pedido = transformar_audio_en_texto().lower()
        
        if "youtube" in pedido:
            hablar("Con gusto, estoy abriendo YouTube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "navegador" in pedido:
            hablar("Claro, estoy en eso")
            webbrowser.open("https://www.google.com")
            continue
        elif "día" in pedido:
            pedir_dia()
            continue
        elif "hora" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("Buscando eso en wikipedia")
            pedido = pedido.replace("busca en wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences = 1)
            hablar("Wikipedia dice lo siguiente: ")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("Ya mismo estoy en eso")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("Buena idea, ya comienzo a reproducirlo")
            pywhatkit.playonyt(pedido)
            continue
        elif "chiste" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "dólar" in pedido:
            hablar("Ya estoy en eso")
            ticker = "COP=X"
            datos = yf.Ticker(ticker)
            historial = datos.history(period = "1d")
            precio_actual = historial['Close'].iloc[-1]
            hablar(f"El precio del dolar actualmente es: {precio_actual} pesos colombianos")
            continue
        elif "mente" in pedido:
            hablar("Algo real, que es lo real? nada realmente")
            continue
        elif "adiós" in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            comenzar = False
        
pedir_cosas()