g_cnt = 0

def calc_result(m_operations):
    n_nrs = len(m_operations)+1
    out_str = ""
    for ii in range(n_nrs):
        out_str += str(ii + 1)
        if ii > 0 and ii < len(m_operations):
            if m_operations[ii] != "0":
                out_str += m_operations[ii]
    return out_str

def split_numbers(n_len, n_bin, nn):
    global g_cnt
    if len(n_bin) == n_len:
        abc = calc_result(n_bin)
        math_string, res = calc_string(abc)
        if res == 100:
            print(n_bin, abc, res, g_cnt)
        g_cnt += 1
    else:
        for j in range(1, 4):
            if j == 1:
                n_bin += "0"
            elif j == 2:
                n_bin += "-"
            elif j == 3:
                n_bin += "+"
            split_numbers(n_len, n_bin, nn+1)
            n_bin = n_bin[:len(n_bin) - 1]

def getMove(i_list, numx, nn):
    if len(numx) == 3:
        print(numx)
    else:
        for i in range(len(i_list)):
            numx = numx + str(i_list[i])
            getMove(i_list, numx, nn+1)
            numx = numx[:len(numx)-1]

def calc_string(math_string):
    math_list = []
    tmp_str = ""
    for ii in range(len(math_string)):
        if math_string[ii] != "+" and math_string[ii] != "-":
            tmp_str += math_string[ii]
        else:
            math_list.append(tmp_str)
            math_list.append(math_string[ii])
            tmp_str = ""
    math_list.append(tmp_str)
    res = int(math_list[0])
    for ii in range(len(math_list)):
        if math_list[ii] == "+":
            res = res + int(math_list[ii + 1])
        elif math_list[ii] == "-":
            res = res - int(math_list[ii + 1])
    return math_list, res

def main():
    abc = [1, 2, 3, 4, 5, 6, 8, 9, 10]
    #abc = [1, 2, 3, 4, 5]
    split_numbers(len(abc) - 1, "", 0)


main()