#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np

def dist(posa, posb):
        """
            Distância entre dois pontos bidimensionais.
        """

        return ((posa[0] - posb[0])**2 + (posa[1] - posb[1])**2)**0.5


class Node:

    def __init__(self, x, y, parent_id=None):
        self.pos = [x, y]
        self.parent_id = parent_id


class RTT:

    def __init__(self, x_max=800, y_max=600):
        self.nodes = []  # Lista de nodos da árvore.
        self.node_count = 0

        self.target_pos = None  # Posição que se deseja alcançar.
        self.target_radius = 0  # Raio da região em torno do ponto alvo.

        # Índice do nodo mais próximo à posição alvo na lista 'self.nodes'.
        self.nearest_node_id = None
        self.curr_dist = None  # Distância do nodo mais próximo.

        self.target_found = False

        self.x_max = x_max
        self.y_max = y_max

        self.obsts_matrix = []

        for x in range(0, self.x_max):
            self.obsts_matrix.append([])
            for y in range(0, self.y_max):
                self.obsts_matrix[x].append(False)

        self.var = 0

    def set_root(self, x, y):
        """
            Cria nodo raiz para iniciar a árvore.
        """

        if(self.node_count == 0):
            self.__add_node([x, y])
            return True
        else:
            print("Raiz já existente.")
            return False

    def generate_node_uniform(self):
        """
            Gera posição de novo nodo. Ponto aleatório obtido com distribui-
            ção uniforme.
        """

        # Gera ponto aleatório.
        rand_point = [random.randint(0, self.x_max),
                      random.randint(0, self.y_max)]

        ret_val = self.__generate_node(rand_point)
        while ret_val is False:
            rand_point = [random.randint(0, self.x_max),
                          random.randint(0, self.y_max)]

            ret_val = self.__generate_node(rand_point)

        return ret_val

    def generate_node_normal(self):
        """
            Gera posição de novo nodo. Ponto aleatório obtido com distribui-
            ção normal.
        """

        # Gera ponto aleatório.
        rand_point = [int(np.random.normal(self.target_pos[0], self.var)),
                      int(np.random.normal(self.target_pos[1], self.var))]

        ret_val = self.__generate_node(rand_point)
        while ret_val is False:
            rand_point = [int(np.random.normal(self.target_pos[0], self.var)),
                          int(np.random.normal(self.target_pos[1], self.var))]
            ret_val = self.__generate_node(rand_point)

        return ret_val

    def __generate_node(self, rand_point):
        """

        """

        # Acha nodo mais próximo.
        nearest_node_id = self.__nearest_node(rand_point)
        nearest_node_pos = self.nodes[nearest_node_id].pos

        # Cria vetor na direção do ponto aleatório.
        vec = [rand_point[0] - nearest_node_pos[0],
               rand_point[1] - nearest_node_pos[1]]
        vec_norm = np.linalg.norm(vec)

        if vec_norm == 0:
            print("Norma 0.")
            return False

        # Corrige tamanho.
        vec[0] *= (self.target_radius / 2) / vec_norm
        vec[1] *= (self.target_radius / 2) / vec_norm

        # Coloca origem no nodo mais próximo.
        vec[0] += nearest_node_pos[0]
        vec[1] += nearest_node_pos[1]
        vec[0] = int(vec[0])
        vec[1] = int(vec[1])

        if self.__pos_ok(vec):
            self.__add_node(vec, nearest_node_id)
            return [nearest_node_pos, vec]
        else:
            return False

    def __add_node(self, pos, nearest_node_id=None):
        """
            Adiciona novo nodo que será filho do nodo mais próximo da posi-
            ção aleatória criada.
        """

        new_node = Node(pos[0], pos[1], nearest_node_id)
        self.nodes.append(new_node)
        self.node_count += 1

    def update_closest_node(self):
        """
            Atualiza informação sobre nodo mais próximo da posição alvo
            e se região do alvo já foi atingida.
        """

        if(self.node_count != 0):
            for curr_node_id in range(0, self.node_count):
                curr_dist = dist(self.nodes[curr_node_id].pos, self.target_pos)
                if(curr_dist < self.curr_dist or self.curr_dist is None):
                    self.curr_dist = curr_dist
                    self.nearest_node_id = curr_node_id

            if(self.curr_dist <= self.target_radius):
                self.target_found = True
        else:
            print("Árvore vazia.")
            return None

    def __nearest_node(self, pos):
        """
            Acha nodo mais perto de 'pos'.
        """

        if(self.node_count != 0):
            nearest_node_id = 0
            min_dist = dist(self.nodes[0].pos, pos)

            for curr_node_id in range(1, self.node_count):
                curr_dist = dist(self.nodes[curr_node_id].pos, pos)
                if(curr_dist < min_dist):
                    min_dist = curr_dist
                    nearest_node_id = curr_node_id

            return nearest_node_id
        else:
            print("Árvore vazia.")
            return None

    def __pos_ok(self, pos):
        if((not (0 <= pos[0] < self.x_max)) or
                (not (0 <= pos[1] < self.y_max))):
            return False

        if(self.obsts_matrix[(pos[0])][(pos[1])]):
            return False

        return True
