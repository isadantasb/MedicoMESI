from random import randint

class MemoriaPrincipal:
    def __init__(self, tam=50):
        self.tamanho = tam
        self.celulas = [randint(1, 4) for _ in range(tam)] #Vi isso aqui na net mas não sei se é o melhor jeito #acho legal 
    
    def ler_bloco(self, endereco):
        self.validaendereco(endereco)
        return self.celulas[endereco:endereco+5]
    
    def escrever_bloco(self, endereco, dados):
        self.validaendereco(endereco)
        for i in range(5):
            self.celulas[endereco + i] = dados[i]

    def validaendereco(self, endereco): 
        if endereco < 0 or endereco >= self.tamanho:
            raise IndexError("Endereço fora da memória!")
        
