from CacheLine import CacheLine

class Cache:
    '''
    Gerencia um conjunto de linhas de cache (CacheLine)
    Responsável por buscar dados (Hit/Miss) e gerenciar a política de substituição
    '''
    def __init__(self, tamanho=5):
        '''
        Inicializa a Cache
        Parâmetros:
            tamanho (int): Quantidade total de linhas que a cache comporta
        '''

        self.elementos: list[CacheLine] = [CacheLine(None, None, "I") for _ in range(tamanho)] 
        self.topo = 0
        self.tam_max = tamanho

    def busca(self, endereco):
        '''
        Procura por um endereço na cache
        
        Retorna a CacheLine em caso de Cache Hit e None caso o estado seja inválido ou não encontrado
        '''
        for elemento in self.elementos:
            if elemento.contem_endereco(endereco) and elemento.protocolo != "I":
                return elemento
        return None
    
    def remove(self):
        '''
        Remove uma linha da cache baseada na política FIFO
        O ponteiro topo indica quem o próximo a sair
        
        Retorna a CacheLine que foi removida
        '''
        rem = self.elementos[self.topo]
        self.topo = (self.topo + 1) % self.tam_max
        return rem
        
    def insere(self, linha_nova: CacheLine):
        '''
        Insere uma nova linha na cache, lidando com subtituição caso esteja cheia
        
        retorna a CacheLine ou None 
        Se uma linha foi expulsa para dar lugar à nova, ela é retornada, o que é importante
        caso ela esteja modificada ou inválida
        '''
        # Cenário 1: Se já existe esse bloco na cache, ele será substituido
        for i, linha in enumerate(self.elementos):
            if linha.endereco_base == linha_nova.endereco_base:
                self.elementos[i] = linha_nova
                return 
        
        # Cenário 2: Caso contrário, insere na primeira posição vazia
        for i, linha in enumerate(self.elementos):
            if linha is None or linha.protocolo == "I":
                self.elementos[i] = linha_nova
                return 
        # Cenário 3: A cache está cheia, e o write back é aplicado
        linha_expulsa = self.remove()

        # Insere na posição que acabou de ser liberada (topo-1)
        pos = (self.topo - 1) % self.tam_max
        self.elementos[pos] = linha_nova

        return linha_expulsa
    
        
