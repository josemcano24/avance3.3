import collections
import heapq

# --- 1. CONFIGURACIÓN DEL NUEVO LABERINTO ---

# Copié el contenido exacto de tu archivo de texto aquí para que no tengas errores de lectura
MAZE_STRING = """
10111111111111111111111111111111
10100010001000000000100000000011
10101010101111101110111011111011
10001000101000001010000010001001
11111111101011111011111110101111
10000000101000001000001000100011
11101111101011101011101111101011
10001000001010001010001000001011
10111011111110111010111011111111
10100010001000100010001010000001
10101110101011101111101010111111
10101000100010001000101010001011
10101010111110101011101011101011
10001010100010101000000010001001
10111110101010101011111110111111
10000010101010101000100010000011
11111010101010101110101011111011
10000010001010101000101000001011
10111110111010101111101110101011
10001000100010100000000010101011
11101111101111101111111110101011
10101000001000101000100000101011
10101011111010101010101111111011
10101000100010101010001000000011
10101110101110111010111011111111
10001000101010001010100010000011
10111011101011101011101110111011
10001000001000101000001000100011
11101110111011101011111010111011
10100010000010001010000010001001
10111010111110111010111111101111
10100010100000101010100010001011
10101111101111101010101010111011
10100000101000001010101000101001
10111110101010111011101111101011
10000000001010000000000000000001
11111111111111111111111111111101
"""

def parse_maze(maze_str):
    grid = []
    for line in maze_str.strip().split('\n'):
        # Convertir caracteres a enteros: '1' -> 1 (Muro), '0' -> 0 (Camino)
        row = [int(ch) for ch in line.strip()]
        grid.append(row)
    return grid

MAZE = parse_maze(MAZE_STRING)

# Definimos Inicio y Fin basados en los huecos del laberinto texto
# Fila 0, columna 1 tiene un '0'
START = (0, 1) 
# Última fila, penúltima columna tiene un '0'
END = (len(MAZE)-1, len(MAZE[0])-2)


# --- 2. ALGORITMOS DE BÚSQUEDA ---

def solve_maze_bfs(maze, start, end):
    """Búsqueda en Amplitud (BFS) - Cola"""
    rows, cols = len(maze), len(maze[0])
    queue = collections.deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        (curr_row, curr_col), path = queue.popleft() # FIFO

        if (curr_row, curr_col) == end:
            return path

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_row, next_col = curr_row + dr, curr_col + dc
            if 0 <= next_row < rows and 0 <= next_col < cols and \
               maze[next_row][next_col] == 0 and (next_row, next_col) not in visited:
                visited.add((next_row, next_col))
                queue.append(((next_row, next_col), path + [(next_row, next_col)]))
    return None

def solve_maze_dfs(maze, start, end):
    """Búsqueda en Profundidad (DFS) - Pila"""
    rows, cols = len(maze), len(maze[0])
    stack = [(start, [start])] # Usamos lista como Pila
    visited = set()
    visited.add(start)

    while stack:
        (curr_row, curr_col), path = stack.pop() # LIFO

        if (curr_row, curr_col) == end:
            return path

        # En DFS el orden de exploración afecta el camino visualmente
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_row, next_col = curr_row + dr, curr_col + dc
            if 0 <= next_row < rows and 0 <= next_col < cols and \
               maze[next_row][next_col] == 0 and (next_row, next_col) not in visited:
                visited.add((next_row, next_col))
                stack.append(((next_row, next_col), path + [(next_row, next_col)]))
    return None

def heuristic(a, b):
    """Distancia Manhattan para A*"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_maze_astar(maze, start, end):
    """Algoritmo A* (A-Star) - Cola de Prioridad"""
    rows, cols = len(maze), len(maze[0])
    # Heap almacena: (f_score, (row, col), path)
    priority_queue = []
    heapq.heappush(priority_queue, (0, start, [start]))
    
    visited = set()
    visited.add(start)
    
    g_score = {start: 0}

    while priority_queue:
        current_f, (curr_row, curr_col), path = heapq.heappop(priority_queue)

        if (curr_row, curr_col) == end:
            return path

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_row, next_col = curr_row + dr, curr_col + dc
            
            if 0 <= next_row < rows and 0 <= next_col < cols and maze[next_row][next_col] == 0:
                new_g = g_score[(curr_row, curr_col)] + 1
                
                if (next_row, next_col) not in g_score or new_g < g_score[(next_row, next_col)]:
                    g_score[(next_row, next_col)] = new_g
                    f = new_g + heuristic((next_row, next_col), end)
                    heapq.heappush(priority_queue, (f, (next_row, next_col), path + [(next_row, next_col)]))
                    visited.add((next_row, next_col))
    return None
