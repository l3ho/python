combs = []
sumBase = "12345678"

def main():    
    sumTotal = 25
    combinations()
    findRes(sumTotal)

def findRes(totalX):
    for i in range(0,256):
        tmpSign = genSigns(combs[i])
        evalStr = genEquation(sumBase,tmpSign)
        valCheck = eval(evalStr)
        if valCheck == totalX:
            print(evalStr + "=" + str(totalX))            

def genEquation(baseX, signsX):
    retStr = ""
    for i in range(0,len(baseX)-2):
        retStr = retStr + baseX[i] + signsX[i]
    return retStr + baseX[len(baseX)-1]

def genSigns(binStr):
    newStr = ""
    for j in range(len(binStr)):
        if binStr[j]=="0":
            newStr=newStr+"+"
        else:
            newStr=newStr+"-"
    return newStr

def combinations():
    for i in range(0,256):
        tmpS = format(i,'b')
        if len(tmpS) < 8:
            for j in range(1,8-len(tmpS)+1):
                tmpS = '0' + tmpS
        combs.append(tmpS)
    
main()