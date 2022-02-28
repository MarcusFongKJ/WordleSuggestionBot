# Libraries
from re import I
import pygame
from datetime import date
import ast

# Obtain data
# Open answer file and store in a answerList
f = open("data/answers.txt", "r")
answerList = f.read().split("\n")
f.close()

# Open allowed words file and store in a allowedList (allowedList is a list of 12972 words that are approved)
f = open("data/allowedWords.txt", "r")
allowedList = f.read().split("\n")
f.close()

# Open file containing 5 letter words and store in a list
f = open("data/fiveLetterWords.txt", "r")
engDict = f.read().split("\n")
f.close()

# Obtain word of the day from answerList
d0 = date(2021, 6, 19)  # date when wordle list starts
d1 = date(date.today().year, date.today().month, date.today().day)
delta = d1 - d0
todaysWord = answerList[delta.days].upper()
# print(todaysWord)

# Open file containing a dictionary of words and its freq value
f = open("data/allowedWordsFreq.txt", "r")
wordFreq = f.read()
f.close()
# Convert string to dictionary
wordFreqDict = ast.literal_eval(wordFreq)

# Duplicate engDict of 5 letter words as suggestionList where words will be removed from (can do without duplication)
suggestionList = engDict

# Parameters of the game
wordLength = 5
numGuesses = 6

# Initialise pygame
pygame.init()
fps = 60
timer = pygame.time.Clock()
running = True
gameOver = False
turn = 0
letterCount = 0
wordVerification = False
letterCountVerification = False

# Fonts
guessFont = pygame.font.Font('freesansbold.ttf', 45)
suggestionsFont = pygame.font.Font('freesansbold.ttf', 20)
keyboardFont = pygame.font.Font('freesansbold.ttf', 25)
messageFont = pygame.font.Font('freesansbold.ttf', 25)

# Screen Setup
WIDTH = 950
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Wordle Suggestion Bot')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (60, 60, 60)
yellow = (204, 204, 0)
green = (83, 141, 78)
lightGrey = (130, 130, 130)

# Board Setup
board = []
for row in range(numGuesses):
    board.append([])
    for col in range(wordLength):
        board[row].append(" ")

def drawBoard():
    global turn
    global board
    for col in range(wordLength):
        for row in range(numGuesses):
            pygame.draw.rect(screen, grey, [col * 65 + 50, row * 65 + 15, 60, 60], 2)
            guessText = guessFont.render(board[row][col], True, white)
            screen.blit(guessText, (col * 65 + 62, row * 65 + 25))


# Check duplicate letters in word (if word has repeated letters, return True)
def checkDuplicate(word):
    for char in word:
        counts = word.count(char)
        if counts > 1:
            return True
    return False


# Suggestions Box
def drawSuggestions():
    pygame.draw.rect(screen, grey, [wordLength * 65 + 50, 15, 500, 385], 2)

    verticalSpacing = 0
    horizontalSpacing = 0
    wordIndex = 0

    # Order suggestionList by freq
    suggestionDict = {}
    for word in suggestionList:
        if word not in wordFreqDict:
            suggestionDict[word] = 0
        else:
            # Rate words with no repeated letters a little higher (value added = half the value of "which" which is the most common word with 0.002061152)
            if checkDuplicate(word):
                suggestionDict[word] = wordFreqDict[word]
            else:
                suggestionDict[word] = wordFreqDict[word] + 0.0010

    # Sort dict (returns list of tuples)
    import operator
    sortedSuggestionsDict = sorted(suggestionDict.items(), key=operator.itemgetter(1))

    # Convert dictionary back to list (since its sorted)
    sortedSuggestions = []
    for i in sortedSuggestionsDict:
        sortedSuggestions.append(i[0])

    # Reverse list
    sortedSuggestions.reverse()

    if len(sortedSuggestions) >= 114:

        # Convert back to list

        for col in range(6):
            for row in range(19):
                suggestionText = suggestionsFont.render(sortedSuggestions[wordIndex], True, white)
                screen.blit(suggestionText, (wordLength * 65 + 55 + horizontalSpacing, 20 + verticalSpacing))
                verticalSpacing += 20
                wordIndex += 1

            # Reset vertical spacing
            verticalSpacing = 0

            # Add horizontal spacing for new column
            horizontalSpacing += 80

    else:
        # Determine number of columns and rows needed
        if len(sortedSuggestions) % 19 != 0:
            numCols = (len(sortedSuggestions)//19) + 1
            rowsLast = 19 - ((numCols * 19) - len(sortedSuggestions))

        else:
            numCols = (len(sortedSuggestions)//19)
            rowsLast = 19

        for col in range(numCols):

            if int(col + 1) == int(numCols):
                for row in range(rowsLast):
                    suggestionText = suggestionsFont.render(sortedSuggestions[wordIndex], True, white)
                    screen.blit(suggestionText, (wordLength * 65 + 55 + horizontalSpacing, 20 + verticalSpacing))
                    verticalSpacing += 20
                    wordIndex += 1
            
            else:
                for row in range(19):
                        suggestionText = suggestionsFont.render(sortedSuggestions[wordIndex], True, white)
                        screen.blit(suggestionText, (wordLength * 65 + 55 + horizontalSpacing, 20 + verticalSpacing))
                        verticalSpacing += 20
                        wordIndex += 1


            # Reset vertical spacing
            verticalSpacing = 0

            # Add horizontal spacing for new column
            horizontalSpacing += 80


# Create list and dictionary to check input against possible list of words
greyLetters = []
yellowLetters = {}
greenLetters = {}

# Check word and update color on new turn (achieved by pressing Enter)
def checkWord():
    global turn
    global board
    global todaysWord

    for col in range(wordLength):
        for row in range(numGuesses):
            if (turn > row):
                if board[row][col] in todaysWord:

                    if board[row][col] == todaysWord[col]:
                        pygame.draw.rect(screen, green, [col * 65 + 50, row * 65 + 15, 60, 60], 0, 3)

                    else:
                        pygame.draw.rect(screen, yellow, [col * 65 + 50, row * 65 + 15, 60, 60], 0, 3)

                else:
                    pygame.draw.rect(screen, grey, [col * 65 + 50, row * 65 + 15, 60, 60], 0, 3)


# Keyboard
KEYBOARD = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM']

def drawKeyboard():
    global turn
    global board
    global greenLetters
    global yellowLetters
    global greyLetters

    pygame.draw.rect(screen, grey, [50, 420, 825, 150], 2)
    verticalSpacing = 0
    horizontalSpacing = 0

    if turn == 0:
        for row in range(len(KEYBOARD)):
            for i in range(len(KEYBOARD[row])):
                if row == 0:
                    rowXPosition = 0
                elif row == 1:
                    rowXPosition = 25
                elif row == 2:
                    rowXPosition = 75

                pygame.draw.rect(screen, lightGrey, [80 + horizontalSpacing + rowXPosition, 425 + verticalSpacing, 40, 40], 0, 2)
                keyboardText = keyboardFont.render(KEYBOARD[row][i], True, white)
                screen.blit(keyboardText, (90 + horizontalSpacing + rowXPosition, 435 + verticalSpacing))
                horizontalSpacing += 50

            horizontalSpacing = 0
            verticalSpacing += 50


    else:
        for row in range(numGuesses):
            if (turn > row):
                for i in range(len(KEYBOARD)):
                    for j in range((len(KEYBOARD[i]))):
                        if i == 0:
                            rowXPosition = 0
                        elif i == 1:
                            rowXPosition = 25
                        elif i == 2:
                            rowXPosition = 75

                        if KEYBOARD[i][j] in greyLetters:
                            pygame.draw.rect(screen, grey, [80 + horizontalSpacing + rowXPosition, 425 + verticalSpacing, 40, 40], 0, 2)
                        elif KEYBOARD[i][j] in yellowLetters:
                            pygame.draw.rect(screen, yellow, [80 + horizontalSpacing + rowXPosition, 425 + verticalSpacing, 40, 40], 0, 2)
                        elif KEYBOARD[i][j] in greenLetters:
                            pygame.draw.rect(screen, green, [80 + horizontalSpacing + rowXPosition, 425 + verticalSpacing, 40, 40], 0, 2)
                        else:
                            pygame.draw.rect(screen, lightGrey, [80 + horizontalSpacing + rowXPosition, 425 + verticalSpacing, 40, 40], 0, 2)

                        keyboardText = keyboardFont.render(KEYBOARD[i][j], True, white)
                        screen.blit(keyboardText, (90 + horizontalSpacing + rowXPosition, 435 + verticalSpacing))
                        horizontalSpacing += 50

                    horizontalSpacing = 0
                    verticalSpacing += 50

            verticalSpacing = 0



# Game Start
while running:
    timer.tick(fps)
    screen.fill(black)
    checkWord()
    drawBoard()
    drawSuggestions()
    drawKeyboard()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letterCount > 0:
                letterCount -= 1
                board[turn][letterCount] = " "

            elif event.key == pygame.K_RETURN and not gameOver:

                guess = "".join(board[turn])
                wordVerification = False
                letterCountVerification = False

                if letterCount != wordLength:
                    # print("Not enough letters")
                    letterCountVerification = True

                elif guess.lower() not in allowedList:
                    # print("Word not allowed")
                    wordVerification = True
                    

                else:

                    if guess == todaysWord:
                        gameOver = True

                    # Add to letters to list/dict
                    for pos in range(wordLength):

                        if board[turn][pos] in todaysWord:

                            # Green
                            if board[turn][pos] == todaysWord[pos]:
                                if board[turn][pos] not in greenLetters:
                                    greenLetters[board[turn][pos]] = pos
                                    # remove from yellowLetters dict once the letter is placed in correct position
                                    if board[turn][pos] in yellowLetters:
                                        yellowLetters.pop(board[turn][pos])

                            # Yellow
                            else:
                                # Add new yellow letter and its position
                                if board[turn][pos] not in yellowLetters:
                                    yellowLetters[board[turn][pos]] = pos
                                # Update position of yellow letter for new guess
                                else:
                                    if yellowLetters[board[turn][pos]] != pos:
                                        yellowLetters[board[turn][pos]] = pos


                        else:
                            if board[turn][pos] not in greyLetters:
                                    greyLetters.append(board[turn][pos])

                    # print("Grey:", greyLetters)
                    # print("Yellow:", yellowLetters)
                    # print("Green:", greenLetters)

                    # Eliminate Grey letters
                    if greyLetters:
                        for greyLetter in greyLetters:
                            for word in suggestionList[::-1]:
                                if greyLetter.lower() in word:
                                    suggestionList.remove(word)

                    # Eliminate words with letters in the wrong position (yellowLetters), eliminate words without 'Yellow' letters
                    if yellowLetters:
                        for yellowLetter, pos in yellowLetters.items():
                            for word in suggestionList[::-1]:
                                if word[pos] == yellowLetter.lower():
                                    suggestionList.remove(word)
                                if yellowLetter.lower() not in word:
                                    suggestionList.remove(word)


                    # Keep words with letters in the correct position (greenLetters)
                    if greenLetters:
                        for greenLetter, pos in greenLetters.items():
                            for word in suggestionList[::-1]:
                                if word[pos] != greenLetter.lower():
                                    suggestionList.remove(word)

                    # print("Suggestions:", suggestionList)
                    
                    # Increment turn and reset letterCount
                    turn += 1
                    letterCount = 0
            
        # Show user input 
        if event.type == pygame.TEXTINPUT and not gameOver:
            entry = event.__getattribute__('text')
            
            if (entry.isalpha()) and (letterCount != wordLength):
                board[turn][letterCount] = entry.upper()
                letterCount += 1

    # Game Over
    if turn == 6 and not gameOver:
        pygame.draw.rect(screen, grey, [600, 465, 265, 50], 2)
        messageText = messageFont.render("Game Lost", True, white)
        screen.blit(messageText, (660, 480))

    # Game Won
    if gameOver:
        pygame.draw.rect(screen, grey, [600, 465, 265, 50], 2)
        messageText = messageFont.render("Game Won", True, white)
        screen.blit(messageText, (660, 480))

    if wordVerification:
        pygame.draw.rect(screen, grey, [600, 465, 265, 50], 2)
        messageText = messageFont.render("Word Error", True, white)
        screen.blit(messageText, (660, 480))

    if letterCountVerification:
        pygame.draw.rect(screen, grey, [600, 465, 265, 50], 2)
        messageText = messageFont.render("Insufficient Letters", True, white)
        screen.blit(messageText, (610, 480))

    pygame.display.flip()

pygame.quit()
