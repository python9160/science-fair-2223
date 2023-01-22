def dfs(adjList, getDistance, points, source, destination):
  def _dfs(adjList, node, destination, currentPath):
    if node == destination:
      # found path
      currentPath.append(node)
      return True
    visited.add(node)
    for successor in adjList[node]:
      if successor not in visited:
        currentPath.append(node)
        if _dfs(adjList, successor, destination, currentPath):
          return True
        currentPath.pop(-1)
  
  visited = set() # to make sure it doesn't loop on itself
  currentPath = []
  _dfs(adjList, source, destination, currentPath)
  return currentPath