# graph-utilities
a collection of scripts for exploring mathematical properties of graphs such as symmetry, or optimal edge-covering paths

Supply graph information in comma separated node index pairs, one for each edge, in a csv "edges.csv."
Optionally for 3d/2d frameworks, supply coordinates in order of node index in "nodes.csv."

- "autgrp.py" computes the automorphisms of the graph. Use the generated "graphSym.png" as a visual aid.
- "postman.py" computes the solution to the route inspection problem.
- "vertex cover.py" computes a shortest collection of cycles that cover all vertices.

May require:
- pynauty
- pulp
- networkx
- pygraphviz
