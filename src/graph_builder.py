import collections
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

FIG_SIZE = (12, 8)
LAYOUT_K = 0.5
LAYOUT_ITER = 50
NODE_SIZE = 2000
FONT_SIZE = 10
ARROW_SIZE = 20
DPI = 150

def load_test_graph_from_txt(filepath: str) -> dict[str, list[str]]:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Тестовый файл графа не найден: {filepath}")
    
    graph_data = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            pkg, deps = line.split(":", 1)
            pkg = pkg.strip()
            dep_list = deps.strip().split()
            graph_data[pkg] = dep_list
    return graph_data


def build_transitive_graph(start_package: str, get_deps_func) -> nx.DiGraph:
    graph = nx.DiGraph()
    queue = collections.deque([start_package])
    visited = set([start_package])

    while queue:
        current_pkg = queue.popleft()
        
        try:
            dependencies = get_deps_func(current_pkg)
        except ValueError:
            dependencies = []

        for dep in dependencies:
            graph.add_edge(current_pkg, dep)
            if dep not in visited:
                visited.add(dep)
                queue.append(dep)
                
    return graph


def draw_and_save_graph(graph: nx.DiGraph, output_file: str) -> None:
    plt.figure(figsize=FIG_SIZE)
    
    pos = nx.spring_layout(graph, k=LAYOUT_K, iterations=LAYOUT_ITER)
    
    nx.draw(
        graph, pos, 
        with_labels=True, 
        node_color="lightblue", 
        edge_color="gray",
        node_size=NODE_SIZE, 
        font_size=FONT_SIZE,
        font_weight="bold",
        arrows=True,
        arrowsize=ARROW_SIZE
    )
    
    plt.title(f"Граф зависимостей")
    plt.tight_layout()
    plt.savefig(output_file, format="png", dpi=DPI)
    plt.close()
    print(f"Граф успешно сохранен в файл: {output_file}")