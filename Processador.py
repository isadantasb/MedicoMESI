from Cache import *

class Processador:
    '''
    Representa um processador no sistema, no contexto da aplicação, é um profissional 
    da saúde no hospital
    
    Cada processador possui sua própria memória Cache e se comunica
    com a Memória Principal e outros processadores através do Barramento
    '''
    def __init__(self, id, nome, tamanho_cache=5):
        '''
        Inicializa o processador

        Parâmetros:
            id (int): Identificador único do processador
            nome (str): A função do profissional
            tamanho_cache (int): Quantidade de blocos que a cache local pode armazenar
        '''
        self.id = id
        self.nome = nome 
        self.cache = Cache(tamanho_cache)
        self.barramento = None 
        

    def conecta_barramento(self, barramento):
        '''
        Estabelece uma conexão com o barramento do sistema
        
        Parâmetros:
            barramento (Barramento): A instância do barramento compartilhado
        '''
        self.barramento = barramento

    def ler(self, endereco):
        '''
        Simula uma operação de leitura (Read)
        O processador tenta ler um dado de um endereço. No contexto do sistema
        é a leitura do status do paciente de determinado identificador

        Parãmetros:
            endereco (int): O endereço de memória a ser lido, ou seja, o identificador do paciente
        '''
        print(f"{self.nome} deseja ler o prontuário número {endereco}")
        if self.barramento == None:
            print(f'Erro: o {self.nome} não tem um correspondente para enviar a informação')
            return None
        valor = self.barramento.busca_processador(endereco, self.id)
        status = self.traduz_status(valor)
        print(f"{self.nome} encontrou o status atual do paciente: O paciente se encontra no status {valor}. {status}")

    def traduz_status(self, valor):
        '''
        Converte o código numérico armazenado na memória
        para uma descrição legível do estado do paciente

        Parâmetros:
            valor (int): O código do status, que vai de 1 a 4

        Retorna uma descrição textual do status
        '''
        status = {
            1: "Em triagem",
            2: "Em atendimento",
            3: "Em medicação",
            4: "Em alta"
        }
        return status.get(valor, str(valor))
    
    def escrever(self, endereco, novo_valor):
        '''
        Simula uma operação de escrita (Write)
        O processador tenta alterar um dado na memória/cache, No contexto do sistema
        é a alteração do status do paciente

        Parãmetros:
            endereco (int): O endereço a ser alterado
            novo_valor (int): O novo código de status a ser gravado
        '''
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

