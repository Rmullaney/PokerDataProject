####across the board, cards will be in lists, where each card will be '3S', where the first char is the number value, and the second digit is the suit. 
###a ten of spades will be written as '0S'. Tens will be zeros
import value
import data
import test
def giveShuffledDeck():
  import random
  deck = ['2H', '2S', '2C', '2D', '3H', '3S', '3C', '3D', '4H', '4S', '4C', '4D', '5H', '5S', '5C', '5D', '6H', '6S', '6C', '6D', '7H', '7S', '7C', '7D', '8H', '8S', '8C', '8D', '9H', '9S', '9C', '9D', '0H', '0S', '0C', '0D', 'JH', 'JS', 'JC', 'JD', 'QH', 'QS', 'QC', 'QD', 'KH', 'KS', 'KC', 'KD', 'AH', 'AS', 'AC', 'AD']
  shuffledDeck = []
  for y in range(7):
    for card in deck:
      if random.randint(0, 10) < 6:
        shuffledDeck.append(card)
      else:
        shuffledDeck.insert(0, card)
    deck.clear()
    for card in shuffledDeck:
      if random.randint(0, 10) < 6:
        deck.append(card)
      else:
        deck.insert(0, card)
    shuffledDeck.clear()
  return deck

def getInput():
  while True:
    inp = input("How many players are there? (Max 8) ")
    if inp in '2345678' and int(inp) > 1 and int(inp) < 9:
      return int(inp)
    else:
      print("Invalid Input. Try Again")

def convertTrendToNum(trend):
  '''
  converts a trend to a ranked number
  '''
  if trend == 'None':
    return 0
  elif trend == 'pair':
    return 1
  elif trend == 'twoPair':
    return 2
  elif trend == 'trips':
    return 3
  elif trend == 'str8':
    return 4
  elif trend == 'flush':
    return 5
  elif trend == 'fullHouse':
    return 6
  elif trend == 'quads':
    return 7
  elif trend == 'str8Flush':
    return 8
  elif trend == 'royFlush':
    return 9
  else:
    return 'ERROR'

def compareHands(trend, hand1, hand2):
  '''
  Returns True if hand1 beats hand2, False if hand1 loses to hand2, and 'tie' if they tie
  '''
  hand1 = hand1.copy()
  hand2 = hand2.copy()
  for x in range(len(hand1)):
    hand1[x] = value.convertToValue(hand1[x])
  for x in range(len(hand2)):
    hand2[x] = value.convertToValue(hand2[x])
  if trend == 'None' or trend == 'flush' or trend == 'str8' or trend == 'str8Flush' or trend == 'royFlush':
    return compareKickers(hand1, hand2)
  elif trend == 'pair':
    if hand1[4] == hand2[4]:
      for x in range(2):
        hand1.pop()
        hand2.pop()
      return compareKickers(hand1, hand2)
    elif hand1[4] > hand2[4]:
      return True
    else:
      return False
  elif trend == 'trips':
    if hand1[4] == hand2[4]:
      for x in range(3):
        hand1.pop()
        hand2.pop()
      return compareKickers(hand1, hand2)
    elif hand1[4] > hand2[4]:
      return True
    else:
      return False
  elif trend == 'quads':
    if hand1[4] == hand2[4]:
      for x in range(4):
        hand1.pop()
        hand2.pop()
      return compareKickers(hand1, hand2)
    elif hand1[4] > hand2[4]:
      return True
    else:
      return False
  elif trend == 'twoPair':
    if max(hand1[2], hand1[4]) > max(hand2[2], hand2[4]):
      return True
    elif max(hand1[2], hand1[4] < max(hand2[2], hand2[4])):
      return False
    else:
      if min(hand1[2], hand1[4]) > min(hand2[2], hand2[4]):
        return True
      elif min(hand1[2], hand1[4] < min(hand2[2], hand2[4])):
        return False
      else:
        if hand1[0] > hand2[0]:
          return True
        elif hand1[0] < hand2[0]:
          return False
        else:
          return 'tie'
  elif trend == 'fullHouse':
    if hand1[0] > hand2[0]:
      return True
    elif hand1[0] < hand2[0]:
      return False
    else:
      if hand1[4] > hand2[4]:
        return True
      elif hand1[4] < hand2[4]:
        return False
      else:
        return 'tie'
def compareKickers(hand1, hand2):
  '''
  Returns True if hand1 beats hand2, False if hand1 loses to hand2, and 'tie' if they tie
  '''
  if len(hand1) < 2 and hand1[0] == hand2[0]:
    return 'tie'
  else:
    if max(hand1) == max(hand2):
      hand1.pop(hand1.index(max(hand1)))
      hand2.pop(hand2.index(max(hand2)))
      return compareKickers(hand1, hand2)
    elif max(hand1) > max(hand2):
      return True
    else:
      return False
def determineWinner(valueList):
  '''
  value list is the list of each hand's trend/value outcome.
  will return the winning index of valueList
  '''
  tempDict = {}
  for x in range(len(valueList)):
    tempDict[x] = convertTrendToNum(valueList[x][0])
  maxi = max(tempDict.values())
  indexList = []
  for x in tempDict:
    if tempDict[x] == maxi:
      indexList.append(x)
  if len(indexList) == 1:
    return indexList[0]
  else:
    newDict = {}
    trend = valueList[indexList[0]][0]
    for x in indexList:
      newDict[x] = valueList[x][1:6]
    condition = True
    while len(newDict) > 2 and condition:
      conditionTwo = True
      x = 0
      lim = len(newDict)
      while (x + 1) < lim:
        keys = getKeys(newDict)
        outcome = compareHands(trend, newDict[keys[x]], newDict[keys[x-1]])
        if outcome != 'tie':
          conditionTwo = False
          lim = lim - 1
          if outcome == True:
            newDict.pop(keys[x-1])
          else:
            newDict.pop(keys[x])
        x = x + 1
      if conditionTwo == True:
        condition = False
    keys = getKeys(newDict)
    outcome = compareHands(trend, newDict[keys[0]], newDict[keys[1]])
    if outcome == 'tie':
      return 'tie'
    else:
      if outcome:
        return keys[0]
      else:
        return keys[1]

def getKeys(dict):
  list = []
  for x in dict:
    list.append(x)
  return list

def runGame(playerCount):
  '''
  Returns the winning hand; appends all hands to appropriate data doc
  '''
  deck = giveShuffledDeck()
  playerList = []
  for x in range(playerCount):
    playerList.append([])
  for y in range(2):
    for x in range(playerCount):
      card = deck.pop(0)
      playerList[x].append(card)
  river = []
  deck.pop(0)
  for x in range(3):
    card = deck.pop(0)
    river.append(card)
  for x in range(2):
    deck.pop(0)
    card = deck.pop(0)
    river.append(card)
  playerHands = playerList.copy()
  appendHandData(playerHands, playerCount)
  for x in range(len(playerList)):
    playerList[x] = value.getValueList(playerList[x], river)
  winningIndex = determineWinner(playerList)
  if winningIndex != 'tie':
    return playerHands[winningIndex]
  else:
    return 'tie'

def getInputTwo():
  while True:
    inp = input("How many trials? (At least ten) ")
    try:
      if int(inp) > 9 and int(inp) != 0:
        return int(inp)
      else:
        print("Invalid Input")
    except:
      print("Invalid Input")

def appendHandData(list, playerCount):
  fileName = "data/" + str(playerCount) + "playersAllHands.txt"
  for x in list:
    data.appendToFile(fileName, data.cleanDataPoint(x))
  
def main():
  '''
  determines which side of the program will be run.
  '''
  userInput = input("Run data program or run play program(input D, play program not complete) [D/P]")
  if userInput == 'D':
    dataSide()
  elif userInput == 'P':
    pass #need to put this in
  else:
    print("faulty input, try again")
    main()


def dataSide():
  import time
  trialCount = getInputTwo()
  playerCount = getInput()
  fileName = "data/" + str(playerCount) + "players.txt"
  allHandsName = "data/" + str(playerCount) + "playersAllHands.txt"
  winRateName = "data/" + str(playerCount) + "handWRs.txt"
  for x in range(trialCount):
    #time.sleep(.01)
    winningHand = data.cleanDataPoint(runGame(playerCount))
    print(str(x) + ": " + winningHand)
    data.appendToFile(fileName, winningHand)
  data.sortFile(fileName)
  data.sortFile(allHandsName)
  data.winRateFileUpdate(fileName, allHandsName, winRateName)
  data.winRateFileSort(winRateName)

main()