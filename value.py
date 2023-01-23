## Value statement of a hand can be a list that states the general trend of the hand (None, pair, twoPair, trips, str8, flush, fullHouse, quads, str8Flush, royFlush) and then what the kicker is (stating the highest value card of the trend if trend is 5 cards long(flush, str8))
##ex: value = {trend: flush, kicker: A}
##ex: value = {trend: 2pair, kicker: 9}
def getValueList(hand, river):
  ##both hand and river are lists
  sortedDict = getSortedDict(hand, river)
  one, two = findHighestTrend(sortedDict, hand, river)
  return [one] + two
def getSortedDict(hand, river):
  sortedDict = {'values':[], 'suits':[]}
  for x in hand:
    sortedDict['values'].append(x[0])
    sortedDict['suits'].append(x[1])
  for x in river:
    sortedDict['values'].append(x[0])
    sortedDict['suits'].append(x[1])
  return sortedDict
  
def findHighestTrend(sortedDict, hand, river):
  combinedList = hand + river
  flush, flushList = checkFlush(sortedDict)
  str8 = checkStr8(sortedDict)
  quad = checkQuads(sortedDict)
  trips = checkTrips(sortedDict)
  pairs = checkPairs(sortedDict)
  if flush != False and str8 != False:
    aboveTen = True
    same = True
    str8List = []
    for x in range(len(str8)):
      if str8[x] == 10:
        str8List.append('0')
      elif str8[x] == 11:
        str8List.append('J')
      elif str8[x] == 12:
        str8List.append('Q')
      elif str8[x] == 13:
        str8List.append('K')
      elif str8[x] == 1 or str8[x] == 14:
        str8List.append('A')
      else:
        str8List.append(str(str8[x]))
    for x in str8List:
      if x not in '0JQKA':
        aboveTen = False
      for y in combinedList:
        if y[0] == x:
          if y[1] != flush:
            same = False
    if same and aboveTen:
      return 'royFlush', [14, 13, 12, 11, 10]
    elif same and not aboveTen:
      return 'str8Flush', str8

  if quad != False:
    return 'quads', kickers(sortedDict, [quad]*4) + [quad]*4
  elif trips != False and pairs != False:
    if len(trips) == 1 and len(pairs) == 1:
      return 'fullHouse', [trips[0]]*3 + [pairs[0]]*2
    elif len(trips) == 1 and len(pairs) == 2:
      betterPair = max(pairs)
      return 'fullHouse', [trips[0]]*3 + [betterPair]*2
  elif flush != False:
    return 'flush', flushList
  elif str8 != False:
    return 'str8', str8
  elif trips != False:
    return 'trips', kickers(sortedDict, [max(trips)]*3) + [max(trips)]*3
  elif pairs != False:
    if len(pairs) > 1:
      if len(pairs) > 2:
        pairs.pop(pairs.index(min(pairs)))
      cardList = [pairs[0]]*2 + [pairs[1]]*2
      return 'twoPair', kickers(sortedDict, cardList) + cardList
    else:
      return 'pair', kickers(sortedDict, [pairs[0]]*2) + [pairs[0]]*2
  else:
    return 'None', kickers(sortedDict, [])
def kickers(sortedDict, handTrend):
  returnList = []
  values = getValues(sortedDict)
  count = 5 - len(handTrend)
  tempDict = {'values':handTrend}
  handTrend = getValues(tempDict)
  for x in handTrend:
    if x in values:
      values.remove(x)
  for x in range(len(values)):
    values[x] = int(values[x])
  for x in range(count):
    returnList.append(str(values.pop(values.index(max(values)))))
  return returnList

def checkTrips(sortedDict):
  list = sortedDict['values'].copy()
  returnList = []
  for x in list:
    if list.count(x) == 3:
      returnList.append(x)
      list.remove(x)
  if len(returnList) == 0:
    return False
  else:
    return returnList
    
def checkPairs(sortedDict):
  list = sortedDict['values'].copy()
  returnList = []
  for x in list:
    if list.count(x) == 2:
      returnList.append(x)
      list.remove(x)
  if len(returnList) == 0:
    return False
  else:
    return returnList
    
def checkQuads(sortedDict):
  list = sortedDict['values']
  for x in list:
    if list.count(x) > 3:
      return x
  return False
  
def checkFlush(sortedDict):
  values = getValues(sortedDict)
  suits = sortedDict['suits']
  spades = 0
  sList = []
  hearts = 0
  hList = []
  clubs = 0
  cList = []
  diamonds = 0
  dList = []
  for x in range(len(suits)):
    if suits[x] == 'S':
      if len(sList) > 4:
        if values[x] > min(sList):
          sList.remove(min(sList))
          sList.append(values[x])
      else:
        sList.append(values[x])
      spades += 1
    elif suits[x] == 'D':
      if len(dList) > 4:
        if values[x] > min(dList):
          dList.remove(min(dList))
          dList.append(values[x])
      else:
        dList.append(values[x])
      diamonds += 1
    elif suits[x] == 'C':
      if len(cList) > 4:
        if values[x] > min(cList):
          cList.remove(min(cList))
          cList.append(values[x])
      else:
        cList.append(values[x])
      clubs += 1
    elif suits[x] == 'H':
      if len(hList) > 4:
        if values[x] > min(hList):
          hList.remove(min(hList))
          hList.append(values[x])
      else:
        hList.append(values[x])
      hearts += 1
  if spades > 4:
    return 'S', sList
  elif hearts > 4:
    return 'H', hList
  elif diamonds > 4:
    return 'D', dList
  elif clubs > 4:
    return 'C', cList
  else:
    return False, False
    
def getValues(sortedDict):
  values = sortedDict['values'].copy()
  aceCount = 0
  for x in range(len(values)):
    if values[x] == 'J':
      values[x] = '11'
    elif values[x] == 'Q':
      values[x] = '12'
    elif values[x] == 'K':
      values[x] = '13'
    elif values[x] == 'A':
      values[x] = '14'
      aceCount += 1
    elif values[x] == '0':
      values[x] = '10'
  for x in range(aceCount):
    values.append('1')
  return values

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
  
def checkStr8(sortedDict):
  values = getValues(sortedDict)
  checker1 = ''
  checker2 = ''
  checker3 = ''
  checker = [1, 2, 3, 4, 5]
  x = 1
  while x < 11:
    condition = True
    for y in checker:
      if str(y) not in values:
        condition = False
    if condition:
      if checker1 == '':
        checker1 = checker.copy()
      elif checker2 == '':
        checker2 = checker.copy()
      elif checker3 == '':
        checker3 = checker.copy()
    x += 1
    for z in range(len(checker)):
      checker[z] = checker[z] + 1
  if checker3 != '':
    return checker3
  elif checker2 != '':
    return checker2
  elif checker1 != '':
    return checker1
  else:
    return False

