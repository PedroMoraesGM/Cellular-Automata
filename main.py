import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parâmetros do modelo
GRID_SIZE = 50          # Tamanho da grade
P_CRESCIMENTO = 0.05    # Probabilidade de uma árvore crescer em uma célula vazia
P_RAIO = 0.001          # Probabilidade de uma árvore ser atingida por um raio e pegar fogo
STEPS = 100             # Número de iterações da simulação

# Estados das células
VAZIO = 0
ARVORE = 1
INCENDIO = 2

# Inicialização da grade com árvores distribuídas aleatoriamente
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
# 60% das células iniciam com árvore
grid[np.random.rand(GRID_SIZE, GRID_SIZE) < 0.6] = ARVORE

def atualizar(grid):
    """Atualiza o estado da grade segundo as regras do modelo de incêndio florestal."""
    nova_grid = grid.copy()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i, j] == INCENDIO:
                # Células em incêndio se tornam vazias na próxima iteração
                nova_grid[i, j] = VAZIO
            elif grid[i, j] == ARVORE:
                # Se alguma célula vizinha está em incêndio ou se ocorrer um raio, a árvore pega fogo
                vizinho_incendiado = False
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                            if grid[ni, nj] == INCENDIO:
                                vizinho_incendiado = True
                if vizinho_incendiado or np.random.rand() < P_RAIO:
                    nova_grid[i, j] = INCENDIO
            elif grid[i, j] == VAZIO:
                # Células vazias podem gerar uma nova árvore
                if np.random.rand() < P_CRESCIMENTO:
                    nova_grid[i, j] = ARVORE
    return nova_grid

# Configuração da animação
fig, ax = plt.subplots()
# Utiliza um colormap com 3 cores para os estados
cmap = plt.get_cmap("viridis", 3)
mat = ax.matshow(grid, cmap=cmap, vmin=0, vmax=2)
plt.colorbar(mat, ticks=[VAZIO, ARVORE, INCENDIO], label="Estado")

def animar(frame):
    global grid
    grid = atualizar(grid)
    mat.set_data(grid)
    return [mat]

ani = animation.FuncAnimation(fig, animar, frames=STEPS, interval=200, repeat=False)
plt.title("Simulação de Incêndio Florestal com Autômatos Celulares")
plt.show()
