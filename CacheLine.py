class CacheLine:
    def __init__(self, endereco_base, dados, protocolo):
        self.endereco_base = endereco_base #endereço da MP que o paciente se encontra
        self.dados = dados if dados is not None else [None]*5 #status do paciente
        self.protocolo = protocolo #MOESI
        
    def contem_endereco(self, endereco):
        """Retorna True se o endereço pertence a este bloco."""
        if self.endereco_base is None:
            return False
        return self.endereco_base <= endereco < self.endereco_base + 5

    def indice_no_bloco(self, endereco):
        """Retorna o índice 0–4 dentro do bloco."""
        return endereco - self.endereco_base    
