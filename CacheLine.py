class CacheLine:
    def __init__(self, endereco, status, protocolo):
        self.endereco = endereco #endereço da MP que o paciente se encontra
        self.status = status #status do paciente
        self.protocolo = protocolo #MOESI
        
        

    def vazio(self): 
        return self.endereco == None
    
    def invalidar(self):
        self.protocolo = "I"

    def printar(self):
        return f"[Protocolo={self.protocolo}, Status do paciente:{self.status}, Endereço:{self.endereco}]"