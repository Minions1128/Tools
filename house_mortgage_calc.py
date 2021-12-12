import numpy as np


def rate_calc(rate=0.05, pr=1000000, year=1):
    if pr < 100000:
        return
    # create 2 matrix str
    a, b = "", ""
    for i in range(1, 12 * year + 1):
        for j in range(1, 12 * year + 1):
            if i == j:
                a += "1,"
            elif i < j:
                a += "0,"
            else:
                a += "{},".format((rate / 12) * (-1))
        a += "-1;"
    for i in range(year * 12):
        a += "1,"
        b += "{},".format(pr * (-1) * rate / 12)
    a += "0"
    b += str(pr)

    A = np.mat(a)
    B = np.mat(b).T
    R = np.linalg.solve(A, B)

    # output
    mon_pay = float(R[-1])
    rest = pr
    total_int = 0
    for i in range(len(R) - 1):
        if i % 12 == 0:
            yearth = int(i / 12 + 1)
            yearth_str = ""
            if yearth in [1, 21]:
                yearth_str = str(yearth) + "st"
            elif yearth in [2, 22]:
                yearth_str = str(yearth) + "nd"
            else:
                yearth_str = str(yearth) + "th"
            print("The " + yearth_str + " year:")
            print("\tMon:     Total, Principal,  Interest,       Rest")
        mon = int(i % 12 + 1)
        pri = float(R[i])
        interest = rest * rate / 12
        total_int += interest
        rest = rest - pri
        print("\t{}: {}, {}, {}, {}".format(
            str(mon).rjust(3),
            str(round(mon_pay, 2)).rjust(9),
            str(round(pri, 2)).rjust(9),
            str(round(interest, 2)).rjust(9),
            str(round(rest, 2)).rjust(10),
        ))
    print("============================================================")
    print("Monthly Pay: " + str(round(mon_pay, 2)))
    print("Total Principal: " + str(int(pr / 1000000)) + " Mil")
    print("Total Interest: " + str(round(total_int, 2)))
    print("Year: " + str(year))


rate_calc(pr=1000000, year=30, rate=0.0465)
