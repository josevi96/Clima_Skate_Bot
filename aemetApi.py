import requests
import http.client
import ssl
import json

import telebot # Librería de la API del bot.
from telebot import TeleBot 
import time # Librería para hacer que el programa que controla el bot no se acabe.


context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
conn = http.client.HTTPSConnection("opendata.aemet.es", context = context)
    
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqb3NldmlnYXJjaWE5NkBnbWFpbC5jb20iLCJqdGkiOiI0MDkyNDkzZi1mMDEzLTRhYTAtOWYyZS03M2Y2NmFhMzQzMjUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU0Mjc5ODI1MCwidXNlcklkIjoiNDA5MjQ5M2YtZjAxMy00YWEwLTlmMmUtNzNmNjZhYTM0MzI1Iiwicm9sZSI6IiJ9.qfnZwyeTjU-G-pooGDRTDVne-jNYwujiURZ56grYDT4"

headers = {
    'cache-control': "no-cache"
}

token_file = open("token.txt","r")
bot_token =
#token_file.read()
mi_bot = telebot.TeleBot(token = bot_token)


#-------------------------------------BOT MENSAJES-------------------------------------#


@mi_bot.message_handler(commands=['start'])
def welcome(message):
    mi_bot.reply_to(message,"bienvenido, gracias por usar este bot")

@mi_bot.message_handler(commands=['help'])
def help(message):
    mi_bot.reply_to(message,"lista de ")

@mi_bot.message_handler(commands=['probeta'])
def clima_sanagus(message):
    url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28129"
    conn.request("GET", f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28129?api_key={api_key}", headers=headers, )
    res = conn.getresponse()
    data = res.read().decode('utf-8','ignore')
    data = json.loads(data)
    extraer_json(data,message)

    
@mi_bot.message_handler(commands=['nepal'])
def clima_alcobendas(message):
    url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28006"
    conn.request("GET", f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28129?api_key={api_key}", headers=headers, )
    res = conn.getresponse()
    data = res.read().decode('utf-8','ignore')
    data = json.loads(data)
    extraer_json(data,message)


@mi_bot.message_handler(commands=['3cantos'])
def clima_3cantos(message):
    url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28903"
    conn.request("GET", f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28129?api_key={api_key}", headers=headers, )
    res = conn.getresponse()
    data = res.read().decode('utf-8','ignore')
    data = json.loads(data)
    extraer_json(data,message)


@mi_bot.message_handler(commands=['tetuan','rio','escombro'])
def clima_Madrid(message):
    url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28079"
    conn.request("GET", f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28129?api_key={api_key}", headers=headers, )
    res = conn.getresponse()
    data = res.read().decode('utf-8','ignore')
    data = json.loads(data)
    extraer_json(data,message)

    
def extraer_json(data,message):
    conn.request("GET", data['datos'], headers=headers, )
    res= conn.getresponse()
    datos = res.read().decode('utf-8','ignore')
    datos= json.loads(datos)
    for x in datos:
        dias = x['prediccion']['dia']
        cont = 1
        for d in dias:
            precipitacion = d['probPrecipitacion']
            r = parse(precipitacion)
            if cont == 1:
                mi_bot.reply_to(message,f"Hoy \n {r}")
                cont = cont + 1
            elif cont == 2:
                mi_bot.reply_to(message,f"Mañana \n {r}")
                cont = cont + 1
            else:
                mi_bot.reply_to(message,f"Pasado  Mañana \n {r}")


def parse(precipitacion):
    cadena =""
    for par in precipitacion:
        if par['value'] != "":
            cadena = cadena+f"Precipitacion:{par['value']}%, horas: {par['periodo']}"+"\n"
    return cadena
                    
while True:
    try:
        mi_bot.polling()
    except Exception:
        time.sleep(15)

        
