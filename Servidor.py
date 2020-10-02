# servidor de ping
# uso:
# python3 pingServidor.py [<porta servidor>]

from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
from os import fork
from gtts import gTTS
from speech_recognition import AudioData
import speech_recognition as sr
import time


_service = None


class _Text2Speech:
    def __init__(self):
        return

    def run(self, text, conn):
        output = gTTS(text=text, lang='pt', slow=False)
        output.save("output.mp3")
        with open("output.mp3", "rb") as file:
            speech_mp3_bytes = file.read()
        conn.sendall(speech_mp3_bytes)
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
            conn.sendall(bytes(frase))
            # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except:
            conn.sendall(bytes())
        return


def choose_service(conn):
    global _service
    while True:
        msg = conn.recv(4096)
        if not msg:
            continue
        if int(msg):
            _service = _Text2Speech()
        elif not int(msg):
            _service = _Speech2Text()
        break
    return


def execute_service(conn):
    global _service
    tolerance_connection = 8
    msg = bytes()
    while True:
        buff_msg = conn.recv(4096)
        if buff_msg:
            msg += buff_msg
        elif not tolerance_connection:
            _service.run(msg, conn)
            break
        else:
            time.sleep(0.05)
            tolerance_connection -= 0.05
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
        pid = fork()    # 2o processo criado
        if pid == 0:
            # o filho nao precisa mais do socket sem o cliente
            tcp.close()
            print(f"Conectado por {cliente}")
            choose_service(conn)
            execute_service(conn)
            conn.close()
            # sair sem erro (abort sai com erro)
            # quem esta saindo e' o filho (nao o pai)
            exit()
        else:
            # e' pai
            # o pai nao precisa do socket com o cliente
            conn.close()
    return


if __name__ == '__main__':
    main()
