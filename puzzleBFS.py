import heapq
import pygame
import sys
import time
from collections import deque

class PuzzleState:
    def __init__(self, board, parent, move, depth):
        self.board = board  
        self.parent = parent  
        self.move = move  
        self.depth = depth  

# Estado Obrigatório
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Movimentos
moves = {
    'U': -3,  
    'D': 3,   
    'L': -1,  
    'R': 1    
}

def move_tile(board, move, blank_pos):
    new_board = board[:]
    new_blank_pos = blank_pos + moves[move]
    new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
    return new_board

# Implementação da BFS
def bfs(start_state):
   
    queue = deque()
    visited = set()
    
    start_node = PuzzleState(start_state, None, None, 0)
    
    queue.append(start_node)
    visited.add(tuple(start_state))

    nodes_count = 0

    while queue:
        
        current_state = queue.popleft() 
        nodes_count += 1

        # Verifica Objetivo
        if current_state.board == goal_state:
            return current_state, nodes_count

        blank_pos = current_state.board.index(0)

        for move in moves:
            # Regras de borda
            if move == 'U' and blank_pos < 3: continue
            if move == 'D' and blank_pos > 5: continue
            if move == 'L' and blank_pos % 3 == 0: continue
            if move == 'R' and blank_pos % 3 == 2: continue

            new_board = move_tile(current_state.board, move, blank_pos)
            board_tuple = tuple(new_board)

            # Se não visitou, adiciona na fila
            if board_tuple not in visited:
                visited.add(board_tuple)
                
                new_state = PuzzleState(new_board, current_state, move, current_state.depth + 1)
                queue.append(new_state)

    return None, nodes_count

# --- Visualizador PYGAME ---

def recuperar_caminho(solution_node):
    """Transforma a lista encadeada de pais em uma lista de tabuleiros"""
    path = []
    current = solution_node
    while current:
        path.append(current.board)
        current = current.parent
    path.reverse()
    return path

def visualizar_pygame(path_states):
    pygame.init()
    LARGURA, ALTURA = 400, 400
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Visualização BFS - Final")
    
    # Cores e Fonte
    BRANCO = (240, 240, 240)
    CINZA_ESCURO = (50, 50, 50)
    LARANJA = (255, 140, 0) 
    AZUL = (0, 120, 215)
    
    font = pygame.font.Font(None, 80)
    tam_celula = LARGURA // 3
    
    print("Iniciando animação...")
    
    for estado in path_states:
        screen.fill(CINZA_ESCURO)
        
        for i in range(9):
            row, col = divmod(i, 3)
            val = estado[i]
            
            if val != 0:
                x = col * tam_celula
                y = row * tam_celula
                
                # Desenha bloco
                rect = pygame.Rect(x + 5, y + 5, tam_celula - 10, tam_celula - 10)
                pygame.draw.rect(screen, AZUL, rect, border_radius=8)
                
                # Desenha número
                text = font.render(str(val), True, BRANCO)
                text_rect = text.get_rect(center=(x + tam_celula/2, y + tam_celula/2))
                screen.blit(text, text_rect)
        
        pygame.display.flip()
        time.sleep(0.6) # Velocidade da animação
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Método Main
if __name__ == "__main__":

    print("Digite os 9 números (0-8) separados por espaço:")
    input_str = input()

    try:
        initial_state = [int(n) for n in input_str.split()]
        
        if len(initial_state) != 9:
            raise ValueError("O puzzle deve ter 9 elementos.")

    except ValueError as e:
        initial_state = [0, 2, 3,
                         1, 4, 8,  
                         7, 6, 5]
        
        
    print(f"Resolvendo puzzle com BFS: {initial_state}")
    print("Calculando...")
    
    start_time = time.time()
    solution, nodes = bfs(initial_state)
    end_time = time.time()
    
    if solution:
        tempo = end_time - start_time
        
        # --- Lógica Adicionada Aqui ---
        moves_list = []
        temp_node = solution
        # Percorre de trás pra frente (filho -> pai)
        while temp_node.parent is not None:
            moves_list.append(temp_node.move)
            temp_node = temp_node.parent
        moves_list.reverse() # Inverte para ordem correta
        
        print("\n" + "="*40)
        print(f"ESTATÍSTICAS DA SOLUÇÃO (BFS)")
        print("="*40)
        print(f"Tempo: {tempo:.4f} segundos.")
        print(f"Nós explorados: {nodes}")
        print(f"Profundidade: {solution.depth}")
        print("-" * 40)
        print(f"CAMINHO FEITO (Movimentos):")
        print(f"{moves_list}")
        print("="*40 + "\n")
        # -----------------------------
        
        print("Abrindo visualização...")
        
        caminho = recuperar_caminho(solution)
        visualizar_pygame(caminho)
    else:
        print("Falha. Sem solução encontrada.")