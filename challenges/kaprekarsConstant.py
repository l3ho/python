def sortAsc(strx):
    newStr = ""
    strLits = list(strx)
    cFlag = False
    while cFlag == False:
        cFlag = True
        for ii in range(len(strx)-1):
            if strLits[ii]>strLits[ii+1]:
                tmpval = strLits[ii+1]
                strLits[ii+1]=strLits[ii]
                strLits[ii]=tmpval
                cFlag=False
    
    for ii in range(len(strLits)):
        newStr=newStr + strLits[ii]
    return newStr

def sortDesc(strx):
    newStr = ""
    strLits = list(strx)
    cFlag = False
    while cFlag == False:
        cFlag = True
        for ii in range(len(strx)-1):
            if strLits[ii]<strLits[ii+1]:
                tmpval = strLits[ii+1]
                strLits[ii+1]=strLits[ii]
                strLits[ii]=tmpval
                cFlag=False
    
    for ii in range(len(strLits)):
        newStr=newStr + strLits[ii]
    return newStr

def main():
    kap = 6174
    num = 9831
    cntr = 0
    while num !=kap:
        num1 = sortDesc(str(num))
        num2 = sortAsc(str(num))
        num = int(num1)-int(num2)
        if len(str(num))<4:
            for kk in range(4-len(str(num))):
                num_s=str(num)+"0"
            num=int(num_s)
        cntr = cntr+1
    print(cntr)


main()