import random

class MemoriaPrincipal:
    def __init__(self, tam=50):
        self.tamanho = tam
        self.celulas = [random.randint(1, 4) for _ in range(tam)] #Vi isso aqui na net mas não sei se é o melhor jeito
    
    def ler(self, endereco):
        self.verifica_endereco(endereco)
        return self.celulas[endereco]
    
    def escrever(self, endereco, valor):
        self.verifica_endereco(endereco)
        self.celulas[endereco] = valor
    
    def verifica_endereco(self, endereco):
       pass
    