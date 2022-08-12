def getBiggest(dicx):
    mCntr = 0
    tmpCntr = 0
    biggestCount = 0
    tList = list(dicx.values())
    for i in range(len(tList)):
        for j in range(len(tList[i])):
            tmpCntr = 0
            for k in range(len(tList)):
                if tList[i][j] in tList[k]:
                    tmpCntr += 1
            if tmpCntr > mCntr:
                biggestCount = tList[i][j]
                mCntr = tmpCntr


    return biggestCount

def main():
    # prefs = {
    #     0: [0, 1, 3, 6],
    #     1: [1, 4, 7],
    #     2: [2, 4, 7, 5],
    #     3: [3, 2, 5],
    #     4: [5, 8]
    # }
    prefs = {
        0: [0, 1],
        1: [1, 2],
        2: [2, 3],
        3: [3, 4, 6],
        4: [4, 5]
    }
    avKeys = list(prefs.keys())
    finalDrinks = []
    drink = -1
    mCounter = 0
    initList = len(prefs)
    while mCounter < initList:
        drink = getBiggest(prefs)
        for ii in range(len(avKeys)):
            if drink in prefs[avKeys[ii]]:
                del(prefs[avKeys[ii]])
                mCounter += 1
        avKeys = list(prefs.keys())
        finalDrinks.append(drink)

    print(finalDrinks)




main()