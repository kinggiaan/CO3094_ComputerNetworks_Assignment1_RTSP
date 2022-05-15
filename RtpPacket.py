import sys
from time import time
HEADER_SIZE = 12

class RtpPacket:	
	header = bytearray(HEADER_SIZE)
	
	def __init__(self):
		pass
		
	def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
	#TODO Trung Black
		"""Encode the RTP packet with header fields and payload."""
		timestamp = int(time())
		header = bytearray(HEADER_SIZE)
		#--------------
		# TO COMPLETE
		#--------------
		# Fill the header bytearray with RTP header fields
		
		# header[0] = ...
		# ...
		
		# Get the payload from the argument
		# self.payload = ...
		
		# self, V = 2, P = 0, X = 0, CC = 0, seqnum = frameNbr, M = 0, PT = 26, SSRC = 0, payload = payload
		# To set bits n and n + 1 to the value of foo in variable mybyte:
        #               mybyte = mybyte | foo << (7 - n)
        # To copy a 16-bit integer foo into 2 bytes, b1 and b2:
        #               b1 = (foo >> 8) & 0xFF: 8 high-order bits
        #               b2 = foo & 0xFF       : 8 low-order bits

        # Fill the header bytearray with RTP header fields
        # header[0] = (header[0] | version << 6) & 0xC0  	# 2 bits: V
        #                         # version << 6 (= VV-00 0000) and 0xC0 (= 1100 0000)
		header[0] = header[0] | version << 6 	        # 2 bits: V
						# version << 6 (= VV-00 0000)
		header[0] = header[0] | padding << 5  		# 1 bit:  P
						# padding << 5 (= 00-P-0 0000)
		header[0] = header[0] | extension << 4  		# 1 bit:  X
						# extension << 4 (= 000-X 0000)
		header[0] = header[0] | (cc & 0x0f)  			# 4 bits: CC
						# cc (= 0000 0000) & 0x0F (= 0000 1111) = 0000 CCCC
		header[1] = header[1] | marker << 7  			# 1 bit:  M
						# marker << 7 (= M-000 0000)
		header[1] = header[1] | (pt & 0x7f)  			# 7 bits: PT
						# pt (= 0001 1010) & 0x7f (= 0111 1111)
						# rs = 0001 1010
		header[2] = seqnum >> 8  			            # 16 bits in total: sequence number
		header[3] = seqnum & 0xff  					    # ./
		header[4] = timestamp >> 24  					# 32 bit in total: timestamp
		header[5] = (timestamp >> 16) & 0xff            # .
		header[6] = (timestamp >> 8) & 0xff             # .
		header[7] = (timestamp & 0xff)                  # ./
		header[8] = (ssrc >> 24)  						# 32 bit SSRC
		header[9] = (ssrc >> 16) & 0xff                 # .
		header[10] = (ssrc >> 8) & 0xff                 # .
		header[11] = ssrc & 0xff                        # ./

		self.header = header

		# Get the payload from the argument
		self.payload = payload

	def decode(self, byteStream):
		"""Decode the RTP packet."""
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]
	
	def version(self):
		"""Return RTP version."""
		return int(self.header[0] >> 6)
	
	def seqNum(self):
		"""Return sequence (frame) number."""
		seqNum = self.header[2] << 8 | self.header[3]
		return int(seqNum)
	
	def timestamp(self):
		"""Return timestamp."""
		timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
		return int(timestamp)
	
	def payloadType(self):
		"""Return payload type."""
		pt = self.header[1] & 127
		return int(pt)
	
	def getPayload(self):
		"""Return payload."""
		return self.payload
		
	def getPacket(self):
		"""Return RTP packet."""
		return self.header + self.payload