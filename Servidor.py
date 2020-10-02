# servidor de ping
# uso:
# python3 pingServidor.py [<porta servidor>]

from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
import _thread
from gtts import gTTS
from speech_recognition import AudioData
import speech_recognition as sr
import time


_service = None


class _Text2Speech:
    def __init__(self):
        return

    def run(self, text, conn):
        text = str(text)
        output = gTTS(text=text, lang='pt', slow=False)
        output.save("output.mp3")
        with open("output.mp3", "rb") as file:
            speech_mp3_bytes = file.read()
        try:
            conn.sendall(speech_mp3_bytes)
        except:
            pass
        return


class _Speech2Text:
    def __init__(self):
        return

    def run(self, voice_bytes, conn):
        audio = AudioData(frame_data=voice_bytes, sample_rate=44100, sample_width=2)
        speech_rec = sr.Recognizer()
        try:
            # Passa o audio para o reconhecedor de padroes do speech_recognition
            frase = speech_rec.recognize_google(audio, language='pt-BR')
            # Após alguns segundos, retorna a frase falada
            conn.sendall(bytes(frase, encoding='utf-8'))
            # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except:
            pass
        return


def connection(conn, cliente):
    service = None
    print(f"Conectado por {cliente}")
    while True:
        try:
            msg = conn.recv(4096)
        except:
            print(f"Conexão encerrada por {cliente}")
            _thread.exit()
            return
        if not msg:
            conn.close()
            _thread.exit()
            return
        if int(msg):
            service = _Text2Speech()
        elif not int(msg):
            service = _Speech2Text()
        break
    while True:
        try:
            msg = conn.recv(2**20)
        except:
            print(f"Conexão encerrada por {cliente}")
            _thread.exit()
            return
        if len(msg):
            service.run(msg, conn)
        else:
            conn.close()
            break
    _thread.exit()
    return


def main():
    HOST = '127.0.0.1'  # Endereco IP do Servidor
    PORT = 8752  # Porta que o Servidor esta
    # cria um socket de servidor (sem cliente)
    tcp = socket(AF_INET, SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    # colocar em modo passivo
    tcp.listen(0)
    print("Pronto!")
    while True:
        # accept espera por uma conexao
        # retorna um socket com cliente e servidor e o endereco do cliente
        conn, cliente = tcp.accept()
        # Criar novo processo para servidor concorrente
        _thread.start_new_thread(connection, (conn, cliente))  # thread criada
    tcp.close()
    return


if __name__ == '__main__':
    main()
