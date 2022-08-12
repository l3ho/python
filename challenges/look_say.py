def getNextTerm(prx):
    curx = ""
    cntr = 1
    for i in range(len(prx)):
        if i < len(prx)-1:
            if prx[i] == prx[i+1]:
                cntr += 1
            else:
                curx = curx + str(cntr) + prx[i]
                cntr = 1
        else:
            curx = curx + str(cntr) + prx[i]
    return curx

def main():
    nn = 6
    prev = "1"
    cur = ""

    for i in range(1, nn):
        print("The " + str(i) + " term is: " + prev)
        cur = getNextTerm(prev)
        prev = cur

    print("The " + str(nn) + " term is: " + cur)

main()