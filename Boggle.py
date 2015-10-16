import random
#use urllib if you dont want to download word.txt, however words.txt is faster. More on line 130.
#import urllib.request

def checkword(word,vector,matrix,wordList):
    # all comparisons in upper case
    wordUpper = word.upper()

    #word must be 3 letters or longer
    if len(word) < 3:
        return False

    # 1. word is in dictionary
    if wordUpper not in wordList:
        print(wordUpper,'is NOT in the dictionary!')
        return False
    
    # 2. letters of word exist in board
    for letter in wordUpper:
        if letter not in vector:
            return False
    
    # 3. word can be spelled
    pointList = getAllPoints(wordUpper,matrix)
    #pointList are the locations of the fist letter
    #pointPerms are their permutations
    #wordPerms is a dictionary of words to points
    pointPerms = list(permutations(pointList, len(wordUpper)))
    wordPerms = []
    for permPhrase in pointPerms:
        wordPerms.append(''.join([matrix[(point)] for point in permPhrase]))

    #now make a list of the possible words
    goodWords = []
    goodPoints = []
    for w in range(len(wordPerms)):
        if wordPerms[w] == wordUpper:
            goodWords.append(wordPerms[w])
            goodPoints.append(pointPerms[w])

    #now check if all the points are next to each other        
    numberPossible = 0        
    for GP_list in goodPoints:
        if areAllNextTo(GP_list,matrix) == True:
            numberPossible += 1
        else:
            pass
    if numberPossible > 1:
        print('There are',numberPossible,wordUpper+"'s on the board.")
        return True
    elif numberPossible == 1:
        print('There is one',numberPossible,wordUpper,'on the board.')
        return True
    else:
        print(wordUpper,'is NOT on the grid!')
        return False    

    
def areAllNextTo(points,matrix):
    '''Are all letter points next to another'''
    for x in range(len(points)-1):
        pointx = points[x]
        pointy = points[x+1]
        if isNextTo(pointx,pointy) == True:
            pass
        else:
            return False
    return True    
    
def isNextTo(pointx,pointy):
    '''Is a letter point next to another'''
    if abs(pointx[0]-pointy[0]) <= 1 and abs(pointx[1]-pointy[1]) <= 1:
        return True
    else:
        return False
           
def permutations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = [i for i in range(n)]
    cycles = [k for k in range(n, n-r, -1)]
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

def getAllPoints(word, matrix):
    '''Get all points for words'''
    pointList = []
    for row in range(4):
        for col in range(4):
            if matrix[(row,col)] in word:
                pointList.append((row, col))            
    return pointList            
        
def newBoard():
    '''creates a random boggle board'''
    words  = ['AAEEGN', 'ELRTTY', 'AOOTTW', 'ABBJOO', 'EHRTVW', 'CIMOTU', 'DISTTY', 'EIOSST',
             'DELRVY', 'ACHOPS', 'HIMNQU', 'EEINSU', 'EEGHNW', 'AFFKPS', 'HLNNRZ', 'DELIRX']
    vectorLocal = [words[x][random.randint(0,5)] for x in range(16)]
    matrixLocal = {(x,y):0 for x in range(4) for y in range(4)}
    
    for row in range(4):
        for col in range(4):
            matrixLocal[(row,col)] = vectorLocal[row*4 + col]

    return(vectorLocal, matrixLocal)

def printBoard(matrixLocal):
    for row in range(4):
        print ('\n ', end="")
        for col in range(4):
            print (matrixLocal[(row,col)],end="")
            print ('  ', end="")
        print ('\n',end="")
    print ('\n',end="")


boardvars = newBoard()
vector = boardvars[0]
matrix = boardvars[1]
printBoard(matrix)

#Boggle game currently requires a word list, however I can make it work with
#hosted word file, however it will be slower

#inputFile = urllib.request.urlopen('http://paste.openstack.org/raw/476208/')
inputFile = open('words.txt','r')
wordList = []
for word in inputFile:
    #newlines count for 2 characters, only include words length 3 or more
    if len(word) > 4:
        wordList.append(word.upper()[0:len(word)-2])
inputFile.close()
word = input('Enter your word (leave blank to quit): ')
words = []
wordsUsed = []
while word != '':
    if word not in wordsUsed:
        result = checkword(word,vector,matrix,wordList)
        if result == True:
            wordsUsed.append(word)
            words.append(word.upper())
            print(word.upper(),'is a valid word!')
        else:
            pass
        printBoard(matrix)
    word = input('Enter your word (leave blank to quit): ')

print("Here's your score:")
score = 0
for w in words:  
    if len(w) == 3:
        score += 1
        wordScore = 1
    elif len(w) == 4:
        score += 1
        wordScore = 1
    elif len(w) == 5:
        score += 2
        wordScore = 2
    elif len(w) == 6:
        score += 3
        wordScore = 3
    elif len(w) == 7:
        score += 5
        wordScore = 5
    elif len(w) >= 8:
        score += 11
        wordScore = 11
    else:
        wordScore = 0 
    print(w,'scores',wordScore)
print('TOTAL SCORE:',score)
print('Thanks for playing!')
