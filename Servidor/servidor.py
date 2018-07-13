


import os, sys
import socket
import thread
import string

HOST = '192.168.0.102'# Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

def conectado(con, cliente):

    ini = time.time()
    print 'Conectado por', cliente [0]
    if (not os.path.isdir( sys.path[0] + "\\" + cliente[0]) ):#se não tem uma pasta do cliente, então ela será criada
        os.system("mkdir "+cliente[0])#mkdir + cliente cria pasta com nome do cliente

    menu = con.recv(1024)

    if (menu == '1' or menu == "-1"): # Sair do sistema
        print "\n"
    elif menu == '2': # Receber arquivo do cliente
        usuarioDest = con.recv(1024)
        arquivo = con.recv(1024)
        try:
            if usuarioDest =="1":
                usuarioDest = cliente[0]

            arq = open(sys.path[0] + "\\" + usuarioDest + "\\" + arquivo,'wb')
            con.send('1')
            print "Recebendo arquivo..."
            while 1:
                aux=con.recv(1024)
                if not aux:
                    break
                arq.write(aux)
        except IOError:
            con.send('-1')
            print "\nNao foi possivel receber o arquivo\n"

    elif menu == '3': #Listar diretorio do cliente
        print "Enviar para cliente lista de diretorio de arquivo"
        dirs = os.listdir(sys.path[0] + "\\" + cliente[0])
        dirs = '\n'.join(dirs)
        con.send(dirs)
    else: #Obter arquivo no servidor
        arquivo = con.recv(1024)
        try:
            arq = open(sys.path[0] + "\\" + cliente[0] + "\\" + arquivo, 'rb')
            if arq:
                con.send('1')
                print 'Enviando...'
                for i in arq:
                    con.send(i)
                print "Arquivo enviado com sucesso!"
            else:
                con.send('-1')
                print "Nao foi possivel enviar o arquivo"
        except IOError:
            print "\nNao foi possivel enviar o arquivo\n"
    print 'Finalizando conexao do cliente', cliente[0], '\n\n'
    con.close()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)
print "\nServidor iniciado\n"

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
print "Servidor encerrado"
