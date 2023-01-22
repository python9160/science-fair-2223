def idaStar(adjList, getDistance, points, source, destination):
  FOUND = -1 # -1 does not mean error
  NOT_FOUND = -2

  def h(n):
    return getDistance(points, n, destination)

  def search(path, g, bound):
    node = path[-1]
    f = g + h(node)
    if f > bound: return f
    if node == destination: return FOUND
    minimum = float("inf")
    for successor in adjList[node]:
      path.append(successor)
      t = search(path, g + getDistance(points, node, successor), bound)
      if t == FOUND: return FOUND
      if t < minimum: minimum = t
      path.pop(-1)
    return minimum

  bound = h(source)
  path = [source]

  while True:
    t = search(path, 0, bound)
    if t == FOUND:  return path
    if t == float("inf"): return NOT_FOUND
    bound = t

def idaStar_iterative(adjList, getDistance, points, source, destination):
    NOT_FOUND = -1

    def h(n):
        return getDistance(points, n, destination)

    stack = [(source, 0, h(source))]
    while stack:
        node, g, bound = stack.pop()
        if node == destination:
            return [node]
        f = g + h(node)
        if f > bound:
            continue
        for successor in adjList[node]:
            cost = g + getDistance(points, node, successor)
            stack.append((successor, cost, bound))

    return NOT_FOUND