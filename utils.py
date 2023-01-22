from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def getDistance(points, p1, p2):
  # finds distance from point p1 to p2 in points ndarray
  return np.linalg.norm(points[p1] - points[p2])

def createRandomGraph(N, K, sX, sY):

  def generateRandomAdjMat(N, K):
    n = int(N * (N-1) / 2)
    
    if K < N:
      raise ValueError(f"Number of connections (K, {K}) must be greater than number of nodes (N, {N})")
    elif K > n:
      raise ValueError(f"Number of connections (K, {K}) must be less than {n} for number of nodes (N, {N})")

    arr = np.array([0] * (n-K) + [1] * K)

    valid = False
    while not valid:
      # shuffle array
      np.random.shuffle(arr)

      # convert to upper triangle matrix
      triu = np.zeros((N, N))
      triu[np.triu_indices(N, 1)] = arr

      # check valid
      if np.all(np.sum(triu, axis=1)[:-1]):
        valid = True

    triu += triu.transpose()
    return triu

  def adjMatToList(adjMat, N):
    adjList = defaultdict(list)
    for i in range(N):
      for j in range(N):
        if adjMat[i, j] == 1:
          adjList[i].append(j)
    return dict(adjList)

  adjList = adjMatToList(generateRandomAdjMat(N, K), N)

  def createPoints(N, sX, sY):
    points = np.random.rand(N, 2)
    points[:, 0] *= sX
    points[:, 1] *= sY
    np.around(points)
    return points.astype("int32")

  points = createPoints(N, sX, sY)

  return [points, adjList]

def createRandomGraph2(N, sX, sY, maxLength):
  """
  Creates a random graph with N nodes and a maximum edge length of maxLength
  @returns points, adjList
  """
  # create random graph
  # 1. create random points
  # 2. connect all nodes together
  # 3. remove all connections longer than maxLength

  def createPoints(N, sX, sY):
    random_points = np.random.rand(N, 2)
    scaling_matrix = np.array([[sX, 0], [0, sY]])
    points = np.dot(random_points, scaling_matrix)
    return points.astype("int32")

  def createAdjList(points, maxLength):
    distances = np.sum((points[np.newaxis, :, :] - points[:, np.newaxis, :]) ** 2, axis=-1)
    adjList = {i: np.where(distances[i] <= maxLength**2)[0].tolist() for i in range(len(points))}

    connections_count = np.array([len(adjList[i]) for i in range(len(points))])
    disconnected_nodes = np.where(connections_count == 0)[0].reshape(-1,1)
    distances = np.sum((points[disconnected_nodes] - points) ** 2, axis=2)
    nearest_nodes = np.argmin(distances, axis=1).reshape(-1,1)[:, 0]

    for i, node in enumerate(disconnected_nodes):
        adjList[node].append(nearest_nodes[i])
        adjList[nearest_nodes[i]].append(node)

    return adjList

  points = createPoints(N, sX, sY)
  adjList = createAdjList(points, maxLength)

  return [points, adjList]

def visualize(points, adjList, path=None, offset=np.array([-2, -2])):
  fig, ax = plt.subplots()

  # show connections/edges
  lines = []
  for sNode in adjList.keys():
    for eNode in adjList[sNode]:
      lines.append([
        points[sNode],
        points[eNode]
      ])
  ax.add_collection(LineCollection(lines, color="black", lw=0.25, zorder=1))

  # show path
  if path:
    pLines = []
    path2 = path + [path[-1]]
    lines = [[
      points[node],
      points[path2[i+1]]
    ] for i, node in enumerate(path) if node != path2[i+1]]
    ax.add_collection(LineCollection(lines, color="blue", lw=1.5, zorder=2))

  # show nodes/vertices
  ax.scatter(points[:, 0], points[:, 1], zorder=3, s=50)

  # add text
  for i, position in enumerate(points):
    ax.annotate(i, position + offset, zorder=4, size=8)

  plt.show()

def getCost(points, path):
  path2 = path + [path[-1]]
  return sum([
    getDistance(points, path2[i], path2[i+1])
    for i in range(len(path2) - 1)
  ])