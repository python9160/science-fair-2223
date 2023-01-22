def aStar(adjList, getDistance, points, source, destination):
  def h(n):
    return getDistance(points, n, destination)

  frontier = set([source])
  explored = set()
  g = {} # saves cost of path to start node, g(n)
  parent = {}

  g[source] = 0
  parent[source] = source

  while len(frontier) > 0:
    current = None

    # find lowest f() successor
    for oNode in frontier:
      if current is None or g[oNode] + h(oNode) < g[current] + h(current):
        current = oNode # assign to current
    
    if current != destination:
      for successor in adjList[current]:
        cost = getDistance(points, current, successor)
        if successor not in frontier and successor not in explored:
          # add to openSet
          frontier.add(successor)
          parent[successor] = current
          g[successor] = g[current] + cost

        else: # successor is in frontier or has been explored
          if g[successor] > g[current] + cost: # existing path is suboptimal
            # replace with better path
            g[successor] = g[current] + cost
            parent[successor] = current

            if current in explored: 
              # recheck
              explored.remove(current)
              frontier.add(current)
    else:
      path = []
      while parent[current] != current: # this is only false for start node
        path.append(current)
        current = parent[current] # move up hierarchy
      path.append(source)
      path.reverse()
      return path

    # move current from frontier to explored
    frontier.remove(current)
    explored.add(current)