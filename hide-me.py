#!/usr/bin/env python3

####################################################################################
# hide-me - this script will change the mac address to a random one                #
# and will pick a random hostname from specified file                              #
# Requirements: macchanger needs to be installed                                   #
# Written by: Andrei Zgirvaci                                                      #
# Github: https://github.com/MD3XTER/                                              #
####################################################################################

__name__ = "hide-me"

import sys

def usage():
	print ("\n"+__name__+"\n")
	print ("usage: "+__name__+" device [file_location]\n")
	print ("Try "+__name__+" -h for more options.\n")
	exit()

def help():
	print ("\n"+__name__+"\n")
	print ("usage: "+__name__+" device [file]\n\n")
	print ("  -h, --help       Print this help\n")
	print ("  [file_location]  Indicate file location with hostnames\n")
	print ("  quit             Retrieve changes to original\n")
	print ("\nReport bugs to https://github.com/MD3XTER/"+__name__+"/issues.\n")
	exit()

total = len(sys.argv)

if total == 3:

	import os
	import subprocess

	def error():
		print ("Script encounter an error, sorry...\n")
		exit()

	def interfaceup(interface):
		if not subprocess.call(["ifconfig "+interface+" up"], shell=True):
			subprocess.call(["service network-manager restart"], shell=True)
			print ("Interface should be up!!!\n")
		else:
			error()

	def hostname():
		tmphost = str(subprocess.check_output("hostname", shell=True)[:-1])
		tmphost = tmphost[1:]
		tmphost = tmphost.replace("'", "")
		return tmphost

	def change(interface):
		#changing mac address to a random one
		print ("\nChanging mac addres... \n")
		subprocess.call(["macchanger -A "+interface], shell=True)

		#changing hostname to a random line from file
		print ("\nChanging Hostname...\n")
		print ("Previus Hostname: "+hostname())
		subprocess.call(["hostname "+line], shell=True)
		print ("Current Hostname: "+hostname()+"\n")

		#putting interface up
		interfaceup(interface)

	def retrieve(interface, oldhost):
		#change mac addres back to original one
		print ("\nChanging macc addres to permanent one...\n")
		subprocess.call(["ifconfig "+interface+" down"], shell=True)
		subprocess.call(["macchanger -p "+interface], shell=True)

		#change hostname back to original one
		print ("\nRetrieving hostname to original...\n")
		subprocess.call(["hostname "+oldhost], shell=True)
		print ("Hostname changed to: "+hostname()+"\n")

		#putting interface up
		interfaceup(interface)

	#check if interface exists
	checkINTERFACE = str(os.listdir('/sys/class/net/'))
	if str(sys.argv[1]) in checkINTERFACE:

		#declare interface
		interface = str(sys.argv[1])

		if os.path.isfile(str(sys.argv[2])):
			#pick a random line from file
			import random
			lines = open(str(sys.argv[2])).read().splitlines()
			line = random.choice(lines)
		else:
			print ("\n"+__name__+"\n")
			print ("usage: "+__name__+" device [file_location]\n")
			print ("File does not exist.")
			print ("Try "+__name__+" -h for more options.\n")
			exit()

		if not subprocess.call(["ifconfig "+interface+" down"], shell=True):

			oldhost = hostname()

			#change mac addres and hostname
			change(interface)

			#whait for 'quit' input
			while True:
				var = input("Type 'quit', to retrieve changes to original: ")
				if var == "quit":
					break

			#Retrieve changes
			retrieve(interface, oldhost)

		else:
			error()
	else:
		print ("\n"+__name__+"\n")
		print ("[ERROR] Set device name: No such device.\n")
		print ("Try "+__name__+" -h for more options.\n")
		exit()

elif total == 2:
	if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
		help()
	else:
		usage()
else:
	usage()