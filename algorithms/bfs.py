def bfs(adjList, getDistance, points, source, destination,):
  queue = [(source,[source])]
  visited = set()

  while queue:
    vertex, path = queue.pop(0)
    visited.add(vertex)
    for node in adjList[vertex]:
      if node == destination:
        return path + [destination]
      else:
        if node not in visited:
          visited.add(node)
          queue.append((node, path + [node]))