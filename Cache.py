from CacheLine import CacheLine

class Cache:
    def __init__(self, tamanho=5):
        self.elementos: list[CacheLine] = [CacheLine(None, None, "I") for _ in range(tamanho)] 
        self.topo = 0
        self.tam_max = tamanho

    def busca(self, endereco):
        #busca um elemento dentro da cache pelo endereço buscado
        for elemento in self.elementos:
            if elemento.endereco == endereco and elemento.protocolo != "I":
                return elemento
        return None
    
    def remove(self):
        rem = self.elementos[self.topo]
        return rem
        
    def insere(self, linha_nova: CacheLine):
        # Se já existe esse endereço na cache, substitui
        for i, linha in enumerate(self.elementos):
            if linha is not None and linha.endereco == linha_nova.endereco:
                self.elementos[i] = linha_nova
                return 
        
        # Caso contrário, insere na primeira posição vazia
        for i, linha in enumerate(self.elementos):
            if linha is None or linha.protocolo == "I":
                self.elementos[i] = linha_nova
                return 
