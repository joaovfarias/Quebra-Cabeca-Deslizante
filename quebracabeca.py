import numpy as np
import random
import time

class Nodo:
  def __init__(self, quebraCabeca, pai):
    self.quebraCabeca = quebraCabeca
    self.pai = pai
    self.filhos = []
    self.level = 0
    self.custo_f = 0
    self.heuristicaPosErrada = 0

  def addFilho(self, filho):
    self.filhos.append(filho)
    return filho

class QuebraCabeca:
  def __init__(self, lado):
    self.lado = lado
    self.LinhaVazio = lado-1
    self.ColunaVazio = lado-1
    self.tabuleiro = np.arange(1,self.lado*self.lado+1)
    self.tabuleiro = np.reshape(self.tabuleiro,(self.lado,self.lado))
    self.tabuleiro[self.LinhaVazio][self.ColunaVazio] = 0

  def SetTabuleiro(self, tabuleiro, linha, coluna):
    self.LinhaVazio = linha
    self.ColunaVazio = coluna
    self.tabuleiro = np.array(tabuleiro)

  def Imprime(self):
    print(self.tabuleiro)

  def MovimentosPossiveis(self):
    ListaMovimentosPossiveis = []

    # Para Esquerda
    if self.ColunaVazio > 0:
        ListaMovimentosPossiveis.append((self.LinhaVazio, self.ColunaVazio-1))

    # Para Direita
    if self.ColunaVazio < (self.lado - 1):
        ListaMovimentosPossiveis.append((self.LinhaVazio, self.ColunaVazio+1))

    # Para cima
    if self.LinhaVazio > 0:
        ListaMovimentosPossiveis.append((self.LinhaVazio-1, self.ColunaVazio))

    # Para baixo
    if self.LinhaVazio < (self.lado - 1):
        ListaMovimentosPossiveis.append((self.LinhaVazio+1, self.ColunaVazio))

    return ListaMovimentosPossiveis

  def Embaralhar(self, vezes):
    posicaoAnterior = (self.LinhaVazio,self.ColunaVazio)

    for i in range(vezes):
      posicaoSorteada = random.choice(self.MovimentosPossiveis())

      while (posicaoSorteada == posicaoAnterior):
        posicaoSorteada = random.choice(self.MovimentosPossiveis())

      posicaoAnterior = (self.LinhaVazio,self.ColunaVazio)
      self.FazerMovimento(posicaoSorteada)

  def FazerMovimento(self, movimento):
    temp = self.tabuleiro[movimento]
    self.tabuleiro[movimento] = 0
    self.tabuleiro[self.LinhaVazio][self.ColunaVazio] = temp

    self.LinhaVazio = movimento[0]
    self.ColunaVazio = movimento[1]

    return movimento

  def VerificarJogo(self):
    resolvido = QuebraCabeca(self.lado)
    return np.array_equal(resolvido.tabuleiro, self.tabuleiro)

def GerarArvoreBFS(root):
    queue = []
    queue.append(root)
    while(queue):
      pop = queue.pop(0)
      if (pop.quebraCabeca.VerificarJogo()):
        return pop
      mv = pop.quebraCabeca.MovimentosPossiveis()

      filho = 0
      for movimento in mv:
        if pop.pai is None or (pop.pai.quebraCabeca.LinhaVazio, pop.pai.quebraCabeca.ColunaVazio) != movimento:
          pop.addFilho(Nodo(QuebraCabeca(pop.quebraCabeca.lado), pop))
          pop.filhos[filho].quebraCabeca.SetTabuleiro(pop.quebraCabeca.tabuleiro, pop.quebraCabeca.LinhaVazio, pop.quebraCabeca.ColunaVazio)
          pop.filhos[filho].quebraCabeca.FazerMovimento(movimento)
          queue.append(pop.filhos[filho])
          pop.filhos[filho].level = pop.level + 1
          filho += 1

def GerarArvoreDFS(root):
    stack = []
    stack.append(root)
    while(stack):
      pop = stack.pop(-1)
      if (pop.quebraCabeca.VerificarJogo()):
        return pop
      mv = pop.quebraCabeca.MovimentosPossiveis()

      filho = 0
      for movimento in mv:
        if pop.pai is None or (pop.pai.quebraCabeca.LinhaVazio, pop.pai.quebraCabeca.ColunaVazio) != movimento:
          pop.addFilho(Nodo(QuebraCabeca(pop.quebraCabeca.lado), pop))
          pop.filhos[filho].quebraCabeca.SetTabuleiro(pop.quebraCabeca.tabuleiro, pop.quebraCabeca.LinhaVazio, pop.quebraCabeca.ColunaVazio)
          pop.filhos[filho].quebraCabeca.FazerMovimento(movimento)
          stack.append(pop.filhos[filho])
          pop.filhos[filho].level = pop.level + 1
          filho += 1

def GerarArvoreDLS(root, levelLimit):
  stack = []
  stack.append(root)

  while(stack):
     pop = stack.pop(-1)

     if (pop.quebraCabeca.VerificarJogo()):
        return pop
     
     if (pop.level < levelLimit):
        mv = pop.quebraCabeca.MovimentosPossiveis()

        filho = 0
        for movimento in mv:            
          if pop.pai is None or (pop.pai.quebraCabeca.LinhaVazio, pop.pai.quebraCabeca.ColunaVazio) != movimento:
            pop.addFilho(Nodo(QuebraCabeca(pop.quebraCabeca.lado), pop))
            pop.filhos[filho].quebraCabeca.SetTabuleiro(pop.quebraCabeca.tabuleiro, pop.quebraCabeca.LinhaVazio, pop.quebraCabeca.ColunaVazio)
            pop.filhos[filho].quebraCabeca.FazerMovimento(movimento)
            stack.append(pop.filhos[filho])
            pop.filhos[filho].level = pop.level + 1
            filho += 1

  return None

def GerarArvoreAStar(root):
    heap = []

    heap.append(root)

    while heap:
        heap.sort(key=lambda x: x.custo_f)
        pop = heap.pop(0)

        if pop.quebraCabeca.VerificarJogo():
            return pop

        movimentos_possiveis = pop.quebraCabeca.MovimentosPossiveis()

        filho = 0
        for movimento in movimentos_possiveis:
            pop.addFilho(Nodo(QuebraCabeca(pop.quebraCabeca.lado), pop))
            pop.filhos[filho].quebraCabeca.SetTabuleiro(pop.quebraCabeca.tabuleiro, pop.quebraCabeca.LinhaVazio, pop.quebraCabeca.ColunaVazio)
            pop.filhos[filho].quebraCabeca.FazerMovimento(movimento)
            pop.filhos[filho].level = pop.level + 1
            pop.filhos[filho].heuristicaPosErrada = HeuristicaPosErrada(pop.filhos[filho])
            pop.filhos[filho].custo_f = pop.filhos[filho].level + pop.filhos[filho].heuristicaPosErrada
            heap.append(pop.filhos[filho])
            filho += 1

    return None

def HeuristicaPosErrada(nodo):
    lista = nodo.quebraCabeca.tabuleiro.ravel().tolist()

    posicoesErradas = 0

    for i in range(len(lista)-1):
      if lista[i] != i+1:
        posicoesErradas += 1

    return posicoesErradas

def MostrarCaminho(nodo, passos):
  if (not nodo):
    if (passos == -1):
       print("Caminho não encontrado")
       return
    print("Passos até resoluçao: " + str(passos))
    print("")
    return

  MostrarCaminho(nodo.pai, passos+1)

  if nodo.pai == None:
    print("Estado inicial: ")
  print(nodo.quebraCabeca.tabuleiro)
  print("")


def main():
    lado = 4
    quebraCabecaInicial = QuebraCabeca(lado)
    quebraCabecaInicial.Embaralhar(15)
    
    raiz = Nodo(quebraCabecaInicial, None)

    flag = 1

    while (flag):
        print("1- Busca em largura")
        print("2- Busca em profundidade")
        print("3- Busca em profundidade limitada")
        print("4- Busca A*")
        print("5- Sair")
        ans = int(input("Opcão: "))
        match ans:
            case 1:
                start = time.time()
                MostrarCaminho(GerarArvoreBFS(raiz), -1)
                end = time.time()
                print(f"Tempo: {end - start}s")
            case 2:
                start = time.time()
                MostrarCaminho(GerarArvoreDFS(raiz), -1)
                end = time.time()
                print(f"Tempo: {end - start}s")
            case 3:
                ll = int(input("Limite: "))
                start = time.time()
                MostrarCaminho(GerarArvoreDLS(raiz, ll), -1)
                end = time.time()
                print(f"Tempo: {end - start}s")
            case 4:
                start = time.time()
                MostrarCaminho(GerarArvoreAStar(raiz), -1)
                end = time.time()
                print(f"Tempo: {end - start}s")
            case 5:
                flag = 0
            case _:
                print("Valor inválido")



if __name__ == "__main__":
    main()