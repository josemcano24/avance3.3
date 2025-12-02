import streamlit as st
import pandas as pd
import time
import collections
import heapq

# ==========================================
# 1. CONFIGURACIÓN Y DATOS DEL LABERINTO
# ==========================================

st.set_page_config(page_title="Maze Solver Final", layout="wide")

# Laberinto exacto del archivo txt
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
    lines = maze_str.strip().split('\n')
    for line in lines:
        clean_line = line.strip()
        if clean_line:
            row = [int(ch) for ch in clean_line]
            grid.append(row)
    return grid

MAZE = parse_maze(MAZE_STRING)
START = (0, 1)  # Coordenada del inicio (fila 0, col 1)
END = (35, 30)  # Coordenada del final (fila 35, col 30)

# ==========================================
# 2. ALGORITMOS DE BÚSQUEDA
# ==========================================

def solve_maze_bfs(maze, start, end):
    """BFS: Búsqueda en Amplitud (Cola)"""
    rows, cols = len(maze), len(maze[0])
    if maze[start[0]][start[1]] == 1: return None
    
    queue = collections.deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        (curr_row, curr_col), path = queue.popleft()
        if (curr_row, curr_col) == end: return path

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_row + dr, curr_col + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return None

def solve_maze_dfs(maze, start, end):
    """DFS: Búsqueda en Profundidad (Pila)"""
    rows, cols = len(maze), len(maze[0])
    if maze[start[0]][start[1]] == 1: return None
    
    stack = [(start, [start])]
    visited = set()
    visited.add(start)

    while stack:
        (curr_row, curr_col), path = stack.pop()
        if (curr_row, curr_col) == end: return path

        # Orden invertido para explorar visualmente interesante
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
            nr, nc = curr_row + dr, curr_col + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))
    return None

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_maze_astar(maze, start, end):
    """A*: A-Star (Cola de Prioridad)"""
    rows, cols = len(maze), len(maze[0])
    if maze[start[0]][start[1]] == 1: return None
    
    pq = []
    heapq.heappush(pq, (0, start, [start]))
    visited = set()
    visited.add(start)
    g_score = {start: 0}

    while pq:
        _, (curr_row, curr_col), path = heapq.heappop(pq)
        if (curr_row, curr_col) == end: return path

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_row + dr, curr_col + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                new_g = g_score[(curr_row, curr_col)] + 1
                if (nr, nc) not in g_score or new_g < g_score[(nr, nc)]:
                    g_score[(nr, nc)] = new_g
                    f = new_g + heuristic((nr, nc), end)
                    heapq.heappush(pq, (f, (nr, nc), path + [(nr, nc)]))
                    visited.add((nr, nc))
    return None

# ==========================================
# 3. INTERFAZ GRÁFICA (STREAMLIT)
# ==========================================

st.title("Visualizador de Algoritmos (Entrega Final 3.3)")
st.markdown("Implementación de **BFS**, **DFS** y **A***.")

def render_maze_html(maze, path=None):
    if path is None: path = []
    path_set = set(path)
    
    html = '<div style="font-family: monospace; line-height: 10px; font-size: 10px; white-space: pre;">'
    for r in range(len(maze)):
        row_str = ""
        for c in range(len(maze[0])):
            if (r, c) == START: char = "🚀"
            elif (r, c) == END: char = "🏁"
            elif (r, c) in path_set: char = "🔹"
            elif maze[r][c] == 1: char = "⬛"
            else: char = "⬜"
            row_str += char
        html += row_str + "<br>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Controles")
algo_choice = st.sidebar.selectbox("Algoritmo", ["BFS", "DFS", "A*"])
run_btn = st.sidebar.button("Resolver Laberinto")

col1, col2 = st.columns([3, 1])

with col1:
    if run_btn:
        start_time = time.time()
        
        path = None
        if algo_choice == "BFS":
            path = solve_maze_bfs(MAZE, START, END)
        elif algo_choice == "DFS":
            path = solve_maze_dfs(MAZE, START, END)
        elif algo_choice == "A*":
            path = solve_maze_astar(MAZE, START, END)
            
        end_time = time.time()
        
        if path:
            st.success(f"¡Solución encontrada con {algo_choice}!")
            render_maze_html(MAZE, path)
        else:
            st.error("No se encontró solución (Revisa Start/End).")
            render_maze_html(MAZE)
            
        st.session_state['res'] = (algo_choice, end_time - start_time, len(path) if path else 0)
    else:
        st.info("Presiona Resolver para iniciar.")
        render_maze_html(MAZE)

with col2:
    st.subheader("Métricas")
    if 'res' in st.session_state:
        alg, t, pas = st.session_state['res']
        st.metric("Algoritmo", alg)
        st.metric("Tiempo", f"{t:.6f} s")
        st.metric("Pasos", pas)
