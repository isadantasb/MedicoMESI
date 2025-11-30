from random import randint

class MemoriaPrincipal:
    '''
    Simula a memória principal (RAM) de um computador.
    Armazena dados em células endereçáveis e permite leitura/escrita
    de valores individuais ou blocos de dados.
    '''

    def __init__(self, tam=50):
        '''
        Inicializa a memória com valores aleatórios, que variam de 1 a 4, 
        de acordo com o estado do paciente

        1 - Em triagem
        2 - Em tratamento
        3 - Em medicação
        4 - Em alta

        Parãmetros:
            tam (int): O tamanho total da memória (número de células)
        '''
        self.tamanho = tam
        self.celulas = [randint(1, 4) for _ in range(tam)] 
    
    def ler_bloco(self, endereco):
        '''
        Primeiro, verifica se o endereço inicial é válido, e depois 
        lê um bloco de 5 células a partir de um endereço específico

        Parâmetros:
            endereco (int): O endereço inicial do bloco

        Retorna uma lista contendo os valores das 5 células lidas
        '''
        self.validaendereco(endereco)
        # Nota: Idealmente, deveríamos verificar se o bloco inteiro cabe na memória aqui - Não sabia se podia remover esse
        return self.celulas[endereco : endereco + 5]
    
    def ler(self, endereco):
        '''
        Primeiro, verifica se o endereço é válido, e depois 
        lê o valor de uma única célula

        Parâmetros:
            endereco (int): O endereço da célula a ser lida

        Retorna o valor armazenado naquele endereço
        '''
        self.validaendereco(endereco)
        return self.celulas[endereco]
    
    def escrever_bloco(self, endereco, dados):
        '''
        Primeiro, verifica se o endereço inicial é válido, e depois
        escreve um bloco de dados na memória a partir de um endereço

        Parâmetros:
            endereco (int): O endereço inicial para escrita
            dados (list): Uma lista de dados para escrever
        '''
        self.validaendereco(endereco)
        for i in range(5):
            if (endereco + i) < self.tamanho:
                self.celulas[endereco + i] = dados[i]
            else:
                print(f"Aviso: Tentativa de escrita fora da memória no índice {endereco + i}")

    def validaendereco(self, endereco): 
        '''
        Verifica se um endereço está dentro dos limites da memória

        Parâmetros:
            endereco (int): O endereço a ser validado

        Retorna um IndexError se o endereço for menor que zero ou maior igual ao tamanho da memória
        '''
        if endereco < 0 or endereco >= self.tamanho:
            raise IndexError(f"Endereço {endereco} fora da memória!")