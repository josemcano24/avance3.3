import streamlit as st
import time
import collections
import heapq

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
st.set_page_config(page_title="Maze Solver Final 3.3", layout="wide")

# ==========================================
# 2. DEFINICIÓN DEL LABERINTO (TU NUEVA VERSIÓN)
# ==========================================
# Copiado exactamente de tu mensaje
MAZE = [
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1],
    [1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1],
    [1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1],
    [1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1],
    [1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1],
    [1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1],
    [1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1],
    [1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1],
    [1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1],
    [1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1],
    [1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1],
    [1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1],
    [1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,1],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1],
    [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1],
    [1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,1],
    [1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1],
    [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,1],
    [1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1]
]

# Definimos Inicio y Fin (Automático basado en los huecos de la primera y última fila)
START = (0, 1)  
END = (36, 30) # Fila 36, Columna 30

# ==========================================
# 3. ALGORITMOS (BFS, DFS, A*)
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
        # Orden cambiado para visualización interesante
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
# 4. INTERFAZ GRÁFICA (Visualización Clarita)
# ==========================================

st.title("Visualizador de Algoritmo de Búsqueda en Laberinto")

def render_maze_html(maze, path=None):
    if path is None: path = []
    path_set = set(path)
    
    # Renderizado HTML ajustado para que se vea denso y clarito
    html = '<div style="font-family: monospace; line-height: 10px; font-size: 14px; white-space: pre; letter-spacing: -1px;">'
    for r in range(len(maze)):
        row_str = ""
        for c in range(len(maze[0])):
            if (r, c) == START: char = "🚀"
            elif (r, c) == END: char = "🚩"
            elif (r, c) in path_set: char = "🔹"
            elif maze[r][c] == 1: char = "⬛" # Muro Negro
            else: char = "⬜" # Camino Clarito (Blanco)
            row_str += char
        html += row_str + "<br>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox("Selecciona el algoritmo", ["BFS", "DFS", "A*"])
solve_button = st.sidebar.button("Resolver Laberinto")

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
