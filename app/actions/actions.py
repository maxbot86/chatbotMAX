# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
# Custom Libs - Libs =========
import smtplib
import pyodbc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv, dotenv_values 
# =============================
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


v = ''
#===ENV VARS = ===================
load_dotenv()
dominio = os.getenv("DOMINIO")
mail_soporte = os.getenv("MAIL_TICKETERA")
smtp_server_env = os.getenv("SMTP_SERVER")

db_driver = os.getenv("DB_DRIVER")
db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")
db_uid = os.getenv("DB_UID")
db_pwd = os.getenv("DB_PWD")
# =============================
#  Custom Functions

def enviar_correo(cuenta_origen, subject, body, cuenta_destino=mail_soporte, smtp_server=smtp_server_env, smtp_port=25):
    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = cuenta_origen
    msg['To'] = cuenta_destino
    msg['Subject'] = subject

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conectar al servidor SMTP
        server = smtplib.SMTP(smtp_server)
        # Enviar el correo
        server.sendmail(cuenta_origen, cuenta_destino, msg.as_string())
        print(f"Correo enviado correctamente a {cuenta_destino}")
        result = True
        server.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        result = False
    return result

def remove_words(text, words_to_remove):
    text = text.lower()
    text = text.split(" ")
    for n in words_to_remove:
        text = list(filter((n.lower()).__ne__, text))
    return text

def convertSearchQuery(arr_words):
    qry_str = "SELECT id, question,answer,"
    qry_str +="((("
    filtro=""
    for wd in arr_words:
        filtro+="(CASE WHEN LOWER(question) LIKE '%"+wd+"%' THEN 1 ELSE 0 END) +"
    qry_str += filtro[0:-1]
    qry_str +=")*100)/"+str(len(arr_words))+") AS match_perc"
    qry_str +=" FROM faq ORDER BY match_perc DESC"
    print(qry_str)
    return qry_str

#  RASA - Actions Class =============================
class ActionHelloWorld(Action):
#
    def name(self) -> Text:
        return "action_hello_world"
#
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hola "+str(tracker.sender_id)+" , en que puedo ayudarte?")

        return []

class ActionSayGoodBye(Action):
#
    def name(self) -> Text:
        return "action_goodbye"
#
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hasta luego "+str(tracker.sender_id)+" , espero haberte ayudado. Ya sabes donde encontrarme.")

        return []

class ActionDecideSoporte(Action):
#
    def name(self) -> Text:
        return "action_decide_soporte"
#
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         # Acceder al último mensaje del usuario

        last_message = tracker.latest_message.get('text')

        print(last_message)
        if "remoto" in last_message.lower() :
            dispatcher.utter_message(text="Perfecto ,con que estaria necesitando ayuda?")
        else:
            #enviar mail a soporteti de alguna otra forma informar
            r = enviar_correo(str(tracker.sender_id)+'@'+dominio, "Solicitud de soporte presencial - (Generado por CHATBOT)", "Se solicita que un tecnico se acerque en persona al escritorio.")
            if r:
                dispatcher.utter_message(text="Ok "+str(tracker.sender_id)+", se cargo un ticket, alguien se estara acercando a su escritorio a la brevedad.")
            else:
                dispatcher.utter_message(text="Hubo un error al generar el ticket, por favor solicite soporte via TEAMS.")

        return []

class ActionAnswerFAQ(Action):
#
    def name(self) -> Text:
        return "action_answer_faq"
#
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obtener la última pregunta del usuario
        global v        
        user_message = tracker.latest_message.get('text')
        eliminar_char = {'que','cual','cuando','donde','como','con','hasta','a','desde','alla','el','la','con', 'de', '?','¡','!'}
        arra_keyWords = remove_words(user_message,eliminar_char)
        query = convertSearchQuery(arra_keyWords)
        #recuepero de la base de datos las respuestas a la pregunta que hizo el usuario
        try:
            # ===  Connnect to DB
            str_conn = (
                "DRIVER={"
                +db_driver
                +"};SERVER="
                +db_server
                +";DATABASE="
                +db_name
                + ";UID="
                + db_uid
                + ";PWD="
                + db_pwd
            )
            conexion = pyodbc.connect(str_conn)
            print("CONECTADO DB")
            cursor = conexion.cursor()
            cursor.execute(query)
            print("QUERY EJECUTADO")
            try:
                v = cursor.fetchone()
                print(v)
                answer = v[2]
                print("Hay una respuesta")
            except:
                answer = "Creo que tengo una respuesta para eso..."
            # =================================================
            
            
        except:
            answer = "Lo siento , estamos teniendo problemas tecnicos, por favor comuniquese via TEAMS."

        dispatcher.utter_message(text=answer)

        return []