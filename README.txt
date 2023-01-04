#project1

#Console_SmartPlug3.py

```bash
fonction:créate les fênetres de "Ma console" et "Historique",créate la base de donnée project1 et collection est eventrecord,connecter le serveur mqtt,etc
```

définier les fonctions:fermer--pour fermer l'affichage d'historique

cmd_alarm_on,cmd_alarm_off,cmd_light_enter_on,cmd_light_enter_off,cmd_light_salon_on,cmd_light_salon_off--commandes

on_alarm_Message,on_light_enter_message,on_light_salon_message--changer l'état par appuyer les boutons et update le database

history_update--pour afficher 20 dernières recordes
history_close--pour fermer l'affichage
history_onclick--pour créate la fenêtre de l'affichage et montrer les recordes

#MQTT

protocole:node02.myqtthub.com

serveur:MongoDB

créate database sur pymongo 

créate le protocole pour communiquer mqtt et envoyer des messages

subscribe pour recever des messages 

#Tkinter

créate GUI de "Ma console"

#fin


#smartPlug_MQTT3.py

```bash
fonction:créate smartPlug GPIO.output 17 et GPIO.output 18 répresente lumière enter et lumière salon, écrire la base de donnée project1, communiquer mqtt pour les controler
```

créate les fonctions: terminer--l'entête de tkinter pour fermer la fenêtre
on_alarm_message,on_light_enter_message,on_light_salon_message--controler GPIO 17 et 18 les output résultats et écrire la base de donnée 

gerer l'exceptions

#MQTT

protocole:node02.myqtthub.com

serveur:MongoDB

créate database sur pymongo

créate le protocole pour communiquer mqtt et envoyer des messages

subscribe pour recever des messages

## Reference
Beginners Guide To The Paho MQTT Python Client
http://www.steves-internet-guide.com/into-mqtt-python-client/

How to use MQTT in Python (Paho)
https://www.emqx.io/blog/how-to-use-mqtt-in-python

MQTT Beginners Guide
https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4

DELETE eventrecord:
mongo->show dbs->use project1->show collections->db.dropDatabase()




