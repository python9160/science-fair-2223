def bidirectional(adjList, getDistance, points, source, destination):
  # Get dictionary of currently active vertices with their corresponding paths.
  frontier = {source: [source], destination: [destination]}
  # Vertices we have already examined.
  explored = set()

  while len(frontier) > 0:

    # Make a copy of active vertices so we can modify the original dictionary as we go.
    active_vertices = list(frontier.keys())
    for vertex in active_vertices:
      # Get the path to where we are.
      current_path = frontier[vertex]
      # Record whether we started at start or goal.
      origin = current_path[0]
      # Check for new neighbours.
      current_neighbours = set(adjList[vertex]) - explored
      # Check if our neighbours hit an active vertex
      if len(current_neighbours.intersection(active_vertices)) > 0:
        for meeting_vertex in current_neighbours.intersection(active_vertices):
          # Check the two paths didn't start at same place. If not, then we've got a path from start to goal.
          if origin != frontier[meeting_vertex][0]:
            # Reverse one of the paths.
            frontier[meeting_vertex].reverse()
            # return the combined results
            return frontier[vertex] + frontier[meeting_vertex]

      # No hits, so check for new neighbours to extend our paths.
      if len(set(current_neighbours) - explored - set(active_vertices))  == 0:
        # If none, then remove the current path and record the endpoint as inactive.
        frontier.pop(vertex, None)
        explored.add(vertex)
      else:
        # Otherwise extend the paths, remove the previous one and update the inactive vertices.
        for neighbour_vertex in current_neighbours - explored - set(active_vertices):
          frontier[neighbour_vertex] = current_path + [neighbour_vertex]
          active_vertices.append(neighbour_vertex)
        frontier.pop(vertex, None)
        explored.add(vertex)