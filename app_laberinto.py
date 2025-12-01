import streamlit as st
import time
# Importamos las nuevas funciones
from maze_solver import MAZE, START, END, solve_maze_bfs, solve_maze_dfs, solve_maze_astar

st.set_page_config(page_title="Maze Solver 3.3", layout="wide")

st.title("Visualizador de Algoritmos de Búsqueda (Avance 3.3)")
st.markdown("Implementación de **BFS**, **DFS** y **A*** sobre el nuevo laberinto.")

def render_maze(maze, path=None):
    if path is None:
        path = []
    
    # Usamos un estilo más compacto para el laberinto grande
    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, col in enumerate(row):
            if (r_idx, c_idx) == START:
                display_row.append("🚀") 
            elif (r_idx, c_idx) == END:
                display_row.append("🏁") 
            elif (r_idx, c_idx) in path:
                display_row.append("🔹") 
            elif col == 1:
                display_row.append("⬛") 
            else:
                display_row.append("⬜") 
        # Unir sin espacios para que se vea más compacto en el laberinto grande
        display_maze.append("".join(display_row))
    
    # Ajustamos el line-height para que se vea cuadrado
    st.markdown(
        f"<div style='font-family: monospace; line-height: 10px; font-size: 10px;'>{'<br>'.join(display_maze)}</div>", 
        unsafe_allow_html=True
    )

# --- SIDEBAR ---
st.sidebar.header("Configuración")
algorithm = st.sidebar.selectbox(
    "Selecciona el algoritmo", 
    ["BFS (Búsqueda en Amplitud)", "DFS (Búsqueda en Profundidad)", "A* (A-Star)"]
)
solve_button = st.sidebar.button("Resolver Laberinto")

# Layout de columnas para ver laberinto y estadísticas
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Visualización")
    if solve_button:
        start_time = time.time()
        path = None
        
        # Selección de algoritmo
        if "BFS" in algorithm:
            path = solve_maze_bfs(MAZE, START, END)
        elif "DFS" in algorithm:
            path = solve_maze_dfs(MAZE, START, END)
        elif "A*" in algorithm:
            path = solve_maze_astar(MAZE, START, END)
            
        end_time = time.time()
        execution_time = end_time - start_time

        if path:
            render_maze(MAZE, path)
            st.success(f"¡Camino encontrado con éxito!")
        else:
            render_maze(MAZE)
            st.error("No se encontró solución.")
            
        # Guardar datos en session state para que no se borren al recargar
        st.session_state['exec_time'] = execution_time
        st.session_state['path_len'] = len(path) if path else 0
        st.session_state['algo_used'] = algorithm
    else:
        render_maze(MAZE)

with col2:
    st.subheader("Métricas")
    if 'exec_time' in st.session_state and solve_button:
        st.metric(label="Algoritmo", value=st.session_state['algo_used'].split()[0])
        st.metric(label="Tiempo de Ejecución", value=f"{st.session_state['exec_time']:.6f} s")
        st.metric(label="Pasos en el camino", value=st.session_state['path_len'])
    else:
        st.info("Presiona 'Resolver' para ver las estadísticas.")
