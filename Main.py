import os
from Memoria import *
from Processador import *
from Barramento import *

# Função de impressão do estado geral gerada automaticamente; será revisada futuramente.
def imprimir_estado_geral(memoria, processadores):
    """
    Exibe o estado completo do sistema: RAM + Caches
    Requisito: "Deve ser possível visualizar... a qualquer momento"
    """
    print("\n" + "="*60)
    print("STATUS GERAL DO SISTEMA (MOESI)")
    print("="*60)
    
    # 1. Mostrar um resumo da RAM (apenas as primeiras 10 posições para não poluir)
    print("\n[MEMÓRIA PRINCIPAL (RAM) - Primeiras 10 Posições]")
    for i in range(10):
        val = memoria.ler(i)
        # Tradução simples só para visualização
        status = {1:"Triagem", 2:"Atendimento", 3:"Medicação", 4:"Alta"}.get(val, str(val))
        print(f"| End {i:02d}: {val} ({status}) ", end="")
        if (i+1) % 2 == 0: print("|") # Quebra de linha a cada 2
    if 10 % 2 != 0:
        print("|")  # Garante quebra de linha se número de posições for ímpar
    print("| ... (mais 40 posições ocultas) ... |")
    if memoria_tam > 10:
        print("| ... (mais 40 posições ocultas) ... |")
    else:
        print("|")

    # 2. Mostrar as Caches de cada processador
    for p in processadores:
        p.mostrar_visao_interna()
    
    print("="*60 + "\n")


def main():
    print("Inicializando o sistema de prontuários médicos...")
    ram = MemoriaPrincipal(tam=50)

    p0 = Processador(0, "Médico")
    p1 = Processador(1, "Enfermeiro")
    p2 = Processador(2, "Farmacêutico")
    lista_processadores = [p0, p1, p2]

    barramento = Barramento(ram, lista_processadores)
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
            print("1. ler um Prontuário (Consultar Status)")
            print("2. escrever em um Prontuário (Atualizar Status)")
            print("3. Voltar")
            
            acao = input("O que deseja fazer? ")

            if acao == '1': 
                    end = int(input("Digite o Nº do Prontuário (Endereço 0-49): "))
                    if 0 <= end < 50:
                        processador_atual.ler(end)
                    else:
                        print("Erro: Endereço inválido.")

            elif acao == '2': 
                end = int(input("Digite o Nº do Prontuário (Endereço 0-49): "))
                if 0 <= end < 50:
                    val = int(input("Novo Status (1-4): "))
                    if 1 <= val <= 4:
                        processador_atual.escrever(end, val)
                    else:
                        print("Erro: Status inválido (use 1 a 4).")
                else:
                    print("Erro: Endereço inválido.")

            elif acao == '3':
                opcao = "0"


if __name__ == "__main__":
    main()
