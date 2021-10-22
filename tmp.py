result = ""
with open('ccf.txt', 'r') as f:
    while True:
        cur = f.readline()
        if not cur:
            break
        tmp = ""
        tmp += cur[1] + ' ';
        for i, c in enumerate(cur):
            if c=='/' and (cur[i+1]=='c' or cur[i+1]=='j'):
                while cur[i]=='/' or cur[i].isalpha() or cur[i].isdigit():
                    tmp += cur[i]
                    i += 1
                break
        if len(tmp)!=2:
            result += tmp + '\n'
f  = open('ccfrank.txt', 'w')
f.writelines(result)
f.close()
    