def parse(num):
    res = ""
    while num>=1000:
        s = str(int(num%1000))
        while len(s)<3:
            s = '0' + s
        res = ',' + s + res;
        num //= 1000;
    res = str(num) + res;
    return res;