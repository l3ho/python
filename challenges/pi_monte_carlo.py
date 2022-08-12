import random

def main():
    rr = 2.0
    nn=100000
    n_ok = 0
    n_error = 0

    for i in range(nn):
        xx = rr*(random.random())
        yy = rr*(random.random())
        tmpSum = xx*xx + yy*yy
        if tmpSum<=rr*rr:
            n_ok+=1
        else:
            n_error+=1

    Pmc = (2.0*rr)*(2.0*rr)*float(n_ok/nn)
    Pi = Pmc/(rr*rr)
    print(Pi)


main()