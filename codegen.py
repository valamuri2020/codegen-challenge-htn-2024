import os
import ast
import networkx as nx
import matplotlib.pyplot as plt


def parse_imports_from_file(file_path):
    """Parse a single Python file to extract base import module names with filenames."""
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            tree = ast.parse(file.read(), filename=file_path)
        except SyntaxError:
            return []  # Skip files with syntax errors

    imports = set()  # Using a set to avoid duplicates
    filename = os.path.basename(file_path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_module = alias.name.split(".")[0]  # Get the base module name
                imports.add((filename, base_module))
        elif isinstance(node, ast.ImportFrom):
            # Get the base module name
            module = node.module.split(".")[0] if node.module else None
            if module:
                imports.add((filename, module))
    return list(imports)


def parse_imports_from_codebase(codebase_path):
    """Parse all Python files in a codebase to extract base import module names."""
    all_imports = []
    for root, _, files in os.walk(codebase_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_imports = parse_imports_from_file(file_path)
                all_imports.extend(file_imports)
    return all_imports


def build_graph_with_base_modules(imports):
    """Build a graph with nodes representing base modules."""
    G = nx.DiGraph()
    for filename, module in imports:
        file_node_label = filename
        module_node_label = module

        # Add nodes for the file and the base module
        G.add_node(file_node_label)
        G.add_node(module_node_label)

        # Add an edge from the file to the module
        G.add_edge(file_node_label, module_node_label)

    return G


def visualize_graph_natural_layout(G):
    """Visualize the graph using a natural layout."""
    plt.figure(figsize=(14, 14))

    # Using a spring layout for a natural distribution of nodes
    pos = nx.spring_layout(G, k=0.5, iterations=100)

    # Determine node colors based on the number of outgoing edges
    node_colors = ["red" if G.out_degree(node) > 5 else "skyblue" for node in G.nodes()]

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, node_color=node_colors, node_size=2000, edgecolors="black"
    )

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.7, arrows=True)

    # Draw custom labels
    nx.draw_networkx_labels(
        G, pos, font_size=8, font_family="sans-serif", font_weight="bold"
    )

    plt.axis("off")
    plt.show()


# Example usage
codebase_path = "path/to/your/codebase"
codebase_path = "/Users/vivek/Desktop/Vivek-Folder/Waterloo/4A/htn/flask-examples"
all_imports = parse_imports_from_codebase(codebase_path)
G = build_graph_with_base_modules(all_imports)
visualize_graph_natural_layout(G)
