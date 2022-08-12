def super_digit(nn):
    if len(str(nn))==1:
        return nn
    else:
        sumn = 0
        for i in range(len(nn)):
            sumn = sumn+int(nn[i])
        return super_digit(str(sumn))

def main():
    print(super_digit("11"))

main()