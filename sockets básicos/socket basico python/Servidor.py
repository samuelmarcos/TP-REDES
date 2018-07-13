# Servidor
import shutil
import os, sys
import socket
 
HOST = "192.168.1.110"  #ip da maquina atual
PORT = 57000 # porta utilizada para conexao

print "Servidor ", HOST, "porta " , PORT, "\n"
 
while 1:
	print "Aguardando conexao"
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	s.bind((HOST,PORT))
	s.listen(10) #quantidade de clientes ouvidos
	conn,addr= s.accept()
	comand = conn.recv(1024) #Comando para criar pasta do cliente
	clientIpName = conn.recv(1024) #ClientIpName do cliente
	if not os.path.exists(clientIpName):
		os.system(comand) #Criar pasta do cliente
	print "Aceitando a conexao com ", addr
	menu = conn.recv(1024); #Opcao do cliente para com o servidor
	if menu == str(1) or menu == str(3) or menu == str(4):
		conn.close()
		s.close()
		HOST = clientIpName  #ip da maquina cliente
		PORT=57000
		sClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print "Estabelecendo conexao com o cliente " + clientIpName
			.connect((HOST,PORT))
		print "Conexao estabelecida com sucesso!\n"
		if menu == str(3): #remover arquivo
			try:
				os.remove('C:\TP de SO\Servidor\\'+clientIpName+'\\arquivoCliente.zip')
				sClient.send("Arquivo removido no servidor com sucesso")
			except OSError:	
				sClient.send("Erro ao excluir o arquivo")
			
		elif menu == str(4): #listar diretorio
			dirs = os.listdir('C:\TP de SO\Servidor\\'+clientIpName)
			dirs = ''.join(dirs)
			sClient.send(dirs)
			
		elif menu == str(1): #enviara arquivo do servidor para o cliente
			if os.path.isfile('C:\TP de SO\Servidor\\'+clientIpName+'\\arquivoCliente.zip'):				
				sClient.send("1")
				print "Abrindo arquivo..."
				arqClient=open("C:\TP de SO\Servidor\\"+clientIpName+"\\arquivoCliente.zip",'rb')	
				print "Enviando arquivo..."
				for i in arqClient:
					sClient.send(i)
				arqClient.close()
				print "Arquivo enviado com sucesso!\nConexao com o "+clientIpName+" finalizada\n\n"		
			else:
				sClient.send("0")
				print "Arquivo nao encontrado!\nConexao com o "+clientIpName+" finalizada\n\n"		
		sClient.close()
		HOST = "localhost"  #ip da maquina atual		
	elif menu == str(2):
		print "Recebendo o arquivo..."
		arq = open('arquivoCliente.zip','wb')
	
		while 1:
			try:
				dados=conn.recv(1024)
				if not dados:
					break;
			except socket.error , msg:
				print "Transferencia de arquivo interrompida inesperadamente"
			arq.write(dados)
		arq.close()
		conn.close()
		s.close()	
		#Se existir um arquivo antigo, deleta-o antes de mover o novo
		if os.path.isfile('C:\TP de SO\Servidor\\'+clientIpName+'\\arquivoCliente.zip'):
			os.remove('C:\TP de SO\Servidor\\'+clientIpName+'\\arquivoCliente.zip')
		shutil.move("arquivoCliente.zip", "C:\TP de SO\Servidor\\"+clientIpName+"\\")	
		print "Arquivo Recebido com sucesso!\nConexao com o cliente "+clientIpName+" encerrada\n\n"		
print "Servidor finalizado"