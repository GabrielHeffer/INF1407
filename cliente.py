# cliente de ping
# uso:
# python3 pingCliente.py [<endereco servidor> [<porta servidor>]]

from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep


def main():
    host = '127.0.0.1'
    porta = 8752

    # criar o socket
    servidor = socket(AF_INET, SOCK_STREAM)

    # o que usuario deseja ?
    print('Entre com 0 se deseja falar uma frase')
    print('Entre com 1 se deseja escrever uma frase')
    escolha = input()

    if (escolha == '1'):
        print('Entre com a frase desejada:')
        msg = input()

    # conectando com o servidor
    destino = (host, porta)
    servidor.connect(destino)

    # enviando msg para o servidor
    while True:
        try:
            servidor.send(bytearray(msg, 'utf-8'))

        except:
            print("Something else went wrong1")

    return


if __name__ == '__main__':
    main()
