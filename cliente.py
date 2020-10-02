# Trabalho 1 de INF1407
# Jéssica Pereira - 1711179
# Gabriel Heffer Matheus - 1710603

from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

from gtts import gTTS
import playsound
import os
import speech_recognition as sr


def ouvir_microfone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        print("Diga alguma coisa: ")
        audio = microfone.listen(source)

    return audio

def main():
    host = '127.0.0.1'
    porta = 8752

    # criar o socket
    servidor = socket(AF_INET, SOCK_STREAM)

    # o que usuario deseja ?
    print('Entre com 0 se deseja falar uma frase')
    print('Entre com 1 se deseja escrever uma frase')
    escolha = input()

    # conectando com o servidor
    destino = (host, porta)
    servidor.connect(destino)
    servidor.send(bytearray(escolha, 'utf-8'))

    if escolha == '1':
        print('Entre com a frase desejada:')
        msg = input()

        # enviando/recebendo msg para o servidor
        try:
            servidor.send(bytearray(" "+msg, 'utf-8'))

            resposta = servidor.recv(2 ** 20)
            open("output.mp3", "wb").write(resposta)

            print("Reproduzindo...")
            playsound.playsound("output.mp3")

        except:
            print("Algo esta errado com a frase")

    elif not int(escolha):
        audio = ouvir_microfone()
        print("Traduzindo...")
        # enviando/recebendo msg para o servidor
        try:
            servidor.send(audio.frame_data)
            resposta = servidor.recv(2 ** 20).decode()
            print("Voce disse: ", resposta)

        except:
            print("Algo esta errado com o audio")

    else:
        print("Escolha invalida")
        return

    servidor.close()
    return


if __name__ == '__main__':
    main()
