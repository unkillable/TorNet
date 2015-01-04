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
from stem import Signal
from stem.control import Controller
def receive(s,channel):
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
			print channel
			sData = data.split(" PRIVMSG "+channel+" :")[1].strip()
			if sData.startswith(".join "):
				shit, channel = msg.split(".join ")   
				s.send("JOIN " + channel + "\r\n")       
			if sData.startswith(".penis"):
				s.send('PRIVMSG ' + channel + ' :IM GAY :^)\r\n')   
			if sData.startswith(".say "):
				try:
					p = msg.split(".say ")[1].strip()
					s.send('PRIVMSG ' + channel + ' :' + p +'\r\n')   
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
def Soldier():
	nick = "R" + str(random.randint(0, 10000))
	server = "irc.tm"
	port = 6667
	channel = "#raid"
	#Connect to irc server
	s = socks.socksocket()
	s.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
	s.connect(("irc.tm",6667))
	s.send("NICK " + nick + "\r\n")
	s.send("USER " + nick + " " + nick + " " + nick + " "+nick+"\r\n")
	receive(s,channel)
threads = []
def NewTorIP():
	with Controller.from_port(port = 9051) as controller:
		controller.authenticate()
		controller.signal(Signal.NEWNYM)
oldIP = "0.0.0.0"
newIP = "0.0.0.0"
for n in range(2):
	thread = threading.Thread(target=Soldier)
	thread.start()
	threads.append(thread)
	NewTorIP()
	time.sleep(5)
	print "bot started"
print "Waiting..."

for thread in threads:
    thread.join()

print "Complete."
print "stated"
