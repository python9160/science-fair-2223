from algorithms.aStar import aStar
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstras import dijkstras
from algorithms.bidirectional import bidirectional
from algorithms.greedy import greedy

import signal
import sys
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
  ("aStar", aStar),
  ("bidirectional", bidirectional),
  ("bfs", bfs),
  ("dijkstras", dijkstras),
  ("dfs", dfs),
  ("greedy", greedy)
]

HEADER = ["Trial", "bfs", "bfs (cost)", "dfs", "dfs (cost)", "dijkstras", "dijkstras (cost)", "aStar", "aStar (cost)", "bidirectional", "bidirectional (cost)", "greedy", "greedy (cost)"]

N = 1024
maxLength = 25
sX = 400
sY = 400

def getDataLength(file="1024.csv"):
  # print number of lines in csv file
  with open(file, 'r') as file:
    reader = csv.reader(file)
    row_count = sum(1 for row in reader)
    return row_count - 1

def saveData(data):
  # append data to csv file in excel format
  with open('1024.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    # add header if empty
    if os.stat('1024.csv').st_size == 0:
      writer.writerow(HEADER)
    writer.writerows(data)
data = [] # list of data to be written to csv file

saveData(data)

i = 0
try:
  limit = sys.argv[1]
except IndexError:
  limit = 10000

if limit == "forever":
  limit = None
else:
  limit = int(limit)

while on and ((i < limit) if limit != None else True):
  currentData = [getDataLength() + len(data)] + [None] * (len(HEADER) - 1) # add len(data) to account for data that has not been written to csv file
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

    # save data
    currentData[HEADER.index(name)] = end - start
    currentData[HEADER.index(name + " (cost)")] = -1 # default cost to -1
    if path != -1 and type(path) == list and len(path) > 0:
      currentData[HEADER.index(name + " (cost)")] = getCost(points, path) # if valid path, save cost

  data.append(currentData)

  # save data to csv file if data is 1000 points or above
  if len(data) >= 1000:
    saveData(data)
    data = []

  # clear console
  os.system('cls')
  # print number of trials and progress if limit is not None
  print(f"Trial {i + 1}")
  if limit != None:
    print(f"{(i + 1) / limit * 100}%")
  print("-" * round(200 * (len(data) / 1000)))

  i += 1

saveData(data)

# print number of trials in 1024.csv
print(f"Number of trials: {getDataLength()}")

sys.exit()