from random import randint

class MemoriaPrincipal:
    def __init__(self, tam=50):
        self.tamanho = tam
        self.celulas = [randint(1, 4) for _ in range(tam)] #Vi isso aqui na net mas não sei se é o melhor jeito #acho legal 
    
    def ler(self, endereco):
        self.validaendereco(endereco)
        return self.celulas[endereco]
    
    def escrever(self, endereco, valor):
        self.validaendereco(endereco)
        if valor < 1 or valor > 4:
            raise ValueError("Estado inválido (use 1 a 4)")
        self.celulas[endereco] = valor

    def validaendereco(self, endereco): 
        if endereco < 0 or endereco >= self.tamanho:
            raise IndexError("Endereço fora da memória!")
        
