# -*- coding: utf-8 -*-
from random import randint
from jogador import Jogador
from tabuleiro import Tabuleiro


class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        super().__init__(tabuleiro, tipo)
        self.coordenadas = [(i, j) for i in range(3) for j in range(3)]

    def posicoes_livres(self):
        return [(i, j) for i, j in self.coordenadas if self.matriz[i][j] == Tabuleiro.DESCONHECIDO ]

    def verifica_sequencias(self):
        return [ [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
                [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
                [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
        ]


    def encontra_jogada(self, jogador):
        for seq in self.verifica_sequencias():
            valores = [self.matriz[l][c] for l, c in seq]
            if valores.count(jogador) == 2 and Tabuleiro.DESCONHECIDO in valores:
                i = valores.index(Tabuleiro.DESCONHECIDO)
                return seq[i]
        return None

    def acha_oposto(self, coord):
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        opostos = [(2, 2), (2, 0), (0, 2), (0, 0)]
        
        return opostos[cantos.index(coord)]

    def marca_oposto(self):
        for coord in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            oposto = self.acha_oposto(coord)
            if (
                self.matriz[coord[0]][coord[1]] == Tabuleiro.JOGADOR_X
                and oposto
                and self.matriz[oposto[0]][oposto[1]] == Tabuleiro.DESCONHECIDO
            ):
                return oposto
        return None

    def cria_fork(self):
        for pos in self.posicoes_livres():
            self.matriz[pos[0]][pos[1]] = Tabuleiro.JOGADOR_0
            count = 0
            for seq in self.verifica_sequencias():
                valores = [self.matriz[l][c] for l, c in seq]
                if valores.count(Tabuleiro.JOGADOR_0) == 2 and Tabuleiro.DESCONHECIDO in valores:
                    count += 1
            self.matriz[pos[0]][pos[1]] = Tabuleiro.DESCONHECIDO
            if count >= 2:
                return pos
        return None

    def getJogada(self):

        jogada = self.encontra_jogada(Tabuleiro.JOGADOR_0)
        if jogada:
            return jogada


        jogada = self.encontra_jogada(Tabuleiro.JOGADOR_X)
        if jogada:
            return jogada


        jogada = self.cria_fork()
        if jogada:
            return jogada


        if self.matriz[1][1] == Tabuleiro.DESCONHECIDO:
            return (1, 1)


        jogada = self.marca_oposto()
        if jogada:
            return jogada


        for coord in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            if self.matriz[coord[0]][coord[1]] == Tabuleiro.DESCONHECIDO:
                return coord


        for coord in [(0, 1), (1, 0), (1, 2), (2, 1)]:
            if self.matriz[coord[0]][coord[1]] == Tabuleiro.DESCONHECIDO:
                return coord


        livres = self.posicoes_livres()
        if(len(livres) > 0):
            p = randint(0, len(livres)-1)
            return livres[p]

        return None
