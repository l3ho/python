combs=[]
numCombs=[]
tmpComb=[0 for i in range(9)]
sumBase = "123456789"

def main():    
    sumTotal = 23456790
    numCominations(0,0)
    findRes(sumTotal)

def snCombinations(nn,limit,tmpSn):
    if nn==limit:
        tmpstr =""
        for jj in range(0,len(tmpSn)):
            tmpstr = tmpstr + str(tmpSn[jj])
        combs.append(tmpstr)
    else:
        for i in range(0,2):
            if i==0:
                sn ="+"
            else:
                sn="-"
            tmpSn[nn]=sn    
            snCombinations(nn+1,limit,tmpSn)   
        tmpSn[nn]="" 

def findRes(totalX):
    for i in range(0,len(numCombs)):
        tmpSn=[0 for i in range(len(numCombs[i])-1)]
        snCombinations(0,len(numCombs[i])-1,tmpSn)    
        for j in range(0,len(combs)):
            if i==1:
                sdsd=1
            evalStr = genEquation(numCombs[i],combs[j])
            valCheck = eval(evalStr)
            if valCheck == totalX:
                print(evalStr + "=" + str(totalX))
                break
        combs.clear()        

def genEquation(baseX, signsX):
    retStr = ""
    cnt =0
    for i in range(0,len(baseX)-1):
        if int(baseX[i])!=0:
            cnt = cnt +int(baseX[i])
            retStr = retStr + sumBase[i:cnt] + signsX[i]
    return retStr + sumBase[cnt:len(sumBase)]


def numCominations(sumx,nn):
    if sumx==9:
        tmpstr =""
        for jj in range(0,len(tmpComb)):
            if tmpComb[jj]!=0:
                tmpstr = tmpstr + str(tmpComb[jj])
        numCombs.append(tmpstr)
    else:
        for ii in range(1,9):
            tmpComb[nn]=ii
            tmpstr=""
            for jj in range(0,len(tmpComb)):
                tmpstr = tmpstr + str(tmpComb[jj]) + "+"
            tmpstr = tmpstr +  '0'
            if eval(tmpstr)<=9:
                numCominations(eval(tmpstr),nn+1)
            else:
                tmpComb[nn]=0
        tmpComb[nn]=0

    
main()