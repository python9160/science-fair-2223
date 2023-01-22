MAX = 1000
def greedy(adjList, getDistance, points, source, destination):
  current = source
  path = [source]
  i = 0
  while current != destination and i < MAX:
    current = min(adjList[current], key=lambda x: getDistance(points, x, destination))
    path.append(current)
    i += 1
  if i >= MAX:
    return -1
  return path