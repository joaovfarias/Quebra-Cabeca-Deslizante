import numpy as np
import random
import time
import math
class Nodo:
  def __init__(self, quebraCabeca, pai):
    self.quebraCabeca = quebraCabeca
    self.pai = pai
    self.filhos = []
    self.level = 0
    self.custo_f = 0
    self.heuristicaPosErrada = 0
    self.heuristicaDistanciaManhattan = 0

  def addFilho(self, filho):
    self.filhos.append(filho)
    return filho

class QuebraCabeca:
  def __init__(self, lado):
    self.lado = lado
    self.linhaVazio = lado-1
    self.colunaVazio = lado-1
    self.tabuleiro = np.arange(1,self.lado*self.lado+1)
    self.tabuleiro = np.reshape(self.tabuleiro,(self.lado,self.lado))
    self.tabuleiro[self.linhaVazio][self.colunaVazio] = 0

  def SetTabuleiro(self, tabuleiro, linha, coluna):
    self.linhaVazio = linha
    self.colunaVazio = coluna
    self.tabuleiro = np.array(tabuleiro)

  def Imprime(self):
    print(self.tabuleiro)

  def MovimentosPossiveis(self):
    ListaMovimentosPossiveis = []

    # Esquerda
    if self.colunaVazio > 0:
        ListaMovimentosPossiveis.append((self.linhaVazio, self.colunaVazio-1))

    # Direita
    if self.colunaVazio < (self.lado - 1):
        ListaMovimentosPossiveis.append((self.linhaVazio, self.colunaVazio+1))

    # Cima
    if self.linhaVazio > 0:
        ListaMovimentosPossiveis.append((self.linhaVazio-1, self.colunaVazio))

    # Baixo
    if self.linhaVazio < (self.lado - 1):
        ListaMovimentosPossiveis.append((self.linhaVazio+1, self.colunaVazio))

    return ListaMovimentosPossiveis

  def Embaralhar(self, vezes):
    posicaoAnterior = (self.linhaVazio,self.colunaVazio)

    for _ in range(vezes):
      posicaoSorteada = random.choice(self.MovimentosPossiveis())

      while (posicaoSorteada == posicaoAnterior):
        posicaoSorteada = random.choice(self.MovimentosPossiveis())

      posicaoAnterior = (self.linhaVazio,self.colunaVazio)
      self.FazerMovimento(posicaoSorteada)

  def FazerMovimento(self, movimento):
    temp = self.tabuleiro[movimento]
    self.tabuleiro[movimento] = 0
    self.tabuleiro[self.linhaVazio][self.colunaVazio] = temp

    self.linhaVazio = movimento[0]
    self.colunaVazio = movimento[1]

    return movimento

  def VerificarJogo(self):
    lista = self.tabuleiro.ravel().tolist()

    for i in range(len(lista)-1):
      if lista[i] != i+1:
        return False
    
    return True

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
        if pop.pai is None or (pop.pai.quebraCabeca.linhaVazio, pop.pai.quebraCabeca.colunaVazio) != movimento:
          pop.addFilho(Nodo(QuebraCabeca(pop.quebraCabeca.lado), pop))
          pop.filhos[filho].quebraCabeca.SetTabuleiro(pop.quebraCabeca.tabuleiro, pop.quebraCabeca.linhaVazio, pop.quebraCabeca.colunaVazio)
          pop.filhos[filho].quebraCabeca.FazerMovimento(movimento)
          pop.filhos[filho].level = pop.level + 1
          queue.append(pop.filhos[filho])
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
        if pop.pai is None or (pop.pai.quebraCabeca.linhaVazio, pop.pai.quebraCabeca.colunaVazio) != movimento:
          pop.addFilho(Nodo(QuebraCabeca(pop.quebraCabeca.lado), pop))
          pop.filhos[filho].quebraCabeca.SetTabuleiro(pop.quebraCabeca.tabuleiro, pop.quebraCabeca.linhaVazio, pop.quebraCabeca.colunaVazio)
          pop.filhos[filho].quebraCabeca.FazerMovimento(movimento)
          pop.filhos[filho].level = pop.level + 1
          stack.append(pop.filhos[filho])
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
          if pop.pai is None or (pop.pai.quebraCabeca.linhaVazio, pop.pai.quebraCabeca.colunaVazio) != movimento:
            pop.addFilho(Nodo(QuebraCabeca(pop.quebraCabeca.lado), pop))
            pop.filhos[filho].quebraCabeca.SetTabuleiro(pop.quebraCabeca.tabuleiro, pop.quebraCabeca.linhaVazio, pop.quebraCabeca.colunaVazio)
            pop.filhos[filho].quebraCabeca.FazerMovimento(movimento)
            stack.append(pop.filhos[filho])
            pop.filhos[filho].level = pop.level + 1
            filho += 1

  return None
   
def GerarArvoreIDS(root, end):
  for i in range(end+1):
    resultado = GerarArvoreDLS(root, i)
    if resultado is not None:
      return resultado

  return None

def GerarArvoreAStarPosErrada(root):
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
            pop.filhos[filho].quebraCabeca.SetTabuleiro(pop.quebraCabeca.tabuleiro, pop.quebraCabeca.linhaVazio, pop.quebraCabeca.colunaVazio)
            pop.filhos[filho].quebraCabeca.FazerMovimento(movimento)
            pop.filhos[filho].level = pop.level + 1
            pop.filhos[filho].heuristicaPosErrada = HeuristicaPosErrada(pop.filhos[filho])
            pop.filhos[filho].custo_f = pop.filhos[filho].level + pop.filhos[filho].heuristicaPosErrada
            
            heap.append(pop.filhos[filho])
            filho += 1

    return None

def GerarArvoreAStarDistanciaManhattan(root):
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
            pop.filhos[filho].quebraCabeca.SetTabuleiro(pop.quebraCabeca.tabuleiro, pop.quebraCabeca.linhaVazio, pop.quebraCabeca.colunaVazio)
            pop.filhos[filho].quebraCabeca.FazerMovimento(movimento)
            pop.filhos[filho].level = pop.level + 1
            pop.filhos[filho].heuristicaDistanciaManhattan = HeuristicaDistanciaManhattan(pop.filhos[filho])
            pop.filhos[filho].custo_f = pop.filhos[filho].level + pop.filhos[filho].heuristicaDistanciaManhattan
            
            heap.append(pop.filhos[filho])
            filho += 1

    return None


def HeuristicaDistanciaManhattan(nodo):
    lista = nodo.quebraCabeca.tabuleiro.ravel().tolist()

    distanciaManhattan = 0

    for i in range(len(lista)):
        if lista[i] != 0:
            linhaAtual = i // nodo.quebraCabeca.lado
            linhaEsperada = (lista[i] - 1) // nodo.quebraCabeca.lado

            colunaAtual = i % nodo.quebraCabeca.lado
            colunaEsperada = (lista[i] - 1) % nodo.quebraCabeca.lado

            distanciaManhattan += abs(  linhaAtual - linhaEsperada ) + abs( colunaAtual - colunaEsperada )

    return distanciaManhattan

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

  print(nodo.quebraCabeca.tabuleiro)
  print("") 
  print("".join("  " for _ in range(math.ceil(nodo.quebraCabeca.lado / 2))) + "↓")
  print("")

def main():
    lado = int(input("Informe o tamanho do lado do quebra-cabeça: "))
    embaralhar = int(input("Informe o número de embaralhamentos: "))

    quebraCabecaInicial = QuebraCabeca(lado)
    quebraCabecaInicial.Embaralhar(embaralhar)
    raiz = Nodo(quebraCabecaInicial, None)

    flag = 1

    while (flag):
        print("-----------------------------------------------------")
        print("1- Busca em largura")
        print("2- Busca em profundidade")
        print("3- Busca em profundidade limitada")
        print("4- Busca em profundidade iterativa")
        print("5- Busca A* com heurística de peças fora do lugar")
        print("6- Busca A* com heurística de distância de Manhattan")
        print("7- Sair")
        ans = int(input("Opcão: "))
        print("-----------------------------------------------------")
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
                limite = int(input("Limite para iteraçao: "))
                start = time.time()
                MostrarCaminho(GerarArvoreIDS(raiz, limite), -1)
                end = time.time()
                print(f"Tempo: {end - start}s")
            case 5:
                start = time.time()
                MostrarCaminho(GerarArvoreAStarPosErrada(raiz), -1)
                end = time.time()
                print(f"Tempo: {end - start}s")
            case 6:
                start = time.time()
                MostrarCaminho(GerarArvoreAStarDistanciaManhattan(raiz), -1)
                end = time.time()
                print(f"Tempo: {end - start}s")
            case 7:
                flag = 0
            case _:
                print("Valor inválido")

if __name__ == "__main__":
    main()