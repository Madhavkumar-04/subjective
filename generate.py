import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()
nodes = [
    "Frontend\n(HTML, Tailwind CSS)",
    "Flask Backend\n(Python 3.11, Flask 2.3.3)",
    "MySQL Database\n(Aiven Cloud)",
    "NLP Module\n(NLTK, scikit-learn, Sentence Transformers)"
]
G.add_nodes_from(nodes)
edges = [
    ("Frontend\n(HTML, Tailwind CSS)", "Flask Backend\n(Python 3.11, Flask 2.3.3)", {"label": "HTTP Requests"}),
    ("Flask Backend