def isLargest(numx, arx):
    l_flag = True
    for jj in range(len(arx)):
        numx_s = str(numx)
        for kk in range(len(numx_s)):
            if arx[jj]>int(numx_s[kk]):
                l_flag = False
                break
    return l_flag    

def main():
    in_arr = (9,5,3,52,521)
    bigN = ""
    cntr = len(in_arr)
    in_list = list(in_arr)

    while cntr>0:
        for kk in range(len(in_list)):
            if isLargest(in_list[kk],in_list):
                bigN=bigN + str(in_list[kk])
                in_list.remove(in_list[kk])
                cntr=cntr-1
                break

    print(bigN)

main()



