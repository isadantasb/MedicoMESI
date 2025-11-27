
# Simulador de Protocolo MOESI - Sistema de Prontuários Médicos

- Universidade Estadual de Maringá
- Disciplina: Arquitetura e organização de computadores II
- Curso: Ciência da Computação
- Professora: Sandra Cossul
---

Este projeto é uma implementação em **Python** de um simulador de coerência de cache utilizando o protocolo **MOESI**, desenvolvido como trabalho prático para a disciplina de Arquitetura e organização de computadores II.

Para facilitar a visualização de conceitos abstratos, o sistema utiliza uma **analogia hospitalar**: processadores são profissionais de saúde e a memória é o arquivo de pacientes.

## 1. Autores

* **Isadora Dantas Bruchmam** - RA: 140870
* **Letícia Akemi Nakahati Vieira** - RA: 140535
* **Pedro Henrique Pereira da Silva** - RA:

---

## 2. Diagrama de Estados MOESI

O protocolo MOESI garante que todos os processadores (Médicos/Enfermeiros) vejam os mesmos dados. Abaixo, um diagrama explicando o que cada sigla significa dentro do nosso simulador:

|ESTADO(Sigla) | O que significa?|
| :--- | :--- |
| M - Modified | O prontuário teve seu status alterado, a cópia anterior no arquivo central está ultrapasadda|
| O - Owned | O prontuário de determinado funcionário foi alterado, e outro funcionário leu essa alteração. O arquivo central ainda está ultrapassado, e esse funcionário é o "dono" responsável pela atualização posterior desse arquivo|
| E - Exclusive | O prontuário acabou de ser pego no arquivo, ninguém além daquele funcionário o leu ainda e o seu status é igual ao do arquivo central|
| S - Shared | Mais de um funcionário está lendo o arquivo, que é igual ao da RAM, caso alguém decida alterar, precisa "avisar" aos outros |
| I - Invalid | O status atual do paciente que está armazenado com o funcionário x é inválido. É preciso buscar a informaçãpo atualizada caso queira ler o prontuário|

### Fluxo Simplificado de Transição

```text
      (Leitura Inicial)           (Outro lê)
[ RAM ] ----------------> [ E ] ----------------> [ S ]
                           | ^                     ^ |
                           | | (Escrita Local)     | | (Outro escreve)
                           v |                     | v
                          [ M ] <---------------- [ I ]
                           | ^      (Escrita)
                           | |
            (Outro lê)     v |
                          [ O ]
```

-----

## 3. Sobre o Projeto

O objetivo deste software é demonstrar o funcionamento de sistemas multiprocessados com memória compartilhada.

  * **Processadores:** Profissionais de saúde (Médico, Enfermeiro, Farmacêutico).
  * **Memória Principal (RAM):** O arquivo central de prontuários.
  * **Cache:** A prancheta de cada profissional.
  * **Barramento:** O sistema de comunicação (Snooping).
  * **Dados:** Status do paciente (1-Triagem, 2-Atendimento, 3-Medicação, 4-Alta).

## 4. Detalhes da Implementação

  * **Linguagem:** Python 3.
  * **Política de Escrita:** Write-Back (Só escreve na RAM ao expulsar o bloco ou compartilhar dado "Sujo").
  * **Associatividade:** Cache totalmente associativa (simulada).
  * **Tamanho do Bloco:** 5 inteiros.

## 5. Estrutura dos Arquivos

1.  `Main.py`: Interface CLI e loop principal.
2.  `Barramento.py`: Implementa a lógica de *Snooping* e coerência (Onde a mágica do MOESI acontece).
3.  `Processador.py`: Agente que solicita leituras e escritas.
4.  `Cache.py` & `CacheLine.py`: Estruturas de armazenamento local.
5.  `Memoria.py`: Simulação da RAM.

## 6. Como Executar

Certifique-se de ter o Python instalado. No terminal, execute:

```bash
python Main.py
```

## 7. Interação

O sistema apresentará um menu onde você pode assumir o papel de um dos profissionais. Ao tentar ler ou escrever em um prontuário (endereço de memória 0-49), o console exibirá os logs das trocas de mensagens no barramento e as mudanças de estado MOESI.

-----

**Data de Entrega:** 30/11/2025
