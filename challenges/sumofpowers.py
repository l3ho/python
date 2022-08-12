
def checkPow(yy,mm,curSum,sumList,nn):
    if curSum==yy:
        printList(sumList,mm,yy)
    else:
        for i in range(nn,int(yy**(1/mm))+1):
            curval = i**mm
            curSum=curSum+curval
            if curSum<=yy and i not in sumList and i > sumList[len(sumList)-1]:
                sumList.append(i)
                checkPow(yy,mm,curSum,sumList,nn+1)
                curSum=curSum-curval
                sumList.remove(i)
            else:
                curSum=curSum-curval

def printList(xlist,kk,totalSum):
    p_sum = ""
    for i in range(1,len(xlist)):
        if i < len(xlist)-1:
            p_sum = p_sum + str(xlist[i]) + "^" + str(kk) + " + "
        else:
            p_sum = p_sum + str(xlist[i]) + "^" + str(kk)
    p_sum = p_sum + " = " + str(totalSum)
    print(p_sum)
    

def main():
   arx=[]
   arx.append(0)
   checkPow(100,3,0,arx,1)

main()