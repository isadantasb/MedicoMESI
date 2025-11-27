from Memoria import *
from Cache import *

class Barramento:
    def __init__(self, memoria: MemoriaPrincipal, caches):
        self.memoria = memoria  
        self.caches: list[Cache] = caches   
        

    def busca_processador(self, endereco, id_processador, escrita=False):
        cache_solicitante = self.caches[id_processador]

        linha_remota = self.procurar_em_outras_caches(endereco, id_processador)

        if linha_remota is not None:
            if not escrita:
                print(f"[RH] Read Hit | Endereço {endereco} | Estado antigo: {linha_remota.protocolo}")

            if linha_remota.protocolo == "M":
                linha_remota.protocolo = "O"
            elif linha_remota.protocolo == "E":
                linha_remota.protocolo = "S"

            # 2 — Insere a linha REMOTA na cache solicitante
            nova_linha = CacheLine(linha_remota.endereco_base,linha_remota.dados.copy(),"S" if not escrita else "M")

            linha_expulsa = cache_solicitante.insere(nova_linha)

            # Se expulsou algo modificado, write-back
            if linha_expulsa and linha_expulsa.protocolo in ("M", "O"):
                self.memoria.escrever_bloco(linha_expulsa.endereco_base, linha_expulsa.dados)
                print(f"[WRITE-BACK] Endereço {linha_expulsa.endereco_base} → {linha_expulsa.dados}")

            return nova_linha.dados[endereco - nova_linha.endereco_base]

        # 3 — Se não existe em NENHUMA cache → RAM
        if not escrita:
            print(f"[RM] Read Miss | Endereço {endereco}")

        return self.busca_MP(endereco, id_processador)

                

    def busca_para_escrita(self, endereco, id_processador, novo_valor):
        #busca usando as funções de busca. Coloca o dado no endereço desejado (que vai estar S) e dps troca pra M.
        linha_local = self.caches[id_processador].busca(endereco)
        linha_remota = self.procurar_em_outras_caches(endereco, id_processador)
        if linha_local is not None and linha_local.protocolo != "I":
            print(f"[WH] Write Hit | Endereço {endereco} | Estado antigo: {linha_local.protocolo}")

        elif linha_remota is not None:
            print(f"[WH] Write Hit | Endereço {endereco} | Estado antigo: {linha_remota.protocolo}")

        else:
            print(f"[WM] Write Miss | Endereço {endereco}")
        valor = self.busca_processador(endereco, id_processador, escrita=True)
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
        for indice, cache in enumerate(self.caches):
            if indice == id_processador:
                continue
            linha = cache.busca(endereco)
            if linha is not None:
                return linha