import numpy as np
bigN = "0"

def genNumber(itx,numx,i_list):
    global bigN
    if itx == i_list.size:
        if float(numx)>float(bigN):
            bigN=numx
    else:
        for ii in range(0,len(i_list)):
            if i_list[ii]!="":
                numx = numx + str(i_list[ii])
                tmpval=str(i_list[ii])
                i_list[ii]=""
                genNumber(itx+1,numx,i_list)
                i_list[ii]=tmpval
                numx = numx[:(len(numx)-len(tmpval))]

def main():
    arr = np.array([5,1,8,9],dtype=object)

    genNumber(0,"",arr)

    print(bigN)

main()            



