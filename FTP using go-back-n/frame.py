# import libraries
import random
import time
import socket
import crc16
# Define the frame (PDU) structure by yourself.
# A checksum field needs to be added at the end of the PDU. checksum uses
# CRC-CCITT standard. The start and end identifiers of the frame can be ignored.


class PDU:
    def __init__(self, seq_num, data=b''):
        self.seq = seq_num
        self.data = data
        self.crc = crc16.crc16xmodem(data)
        self.start_time = -1

    def __str__(self):
        return "PDU"


# UDT packet
class UDT:
    def __init__(self, lost, err):
        random.seed(time.time())  # random seed
        self.LOST_PROB = lost  # set lost prob and err prbo
        self.ERR_PROB = err
    # Send a packet across the unreliable channel
    # Packet may be lost

    def send(self, packet, sock, addr):
        if random.random() < self.ERR_PROB:
            packet = self.make_error(packet)
        if random.random() > self.LOST_PROB:
            sock.sendto(packet, addr)
        return

    # Receive a packet from the unreliable channel
    def recv(self, sock):
        packet, addr = sock.recvfrom(1024)
        return packet, addr

    def sendack(self, ack, sock, addr):
        ack_bytes = ack.to_bytes(4, byteorder='little', signed=True)
        if random.random() > self.LOST_PROB:
            sock.sendto(ack_bytes, addr)
        return

    def recvack(self, sock):
        ack_bytes, addr = sock.recvfrom(1024)
        ack = int.from_bytes(ack_bytes, byteorder='little', signed=True)
        return ack, addr

    def make_error(self, packet):
        ErrData = b''
        for i in range(len(packet)-8):
            byte = random.randint(65, 121)
            ErrData = ErrData+byte.to_bytes(1, byteorder='little', signed=True)
        return packet[0:8]+ErrData

# packet
 # Creates a packet from a sequence number and byte data


def make(seq_num, crc_num, data=b''):
    seq_bytes = seq_num.to_bytes(4, byteorder='little', signed=True)

    crc_bytes = crc_num.to_bytes(4, byteorder='little', signed=True)

    return seq_bytes + crc_bytes + data

# Creates an empty packet


def make_empty():
    return b''

# Extracts sequence number and data from a non-empty packet


def extract(packet):
    seq_num = int.from_bytes(packet[0:4], byteorder='little', signed=True)
    crc_num = int.from_bytes(packet[4:8], byteorder='little', signed=True)
    return seq_num, crc_num, packet[8:]
