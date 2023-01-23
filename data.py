##1) function to reformat a hand to be more suitable for storage: ['AS', 'KH'] --> 'AKN', where N at the end means not suited, and S at the end would mean suited. For data purposes, the specific suit does not actually matter - only whether the hand is suited or nonsuited This function would also ensure that there are no duplicates like '73S' and '37S'(taken care of by ordering which is addressed next) which are the same hand in a different order. All hands will have highercard, lowercard, N/S. pockets will obviously be samenum, samenum, N


def convertToValue(card):
  if card == '0':
    return 10
  elif card == 'J':
    return 11
  elif card == 'Q':
    return 12
  elif card == 'K':
    return 13
  elif card == 'A':
    return 15
  else:
    return int(card)
  

def cleanDataPoint(raw):
  if raw == 'tie':
    return 'TTT'
  else:
    value = raw[0][0] + raw[1][0]
    suits = raw[0][1] + raw[1][1]
    if suits[0] == suits[1]:
      suits = 'S'
    else:
      suits = 'N'
    a = convertToValue(value[0])
    b = convertToValue(value[1])
    if a < b:
      value = value[1] + value[0]
    collective = value + suits
    return collective
##2) NOTE: pocket hands, like AA and KK will inherently have a lower frequency within the data, due to the fact that they will occur less than all of the combined options of 73 or 0J. Should account for this somewhere. If I am to calculate winrates, this would mess up my assumption that all hands occur the same number of times
##3) function to open a data file based on the number of players and append data; helper function to see whether that data point already exists; if it does, do not add duplicate data point - just add a count next to it:    'AKN1' --> 'AKN2'

def appendToFile(fileName, dataPoint):
  file = open(fileName, 'r')
  masterList = file.readlines()
  file.close()
  file = open(fileName, 'w')
  inList = False
  for x in masterList:
    if x != '\n':
      if x[0:3] == dataPoint:
        try:
          count = int(x.strip()[3:])
        except ValueError:
          count = 1
        x = x[0:3] + str(count+1) + "\n"
        inList = True
      file.write(x)
  if not inList:
    file.write("\n")
    file.write(dataPoint + '1')
  file.close()
      

##4) additional, optional functions to analyze data

def sortByCount(list, startIndex, version):
  dict = {}
  for x in list:
    y = x.strip()[startIndex:]
    if y not in dict:
      dict[y] = [x]
    else:
      dict[y].append(x)
  return runThruKeys(dict, version)
def runThruKeys(dict, version):
  '''
  version will be a or b
  
  this function is taking the dictionary, which currently stores each hand for a certain win rate/occurrence count(works for WR file and other files), and popping and returning the highest Key value and then running the function over with the popped dict. The list stored at that highest key value will be what's returned. Thus, the final returned list will just be the original list, but in order
  
  function needs to function differently based on whether the number values are ints or floats
  a will be for ints(non-WR file sorting)
  b will be for floats(WR file sorting)
  
  '''
  keys = getKeys(dict)
  if version == 'a':
    keysCopy = []
    for x in keys:
      keysCopy.append(int(x))
    maxi = str(max(keysCopy))
  elif version == 'b':
    keysCopy = []
    for x in keys:
      keysCopy.append(float(x))
    maxi = str(max(keysCopy))
  if len(dict) == 1:
    return dict[keys[0]]
  else:
    thing = dict[maxi]
    dict.pop(maxi)
    return thing + runThruKeys(dict, version)
    
def getKeys(dict):
  list = []
  for x in dict:
    list.append(x)
  return list

def sortFile(fileName):
  file = open(fileName, 'r')
  masterList = file.readlines()
  file.close()
  if '\n' not in masterList[-1]:
    masterList[-1] = masterList[-1] + "\n"
  nList = []
  sList = []
  tie = ''
  for x in masterList:
    if x[2] == 'N':
      nList.append(x)
    elif x[2] == 'S':
      sList.append(x)
    elif x[2] == 'T':
      tie = x
  nList = sortByCount(nList, 3, 'a')
  sList = sortByCount(sList, 3, 'a')
  bigList = [tie] + sList + nList
  file = open(fileName, 'w')
  for x in bigList:
    file.write(x)


##4.5) function set to show win rates of each hand (win/total occurrence) * 100

#the win rate for each player count has different meaning. 45% WR for AAN in 2 players is illogical, but for 8 players its really good. Essentially, if all hands had an equal probability to win, the win percent for all hands should be around (100/playerCount). For 2 players, the win rate percent would be 50 percent ish for all hands, and for 8 players it would be around 12.5 percent. However, because all hands have different odds at winning, this is not the case. Thus, a specific hand's difference from the average win rate is how good it is. A 45% win rate hand for 2 players is 5% below the average 50%, so it is a decently bad hand. However, for 8 players, a 45% winrate hand is 32.5% above the average win rate of 12.5%, which means that it is a truly exceptional hand.

def winRateFileUpdate(fileNameWins, fileNameAll, fileNameWR):
  fileWins = open(fileNameWins, 'r')
  masterListWins = fileWins.readlines()
  fileWins.close()
  fileAll = open(fileNameAll, 'r')
  masterListAll = fileAll.readlines()
  fileAll.close()
  handDict = {}
  ##### dict key: {A5S: [all, wins, percent]}
  for x in masterListAll:
    y = x.strip()
    handDict[y[0:3]] = [y[3:]]
  for x in masterListWins:
    y = x.strip()
    if y[0:3] != 'TTT':
      handDict[y[0:3]].append(y[3:])
  for x in handDict:
    try:
      handDict[x].append((int(handDict[x][1]) / int(handDict[x][0])) * 100)
    except IndexError:
      handDict[x].append('0')
      handDict[x].append(0)
  fileWR = open(fileNameWR, 'w')
  for x in handDict:
    fileWR.write(x + ": " + str(round(handDict[x][2], 3)) + "\n")
  fileWR.close()

def winRateFileSort(winRateFile):
  file = open(winRateFile, 'r')
  masterList = file.readlines()
  file.close()
  masterList = sortByCount(masterList, 5, 'b')
  file = open(winRateFile, 'w')
  for x in masterList:
    file.write(x[0:5] + x[5:])
  file.close()
