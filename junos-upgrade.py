#!/usr/bin/python
# A script which upgrades JunOS remotely
import paramiko
import socket
import time
import sys
 
ROUTER_IP='172.16.1.1'
USERNAME='root'
PASSWORD='root123'
JUNOS_URL='http://172.16.1.3/junos-srxsme-11.1R3.5-domestic.tgz'
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
 
CLOSE = """
<rpc>
  <close-session/>
</rpc>"""
 
SOFT_ADD = """
<rpc>
   <request-package-add>
     <package-name>"""+JUNOS_URL+"""
     </package-name>
     <no-copy/>
     <no-validate/>
     <unlink/>
   </request-package-add></rpc>
</rpc>"""
 
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((ROUTER_IP,830))
 
trans = paramiko.Transport(socket)
trans.connect(username=USERNAME, password=PASSWORD)
 
#CREATE CHANNEL FOR DATA COMM
ch = trans.open_session()
name = ch.set_name('netconf')
 
#Invoke NETCONF
ch.invoke_subsystem('netconf')
 
#SEND COMMAND
ch.send(SOFT_ADD)
 
#Recieve data returned
data = ch.recv(2048)
while data:
   data = ch.recv(1024)
   print data,
   if data.find('</rpc-reply>') == 0:
     #We have reached the end of reply
     ch.send(CLOSE)
 
ch.close()
trans.close()
socket.close()
