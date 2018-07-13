# Cliente 
import socket
import os
 
HOST = "192.168.1.110"  #ip do servidor
PORT=57000 #porta do servidor
 
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print "Bem-vindo(a) " + socket.gethostname()

print "Estabelecendo conexao com o servidor..."
s.connect((HOST,PORT))
localIpName = socket.gethostbyname(socket.gethostname()) #Obtem IP
s.send('mkdir ' + localIpName) #Envia o comando mkdir para o servidor
s.send(localIpName) #Envia o nome da pasta do cliente
print "Conexao estabelecida com sucesso!\n"
menu = input ('Digite a opcao desejada:\n1-Obter arquivo do servidor e enviar para cliente\n2-Enviar um arquivo do cliente para o servidor\n3-Apagar um arquivo do servidor\n4-Listar os arquivos do servidor\n')
print "\n"
s.send(str(menu))
if menu == 1 or menu == 3 or menu == 4:
	s.close()
	HOST = localIpName  #ip da maquina cliente
	PORT = 57000 # porta utilizada para conexao		
	print "Aguardando conexao do servidor"
	sServer=socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	sServer.bind((HOST,PORT))
	sServer.listen(1)
	conn,addr= sServer.accept()
	print "Aceitando a conexao com o servidor"
	if menu == 3:	
		print conn.recv(1024)+"\n" #mensagem resposta do servidor
		print "Conexao com o servidor finalizada\n"
	elif menu == 4:
		print "Arquivos no servidor: "
		dirs = conn.recv(1024)
		print dirs
		#for str in dirs:
		#	print str #lista de arquivos
		print "\nConexao com o servidor finalizada\n"	
	elif menu == 1:
		hasFile = conn.recv(1024)
		if  '1' == hasFile:
			print "Recebendo o arquivo..."
			#Caso exista uma versao anterior do arquivo, remove-a para receber a nova
			if os.path.isfile('arquivoServidor.zip'):
				os.remove('arquivoServidor.zip')
			arqServer = open('arquivoServidor.zip','wb')
			while 1:
				try:
					dados=conn.recv(1024)
					if not dados:
						break;
				except socket.error , msg:
					print "Transferencia de arquivo interrompida inesperadamente"
				arqServer.write(dados)
			arqServer.close()
			print "Arquivo Recebido com sucesso!\nConexao com o servidor finalizada\n"
		else:	
			print "Arquivo nao encontrado no servidor!\nConexao com o servidor finalizada\n"
	sServer.close()
	conn.close()
elif menu == 2:
	print "Abrindo arquivo..."
	arq=open('arquivo.zip','rb')
	
	print "Enviando arquivo..."
	for i in arq:
		s.send(i)
	arq.close()
	print "Arquivo enviado com sucesso!\nConexao com o servidor finalizada\n"
s.close()	
os.system("PAUSE")	