# MODULES #
from argprocess import ArgsProcess
import socket
import sys
import os
import time
import struct
import thread
# STATIC VARIABLES #
nm = __file__
# CMD FUNCTIONS #
## HELP
def help(cmd="0"):
    helpDic = { "connect": "Use connect: \n\t" + nm + " connect [IP] [PORT] (port default = 5678)",
               "wake" : "Use wake: \n\t" + nm + " -a [For Wake all]  / -i [IP]"}
    if cmd == "0": #default help
        for com in helpDic.values():
            print com
    else:
        print helpDic[cmd]

## WAKE
def wake(ip):
    print "Enviando paquete magico a:", ip #(EN) Sending magic packet to: IP
    mac = arp[ip]
    print "MAC:", mac
    wakeOnLan(mac)
    """
    time.sleep(2)
    while i == 20:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (ip, int(port))
            sock.connect(server_address)
        except:
            pass
    """

## CONNECT
def connect(ip, port):
    print "Intentando conexion a", ip + ":" + port #(EN) Trying connection to IP:Port
    tryConnect(ip, port)
    time.sleep(2)
    sendCmd(sock)
    time.sleep(5)

###### OTHER FUNCTIONS
## READ DATA
def leerArp():
    arch = open("data/arp.dat") #arp.dat is an ethernet/ip address database
    for linea in arch:
        linea = linea.strip().split("-")
        #print linea
    arch.close()

## WAKEONLAN
def wakeOnLan(macaddress):
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Formato de MAC incorrecto!') #(EN) MAC format is incorrect!

    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = ''

    for i in range(0, len(data), 2):
        send_data = ''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 7))

## SEND CMD
def sendCmd(sock):
    while True:
        cmd = raw_input("camando->") #le damos entrada por teclado al comand que deseamos # (EN) Gets command from user
        sock.send(cmd)#enviamos el comando  # (EN) Sends the command
        time.sleep(2)
        output = sock.recv(100000)#recibimos la salida # (EN) Receives output
        print output #printeamos la salida # (EN) Prints output

## TRY CONNECT
def tryConnect(ip, port):
    global sock
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, int(port))
        sock.connect(server_address)
    except socket.error:
        print "[ERROR] No se pudo establecer conexion con el servidor" # (EN) Could not establish a connection to the server


        #--------------------           creando la clase monitor/ram            -----------------
class RamInUse():
    """docstring for ClassName"""
    def __init__(self):
        #memory_status = commands.getoutput('free') #comando que nos entrega info sobre el total de ram y entre otros datos
        memory_status = '   se      yu      jh      hh      kj      jj      hj      540     440     420'
        memory_status = memory_status.strip().split()[7:]  #procesamiento de texto para el comando 'free'
        self.total = int(memory_status[0])
        self.actualUse = int(memory_status[1])*100 /int(memory_status[0]) #calulamos el porcentaje de ram en uso
        self.free = int(memory_status[2])

    def status(self): #metodo estado para la ram, retorna el porcentaje en uso  
        return self.actualUse

    def TotalMemo(self): #metodo que retorna total de ram
        return self.total

    def FreeMemo(self): #metodo que retorna la ram libre
        return self.free

MEMOram = RamInUse() #creando el objeto MEMOram


def monitoreo(x):
    #time.sleep(20)
    if MEMOram.status() > 80: # si estamos exigiendo la ram mas del 80%
        #Call()
        print 'memoria sobrecargada'
        time.sleep(4)
        
def monitoreoconstante(x):
    timeNow = time.strftime("%H:%M:%S").split(':')
    if int(timeNow[1]) % 10 == 0: #cada diez minutos enviamos el estado actual de la ram al servidor, para ver si es necesario apagar un pc en caso de haber mas de uno encendido

        #sock = socket.socket() #creando el socket
        #sock.connect(('localhost',9950)) #creando la coneccion
        try:
            #sock.send(MEMOram.status()) 
            print 'enviando datos al servidor'
        except:
            print'-Error'
            pass
    else:
        'cada diez minutos enviaremos datos al server'

        #sock.close() #cerrando el socket
    time.sleep(60)
#funcion que voy a colocar en thread
def imprimir_mensaje(mensaje):
    while True:
        print(mensaje)
        time.sleep(4)


## SENDING DATA IF MONITOR RAM FUNCTIONS IS CUMPLY
def Call():

	sock = socket.socket() #creando el socket
	sock.connect(('localhost',9950)) #creando la coneccion
	try:
		sock.send('wakeUp')
	except:
		'-Error'
        pass
	sock.close() #cerrando el socket
    
    
## PRINCIPAL FUNCTION AND THREADS CONTROLLER  
def main():
    while True:
        try:
            mensaje="Thread1" #variable aux
            mensaje2="Thread2" #variable aux
    
        #nuevo thread
            thread.start_new_thread(monitoreo,('',))

        #nuevo thread
            thread.start_new_thread(imprimir_mensaje, (mensaje,))

        #nuevo thread
            thread.start_new_thread(monitoreoconstante,('',))

        except:
            pass #break
    
   
        
###### ARGS
if __name__ == "__main__":
    try:
        os.system("clear")
    except:
        pass

    args =  ArgsProcessClient(__file__)
