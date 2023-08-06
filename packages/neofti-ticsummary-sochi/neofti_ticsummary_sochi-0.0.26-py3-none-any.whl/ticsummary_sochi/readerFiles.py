import os
import re



def readListFilesInFolder(path:str):
    listFilesRaw = os.listdir(path)
    listFiles = sorted(listFilesRaw, key=len)
    
    resultList = list()
    
    for file in listFiles:
        if (
            (file[-1] == 'v') &
            (file[-2] == 's') &
            (file[-3] == 'c') &
            (file[-4] == '.')):
            resultList.append(file)
    return resultList


if __name__ == "__main__":
    print(readListFilesInFolder("D:\Document\eclipse-workspace2\data"))