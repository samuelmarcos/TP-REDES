
 

import os, sys
import socket

HOST = ' 192.168.0.102'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

print "Escolha a opcao:\n\t1 - Sair\n\t2 - Enviar arquivo para servidor\n\t3 - Listar diretorio no servidor\n\t4 - Obter arquivo no servidor\n"
menu = raw_input()

if menu == '1': #Sair
	tcp.send('1')
elif menu == '2': #Enviar arquivo para o servidor
	print "Enviar arquivo\nInforme o nome do arquivo.extensao: "
	arquivo = raw_input()
	print "Informe 1 para enviar para pasta deste cliente ou digite o ip da pasta destino: "
	usuarioDest = raw_input()	
	try:
		arq = open(arquivo, 'rb')
		tcp.send('2')
		tcp.send(usuarioDest)
		tcp.send(arquivo)
		if tcp.recv(1024) == '-1':
			print "Nao foi possivel enviar o arquivo"		
		else:	
			print 'Enviando...'
			for i in arq:
				tcp.send(i)
			print "Arquivo enviado com sucesso!"
	except IOError:
		tcp.send('-1')
		print "\nNao foi possivel enviar o arquivo\n"

elif menu == '3': #Listar diretorio
	print "\nListar diretorio\n"
	tcp.send('3')
	try:
		while 1:
			aux=tcp.recv(1024)
			if not aux:
				break
			print aux
	except IOError:
		print "\nNao foi possivel listar diretorio no servidor\n"  		

elif menu == '4': #Obter arquivo no servidor
	print "Obter arquivo no servidor"
	tcp.send('4')
	print "Informe o nome do arquivo.extensao: "
	arquivo = raw_input()
	tcp.send(arquivo)
	try:
		if tcp.recv(1024) == '1':
			arq = open(sys.path[0] + "\\" + arquivo,'wb')
			print "Recebendo arquivo..."
			while 1:
				aux=tcp.recv(1024)
				if (not aux):
					break
				arq.write(aux)
		else:
			print "\nNao foi possivel receber o arquivo"			
	except IOError:
		print "\nNao foi possivel receber o arquivo\n"
		os.system("del /f /q ", arquivo)
else: #Opcao invalida
	print "Opcao invalida"
	tcp.send('-1')

print "\nConexao encerrada"
tcp.close()
os.system("PAUSE")