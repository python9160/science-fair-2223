# fixes the csv file for incomplete runs
import csv

AFTER = {
  "bfs": "dfs",
  "dfs": "dijkstras",
  "dijkstras": "aStar",
  "aStar": "bidirectional",
  "bidirectional": "greedy",
  "greedy": "bfs"
}

# steps
# 1. start on first row of csv file
# 2. if some rows do not have all algorithms, delete them

# read csv file
with open('1024 copy.csv', 'r') as file:
  reader = csv.reader(file)
  data = list(reader)

deleteIndices = [] # saves indices of rows to be deleted
currentTrial = []
for i, row in enumerate(data):
  # if row is header, skip or first row
  if row[0] == "Algorithm" or i == 1:
    continue
  
  currentTrial.append(i)
  # check row after, unless it is the last row
  if i < len(data) - 1:
    if data[i + 1][0] == AFTER[row[0]]:
      continue
    else:
      # delete all rows in current trial
      deleteIndices += currentTrial
      currentTrial = []

# delete rows
for i in sorted(deleteIndices, reverse=True):
  del data[i]


# write to csv file
with open('1024 copy.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerows(data)