from algorithms.aStar import aStar
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstras import dijkstras
from algorithms.bidirectional import bidirectional
from algorithms.greedy import greedy

import signal
from sys import exit
import time
from utils import *

# import libraries for csv file
import csv
import os

# handle ctrl+c so we can exit gracefully
on = True
def handler(signum, frame):
  global on
  print("Exiting...")
  on = False
signal.signal(signal.SIGINT, handler)

# define algorithms
algorithms = [
  ("bfs", bfs),
  ("dfs", dfs),
  ("dijkstras", dijkstras),
  ("aStar", aStar),
  ("bidirectional", bidirectional),
  ("greedy", greedy)
]

N = 1024
maxLength = 25
sX = 400
sY = 400

def saveData(data):
  # append data to csv file in excel format
  with open('1024.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    # add header if empty
    if os.stat('1024.csv').st_size == 0:
      writer.writerow(["Algorithm", "Time (ms)", "Cost"])
    writer.writerows(data)

  # print number of lines in csv file
  with open('1024.csv', 'r') as file:
    reader = csv.reader(file)
    row_count = sum(1 for row in reader)
    print("Number of lines in csv file: " + str(row_count - 1))
    # print number of trials
    print("Number of trials: " + str((row_count - 1) / len(algorithms)))
data = [] # list of data to be written to csv file

saveData(data)

while on:
  # create random graph
  [points, adjList] = createRandomGraph2(N, sX, sY, maxLength)

  # create start and end points
  source = np.random.randint(0, N)
  destination = np.random.randint(0, N)
  while source == destination:
    destination = np.random.randint(0, N)

  # run algorithms
  for name, algorithm in algorithms:
    # save time
    start = time.perf_counter()
    path = algorithm(adjList, getDistance, points, source, destination)
    end = time.perf_counter()

    if path == -1 or type(path) != list:
      print("              Path not found: " + name)
      data.append([name, (end - start) * 1000, -1])
    else:
      try:   
        data.append([name, (end - start) * 1000, getCost(points, path)])
      except:
        data.append([name, (end - start) * 1000, -1])

    # save data to csv file if data is 1000 points or above
    if len(data) >= 1000:
      saveData(data)
      data = []

saveData(data)

exit()