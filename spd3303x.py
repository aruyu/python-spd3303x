#!/usr/bin/env python
#-*- coding:utf-8 –*-
#-----------------------------------------------------------------------------
# The short script is a example that open a socket, sends a query,
# print the return message and closes the socket.
#
#No warranties expressed or implied
#
#SIGLENT/JAC 05.2018
#
#-----------------------------------------------------------------------------
import socket # for sockets
import sys # for exit
import time # for sleep
import argparse
from argparse import RawTextHelpFormatter
#-----------------------------------------------------------------------------

remote_ip = "192.168.0.51" # should match the instrument’s IP address
port = 5025 # the port number of the instrument service

#Port 5024 is valid for the following:
#SIGLENT SDS1202X-E, SDG1/2X Series, SDG6X Series
#SDM3055, SDM3045X, and SDM3065X
#
#Port 5025 is valid for the following:
#SIGLENT SVA1000X series, SSA3000X Series, and SPD3303X/XE

def connect_socket():
  try:
    #create an AF_INET, STREAM socket (TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error:
    print('Failed to create socket.')
    sys.exit();

  try:
    #Connect to remote server
    sock.connect((remote_ip , port))
  except socket.error:
    print('Failed to connect in {0}'.format(remote_ip))

  return sock

def close_socket(sock):
  #close the socket
  sock.close()
  time.sleep(1)

def control_device(status:str, channel:str):
  try:
    device_socket = connect_socket()

    if status == 'on':
      if channel == 'all':
        device_socket.sendall(b'OUTPUT CH3,ON\n')
        device_socket.sendall(b'OUTPUT CH2,ON\nOUTPUT CH1,ON\n')
      elif channel == '1':
        device_socket.sendall(b'OUTPUT CH1,ON\n')
      elif channel == '2':
        device_socket.sendall(b'OUTPUT CH2,ON\n')
      elif channel == '3':
        device_socket.sendall(b'OUTPUT CH3,ON\n')

    elif status == 'off':
      if channel == 'all':
        device_socket.sendall(b'OUTPUT CH1,OFF\nOUTPUT CH2,OFF\n')
        device_socket.sendall(b'OUTPUT CH3,OFF\n')
      elif channel == '1':
        device_socket.sendall(b'OUTPUT CH1,OFF\n')
      elif channel == '2':
        device_socket.sendall(b'OUTPUT CH2,OFF\n')
      elif channel == '3':
        device_socket.sendall(b'OUTPUT CH3,OFF\n')

  except:
    close_socket(device_socket)
    print("Failed to turn {0} {1} CH for '{2}' device...".format(status.upper(), channel, remote_ip))

  else:
    close_socket(device_socket)
    print("Successfully turn {0} {1} CH for '{2}' device.".format(status.upper(), channel, remote_ip))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Control Power Supply (SPD3303X-E)\n" +
                                               "MIT License <https://github.com/aruyu/remote_power/blob/master/LICENSE/>\n" +
                                               "Report or pull request any time. <https://github.com/aruyu/remote_power/>",
                                   formatter_class=RawTextHelpFormatter)
  parser.add_argument('-i', '--ip', required=False, default="192.168.0.51",
                      help="An IP address for Power Supply which you want to control.\n" +
                           "Default IP address is '192.168.0.51'")
  parser.add_argument('-c', '--channel', choices=['1', '2', '3', 'all'], required=False, default="all",
                      help="Specific channel '1', '2', '3', or 'all'.")
  parser.add_argument('status', metavar='status', choices=['on', 'off'],
                      help="'on' to turn on Device, 'off' to turn off Device.")
  args = parser.parse_args()

  remote_ip = args.ip
  control_device(args.status, args.channel)
