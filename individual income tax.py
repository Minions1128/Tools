def compute_tax(salary):
    tax = 0
    flag = True
    sa = [83500, 58500, 38500, 12500, 8000, 5000, 3500, 0]
    ta = [0.45,  0.35,  0.3,   0.25,  0.2,  0.1,  0.03, 0]
    for idx in range(len(sa)):
        if salary > sa[idx]:
            if flag:
                tax = tax + (salary - sa[idx]) * ta[idx]
                flag = False
                continue
            tax = tax + (sa[idx-1]-sa[idx])*ta[idx]
    return tax


salarys = [2000, 4000, 6000, 10000, 20000, 40000, 80000, 100000]

for salary in salarys:
    tax = compute_tax(salary)
    print "salary:{} tax:{} after_tax:{}".format(salary, tax, salary-tax)
