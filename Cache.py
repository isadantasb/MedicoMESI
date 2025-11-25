from CacheLine import CacheLine

class Cache:
    def __init__(self, tamanho=5):
        self.elementos: list[CacheLine] = [CacheLine() for _ in range(tamanho)]
        self.topo = 0
        self.tam_max = tamanho
        self.qtd = 0

    def busca(self, endereco):
        #busca um elemento dentro da cache pelo endereço buscado
        for elemento in self.elementos:
            if elemento.endereco == endereco and elemento.protocolo != "I":
                return elemento
        return None
    
    def vazia(self) -> bool: 
        return self.qtd == 0
    
    def cheia(self) -> bool:
        return self.qtd == self.tam_max
    
    def remove(self):
        #na vdd ela n ta removendo nada, só ta retornando o topo, quem vai remover de verdade é o Processador.
        if self.cheia():
            rem = self.elementos[self.topo]
            self.qtd -=1
            return rem
    
    def insere(self, x: CacheLine):
        #se tiver vazia ou tiver espaço vazio só insere. Mas se o topo estiver ocupado tem que remover (e add ele na MP) e ai sim inserir
        if self.cheia():
            self.remove()
        self.elementos[self.topo] = x
        self.topo = (self.topo + 1) % self.tam_max
        self.qtd +=1

    def printar_cache(self):
        print("---- CACHE ----")
        for i, linha in enumerate(self.elementos):
            print(f"Linha {i}: {linha.printar()}")
        print("----------------")
        