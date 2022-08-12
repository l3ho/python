solution=[]

def calcMoney(tmpsum,nn,totalsum,strx):
    global solution
    if tmpsum==totalsum:
        if len(solution)==0 and len(strx)!=0:
            solution=strx[:]
            dd=1
        elif len(solution)>len(strx) and len(strx)!=0:
            solution=strx[:]
        #print(strx)
    else:
        for i in range(2):
            if i==0:
                strtmp = str(tmpsum) + " + 1 "
                sn = "+"
                tmpsumx=tmpsum+1               
            else:
                strtmp = str(tmpsum) + " * 2 "
                sn = "*"
                tmpsumx=2*tmpsum               
            if tmpsumx<=totalsum:
                tmpsum=tmpsumx
                strx.append(strtmp)
                calcMoney(tmpsum,nn+1,totalsum,strx)
                del strx[-1]
                if sn=="+":
                    tmpsum=tmpsum-1
                else:
                    tmpsum=tmpsum/2
                                 
def main():
    strout=[]

    calcMoney(1,0,10,strout)
    print(solution)

main()