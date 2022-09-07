from collections import defaultdict
from typing import Sequence


def optimize_strokes(strokes: Sequence[Sequence]) -> list:
    """
    Perform stroke optimization using a version of DFS.

    The main differense is that instead of visiting
    all the vertices the algorithm visits all edges
    to ensure that all the lines contained in the initial
    strokes are included in the optimized version.
    It is archieved by removing visited edges directly
    from the adjacency list.

    Args:
        strokes (:obj:`Sequence` of :obj:`Sequence`):
            List of strokes to optimize. A stroke is
            a sequence of graph vertices.

    Returns:
        list: Optimized strokes.

    """
    adjlist = adj_list(strokes)
    strokes = []
    for p in adjlist:
        if len(adjlist[p]) > 0:
            strokes.append([p])
            dfs(adjlist, p, strokes)
    return strokes


def dfs(adjlist: defaultdict(set), p, strokes: list):
    branch = 0
    # While p has incident not visited edges
    while len(adjlist[p]) > 0:
        # Remove the edge from the adjacency list
        p_next = adjlist[p].pop()
        adjlist[p_next].remove(p)

        if branch > 0:
            strokes.append([p, p_next])  # Add to the current stroke
        else:
            strokes[-1].append(p_next)   # Start a new stroke

        dfs(adjlist, p_next, strokes)    # Go to the next vertex
        branch += 1


def adj_list(strokes: Sequence[Sequence]) -> defaultdict(set):
    adjlist = defaultdict(set)
    for path in strokes:
        for i in range(1, len(path)):
            adjlist[path[i - 1]].add(path[i])
            adjlist[path[i]].add(path[i - 1])
    return adjlist
