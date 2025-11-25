class Barramento:
    def __init__(self, memoria, caches):
        self.memoria = memoria  
        self.caches = caches   
        

    def busca_processador(self, endereco, id_processador):
        #pergunta: algum processador tem esse dado q ta nesse endereço? se SIM: compartilha (S) o dado com o processador q ta pedindo e troca oq deu pra Owned, se NÃO: chama busca_MP
        pass

    def busca_para_escrita(self, endereco, id_processador):
        #busca usando as funções de busca. Coloca o dado no endereço desejado (que vai estar S) e dps troca pra M.
        pass

    def busca_MP(self, endereco, id_processador):
        #busca o dado do endereço na MP, altera o status da CacheLine pra E se achar
        pass

    def invalida():
        #se fizer a escrita, aqui invalida todas as outras CacheLines que tinham esse dado.
        pass

