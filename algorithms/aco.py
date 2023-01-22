from collections import defaultdict
import random

α = 0.5 # pheromone level importance
Q = 1 # pheromone deposit amount
ρ = 0.2 # evaporation rate
bonus = 1 # pheromone deposited on path to destination
iterations = 100
antCount = 100

# ant colony optimization algorithm
def aco(adjList, getDistance, points, source, destination):
  # intialize pheromone levels
  # use functions to get and set pheromone levels

  # defaultdict with defaultvalue .1
  pheromoneLevels = defaultdict(lambda: 0.1)

  def getPheromoneLevel(node1, node2):
    return pheromoneLevels[(node1, node2)]

  def setPheromoneLevel(node1, node2, value):
    # do both so order doesn't matter
    pheromoneLevels[(node1, node2)] = value
    pheromoneLevels[(node2, node1)] = value

  # initialize ants
  ants = [[source]] * antCount

  # run iterations
  for _ in range(iterations):
    destPaths = []
    pheromoneDeposited = []
    # move ants
    for antI, ant in enumerate(ants):
      current = ant[-1]
      if current == destination:
        destPaths.append(ant)
        # move ant to source
        ants[antI] = [source]
        continue

      probablities = []
      possible = [node for node in adjList[current] if node not in ant]
      for node in possible:
        probablities.append(
          (getPheromoneLevel(current, node) ** α) * (getDistance(points, current, node) ** (1 - α))
        )

      if len(possible) == 0:
        # move ant to source
        ants[antI] = [source]
        continue

      # choose next node
      nextNode = random.choices(possible, probablities)[0]

      # deposit pheromone
      pheromoneDeposited.append((current, nextNode))
        
      # move ant
      ant.append(nextNode)

    # update pheromone levels
    for node1 in adjList.keys():
      for node2 in adjList[node1]:
        # check if pheromone was deposited
        Δτ = 0
        if (node1, node2) in pheromoneDeposited or (node2, node1) in pheromoneDeposited:
          Δτ = Q / getDistance(points, node1, node2)

        # evaporate pheromone
        τ = (1-ρ) * getPheromoneLevel(node1, node2) + Δτ
        setPheromoneLevel(node1, node2, τ)
    for path in destPaths:
      # deposit pheromone
      for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]
        setPheromoneLevel(node1, node2, getPheromoneLevel(node1, node2) + bonus)


  # find path with highest pheromone level
  path = [source]
  current = source
  while current != destination:
    # find next node in path
    nextNode = None
    maxPheromoneLevel = 0

    for node in [node for node in adjList[current] if node not in path]:
      if (new := getPheromoneLevel(current, node)) > maxPheromoneLevel:
        nextNode = node
        maxPheromoneLevel = new

    current = nextNode
    path.append(current)
  
  return path