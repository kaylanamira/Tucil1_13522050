def readfile(filename):
    #Asumsi input file benar
    matrix = []
    sequences = []
    rewards = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        buffersize = int(lines[0][0])
        matrixcol = int(lines[1][0])
        matrixrow = int(lines[1][2])
        for i in range(2,matrixrow+2):
            matrix.append(lines[i].split())
        numofsequences = int(lines[matrixrow+2][0])
        for i in range(matrixrow+3,len(lines),2):
            sequences.append(lines[i].split())
            rewards.append(int(lines[i+1].rstrip()))
    return buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences, rewards

def findroute(buffersize, matrixcol, matrixrow, matrix):
    #implements brute force
    possibilities = []
    buffer = ["" for i in range(buffersize)]

    for i in range(matrixcol):
        #reset buffer
        isSelected = [[0 for i in range(matrixcol)] for j in range(matrixrow)]
        buffer[0] = matrix[0][i]
        bufferidx = 1
        while (bufferidx != buffersize-1):
            bufferidx +=1
            #findhorizontalroute(rowidx, buffer, matrix, isSelected)
            #findverticalroute(colidx, buffer, matrix, isSelected)
            #CHECK IF MATRIX ELEMENT HAS NOT BEEN SELECTED -> token as object? or create another matrix
            # if (isSelected[0][i] ==  0):
            #calculate coordinate


        possibilities.append(buffer)
    return possibilities
    

def findmaxreward(possibilities, sequences, rewards):
    max = 0
    return max


def main():
    buffersize, matrixcol, matrixrow, matrix, numofsequences, sequences, rewards = readfile("input.txt")
    #DEBUG
    # print(matrix)
    # print(numofsequences)
    # print(sequences)
    # print(rewards)

    possibilities = findroute(buffersize, matrixcol, matrixrow, matrix)
    maxreward = findmaxreward(possibilities, sequences, rewards)


if __name__ == "__main__":
    main()