import random
import string
import operator
#conditions:
#similarityPercentage
#topPercentage

alphabetsList = list(string.ascii_lowercase)

#type conversions and validation before proper computing
def roll(inputStr,target,noOfMorphs,similarityPercentage,topPercentage):
    if len(inputStr) > len(target):
        print "input string is longer than target string"
        return

    inputStr = inputStr.ljust(len(target))
    print "before: '" + inputStr + "' target: '" + target +"'" ,"number of morphs:", noOfMorphs, "morphs, begin! "
    similarityPercentage = float(similarityPercentage)
    topPercentage = float(topPercentage)

    found = loopingGenerateAndProcessMorphs(inputStr,target,noOfMorphs,similarityPercentage,topPercentage)
    print "FOUND!", found, "BYE BYE!!"
    return
 
def loopingGenerateAndProcessMorphs(inputStr,target,noOfMorphs,similarityPercentage,topPercentage):
    oldMorphArr = processMorphs(generateMorphs(inputStr,noOfMorphs),target,similarityPercentage,topPercentage,noOfMorphs)
    counter = 0
    while True:
        counter = counter + 1
        print "generation " , counter
        newMorphArr = []
        for inputStr in oldMorphArr:
            morphArr = generateMorphs(inputStr,noOfMorphs)
            #print "morphs"
            #print morphArr
            morphArr = processMorphs(morphArr,target,similarityPercentage,topPercentage,noOfMorphs)
            #print "surviving"
            #print morphArr             
            newMorphArr.extend(morphArr)
        
        print "extended "
        print newMorphArr
        print "selected extended"
        newMorphArr = processMorphs(newMorphArr,target,similarityPercentage,topPercentage,noOfMorphs)
        print newMorphArr
        if(target in newMorphArr):
          return counter
        oldMorphArr = newMorphArr
    return

def processMorphs(morphArr,target,similarityPercentage,topPercentage,noOfMorphs):
    #use topPercentage to calculate number of morphs to be kept
    noOfMorphs = int((topPercentage / 100.0) * noOfMorphs) + 1
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

#percentage of indexes where characters are the same
#number of similarities / length of target
def similaritiesPercentage(comp,target):
  return (float(countSameChars(comp,target)) /float(len(target))) * 100 

#count the number of occurrences where characters at same position in two strings are the same
def countSameChars(comp,target):
    counter = 0
    comp = list(comp)
    target = list(target)
    #compare available characters (length of shorter string)
    maxLen = len(comp) if len(comp) < len(target) else len(target)
    for x in xrange(maxLen): 
        if target[x] == comp[x]:
            counter += 1
    return counter

#generate list of morphs from a string
def generateMorphs(inputStr,noOfMorphs):
    targetLen = len(inputStr)
    charArr = list(inputStr)
    #generate morphs
    morphArr = []
    for x in xrange(noOfMorphs):
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

roll("","abcdefghijklmnopqrstuvwxyz",100,2,10)
