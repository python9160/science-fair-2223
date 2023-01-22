from collections import defaultdict
import heapq as heap

def dijkstras(adjList, getDistance, points, source, destination):
  visited = set()
  parent = {source: source}
  pQ = []
  heap.heappush(pQ, (0, source))
  g = defaultdict(lambda: float('inf')) # f() = g() (h(n) is 0, as there is no heuristic)
  g[source] = 0

  while pQ:
    # greedy
    _, node = heap.heappop(pQ)
    if node == destination:
      break
    visited.add(node)

    for successor in adjList[node]:
      if successor not in visited:
        if g[successor] > (new := g[node] + getDistance(points, node, successor)):
          parent[successor] = node
          g[successor] = new
          heap.heappush(pQ, (new, successor))

  path = []
  current = destination
  while parent[current] != current: # this is only false for start node
    path.append(current)
    current = parent[current] # move up hierarchy
  path.append(source)
  path.reverse()
  return path