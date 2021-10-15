from scholar.models import Author
import myweb.wsgi
a = Author.objects()

with open('../Author-test.txt', 'r') as f:
    while True:
        id = f.readline().strip('#index \n')
        name = f.readline().strip('#n \n')
        affiliations = f.readline().strip('#a \n')
        pubcount = f.readline().strip('#pc \n')
        citecount = f.readline().strip('#cn \n')
        hindex = f.readline().strip('#hi \n')
        f.readline() # drop pi
        f.readline() # drop upi
        interests = f.readline().strip('#t \n')
        # print(id, name, affiliations, pubcount, citecount, hindex, interests, sep='\n')
        a.create(id, name, affiliations, pubcount, citecount, hindex, interests)
        if not f.readline():
            break