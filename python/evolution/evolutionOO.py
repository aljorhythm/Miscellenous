# evolution OO
import random
import string
import operator

alphabetsList = list(string.ascii_lowercase)

class Evolution:
  def __init__(self, startStr, target, noOfMorphs, similarityPercentage, topPercentage):
    self.startStr = startStr.ljust(len(target))
    self.target = target
    self.noOfMorphs = int((topPercentage / 100.0) * noOfMorphs) + 1
    self.similarityPercentage = float(similarityPercentage)
    self.topPercentage = float(topPercentage) 
    
  def set_verbose(bool):
    if bool:
        def default_callback(data):
            print data  
            
  def set_callback(self, event, callback):
    setattr(self, 'callback_' + event, callback)
   
  def callback(self, event, morphs):
    if hasattr(self, 'callback_' + event):
        callback_assigned = getattr(self, 'callback_' + event)
        if callback_assigned is not None:
          callback_assigned(morphs)
        
  def start(self):
    oldMorphArr = self.processMorphs(self.generateMorphs(self.startStr))
    counter = 0
    while True:
        counter = counter + 1
        print "generation " , counter
        newMorphArr = []
        for inputStr in oldMorphArr:
            morphArr = generateMorphs(inputStr, noOfMorphs)
            self.callback('generatedMorphs', morphArr)
            morphArr = processMorphs(morphArr, target, similarityPercentage, topPercentage, noOfMorphs)
            self.callback('processedMorphs', morphArr)
            newMorphArr.extend(morphArr)
        
        print "extended "
        print newMorphArr
        print "selected extended"
        newMorphArr = self.processMorphs(newMorphArr)
  def generateMorphs(self, inputStr):
    targetLen = len(inputStr)
    charArr = list(inputStr)
    # generate morphs
    morphArr = []
    for x in xrange(self.noOfMorphs):
        # copy array for morphing
        newCharArr = list(charArr)
        # get positions of characters to morph
        numOfPositions = random.randrange(targetLen)
        positions = random.sample(range(targetLen), numOfPositions)
        global alphabetsList
        for position in positions:
            # new character for position
            newChar = random.choice(alphabetsList)
            newCharArr[position] = newChar
        morphArr.append(''.join(newCharArr))
    return morphArr
  def processMorphs(self, morphArr):
    # use topPercentage to calculate number of morphs to be kept
    selectedNoOfMorphs = int((topPercentage / 100.0) * noOfMorphs) + 1
    morphArr[:] = [ [morphed, (Evolution.similaritiesPercentage(morphed, target))] for i, morphed in enumerate(morphArr) if (Evolution.similaritiesPercentage(morphed, target)) > similarityPercentage ] 
    # print "metadata:",morphArr
    # sort
    getcount = operator.itemgetter(1)
    map(getcount, morphArr)
    morphArr = sorted(morphArr, key=getcount, reverse=True)
    morphArr = morphArr[0:noOfMorphs]
    # remove metadata
    for idx, withMeta in enumerate(morphArr):
        morphArr[idx] = withMeta[0]
    # print "without:",morphArr
    return morphArr

  events = ['processedMorphs', 'generatedMorphs']

  @staticmethod
  def setDefaultCallbacks(evolution):
    for event in Evolution.events:
      print 'hi ' + event
      def callback(data):
        print 'default callback | event: ' + event +' | data: ' + data
      print 'hello callback_' + event
      setattr(evolution, 'callback_' + event , callback)

  @staticmethod
  def similaritiesPercentage(comp, target):
    return (float(Evolution.countSameChars(comp, target)) / float(len(target))) * 100         
  @staticmethod
  def countSameChars(comp, target):
    counter = 0
    comp = list(comp)
    target = list(target)
    # compare available characters (length of shorter string)
    maxLen = len(comp) if len(comp) < len(target) else len(target)
    for x in xrange(maxLen): 
        if target[x] == comp[x]:
            counter += 1
    return counter
startStr = "a"
target = "abcdefghijklmnopqrstuvwxyz"
noOfMorphs = 3
similarityPercentage = 10
topPercentage = 30
evo = Evolution(startStr, target, noOfMorphs, similarityPercentage, topPercentage)
Evolution.setDefaultCallbacks(evo)
for event in Evolution.events:    
  evo.callback(event, "DATA")
# evo.start()
