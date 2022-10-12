import ctypes

def one_loop():
    r_string = "11abc22"
    letters = ""
    new_string = ""
    ii = 0
    zz = len(r_string) - 1
    while len(new_string) < len(r_string):
        if not r_string[ii].isdigit():
            if not r_string[zz].isdigit():
                new_string = new_string + r_string[zz]
                ii += 1
                zz -= 1
            else:
                zz -= 1
        else:
            new_string = new_string + r_string[ii]
            ii += 1
    print(new_string)
    ctypes.windll.user32.MessageBoxW(0, str(new_string), "Information", 1)


def two_loops():
    r_string = "a1b2c"
    letters = ""
    new_string = ""
    for ii in range(len(r_string)):
        if not r_string[ii].isdigit():
            letters = r_string[ii] + letters
    aa = 0
    for ii in range(len(r_string)):
        if not r_string[ii].isdigit():
            new_string += letters[aa]
            aa += 1
        else:
            new_string += r_string[ii]

    print(new_string)


def main():
    one_loop()

if __name__ == '__main__':
    main()
