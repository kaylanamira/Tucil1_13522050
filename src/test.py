import random
import os
from pathlib import Path 
def is_num(s):
    try:
        int(s)
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
    
# print(readNumericInput("Masukkan ukuran buffer: "))
# numoftoken = readNumericInput("Masukkan jumlah token unik: ", 0)
# sequences = []
# tokens = []
# for i in range(numoftoken):
#     token = input("Masukkan token: ")
#     while (len(token) != 2):
#         print("\nToken harus terdiri dari 2 karakter!")
#         token = input("Masukkan token: ")
#     while (not token.isalnum()):
#         print("\nToken harus berupa karakter alfanumerik!")
#         token = input("Masukkan token: ")
#         while (len(token) != 2):
#             print("\nToken harus terdiri dari 2 karakter!")
#             token = input("Masukkan token: ")
#     while (token in tokens):
#         print("\nToken harus unik!")
#         token = input("Masukkan token: ")
#         while (len(token) != 2):
#             print("\nToken harus terdiri dari 2 karakter!")
#             token = input("Masukkan token: ")
#         while (not token.isalnum()):
#             print("\nToken harus berupa karakter alfanumerik!")
#             token = input("Masukkan token: ")
#             while (len(token) != 2):
#                 print("\nToken harus terdiri dari 2 karakter!")
#                 token = input("Masukkan token: ")
#     tokens.append(token)
# buffersize = readNumericInput("Masukkan ukuran buffer: ", 1)
# numofsequences = readNumericInput("Masukkan jumlah sekuens: ", 1)
# maxsequencesize = readNumericInput("Masukkan ukuran maksimal sekuens: ", 2)
# for i in range(numofsequences):
#     temp = []
#     length = random.randint(2,maxsequencesize)
#     token = [random.choice(tokens) for i in range(length)]
#     isUnique = True
#     j = 0
#     while (isUnique and (j < len(sequences))):
#         if (sequences[j][0] == token):
#             token = [random.choice(tokens) for i in range(length)]
#         else: 
#             j += 1
#     reward = random.randint(0, 500)
#     temp.append(token)
#     temp.append(reward)
#     sequences.append(temp)

# def getMatrixSize():
#     matrixsizeinput = input("Masukkan ukuran matriks: ")
#     matrixsize = matrixsizeinput.split()
#     while (len(matrixsize) != 2):
#         print("Masukan harus berupa 'ukuran_kolom ukuran_baris'!")
#         matrixsizeinput = input("Masukkan ukuran matriks: ")
#         matrixsize = matrixsizeinput.split()
#     matrixcol = matrixsize[0]
#     matrixrow = matrixsize[1]
#     while (not is_num(matrixcol) or not is_num(matrixrow)):
#         print("\nMasukan harus berupa angka!")
#         matrixcol, matrixrow = getMatrixSize()
#     while (int(matrixcol) <= 1 or int(matrixrow) <= 1):
#         print("\nMasukan harus berupa bilangan lebih besar dari 1")
#         matrixcol, matrixrow = getMatrixSize()
#     return int(matrixcol), int(matrixrow) #string

def getToken(numoftoken):
    tokeninput = input("Masukkan token: ") #55BD 3$
    tokens = tokeninput.split()
    while (len(tokens) != numoftoken):
        print("Masukan token harus sebanyak ", numoftoken)
        tokeninput = input("Masukkan token: ") #55 BD 3j BD
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

# matrixcol, matrixrow = getMatrixSize()

# print(tokens)
# print(buffersize)
# print(sequences)
# print(matrixcol)
# print(matrixrow)
# tokens = getToken()
# print(tokens)

# filename = input("Masukkan nama file('nama_file.txt') ")
# path = Path().absolute()
# filepath = str(path) + "/../test/" + filename
# print(filepath)
# while not Path(filepath).exists():
#     print("File '" + filename + "' tidak ada pada folder 'test'")
#     filename = input("Masukkan nama file('nama_file.txt') ")
#     path = Path().absolute()
#     filepath = str(path) + "/../test/" + filename
# with open(filepath, 'r') as file:
#     lines = file.readlines()

# print(lines)
filename = input("Masukkan nama file('nama_file.txt') ")
cwd = os.getcwd()
directory = os.path.join(cwd, os.pardir, 'test')
filepath = os.path.join(directory, filename)
while (not os.path.isfile(filepath)):
    print("File '" + filename + "' tidak ada pada folder 'test'")
    filename = input("Masukkan nama file('nama_file.txt') ")
    cwd = os.getcwd()
    directory = os.path.join(cwd, os.pardir, 'test')
    filepath = os.path.join(directory, filename)
with open(filepath, 'r') as file:
    lines = file.readlines()
print(lines)