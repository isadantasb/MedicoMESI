from Memoria import *
from Processador import *
from Barramento import *
import os

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_e_limpar():
    input("\nPressione ENTER para voltar ao menu...")
    limpar_terminal()

def imprimir_estado_geral(memoria, processadores):
    '''
    Exibe o estado completo do sistema: RAM + Caches
    '''

    print("\n" + "="*60)
    print("ESTADO GERAL DO SISTEMA".center(60))
    print("="*60)

    # -------------------------
    #  MOSTRAR MEMÓRIA RAM
    # -------------------------
    print("\nMEMÓRIA PRINCIPAL (RAM):")
    print("-"*60)

    for end in range(memoria.tamanho):
        valor = memoria.ler(end)
        print(f"End {end:02d} | Valor: {valor}")

    # -------------------------
    #  MOSTRAR CACHES
    # -------------------------
    print("\n" + "="*60)
    print("CACHES DOS PROCESSADORES")
    print("="*60)

    for proc in processadores:
        print(f"\nProcessador {proc.id} ({proc.nome})")
        print("-"*60)
        print(f"{'Endereço':<20} {'Valor':<20} {'Protocolo':<20}")
        print("-"*60)

        for linha in proc.cache.elementos:
            end = linha.endereco_base if linha.endereco_base is not None else "--"
            val = linha.dados if not all(d is None for d in linha.dados) else "--" 
            prot = linha.protocolo if linha.protocolo is not None else "--"
            print(f"{str(end):<20} {str(val):<20} {str(prot):<20}")

    print("\n" + "="*60 + "\n")



def main():
    print("Inicializando o sistema de prontuários médicos...")
    ram = MemoriaPrincipal(tam=50)

    p0 = Processador(0, "Médico")
    p1 = Processador(1, "Enfermeiro")
    p2 = Processador(2, "Farmacêutico")
    lista_processadores = [p0, p1, p2]
    
    lista_caches = [p0.cache, p1.cache, p2.cache]
    barramento = Barramento(ram, lista_caches)
    p0.conecta_barramento(barramento)
    p1.conecta_barramento(barramento)
    p2.conecta_barramento(barramento)

    print("Sistema inicializado")
    opcao = "0" 

    while opcao != "5":
        print("Menu Principal")
        print("1. Eu sou um médico")
        print("2. Eu sou um enfermeiro")
        print("3. Eu sou um farmacêutico")
        print("4. Visualizar memória e caches")
        print("5. Sair")

        opcao = input("escolha uma opção: ")
        limpar_terminal()
        processador_atual = None
        if opcao == '1':
            processador_atual = p0
        elif opcao == '2':
            processador_atual = p1
        elif opcao == '3':
            processador_atual = p2
        elif opcao == '4':
            imprimir_estado_geral(ram, lista_processadores)
            input("Pressione ENTER para voltar...")
           
        elif opcao == '5':
            print("Encerrando simulador...")
        if processador_atual is not None:
            print(f"{processador_atual.nome} foi selecionado, o que deseja fazer? ")
            print("1. Ler um Prontuário (Consultar Status)")
            print("2. Escrever em um Prontuário (Atualizar Status)")
            print("3. Voltar")
            
            acao = input("O que deseja fazer? ")
            limpar_terminal()
            if acao == '1': 
                    end = int(input("Opção 1. Ler um Prontuário (Consultar Status) selecionada \nDigite o Nº do Prontuário (Endereço 0-49): "))
                    if 0 <= end < 50:
                        processador_atual.ler(end)
                    else:
                        print("Erro: Endereço inválido.")
                    pausar_e_limpar()

            elif acao == '2': 
                end = int(input("Opção 2. escrever em um Prontuário (Atualizar Status) selecionada \nDigite o Nº do Prontuário (Endereço 0-49): "))
                if 0 <= end < 50:
                    val = int(input(f"1. Em triagem\n2. Em atendimento\n3. Em medicação\n4. Em alta\nNovo Status (1-4): "))
                    if 1 <= val <= 4:
                        processador_atual.escrever(end, val)
                    else:
                        print("Erro: Status inválido (use 1 a 4).")
                else:
                    print("Erro: Endereço inválido.")
                pausar_e_limpar()

            elif acao == '3':
                opcao = "0"
            
        


if __name__ == "__main__":
    main()
