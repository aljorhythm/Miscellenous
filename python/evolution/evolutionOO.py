#evolution OO
class Evolution:
  def __init__(self,startStr,target,noOfMorphs,similarityPercentage,topPercentage):
    self.startStr = startStr.ljust(len(target))
    self.target = target
    self.noOfMorphs = int((topPercentage / 100.0) * noOfMorphs) + 1
    self.similarityPercentage = float(similarityPercentage)
    self.topPercentage = float(topPercentage) 
    
  def set_verbose(bool):
    if bool:
        def default_callback(data):
            print data  
            
  def set_callback(self,event,callback):
    setattr(self, 'callback_'.join([event]), callback)
   
  def callback(self,event,morphs):
    if hasattr(self, 'callback_'.join([event])):
        callback = getattr(self, 'callback_'.join([event]))
        if callback is not None:
          self.callback(morphs)
        
  def start(self):
    oldMorphArr = processMorphs(generateMorphs(self.startStr),target,similarityPercentage,topPercentage,noOfMorphs)
    counter = 0
    while True:
        counter = counter + 1
        print "generation " , counter
        newMorphArr = []
        for inputStr in oldMorphArr:
            morphArr = generateMorphs(inputStr,noOfMorphs)
            self.callback('generatedMorphs',morphArr)
            morphArr = processMorphs(morphArr,target,similarityPercentage,topPercentage,noOfMorphs)
            self.callback('processedMorphs',morphArr)
            newMorphArr.extend(morphArr)
        
        print "extended "
        print newMorphArr
        print "selected extended"
        newMorphArr = processMorphs(newMorphArr,target,similarityPercentage,topPercentage,noOfMorphs)
        print newMorphArr
        if(target in newMorphArr):
          return counter
        oldMorphArr = newMorphArr
        
  def generateMorphs(self,inputStr):
    targetLen = len(inputStr)
    charArr = list(inputStr)
    #generate morphs
    morphArr = []
    for x in xrange(self.noOfMorphs):
        #copy array for morphing
        newCharArr = list(charArr)
        #get positions of characters to morph
        numOfPositions = random.randrange(targetLen)
        positions = random.sample(range(targetLen),numOfPositions)
        for position in positions:
            global alphabetsList
            #new character for position
            newChar = random.choice(alphabetsList)
            newCharArr[position] = newChar
        morphArr.append(''.join(newCharArr))
    return morphArr
  def processMorphs(morphArr):
    #use topPercentage to calculate number of morphs to be kept
    selectedNoOfMorphs = int((topPercentage / 100.0) * noOfMorphs) + 1
    morphArr[:] = [ [morphed,(similaritiesPercentage(morphed,target))] for i,morphed in enumerate(morphArr) if (similaritiesPercentage(morphed,target)) > similarityPercentage ] 
    #print "metadata:",morphArr
    #sort
    getcount = operator.itemgetter(1)
    map(getcount, morphArr)
    morphArr = sorted(morphArr, key=getcount,reverse=True)
    morphArr = morphArr[0:noOfMorphs]
    #remove metadata
    for idx, withMeta in enumerate(morphArr):
        morphArr[idx] = withMeta[0]
    #print "without:",morphArr
    return morphArr

  events = ['processedMorphs','generatedMorphs']

  @staticmethod
  def setDefaultCallbacks(evolution):
     for event in events:
        def callback(data):
            print event,data
        setAttr(evolution,'callback_'.join([event]),callback)
        
startStr = ""
target = "abcdefghijklmnopqrstuvwxyz"
noOfMorphs = 3
similarityPercentage = 20
topPercentage = 20
evo = Evolution(startStr,target,noOfMorphs,similarityPercentage,topPercentage)
Evolution.setDefaultCallbacks(evo)    