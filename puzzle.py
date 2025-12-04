import heapq
import pygame
import sys
import time

class PuzzleState:
    def __init__(self, board, parent, move, depth, cost):
        self.board = board  
        self.parent = parent  
        self.move = move  
        self.depth = depth  
        self.cost = cost  

    def __lt__(self, other):
        return self.cost < other.cost

# Estado Obrigatório
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Movimentos
moves = {
    'U': -3,  
    'D': 3,   
    'L': -1,  
    'R': 1    
}

# Função Heurística
def get_heuristic(board, choice):
    """Calcula o custo h(n) baseado na escolha do usuário"""
    dist = 0
    
    # 1. Misplaced Tiles
    if choice == 1:
        for i in range(9):

            if board[i] != 0 and board[i] != goal_state[i]:
                dist += 1
        return dist

    # 2. Manhattan Distance
    elif choice == 2:
        for i in range(9):
            val = board[i]
            if val != 0:
              
                current_row, current_col = divmod(i, 3)
                
                target_row, target_col = divmod(val - 1, 3)
                dist += abs(current_row - target_row) + abs(current_col - target_col)
        return dist

    # 3. Euclidean Distance
    elif choice == 3:
        for i in range(9):
            val = board[i]
            if val != 0:
                current_row, current_col = divmod(i, 3)
                target_row, target_col = divmod(val - 1, 3)
               
                dist += math.sqrt((current_row - target_row)**2 + (current_col - target_col)**2)
        return dist
    
    return 0


def move_tile(board, move, blank_pos):
    new_board = board[:]
    new_blank_pos = blank_pos + moves[move]
    new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
    return new_board

# Implementação do A*
def a_star(start_state, heuristic_choice):
    open_list = []
    closed_list = set()
    
    # Custo inicial
    h_inicial = get_heuristic(start_state, heuristic_choice)
    start_node = PuzzleState(start_state, None, None, 0, h_inicial)
    
    heapq.heappush(open_list, start_node)

    nodes_count = 0

    while open_list:
        current_state = heapq.heappop(open_list)
        nodes_count += 1

        if current_state.board == goal_state:
            return current_state, nodes_count

        closed_list.add(tuple(current_state.board))

        blank_pos = current_state.board.index(0)

        for move in moves:
            # Regras de borda
            if move == 'U' and blank_pos < 3: continue
            if move == 'D' and blank_pos > 5: continue
            if move == 'L' and blank_pos % 3 == 0: continue
            if move == 'R' and blank_pos % 3 == 2: continue

            new_board = move_tile(current_state.board, move, blank_pos)

            if tuple(new_board) in closed_list:
                continue

            # g(n) = custo real (profundidade)
            g = current_state.depth + 1
            # h(n) = estimativa
            h = get_heuristic(new_board, heuristic_choice)
            # f(n) = g(n) + h(n)
            f = g + h
            
            new_state = PuzzleState(new_board, current_state, move, g, f)
            heapq.heappush(open_list, new_state)

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
    pygame.display.set_caption("Visualização A* - Final")
    
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
    
    # Caso Difícil
    initial_state = [8, 6, 7, 2, 5, 4, 3, 0, 1] 
    
    # Caso Médio
    # initial_state = [2, 8, 3, 1, 6, 4, 7, 0, 5]

    # Heuristicas 
    heuristica = 2

    print(f"Resolvendo puzzle: {initial_state}")
    print("Calculando...")
    
    start_time = time.time()
    solution, nodes = a_star(initial_state, heuristica)
    end_time = time.time()
    
    if solution:
        tempo = end_time - start_time
        print(f"Resolvido em {tempo:.4f} segundos.")
        print(f"Nós explorados: {nodes}")
        print(f"Passos da solução: {solution.depth}")
        
        caminho_visual = recuperar_caminho(solution)
        visualizar_pygame(caminho_visual)
    else:
        print("Sem solução.")