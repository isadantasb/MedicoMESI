from Memoria import *
from Cache import *

class Barramento:
    def __init__(self, memoria: MemoriaPrincipal, caches):
        self.memoria = memoria  
        self.caches: list[Cache] = caches   
        

    def busca_processador(self, endereco, id_processador):
        #pergunta: algum processador tem esse dado q ta nesse endereço? se SIM: compartilha (S) o dado com o processador q ta pedindo e troca oq deu pra Owned, se NÃO: chama busca_MP
        cache_solicitante: Cache = self.caches[id_processador]
        dados = self.procurar_em_outras_caches(endereco, id_processador)
        
        if not dados: #Se não achou o dado em nenhum processador vai procurar na MP
            return self.busca_MP(endereco, id_processador)
        
        #SE cair aqui é pq tem o dado em uma cache
        linha = dados[0]

        if linha.protocolo == "M":
            linha.protocolo = "O"
        if linha.protocolo == "E":
            linha.protocolo = "S"
        c= cache_solicitante.insere(CacheLine(linha.endereco_base, linha.dados.copy(), "S"))
        if c and c.protocolo in ("M", "O"):
            self.memoria.escrever_bloco(c.endereco_base, c.dados)
            print(f"[WRITE-BACK] Endereço {c.endereco_base} → {c.dados}")
        return linha.dados[endereco-linha.endereco_base]
                

    def busca_para_escrita(self, endereco, id_processador, novo_valor):
        #busca usando as funções de busca. Coloca o dado no endereço desejado (que vai estar S) e dps troca pra M.
        valor = self.busca_processador(endereco, id_processador)

        self.invalida(endereco, id_processador)

        linha = self.caches[id_processador].busca(endereco)
        ind = linha.indice_no_bloco(endereco)
        linha.dados[ind] = novo_valor
        linha.protocolo = "M"

        return valor

    def busca_MP(self, endereco, id_processador):
        #busca o dado do endereço na MP, altera o status da CacheLine pra E se achar
        base = (endereco // 5) * 5
        dados = self.memoria.ler_bloco(base)
        linha = CacheLine(base, dados, "E")
        c = self.caches[id_processador].insere(linha)
        if c and c.protocolo in ("M", "O"):
            self.memoria.escrever_bloco(c.endereco_base, c.dados)
            print(f"[WRITE-BACK] Endereço {c.endereco_base} → {c.dados}")
        return dados[endereco - base]

    def invalida(self, endereco, id_processador):
        #se fizer a escrita, aqui invalida todas as outras CacheLines que tinham esse dado.
        for i, cache in enumerate(self.caches):
            if i == id_processador:
                continue

            linha = cache.busca(endereco)
            if linha is not None:
                linha.protocolo = "I"
    
    def procurar_em_outras_caches(self, endereco, id_processador):
        encontrados = []
        for indice, cache in enumerate(self.caches):
            if indice == id_processador:
                continue
            linha = cache.busca(endereco)
            if linha is not None:
                encontrados.append(linha)
        return encontrados

