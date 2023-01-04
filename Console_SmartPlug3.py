'''
Created on 4 juillet 2022

@author: Lihua Zhao
Référence: https://support.asplhosting.com/t/working-myqtthub-com-python-paho-examples/43
'''
from tkinter import *
import paho.mqtt.client as mqtt 
import pymongo

""" Quitter proprement """
def fermer():
    print("Quitter proprement")
    alarmClient.loop_stop()
    alarmClient.disconnect()

    light_enter_client.loop_stop()
    light_enter_client.disconnect()
    
    light_salon_client.loop_stop()
    light_salon_client.disconnect()

    fen1.destroy()

def cmd_alarm_on():
    alarmClient.publish("Alarm/Commandes", "on")


def cmd_alarm_off():
    alarmClient.publish("Alarm/Commandes", "off")

def cmd_light_enter_on():
    light_enter_client.publish("LightEnter/Commandes", "on")

def cmd_light_enter_off():
    light_enter_client.publish("LightEnter/Commandes", "off")

def cmd_light_salon_on():
    light_salon_client.publish("LightSalon/Commandes", "on")

def cmd_light_salon_off():
    light_salon_client.publish("LightSalon/Commandes", "off")
    
def on_alarm_Message(client, userdata, message):
    print("alarm received message: " ,str(message.payload.decode("utf-8")))
    alarmEtat.configure(text=str(message.payload.decode("utf-8")))
    if handle['control']==0:
    	history_update()

def on_light_enter_message(client, userdata, message):
    print("light enter received message: " ,str(message.payload.decode("utf-8")))
    lightEnterEtat.configure(text=str(message.payload.decode("utf-8")))
    if handle['control']==0:
        history_update()

def on_light_salon_message(client, userdata, message):
    print("light salon received message: " ,str(message.payload.decode("utf-8")))
    lightSalonEtat.configure(text=str(message.payload.decode("utf-8")))
    if handle['control']==0:
        history_update()

def history_update():
    global recordframe
    global collection
    resultstr = ''
    #datarecords = [{'date': '22/06/29', 'heure': '20:45:30', 'event': 'Lumiere Salon:OFF'},
    #               {'date': '22/06/29', 'heure': '03:45:30', 'event': 'Alarme:ARME'},
    #               {'date': '22/06/30', 'heure': '22:45:30', 'event': 'Lumiere Entree:ON'}]
    #for item in datarecords:
    recordsum = len(list(collection.find()))
    if recordsum >= 20:
        for item in collection.find().skip(recordsum-20):
            resultstr += item['date'] + '    ' + item['heure'] + '    ' + item['event'] + '\n'
    else:
        for item in collection.find():
            resultstr += item['date'] + '    ' + item['heure'] + '    ' + item['event'] + '\n'
        for i in range(20 - recordsum):
            resultstr += '\n'
    resultlabel = Label(recordframe, text=resultstr, font="Helvetica 16", justify='left')
    resultlabel.grid(row=2, column=0)

def history_close():
    global handle
    global history
    handle['control']=1
    history.destroy()

def history_onclick():
    global recordframe
    global handle
    global history
    if handle['control']:
        history = Toplevel()
        history.protocol("WM_DELETE_WINDOW", history_close)
        recordframe = LabelFrame(history)
        recordframe.grid(row=0, column=0, padx=20, pady=10)
        titlelabel = Label(recordframe, text='Date    Heure    Evennement', font="Helvetica 18 bold")
        titlelabel.grid(row=0,column=0)
        signlabel = Label(recordframe,  text='===========================', font="Helvetica 18 bold")
        signlabel.grid(row=1,column=0)
        history_update()
        exitbtn = Button(history, text="Quitter", font="Helvetica 18 bold", command=history_close)
        exitbtn.grid(row=1,column=0)
        handle['control'] = 0

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

handle = {}
handle['control'] = 1

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

alarmClient.subscribe("Alarm/Etats")
alarmClient.on_message=on_alarm_Message

light_enter_client.loop_start()

light_enter_client.subscribe("LightEnter/Etats")
light_enter_client.on_message=on_light_enter_message

light_salon_client.loop_start()

light_salon_client.subscribe("LightSalon/Etats")
light_salon_client.on_message=on_light_salon_message

""" Interface Tk """
fen1 = Tk()
fen1.protocol("WM_DELETE_WINDOW", fermer)


alarmFrame = LabelFrame(fen1, text='Alarme', font="Helvetica 20 bold",padx=10, pady=10)
alarmFrame.pack(padx=10, pady=10)
alarmONBtn = Button(alarmFrame, text='ON', font="Helvetica 18 bold", command = cmd_alarm_on)
alarmONBtn.grid(row=0, column=0)
alarmOFFBtn = Button(alarmFrame, text='OFF', font="Helvetica 18 bold", command = cmd_alarm_off)
alarmOFFBtn.grid(row=0, column=1)
alarmEtat = Label(alarmFrame, text="Etat", fg='red', font="Helvetica 18 bold",padx=20,width=10)
alarmEtat.grid(row = 0, column = 2)

lightEnterFrame = LabelFrame(fen1, text='Lumiere entree', font="Helvetica 20 bold",padx=10, pady=10)
lightEnterFrame.pack(padx=10, pady=10)
lightEnterONBtn = Button(lightEnterFrame, text='ON', font="Helvetica 18 bold", command = cmd_light_enter_on)
lightEnterONBtn.grid(row=0, column=0)
lightEnterOFFBtn = Button(lightEnterFrame, text='OFF', font="Helvetica 18 bold", command = cmd_light_enter_off)
lightEnterOFFBtn.grid(row=0, column=1)
lightEnterEtat = Label(lightEnterFrame, text="Etat", fg='red', font="Helvetica 18 bold",padx=20,width=10)
lightEnterEtat.grid(row = 0, column = 2)

lightSalonFrame = LabelFrame(fen1, text='Lumiere salon', font="Helvetica 20 bold",padx=10, pady=10)
lightSalonFrame.pack(padx=10, pady=10)
lightSalonONBtn = Button(lightSalonFrame, text='ON', font="Helvetica 18 bold", command = cmd_light_salon_on)
lightSalonONBtn.grid(row=0, column=0)
lightSalonOFFBtn = Button(lightSalonFrame, text='OFF', font="Helvetica 18 bold", command = cmd_light_salon_off)
lightSalonOFFBtn.grid(row=0, column=1)
lightSalonEtat = Label(lightSalonFrame, text="Etat", fg='red', font="Helvetica 18 bold",padx=20,width=10)
lightSalonEtat.grid(row = 0, column = 2)

historyFrame = LabelFrame(fen1, text='Historique', font="Helvetica 20 bold",padx=10, pady=10)
historyFrame.pack(padx=10, pady=10,anchor=W)
historyBtn = Button(historyFrame, text='Afficher', font="Helvetica 18 bold", command=history_onclick)
historyBtn.grid(row=0, column=0)



fen1.mainloop()
