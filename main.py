#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rtt import RTT
from rtt import dist
import pygame
import sys

if(len(sys.argv) == 3 or len(sys.argv) == 4):
    try:
        target_radius = int(sys.argv[1])
    except:
        print("Primeiro argumento deve ser inteiro.")
        sys.exit()

    random_type = str(sys.argv[2])
    if(random_type not in ["uniform", "normal"]):
        print("Segundo argumento deve ser \'uniform\' ou \'normal\'.")
        sys.exit()

    if(random_type == "uniform" and len(sys.argv) == 4):
        print("Para \'uniform\' primeiro argumento deve ser inteiro.")
        print("Não existe segundo parâmetro.")
        sys.exit()

    if(random_type == "normal"):
        try:
            var = float(sys.argv[3])
        except:
            print("Terceiro argumento deve ser número.")
            sys.exit()
else:
    print("Primeiro argumento deve ser inteiro.")
    print("Segundo argumento deve ser \'uniform\' ou \'normal\'.")
    print("Terceiro argumento deve ser número, variância quando usar " +
          "\'normal\'.")
    sys.exit()

(WIDTH, HEIGHT) = (800, 600)

# PyGame.
pygame.display.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
achou_filename = 'achou.png'
achou = pygame.image.load(achou_filename).convert_alpha()
pygame.display.set_caption("RTT")

# Inicializa árvore.
rtt = RTT(WIDTH, HEIGHT)
rtt.target_radius = target_radius
if(random_type == "normal"):
    rtt.var = var

button_down = False
run_game_loop = True
start_ok = False
obsts = False
ready = False
while run_game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game_loop = False
            break
        elif event.type == pygame.MOUSEBUTTONUP and not ready and not obsts:
            if not start_ok:
                pos = pygame.mouse.get_pos()
                rtt.set_root(pos[0], pos[1])
                pygame.draw.circle(screen, (0, 255, 0), rtt.nodes[0].pos,
                                   rtt.target_radius)
                start_ok = True
            elif start_ok:
                rtt.target_pos = pygame.mouse.get_pos()
                pygame.draw.circle(screen, (255, 0, 0), rtt.target_pos,
                                   rtt.target_radius)
                obsts = True
        elif event.type == pygame.MOUSEBUTTONUP and button_down and obsts:
            button_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN and obsts or button_down:
            button_down = True
            circle = pygame.mouse.get_pos()
            pygame.draw.circle(screen, (0, 0, 255), circle, 4)

            for x in range(circle[0] - 4, circle[0] + 4):
                for y in range(circle[1] - 4, circle[1] + 4):
                    if(0 <= x < rtt.x_max and 0 <= y < rtt.y_max):
                        rtt.obsts_matrix[x][y] = True

        elif event.type == pygame.KEYDOWN and not ready:
            if event.key == pygame.K_RETURN:
                obsts = False
                ready = True

    if not run_game_loop:
        break

    if(not rtt.target_found and ready):
        if(random_type == "uniform"):
            new_branch = rtt.generate_node_uniform()
        else:
            new_branch = rtt.generate_node_normal()

        rtt.update_closest_node()
        pygame.draw.line(screen, (64, 64, 64), new_branch[0], new_branch[1])

        if(rtt.target_found):
            curr_node_id = rtt.nearest_node_id
            curr_node_pos = rtt.nodes[curr_node_id].pos
            curr_parent_id = rtt.nodes[curr_node_id].parent_id
            curr_parent_pos = rtt.nodes[curr_parent_id].pos

            path_nodes_count = 0
            while curr_parent_id != 0:
                pygame.draw.line(screen, (0, 255, 0),
                                 curr_node_pos, curr_parent_pos, 4)

                curr_node_id = curr_parent_id
                curr_node_pos = curr_parent_pos
                curr_parent_id = rtt.nodes[curr_node_id].parent_id
                curr_parent_pos = rtt.nodes[curr_parent_id].pos

                path_nodes_count += 1

            screen.blit(achou, (WIDTH / 2 - 200, HEIGHT / 2 - 50))
            print(str(str(rtt.node_count) + " nodos gerados."))
            print(str(str(path_nodes_count) + " nodos no caminho."))

    pygame.display.update()
