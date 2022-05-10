from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
import socket, threading, sys, traceback, os

from RtpPacket import RtpPacket

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

class Client:
	INIT = 0
	READY = 1
	PLAYING = 2
	state = INIT
	
	SETUP = 0
	PLAY = 1
	PAUSE = 2
	TEARDOWN = 3
	
	# Initiation..
	def __init__(self, master, serveraddr, serverport, rtpport, filename):
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.handler)
		self.createWidgets()
		self.serverAddr = serveraddr
		self.serverPort = int(serverport)
		self.rtpPort = int(rtpport)
		self.fileName = filename
		self.rtspSeq = 0
		self.sessionId = 0
		self.requestSent = -1
		self.teardownAcked = 0
		self.connectToServer()
		self.frameNbr = 0
		
	# THIS GUI IS JUST FOR REFERENCE ONLY, STUDENTS HAVE TO CREATE THEIR OWN GUI 	
	def createWidgets(self):
		"""Build GUI."""
		# Create Setup button
		self.setup = Button(self.master, width=20, padx=3, pady=3)
		self.setup["text"] = "Setup"
		self.setup["command"] = self.setupMovie
		self.setup.grid(row=1, column=0, padx=2, pady=2)
		
		# Create Play button		
		self.start = Button(self.master, width=20, padx=3, pady=3)
		self.start["text"] = "Play"
		self.start["command"] = self.playMovie
		self.start.grid(row=1, column=1, padx=2, pady=2)
		
		# Create Pause button			
		self.pause = Button(self.master, width=20, padx=3, pady=3)
		self.pause["text"] = "Pause"
		self.pause["command"] = self.pauseMovie
		self.pause.grid(row=1, column=2, padx=2, pady=2)
		
		# Create Teardown button
		self.teardown = Button(self.master, width=20, padx=3, pady=3)
		self.teardown["text"] = "Teardown"
		self.teardown["command"] =  self.exitClient
		self.teardown.grid(row=1, column=3, padx=2, pady=2)
		
		# Create a label to display the movie
		self.label = Label(self.master, height=19)
		self.label.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=5, pady=5) 
	
	def setupMovie(self):
		"""Setup button handler."""
	#TODO An
	
	def exitClient(self):
		"""Teardown button handler."""
	#TODO An

	def pauseMovie(self):
		"""Pause button handler."""
	#TODO An
	
	def playMovie(self):
		"""Play button handler."""
	#TODO An
	
	def listenRtp(self):		
		"""Listen for RTP packets."""
		#TODO An 
					
	def writeFrame(self, data):
		"""Write the received frame to a temp image file. Return the image file."""
	#TODO An
	
	def updateMovie(self, imageFile):
		"""Update the image file as video frame in the GUI."""
	#TODO An
		
	def connectToServer(self):
		"""Connect to the Server. Start a new RTSP/TCP session."""
	#TODO An
	
	def sendRtspRequest(self, requestCode):
	#TODO An
		"""Send RTSP request to the server."""	
		#-------------
		# TO COMPLETE
		#-------------
		
	
	
	def recvRtspReply(self):
		"""Receive RTSP reply from the server."""
		#TODO Nguyen
		while True:
			reply = self.rtspSocket.recv(1024)
			
			if reply: 
				self.parseRtspReply(reply)
			
			# Close the RTSP socket upon requesting Teardown
			if self.requestSent == self.TEARDOWN:
				self.rtspSocket.shutdown(socket.SHUT_RDWR)
				self.rtspSocket.close()
				break
				
	def parseRtspReply(self, data):
		"""Parse the RTSP reply from the server."""
		#TODO Nguyen
		
		print ("Parsing Received Rtsp data...")

		lines = data.split('\n')
		seqNum = int(lines[1].split(' ')[1])

		# Process only if the server reply's sequence number is the same as the request's
		if seqNum == self.rtspSeq:
			session = int(lines[2].split(' ')[1])
			# New RTSP session ID
			if self.sessionId == 0:
				self.sessionId = session

			# Process only if the session ID is the same
			if self.sessionId == session:
				if int(lines[0].split(' ')[1]) == 200:
					if self.requestSent == self.SETUP:
						
						#-------------
						# TO COMPLETE
						#-------------
						# Update RTSP state.
						
						print ("Updating RTSP state...")
						# self.state = ...
						self.state = self.READY
						
						# Open RTP port.
						#self.openRtpPort()
						print ("Setting Up RtpPort for Video Stream")
						self.openRtpPort()

					elif self.requestSent == self.PLAY:
						 self.state = self.PLAYING
						 print ('-'*60 + "\nClient is PLAYING...\n" + '-'*60)
					elif self.requestSent == self.PAUSE:
						 self.state = self.READY

						# The play thread exits. A new thread is created on resume.
						 self.playEvent.set()

					elif self.requestSent == self.TEARDOWN:
						self.state = self.INIT

						# Flag the teardownAcked to close the socket.
						self.teardownAcked = 1
	def openRtpPort(self):
		#TODO Nguyen
		"""Open RTP socket binded to a specified port."""
		#-------------
		# TO COMPLETE
		#-------------
		# Create a new datagram socket to receive RTP packets from the server
		# self.rtpSocket = ...
		elf.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		# Set the timeout value of the socket to 0.5sec
		# ...
		self.rtpSocket.settimeout(0.5)
		
#		try:
			# Bind the socket to the address using the RTP port given by the client user
			# ...
#		except:
#			tkMessageBox.showwarning('Unable to Bind', 'Unable to bind PORT=%d' %self.rtpPort)

		try:
			#self.rtpSocket.connect(self.serverAddr,self.rtpPort)
			self.rtpSocket.bind((self.serverAddr,self.rtpPort))   # WATCH OUT THE ADDRESS FORMAT!!!!!  rtpPort# should be bigger than 1024
			#self.rtpSocket.listen(5)
			print ("Bind RtpPort Success")

		except:
			tkMessageBox.showwarning('Connection Failed', 'Connection to rtpServer failed...')

	def handler(self):
		"""Handler on explicitly closing the GUI window."""
		#TODO Nguyen
		self.pauseMovie()
		if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
			self.exitClient()
		else: # When the user presses cancel, resume playing.
			#self.playMovie()
			print ("Playing Movie")
			threading.Thread(target=self.listenRtp).start()
			#self.playEvent = threading.Event()
			#self.playEvent.clear()
			self.sendRtspRequest(self.PLAY)
