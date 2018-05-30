import asyncio
import random as rand
from threading import Thread
import os
import discord
import ftplib as ftp
import time


def connect_to_ftp(host, username, pswd) :
	return ftp.FTP(host, username, pswd)	

ftp_co = connect_to_ftp("tornadoprojects.co.nf", "2740733", "Happy_59173")
if ftp_co.getwelcome() :
		ftp_co.cwd("tornadoprojects.co.nf")
		print("Connexion FTP initialisée")


def getCurrentDir() :
	return os.path.dirname(os.path.abspath(__file__))

def sendfileFTP(file) :
	filename = "list.txt"
	if ftp_co.storbinary("STOR {}".format(filename), file) :
		return True
	else :
		return False


def deleteCode(pin) :	
	time.sleep(20)
	with open(getCurrentDir()+"\\list.txt", 'r') as f:
		lines = f.readlines()
	with open(getCurrentDir()+"\\list.txt", 'w') as f:
		for line in lines:
			if line!=str(pin)+"\n":
				f.write(line)

	with open(getCurrentDir()+"\\list.txt", "rb") as file :
		sendfileFTP(file)



def storePin(pin) :
	with open(getCurrentDir()+"\\list.txt", 'a') as f:
		f.write(str(pin)+"\n")


	with open(getCurrentDir()+"\\list.txt", "rb") as file :
		if sendfileFTP(file) :
			t1 = Thread(target=deleteCode, args=(pin,))
			t1.deamon = True
			t1.start()
			return True
		else : 
			return False

client = discord.Client()



@client.event
async def on_ready() :
	print("Logged as : {} - {}".format(client.user.name, client.user.id))
	
	
@client.event
async def on_message(message) :
	msg = message.content.upper()
	if msg.startswith(".") :
		cmd = msg.split(".")[1].lstrip(" ")

		if cmd == "HELP" :
			response = """**Commande du Bot** : \n
			- .pin : Génère un nombre aléatoire à 4 chiffres 
				"""
			await client.send_message(message.channel, response)

		elif cmd == "PIN" : 
			pin = rand.randint(1000, 9999)
			response =  "<@{}> Votre code PIN est {}".format(message.author.id, pin)

			# try :
			if storePin(pin) :
				await client.send_message(message.channel, response)
			
			# except Exception :
			# 	ftp_co.quit()
			# 	print("Le serveur FTP a été quitté suite à une erreur")
				
		elif cmd == 'QUIT' :
			await client.logout()
			await client.close()

client.run("")