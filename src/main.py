from datetime import datetime
import os
import random

# ------CLASS DEFINITIONS-------
class Token:
    def __init__(self,row,col,alphanum):
        self.row = row
        self.col = col
        self.alphanum = alphanum
    def show(self):
        print("Row: ", self.row + 1, end=", ")
        print("Col: ", self.col + 1, end=", ")
        print("Token: ", self.alphanum)

class Sequence:
    def __init__(self, tokens, reward):
        self.size = len(tokens)
        self.tokens = tokens
        self.reward = reward
    def show(self):
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

    def findRoute(self, isVertical, matrix, level, buffersize, sequences, maxreward):
        if (level == self.level and self.rewardgained != maxreward):
            if isVertical : #search vertically
                colidx = self.root.col
                for rowidx in range(len(matrix)):
                    if not self.isTokenSelected(rowidx, colidx):
                        if (rowidx != self.root.row and self.level <= buffersize-1 and self.rewardgained != maxreward):
                            self.child.append(Tree(matrix[rowidx][colidx], self.level+1, self.buffer, sequences))
            else:
                rowidx = self.root.row
                for colidx in range(len(matrix[0])):
                    if not self.isTokenSelected(rowidx, colidx):
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
    
    def isTokenSelected(self, rowidx, colidx):
        for i in range(len(self.buffer)):
            if (self.buffer[i]):
                if (rowidx == self.buffer[i].row and colidx == self.buffer[i].col):
                    return True
            else:
                return False
        return False

            
# ----------FUNCTIONS------------
# ALGORITHM FUNCTIONS
def createTree(buffersize,matrixcol, matrix, sequences):
    possibilities = []
    maxreward = 0
    for sequence in sequences:
        maxreward += sequence.reward
    for j in range(matrixcol):
        possibilities.append(Tree(matrix[0][j], 1, [], sequences))
        level = 1
        isVertical = True
        possibilities[j].findRoute(isVertical, matrix, level, buffersize, sequences, maxreward)
    return possibilities

def getTreeReward(tree, buffersize, maxprize):
    if (tree.level == buffersize or tree.rewardgained == maxprize):
        return tree.rewardgained, tree.buffer, len(tree.buffer)
    else:
        minbufferlength = len(tree.buffer)
        maxreward = -500
        solution = []
        for child in tree.child:
            reward, buffer, bufferlength = getTreeReward(child, buffersize, maxprize)
            if ((reward > maxreward and reward != 0) or (reward == maxreward and reward != 0 and bufferlength < minbufferlength)):
                maxreward = reward
                solution = buffer
                minbufferlength = bufferlength
        if (tree.rewardgained == maxreward):
            return tree.rewardgained, tree.buffer, len(tree.buffer)
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

# I/O FUNCTIONS
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
    return int(matrixcol), int(matrixrow) 

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
    return tokens 

def getPath():
    filename = input("\nMasukkan nama file('nama_file.txt') ")
    cwd = os.getcwd()
    directory = os.path.join(cwd, os.pardir, 'test')
    filepath = os.path.join(directory, filename)
    return filepath

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
        reward = random.randint(-500, 500)
        sequences.append(Sequence(token,reward))

    return buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences

def readFile():
    filepath = getPath()
    while (not os.path.isfile(filepath)):
        print("\nFile tidak ada pada folder 'test'")
        filepath = getPath()
    matrix = []
    sequences = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        buffersize = lines[0][0]
        if (not is_num(buffersize) or int(buffersize) <= 0):
            file.close()
            print("Ukuran buffer harus berupa integer lebih besar dari 1!")
            buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences = readFile()
        matrixcol = lines[1][0]
        matrixrow = lines[1][2]
        if (not is_num(matrixcol) or not is_num(matrixrow) or int(matrixcol) <= 0 or int(matrixrow) <= 0):
            file.close()
            print("Ukuran matrix tidak valid!")
            buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences = readFile()
        matrixcol = int(matrixcol)
        matrixrow = int(matrixrow)
        for i in range(matrixrow):
            tokens = lines[i+2].split()
            temp = []
            j = 0
            for token in tokens:
                temp.append(Token(i,j,token))
                j += 1
            matrix.append(temp)

        numofsequences = lines[matrixrow+2][0]
        if (not is_num(numofsequences) or (int(numofsequences) <= 1)):
            file.close()
            print("Jumlah sekuens harus berupa integer lebih besar dari 1!")
            buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences = readFile()
        for i in range(matrixrow+3,len(lines),2):
            tokens = lines[i].split()
            for token in tokens:
                if (len(token) != 2 or not token.isalnum()):
                    file.close()
                    print("Token harus berupa 2 karakter alfanumerik!!")
                    buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences = readFile()

            isUnique = True
            j = 0
            if (isUnique and (j < len(sequences))):
                if (sequences[j].tokens == tokens):
                    file.close()
                    print("Token harus unik!")
                    buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences = readFile()
                else: 
                    j += 1
            reward = int(lines[i+1].rstrip())
            sequences.append(Sequence(tokens,reward))

    return int(buffersize), matrixcol, matrixrow, matrix, int(numofsequences), sequences

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
            print(token.alphanum, end = " ")
        print()

def printBuffer(buffer):
    for item in buffer:
        print(item.alphanum, end = " ")
    if (buffer != []):
        print()

def printSequence(sequences):
    for sequence in sequences:
        for token in sequence.tokens:
            print(token, end=" ")
        print("\t\t Reward: ", sequence.reward)
    print()

def printCoordinates(buffer):
    for item in buffer:
        print(item.col+1, end=", ")
        print(item.row+1)

def output(maxreward, solution, runtime):
    print(maxreward)
    printBuffer(solution)
    printCoordinates(solution)
    print()
    print(round(runtime), "ms")

def main():
    print()
    print(" ____  ____  ____   __    ___  _  _    ____  ____   __  ____  __    ___  __   __")   
    print("(  _ \(  _ \(  __) / _\  / __)/ )( \  (  _ \(  _ \ /  \(_  _)/  \  / __)/  \ (  )")  
    print(" ) _ ( )   / ) _) /    \( (__ ) __ (   ) __/ )   /(  O ) )( (  O )( (__(  O )/ (_/\\")
    print("(____/(__\_)(____)\_/\_/ \___)\_)(_/  (__)  (__\_) \__/ (__) \__/  \___)\__/ \____/\n")
    print("                Welcome to Cyberpunk 2077 Breach Protocol Solver!                   \n") 

    print("--------------MENU--------------")
    print("1. Input dari file")
    print("2. Hasilkan input secara random")
    print("--------------------------------")
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