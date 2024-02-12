from datetime import datetime
import os
import random

#------CLASS DEFINITIONS-------
class Token:
    def __init__(self,row,col,alphanum):
        self.row = row
        self.col = col
        self.alphanum = alphanum
    def show(self):
        print("Row: ", self.row + 1, end=", ")
        print("Col: ", self.col + 1, end=", ")
        print("Token: ", self.alphanum)
        # print(self.alphanum)

class Sequence:
    def __init__(self, tokens, reward):
        self.size = len(tokens)
        self.tokens = tokens
        self.reward = reward
    def show(self):
        # print("Size: ", self.size, end=", ")
        for sequence in self.tokens:
            print(sequence, end=" ")
        print(", Reward: ", self.reward)
        print()

class Tree:
    def __init__(self, root, level, buffer, sequences):
        self.root = root
        self.child = []
        self.level = level
        temp = []
        for item in buffer:
            temp.append(item)
        temp.append(root)
        self.buffer = temp #buffer so far

        reward = 0
        for sequence in sequences:
            reward += self.calculateReward(sequence)
        self.rewardgained = reward

        # DEBUG
        # print("Level: ", self.level, end = ", ")
        # print("Root:", self.root.alphanum, end = " ")
        # print("Buffer : ",end = "")
        # printBuffer(self.buffer)
        # print("Reward: ", self.rewardgained)

    def findRoute(self, isVertical, matrix, level, buffersize, sequences, maxreward):
        # if isVertical : #search vertically
        #     if (level == self.level):
        #         colidx = self.root.col
        #         for rowidx in range(len(matrix)):
        #             if not isTokenSelected(self.buffer, rowidx, colidx):
        #                 if (rowidx != self.root.row and self.level <= buffersize-1):
        #                     # self.buffer[level] = matrix[rowidx][colidx]
        #                     self.child.append(Tree(matrix[rowidx][colidx], self.level+1, self.buffer))
        # else: #search horizontally
        #     if (level == self.level):
        #         rowidx = self.root.row
        #         for colidx in range(len(matrix[0])):
        #             if not isTokenSelected(self.buffer, rowidx, colidx):
        #                 if (colidx != self.root.col and self.level <= buffersize - 1):
        #                     # buffer[level] = matrix[rowidx][colidx]
        #                     self.child.append(Tree(matrix[rowidx][colidx], self.level+1, self.buffer))
            # else:
            #     for token in self.child:
            #         token.findRoute(isVertical, matrix, level, buffersize)
            # else:
            #     for token in self.child:
            #         token.findRoute(isVertical, matrix, level, buffersize)
        if (level == self.level and self.rewardgained != maxreward):
            # reward = 0
            # if self.level == buffersize:
            #     for sequence in sequences:
            #         reward += self.calculateReward(sequence)
                    # print(reward)
                # self.rewardgained = reward
            if isVertical : #search vertically
                colidx = self.root.col
                for rowidx in range(len(matrix)):
                    if not isTokenSelected(self.buffer, rowidx, colidx):
                        if (rowidx != self.root.row and self.level <= buffersize-1 and self.rewardgained != maxreward):
                            self.child.append(Tree(matrix[rowidx][colidx], self.level+1, self.buffer, sequences))
            else:
                rowidx = self.root.row
                for colidx in range(len(matrix[0])):
                    if not isTokenSelected(self.buffer, rowidx, colidx):
                        if (colidx != self.root.col and self.level <= buffersize - 1 and self.rewardgained != maxreward):
                            self.child.append(Tree(matrix[rowidx][colidx], self.level+1, self.buffer, sequences))
        for token in self.child:
            token.findRoute(not isVertical, matrix, level+1, buffersize, sequences, maxreward)

    def calculateReward(self, sequence):
        sequences = sequence.tokens
        reward = 0
        bufferlength = len(self.buffer)
        bufferidx = 0
        #pattern matching
        while (bufferidx <= (bufferlength - sequence.size)):
            match = True    
            sequenceidx = 0
            while (match and sequenceidx < sequence.size):
                if (self.buffer[bufferidx].alphanum != sequences[sequenceidx]):
                    match = False
                else:
                    sequenceidx += 1
                    bufferidx += 1
            if (match):
                reward += sequence.reward
                break
            else:
                bufferidx += 1
        return reward
    
    def printChild(self):
        print(", Child: [", end="")
        for token in self.child:
            print(token.root.alphanum, end=" ")
        print("]")
        # print()
        for token in self.child:
            token.show()

    def show(self):
        print("Level: ", self.level, end = ", ")
        print(", Root:", self.root.alphanum, end = " ")
        if (self.child != []):
            self.printChild()
        # else:
        #     print()
        print("Buffer : [",end = "")
        for token in self.buffer:
            print(token.alphanum, end = " ")
        print("]")
        print()
            

def createTree(buffersize,matrixcol, matrix, sequences):
    possibilities = []
    maxreward = 0
    for sequence in sequences:
        maxreward += sequence.reward
    for j in range(matrixcol):
        buffer = []
        possibilities.append(Tree(matrix[0][j], 1, buffer, sequences))
        level = 1
        isVertical = True
        possibilities[j].findRoute(isVertical, matrix, level, buffersize, sequences, maxreward)
    return possibilities

def isTokenSelected(buffer, rowidx, colidx):
    for i in range(len(buffer)):
        if (buffer[i]):
            if (rowidx == buffer[i].row and colidx == buffer[i].col):
                return True
        else:
            return False
    return False

def getPath():
    filename = input("\nMasukkan nama file('nama_file.txt') ")
    cwd = os.getcwd()
    directory = os.path.join(cwd, os.pardir, 'test')
    # directory = os.path.join(cwd, os.pardir, 'test')
    filepath = os.path.join(directory, filename)
    return filepath

def readFile():
    filepath = getPath()
    while (not os.path.isfile(filepath)):
        print("\nFile tidak ada pada folder 'test'")
        filepath = getPath()
    #Asumsi konten pada input file benar
    matrix = []
    sequences = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        buffersize = int(lines[0][0])
        matrixcol = int(lines[1][0])
        matrixrow = int(lines[1][2])

        for i in range(matrixrow):
            tokens = lines[i+2].split()
            temp = []
            j = 0
            for token in tokens:
                temp.append(Token(i,j,token))
                j += 1
            matrix.append(temp)

        numofsequences = int(lines[matrixrow+2][0])

        for i in range(matrixrow+3,len(lines),2):
            tokens = lines[i].split()
            reward = int(lines[i+1].rstrip())
            sequences.append(Sequence(tokens,reward))

    return buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences

def savetoFile(maxreward, solution, runtime):
    filepath = getPath()
    with open(filepath, 'w') as file:
        file.write(str(maxreward) + '\n')
        for item in solution:
            file.write(item.alphanum + ' ')
        if (solution != []):
            file.write('\n')
        for item in solution:
            file.write(str(item.col+1) + ', ')
            file.write(str(item.row+1) + '\n')
        file.write('\n' + str(round(runtime)) + " ms\n")
         
def printMatrix(matrix):
    for tokens in matrix:
        for token in tokens:
            # token.show()
            print(token.alphanum, end = " ")
        print()

def printSequence(sequences):
    for sequence in sequences:
        for token in sequence.tokens:
            print(token, end=" ")
        print("\t\t Reward: ", sequence.reward)
    print()

def printBuffer(buffer):
    for item in buffer:
        print(item.alphanum, end = " ")
    if (buffer != []):
        print()

def printCoordinates(buffer):
    for item in buffer:
        print(item.col+1, end=", ")
        print(item.row+1)

def getTreeReward(tree, buffersize, maxprize):
    if (tree.level == buffersize or tree.rewardgained == maxprize):
        return tree.rewardgained, tree.buffer, len(tree.buffer)
    else:
        minbufferlength = 1
        maxreward = -500
        solution = []
        for child in tree.child:
            reward, buffer, bufferlength = getTreeReward(child, buffersize, maxprize)
            if ((reward > maxreward and reward != 0) or (reward == maxreward and reward != 0 and bufferlength < minbufferlength)):
                maxreward = reward
                solution = buffer
                minbufferlength = bufferlength
        return maxreward, solution, minbufferlength

def getMaxReward(possibilities, buffersize, maxprize):
    minbufferlength = 1
    maxreward = -500
    solution = []
    for tree in possibilities:
        reward, buffer, bufferlength = getTreeReward(tree, buffersize, maxprize)
        if ((reward > maxreward and reward != 0) or (reward == maxreward and reward != 0 and bufferlength < minbufferlength)):
            maxreward = reward
            solution = buffer
            minbufferlength = bufferlength
    if (len(solution) == 0):
        maxreward = 0
    return maxreward, solution

def output(maxreward, solution, runtime):
    print(maxreward)
    printBuffer(solution)
    printCoordinates(solution)
    print()
    print(round(runtime), "ms")

def is_num(x):
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True
    
def validateNumericInput(x, message, minvalue):
    while (not is_num(x)):
        print("\nMasukan harus berupa angka!")
        x = input(message)
    while (int(x) <= minvalue):
        print("\nMasukan harus berupa bilangan lebih besar dari", minvalue)
        x = readNumericInput(message, minvalue)
    return int(x)

def readNumericInput(message, minvalue):
    x = input(message)
    return validateNumericInput(x, message, minvalue)

def getMatrixSize():
    matrixsizeinput = input("Masukkan ukuran matriks: ")
    matrixsize = matrixsizeinput.split()
    while (len(matrixsize) != 2):
        print("Masukan harus berupa 'ukuran_kolom ukuran_baris'!")
        matrixsizeinput = input("Masukkan ukuran matriks: ")
        matrixsize = matrixsizeinput.split()
    matrixcol = matrixsize[0]
    matrixrow = matrixsize[1]
    while (not is_num(matrixcol) or not is_num(matrixrow)):
        print("\nMasukan harus berupa angka!")
        matrixcol, matrixrow = getMatrixSize()
    while (int(matrixcol) <= 0 or int(matrixrow) <= 0):
        print("\nMasukan harus berupa bilangan positif")
        matrixcol, matrixrow = getMatrixSize()
    return int(matrixcol), int(matrixrow) #string

def getToken(numoftoken):
    tokeninput = input("Masukkan token: ") 
    tokens = tokeninput.split()
    while (len(tokens) != numoftoken):
        print("Masukan token harus sebanyak ", numoftoken)
        tokeninput = input("Masukkan token: ") 
        tokens = tokeninput.split()
    for i in range(numoftoken):
        if (len(tokens[i]) != 2):
            print("\nToken harus terdiri dari 2 karakter!")
            tokens = getToken(numoftoken)
            break
        if (not tokens[i].isalnum()):
            print("\nToken harus berupa karakter alfanumerik!")
            tokens = getToken(numoftoken)
            break
        for j in range (i+1, numoftoken):
            if (tokens[i] == tokens[j]):
                print("\nToken harus unik!")
                tokens = getToken(numoftoken)
                break
    return tokens #string

def randomizeInput():
    numoftoken = readNumericInput("Masukkan jumlah token unik: ", 0)
    tokens = getToken(numoftoken)
    buffersize = readNumericInput("Masukkan ukuran buffer: ", 1)
    
    matrix = []
    matrixcol, matrixrow = getMatrixSize()
    for i in range(matrixrow):
        temp = []
        for j in range(matrixcol):
            temp.append(Token(i,j,random.choice(tokens)))
        matrix.append(temp)

    sequences = []
    numofsequences = readNumericInput("Masukkan jumlah sekuens: ", 1)
    maxsequencesize = readNumericInput("Masukkan ukuran maksimal sekuens: ", 2)
    for i in range(numofsequences):
        length = random.randint(2,maxsequencesize)
        token = [random.choice(tokens) for i in range(length)]
        isUnique = True
        j = 0
        while (isUnique and (j < len(sequences))):
            if (sequences[j].tokens == token):
                token = [random.choice(tokens) for i in range(length)]
            else: 
                j += 1
        reward = random.randint(0, 500)
        sequences.append(Sequence(token,reward))

    return buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences

def main():
    inputType = input("Silakan pilih jenis masukan!(f : file, r : random)")
    while (inputType != 'f' and inputType != 'r' and inputType != 'F' and inputType != 'R'):
        inputType = input("Silakan pilih jenis masukan!(f : file, r : random)")
    if (inputType == 'f' or inputType == 'F'):
        buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences = readFile()
    else: # (inputType == 'r' inputType == 'R'):
        buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences = randomizeInput()
        print("\nGenerated Matrix :")
        printMatrix(matrix)   
        print("\nGenerated Sequences :")
        printSequence(sequences)

    start = datetime.now()
    possibilities = createTree(buffersize, matrixcol, matrix, sequences)
    maxprize = 0
    for sequence in sequences:
        maxprize += sequence.reward

    maxreward, solution = getMaxReward(possibilities, buffersize, maxprize)
    end = datetime.now()
    runtime = (end - start).total_seconds() * 10**3
    
    output(maxreward, solution, runtime)
    option = input("\nApakah ingin menyimpan solusi?(y/n)")
    while (option != 'y' and option != 'Y' and option != 'n' and option != 'N'):
        print("\nMasukan tidak valid. Harap memasukkan huruf y/n")
        option = input("Apakah ingin menyimpan solusi?(y/n)")
    if (option == 'y' or option == 'Y'):
        savetoFile(maxreward, solution, runtime)

if __name__ == "__main__":
    main()