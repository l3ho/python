def checkPalindrome(nn):
    nnstr = str(nn)
    palFlag = True
    for i in range(int(len(nnstr)/2)):
        if nnstr[i]!=nnstr[len(nnstr)-1-i]:
            palFlag=False
            break
    return palFlag

def main():
    it = 0
    ulimit = 999
    flimit = 100
    bigP = 0
    while ulimit>flimit:
        for i in range(ulimit,flimit,-1):
            numx = i*ulimit
            dd = checkPalindrome(numx)
            it+=1
            if dd == True:
                if bigP<numx:
                    bigP = numx                             
                flimit = i
                break
        ulimit=ulimit-1

    print(bigP,it)
        
    
main()
        