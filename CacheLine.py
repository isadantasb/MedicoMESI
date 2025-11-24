class CacheLine:
    def __init__(self):
        self.protocolo = None #MOESI
        self.status = None #status do paciente
        self.endereco = None #endereço da MP que o paciente se encontra

    def vazio(self): 
        return self.endereco == None
    
    def invalidar(self):
        self.protocolo = "I"

    def printar(self):
        return f"[Protocolo={self.protocolo}, Status do paciente:{self.status}, Endereço:{self.endereco}]"