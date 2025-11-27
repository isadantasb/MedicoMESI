from CacheLine import CacheLine

class Cache:
    def __init__(self, tamanho=5):
        self.elementos: list[CacheLine] = [CacheLine(None, "I") for _ in range(tamanho)] 
        self.topo = 0
        self.tam_max = tamanho

    def busca(self, endereco):
        #busca um elemento dentro da cache pelo endereço buscado
        for elemento in self.elementos:
            if elemento.contem_endereco(endereco) and elemento.protocolo != "I":
                return elemento
        return None
    
    def remove(self):
        rem = self.elementos[self.topo]
        self.topo = (self.topo + 1) % self.tam_max
        return rem
        
    def insere(self, linha_nova: CacheLine):
        # Se já existe esse bloco na cache, substitui
        for i, linha in enumerate(self.elementos):
            if linha.endereco_base == linha_nova.endereco_base:
                self.elementos[i] = linha_nova
                return 
        
        # Caso contrário, insere na primeira posição vazia
        for i, linha in enumerate(self.elementos):
            if linha is None or linha.protocolo == "I":
                self.elementos[i] = linha_nova
                return 
        #caso write back !!!! 
        linha_expulsa = self.remove()

        # Inserir na posição que acabou de ser liberada (topo-1)
        pos = (self.topo - 1) % self.tam_max
        self.elementos[pos] = linha_nova

        return linha_expulsa
