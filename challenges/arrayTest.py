import numpy as np
import numbers

stra = "b6???4xbl5??ee5"

def qMarks(strx):
    qcount = 0  
    nsum = 0
    numcount = 0
    for i in range(len(strx)):
        cr = strx[i]
        if cr.isdigit():
            nsum = nsum + int(cr)
            numcount = numcount +1
            if numcount>2:
                nsum = int(cr)
                numcount = 1
                qcount = 0
        elif cr == "?":
            if numcount > 0:
                qcount=qcount+1

        if nsum == 10 and qcount != 3:
            return False

    return True

def main():
    aaa = qMarks(stra)
    print("result= " + str(aaa))

main()




