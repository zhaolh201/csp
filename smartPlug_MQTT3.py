'''
Created on 4 juillet 2022

@author: Lihua Zhao
Référence: https://support.asplhosting.com/t/working-myqtthub-com-python-paho-examples/43
'''
from RPiSim import GPIO
import paho.mqtt.client as mqtt
import time
import sys
import signal
import pymongo
from datetime import datetime

def terminer(signum, frame):
    print("Terminer")
    GPIO.output(18, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    GPIO.cleanup()
    sys.exit(0)


def on_alarm_message(client, userdata, message):
    global collection
    print("alarm received message: " , str(message.payload.decode("utf-8")))
    commande = str(message.payload.decode("utf-8"))
    if commande == "on":
        print("Alarm: Arme")
        client.publish("Alarm/Etats", "Arme")
        unEventRecord = {"date": datetime.now().strftime('%y/%m/%d'),
                        "heure": datetime.now().strftime('%H:%M:%S'),
                        "event": "Alarme:ARME"}
        collection.insert_one(unEventRecord)
    elif commande == "off":
        print("Alarm: Disarme")
        client.publish("Alarm/Etats", "Disarme")
        unEventRecord = {"date": datetime.now().strftime('%y/%m/%d'),
                         "heure": datetime.now().strftime('%H:%M:%S'),
                         "event": "Alarme:DISARME"}
        collection.insert_one(unEventRecord)

def on_light_enter_message(client, userdata, message):
    print("light enter received message: ", str(message.payload.decode("utf-8")))
    commande = str(message.payload.decode("utf-8"))
    if commande == "on":
        GPIO.output(17, GPIO.HIGH)
        print("Light enter On")
        client.publish("LightEnter/Etats", "on")
        unEventRecord = {"date": datetime.now().strftime('%y/%m/%d'),
                         "heure": datetime.now().strftime('%H:%M:%S'),
                         "event": "Lumiere entree:ON"}
        collection.insert_one(unEventRecord)
    elif commande == "off":
        GPIO.output(17, GPIO.LOW)
        print("Light enter Off")
        client.publish("LightEnter/Etats", "off")
        unEventRecord = {"date": datetime.now().strftime('%y/%m/%d'),
                         "heure": datetime.now().strftime('%H:%M:%S'),
                         "event": "Lumiere entree:OFF"}
        collection.insert_one(unEventRecord)

def on_light_salon_message(client, userdata, message):
    print("light enter received message: " , str(message.payload.decode("utf-8")))
    commande = str(message.payload.decode("utf-8"))
    if commande == "on":
        GPIO.output(18, GPIO.HIGH)
        print("Light salon On")
        client.publish("LightSalon/Etats", "on")
        unEventRecord = {"date": datetime.now().strftime('%y/%m/%d'),
                         "heure": datetime.now().strftime('%H:%M:%S'),
                         "event": "Lumiere salon:ON"}
        collection.insert_one(unEventRecord)
    elif commande == "off":
        GPIO.output(18, GPIO.LOW)
        print("Light salon Off")
        client.publish("LightSalon/Etats", "off")
        unEventRecord = {"date": datetime.now().strftime('%y/%m/%d'),
                         "heure": datetime.now().strftime('%H:%M:%S'),
                         "event": "Lumiere salon:OFF"}
        collection.insert_one(unEventRecord)

""" Les GPIO  """
signal.signal(signal.SIGINT, terminer)
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    """ Lumière """
    GPIO.setup(17, GPIO.MODE_OUT, initial=GPIO.LOW)
    GPIO.setup(18,GPIO.MODE_OUT, initial=GPIO.LOW)
except Exception:
    print("Problème avec les GPIO")

""" MQTT """
host          = "node02.myqtthub.com"
port          = 1883
clean_session = True
alarmClient_id     = "systemAlarm"
light_enter_client_id     = "lampEnter"
light_salon_client_id     = "lampSalon"
user_name     = "zhaolh201"
password      = "test1234"

dbclient = pymongo.MongoClient("localhost")
db = dbclient.project1 # La base de donnée project 1
collection = db.eventrecord


alarmClient = mqtt.Client(client_id = alarmClient_id, clean_session = clean_session)
alarmClient.username_pw_set (user_name, password)
alarmClient.connect (host, port)

light_enter_client = mqtt.Client(client_id = light_enter_client_id, clean_session = clean_session)
light_enter_client.username_pw_set (user_name, password)
light_enter_client.connect (host, port)

light_salon_client = mqtt.Client(client_id = light_salon_client_id, clean_session = clean_session)
light_salon_client.username_pw_set (user_name, password)
light_salon_client.connect (host, port)

alarmClient.loop_start()
alarmClient.subscribe("Alarm/Commandes")
alarmClient.on_message=on_alarm_message

light_enter_client.loop_start()
light_enter_client.subscribe("LightEnter/Commandes")
light_enter_client.on_message=on_light_enter_message

light_salon_client.loop_start()
light_salon_client.subscribe("LightSalon/Commandes")
light_salon_client.on_message=on_light_salon_message

while True:
    time.sleep(0.5)
    
