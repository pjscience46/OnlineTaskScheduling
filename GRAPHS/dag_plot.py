import pydot
import random

# --- Step 1: Load the CSV File ---
csv_path = r"GRAPHS\n=100\daggen_output_1.csv"  # Replace with your CSV filename


# Read the file and extract lines from row 4 onward (DOT content starts here)
with open(csv_path, 'r') as f:
    lines = f.readlines()

# Build DOT data string
dot_data = "digraph G {\n" + "".join(lines[3:]) + "\n}"

# --- Step 2: Parse the DOT data ---
graphs = pydot.graph_from_dot_data(dot_data)
graph = graphs[0]

# Set global Graphviz layout parameters for spacing
graph.set_graph_defaults(
    ranksep="0.5 equally",  # vertical gap between layers
    nodesep="1.5",          # horizontal gap between nodes
    splines="true",         # use smooth curved edges
    overlap="false",        # avoid overlap
    rankdir="TB"            # top to bottom flow
)

# --- Step 3: Apply Styling ---
color_palette = ['#00C9A7', '#845EC2', '#0081CF', '#FF6F91', '#FF9671', '#FFC75F', '#F9F871']

# Style nodes
for node in graph.get_nodes():
    node.set_style("filled")
    node.set_shape("circle")
    node.set_fontcolor("white")
    node.set_fontname("Arial Bold")
    node.set_fillcolor(random.choice(color_palette))

# Style edges
for edge in graph.get_edges():
    edge.set_color("gray")
    edge.set_arrowhead("vee")
    edge.set_penwidth(2)

# --- Step 4: Export the DAG as PNG (or SVG/PDF) ---
output_path = str(csv_path)+"dag.png"
graph.write_png(output_path)
print(f"DAG saved as {output_path}")