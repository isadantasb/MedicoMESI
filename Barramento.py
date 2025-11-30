from Memoria import *
from Cache import *
import logging

class Barramento:
    '''
    Representa o barramento do sistema
    
    Atua como o intermediário entre os Processadores  e a Memória Principal.
    É responsável por garantir a coerência de cache (Protocolo MOESI/MESI),
    implementando a lógica de 'Snooping' (escuta) e invalidação
    '''
    def __init__(self, memoria: MemoriaPrincipal, caches):
        '''
        Inicializa os barramentos

        Parâmetros:
            memoria (MemoriaPrincipal): A instância da RAM
            caches (list[Cache]): Lista contendo as caches de todos os processadores
        '''
        self.memoria = memoria  
        self.caches: list[Cache] = caches   
        

    def busca_processador(self, endereco, id_processador, escrita=False):
        '''
        Gerencia uma solicitação de leitura (Read) ou preparação para escrita
        
        Fluxo:
        1. Verifica a Cache Local (Hit Local)
        2. Se falhar, verifica outras Caches (Snooping / Hit Remoto)
        3. Se falhar em tudo, busca na Memória Principal (RAM)

        Parâmetros:
            endereco (int): Endereço do dado requisitado
            id_processador (int): ID do processador que fez o pedido
            escrita (bool): Se True, indica que estamos buscando o dado para modificá-lo depois
                            Isso afeta o estado inicial da linha (S vs M)
        '''
        cache_solicitante = self.caches[id_processador]

        linha_remota = self.procurar_em_outras_caches(endereco, id_processador)
        linha_local = cache_solicitante.busca(endereco)
        if linha_local is not None:
            if not escrita:
                print(f"[RH] Read Hit | Endereço {endereco} | Estado antigo: {linha_local.protocolo}")
                logging.info(f"[RH] Read Hit | Endereco {endereco} | Estado antigo: {linha_local.protocolo} | Solicitante: P{id_processador}")

            return linha_local.dados[endereco - linha_local.endereco_base]
        if linha_remota is not None:
            if not escrita:
                print(f"[RH] Read Hit | Endereço {endereco} | Estado antigo: {linha_remota.protocolo}")
                logging.info(f"[RH] Read Hit | Endereco {endereco} | Estado antigo: {linha_remota.protocolo} | Solicitante: P{id_processador}")

            if linha_remota.protocolo == "M":
                linha_remota.protocolo = "O"
            elif linha_remota.protocolo == "E":
                linha_remota.protocolo = "S"

            nova_linha = CacheLine(linha_remota.endereco_base,linha_remota.dados.copy(),"S" if not escrita else "M")

            linha_expulsa = cache_solicitante.insere(nova_linha)

            if linha_expulsa and linha_expulsa.protocolo in ("M", "O"):
                self.memoria.escrever_bloco(linha_expulsa.endereco_base, linha_expulsa.dados)
                print(f"[WRITE-BACK] Endereço {linha_expulsa.endereco_base} → {linha_expulsa.dados}")
                logging.info(f"[WRITE-BACK] Endereço {linha_expulsa.endereco_base} -> {linha_expulsa.dados}")

            return nova_linha.dados[endereco - nova_linha.endereco_base]

        if not escrita:
            print(f"[RM] Read Miss | Endereço {endereco}")
            logging.info(f"[RM] Read Miss | Endereco {endereco} | Solicitante: P{id_processador}")

        return self.busca_MP(endereco, id_processador)

                

    def busca_para_escrita(self, endereco, id_processador, novo_valor):
        '''
        Gerencia uma solicitação de escrita (Write)

        Parâmetros:
            endereco (int): Endereço a ser escrito
            id_processador (int): Quem quer escrever
            novo_valor: O dado a ser gravado
        '''
        #busca usando as funções de busca. Coloca o dado no endereço desejado (que vai estar S) e dps troca pra M.
        linha_local = self.caches[id_processador].busca(endereco)
        linha_remota = self.procurar_em_outras_caches(endereco, id_processador)
        if linha_local is not None and linha_local.protocolo != "I":
            print(f"[WH] Write Hit | Endereço {endereco} | Estado antigo: {linha_local.protocolo}")
            logging.info(f"[WH] Write Hit | Endereco {endereco} | Estado antigo: {linha_local.protocolo} | Solicitante: P{id_processador}")

        elif linha_remota is not None:
            print(f"[WH] Write Hit | Endereço {endereco} | Estado antigo: {linha_remota.protocolo}")
            logging.info(f"[WH] Write Hit | Endereco {endereco} | Estado antigo: {linha_remota.protocolo} | Solicitante: P{id_processador}")

        else:
            print(f"[WM] Write Miss | Endereço {endereco}")
            logging.info(f"[WM] Write Miss | Endereco {endereco} | Solicitante: P{id_processador}")
        valor = self.busca_processador(endereco, id_processador, escrita=True)
        self.invalida(endereco, id_processador)

        linha = self.caches[id_processador].busca(endereco)
        ind = linha.indice_no_bloco(endereco)
        linha.dados[ind] = novo_valor
        linha.protocolo = "M"

        return valor

    def busca_MP(self, endereco, id_processador):
        '''
        Busca um bloco diretamente na Memória Principal (RAM)
        Usado quando ocorre um Cache Miss em todos os processadores
        '''
        #busca o dado do endereço na MP, altera o status da CacheLine pra E se achar
        base = (endereco // 5) * 5 
        dados = self.memoria.ler_bloco(base)
        linha = CacheLine(base, dados, "E")
        c = self.caches[id_processador].insere(linha)
        if c and c.protocolo in ("M", "O"):
            self.memoria.escrever_bloco(c.endereco_base, c.dados)
            print(f"[WRITE-BACK] Endereço {c.endereco_base} → {c.dados}")
            logging.info(f"[WRITE-BACK] Endereco {c.endereco_base} -> {c.dados}")
        return dados[endereco - base]

    def invalida(self, endereco, id_processador):
        '''
        Manda um sinal de inválido para todas as outras caches quando uma escrita é
        feita por um processador (um funcionário) e outro possui esse dado
        '''
        for i, cache in enumerate(self.caches):
            if i == id_processador:
                continue

            linha = cache.busca(endereco)
            if linha is not None:
                linha.protocolo = "I"
    
    def procurar_em_outras_caches(self, endereco, id_processador):
        '''
        Implementa o 'Snooping', procurando nas caches vizinhas a informação desejada
        
        Retorna a linha encontrada na cache vizinha (ou None)
        '''
        for indice, cache in enumerate(self.caches):
            if indice == id_processador:
                continue
            linha = cache.busca(endereco)
            if linha is not None:
                return linha