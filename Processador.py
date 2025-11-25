from Cache import *

class Processador:
    def __init__(self, id, nome, tamanho_cache=5):
        self.id = id
        self.nome = nome #se é enfermeiro, medico, farmaceutico e afins
        self.cache = Cache(tamanho_cache)
        self.barramento = None #vai conecta depois de inicializa
        

    def conecta_barramento(self, barramento):
        self.barramento = barramento

    def ler(self, endereco):
        print(f"{self.nome} deseja ler o prontuário número {endereco}")
        if self.barramento == None:
            print(f'Erro: o {self.nome} não tem um correspondente para enviar a informação')
            return None
        valor = self.barramento.busca_processador(endereco, self.id)
        status = self.traduz_status(valor)
        print(f"{self.nome} encontrou o status atual do paciente: O paciente se encontra {status}")

    def traduz_status(self, valor):
        status = {
            1: "em triagem",
            2: "em atendimento",
            3: "em medicação",
            4: "em alta"
        }
        return status.get(valor, str(valor))
    
    def escrever(self, endereco, novo_valor):
        status = self.traduz_status(novo_valor)
        print(f"{self.nome}, com id {self.id} vai alterar o status do paciente.")

        if self.barramento == None:
            print(f'Erro: o {self.nome} não tem um correspondente para enviar a informação')
            return None
        self.barramento.busca_para_escrita(endereco, self.id, novo_valor)
        print(f"Agora, o paciente nº {endereco}, se encontra em {status}. Valor alterado no prontuário ")

    def mostra_cache(self):
        print(f"A visão do {self.nome}, é:")
        self.cache.printar_cache()
