class CacheLine:
    '''
    Representa um bloco (linha) individual dentro da Cache
    Contém a tag, estado do protocolo e os dados 
    '''
    def __init__(self, endereco_base, dados, protocolo):
        '''
        Inicializa a linha da cache

        Parâmetros:
            endereco_base (int): O endereço de memória onde começa este bloco
            dados (list): Os valores do bloco. Se None, cria vazio
            protocolo (str): O estado no protocolo MOESI (M, O, E, S, I)
        '''
        self.endereco_base = endereco_base 
        self.dados = dados if dados is not None else [None]*5 
        self.protocolo = protocolo #MOESI
        
    def contem_endereco(self, endereco):
        '''
        Verifica se um endereço específico está contido neste bloco
        caso sim, gera um 'Cache Hit' na verificação
        
        Retorna True se o endereço faz parte do bloco
        '''
        if self.endereco_base is None:
            return False
        return self.endereco_base <= endereco < self.endereco_base + 5

    def indice_no_bloco(self, endereco):
        '''
        Retorna o índice 0–4 dentro do bloco
        '''
        return endereco - self.endereco_base    
