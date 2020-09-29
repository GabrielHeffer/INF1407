# cliente de ping
# uso:
# python3 pingCliente.py [<endereco servidor> [<porta servidor>]]

from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

def main():
    if len(argv) > 1:
        host = argv[1]
    else:
        host = '127.0.0.1'  # ou ==> host = '::1'
    if len(argv) > 2:
        # a porta e' um numero inteiro e nao uma string
        porta = int(argv[2])
    else:
        # porta acima de 1024 para poder executar o servidor
        # sem ser superusuario
        porta = 8752

    # criar o socket
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    # para casa, usar try except
    tcpSocket.connect((host, porta))
    contador = 1
    while True:
        # para casa, lembrar de colocar aqui tambem um try except
        tcpSocket.send(bytearray('Ping #%d'%contador, 'utf-8'))
        contador += 1
        # espera 1 segundo antes de enviar de novo outro ping
        sleep(1)

    return

if __name__ == '__main__':
    main()
