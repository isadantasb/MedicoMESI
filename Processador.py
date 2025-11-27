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
        print(f"{self.nome} encontrou o status atual do paciente: O paciente se encontra no status {valor}. {status}")

    def traduz_status(self, valor):
        status = {
            1: "Em triagem",
            2: "Em atendimento",
            3: "Em medicação",
            4: "Em alta"
        }
        return status.get(valor, str(valor))
    
    def escrever(self, endereco, novo_valor):
        status = self.traduz_status(novo_valor)
        print(f"{self.nome}, com id {self.id} vai alterar o status do paciente.")

        if self.barramento == None:
            print(f'Erro: o {self.nome} não tem um correspondente para enviar a informação')
            return None
        valor_antigo = self.barramento.busca_para_escrita(endereco, self.id, novo_valor)
        status_antigo = self.traduz_status(valor_antigo)
        if status == status_antigo:
            print(f"O paciente nº {endereco} já estava {status_antigo}. Nenhuma alteração foi necessária")
            return
        print(f"Agora, o paciente nº {endereco}: estava no status {valor_antigo}. {status_antigo}. Agora está {novo_valor}. {status}")

