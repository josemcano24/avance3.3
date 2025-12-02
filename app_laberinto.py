import streamlit as st
import time
import collections
import heapq

# ==========================================
# 1. CONFIGURACIÓN Y CARGA DEL NUEVO LABERINTO
# ==========================================
st.set_page_config(page_title="Maze Solver 3.3 Final", layout="wide")

# DATOS ACTUALIZADOS (El nuevo TXT que enviaste)
RAW_MAZE_DATA = """
[1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
[1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1]
[1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1]
[1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1]
[1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1]
[1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1]
[1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1]
[1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1]
[1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1]
[1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1]
[1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1]
[1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1]
[1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1]
[1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1]
[1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1]
[1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1]
[1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1]
[1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1]
[1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1]
[1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1]
[1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1]
[1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1]
[1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1]
[1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1]
[1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1]
[1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,1]
[1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1]
[1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1]
[1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1]
[1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1]
[1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,0,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1]
[1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0]
[1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1]
[1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,1]
[1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1]
[1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1]
"""

def parse_maze_from_text(raw_data):
    """Convierte el formato [1,0,1...] a una lista de listas real."""
    grid = []
    lines = raw_data.strip().split('\n')
    for line in lines:
        # Quitamos corchetes y separamos por comas
        clean_line = line.strip().replace('[', '').replace(']', '')
        if clean_line:
            # Convertimos cada número a entero
            row = [int(num) for num in clean_line.split(',')]
            grid.append(row)
    return grid

MAZE = parse_maze_from_text(RAW_MAZE_DATA)

# Coordenadas automáticas (Inicio=0,1 | Fin=ÚltimaFila, PenúltimaColumna)
START = (0, 1) 
END = (len(MAZE)-1, len(MAZE[0])-2)

# ==========================================
# 2. ALGORITMOS DE BÚSQUEDA
# ==========================================

def solve_maze_bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = collections.deque([(start, [start])])
    visited = {start}
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end: return path
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return None

def solve_maze_dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    stack = [(start, [start])]
    visited = {start}
    while stack:
        (r, c), path = stack.pop()
        if (r, c) == end: return path
        # Orden mezclado para visualización
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))
    return None

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_maze_astar(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    pq = []
    heapq.heappush(pq, (0, start, [start]))
    visited = {start}
    g_score = {start: 0}
    while pq:
        _, (r, c), path = heapq.heappop(pq)
        if (r, c) == end: return path
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                new_g = g_score[(r, c)] + 1
                if (nr, nc) not in g_score or new_g < g_score[(nr, nc)]:
                    g_score[(nr, nc)] = new_g
                    f = new_g + heuristic((nr, nc), end)
                    heapq.heappush(pq, (f, (nr, nc), path + [(nr, nc)]))
                    visited.add((nr, nc))
    return None

# ==========================================
# 3. INTERFAZ GRÁFICA
# ==========================================

st.title("Visualizador de Algoritmo de Búsqueda en Laberinto")

def render_maze_html(maze, path=None):
    if path is None: path = []
    path_set = set(path)
    
    # HTML para visualización estilo "bloque"
    html = '<div style="font-family: monospace; line-height: 10px; font-size: 14px; white-space: pre; letter-spacing: -1px;">'
    for r in range(len(maze)):
        row_str = ""
        for c in range(len(maze[0])):
            if (r, c) == START: char = "🚀"
            elif (r, c) == END: char = "🚩"
            elif (r, c) in path_set: char = "🔹"
            elif maze[r][c] == 1: char = "⬛"
            else: char = "⬜"
            row_str += char
        html += row_str + "<br>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox("Selecciona el algoritmo", ["BFS", "DFS", "A*"])
solve_button = st.sidebar.button("Resolver Laberinto")

# Columnas
col1, col2 = st.columns([3, 1])

with col1:
    if solve_button:
        start_time = time.time()
        path = None
        
        if algorithm == "BFS":
            path = solve_maze_bfs(MAZE, START, END)
        elif algorithm == "DFS":
            path = solve_maze_dfs(MAZE, START, END)
        elif algorithm == "A*":
            path = solve_maze_astar(MAZE, START, END)
            
        end_time = time.time()
        
        if path:
            st.success(f"¡Camino encontrado con {algorithm}!")
            render_maze_html(MAZE, path)
        else:
            st.error("No se encontró solución.")
            render_maze_html(MAZE)
            
        st.session_state['stats'] = (algorithm, end_time - start_time, len(path) if path else 0)
    else:
        render_maze_html(MAZE)

with col2:
    if 'stats' in st.session_state:
        alg, t, steps = st.session_state['stats']
        st.markdown("### Métricas")
        st.metric("Algoritmo", alg)
        st.metric("Tiempo", f"{t:.6f} s")
        st.metric("Pasos", steps)
