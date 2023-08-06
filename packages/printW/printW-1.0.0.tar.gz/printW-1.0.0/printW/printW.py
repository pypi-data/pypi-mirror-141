#classe para trablhar com maquina de escrever

import sys, time

def printW(mensagem):
    mensagem = mensagem
    
    for char in mensagem:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)


