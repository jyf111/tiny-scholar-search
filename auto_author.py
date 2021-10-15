import pymysql
 
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='scholar')
 
cursor = db.cursor()
cursor.execute('DROP TABLE IF EXISTS AUTHOR')
sql = """CREATE TABLE AUTHOR (
         ID INT NOT NULL,
         NAME CHAR(20) NOT NULL,
         AFFILIATIONS VARCHAR(256),
         PUBCOUNT INT,
         CITECOUNT INT,
         HINDEX INT ,
         INTERESTS VARCHAR(512),
         PRIMARY KEY (ID) );"""
cursor.execute(sql)

def insert(cursor, id, name, affiliations, pubcount, citecount, hindex, interests):
    sql = 'INSERT INTO AUTHOR VALUES (' \
        + id + r', "' \
        + name + r'", "' \
        + affiliations + r'", ' \
        + pubcount + ', ' \
        + citecount + ', ' \
        + hindex + r', "' \
        + interests + r'");'
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

with open('Author-test.txt', 'r') as f:
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
        insert(cursor, id, name, affiliations, pubcount, citecount, hindex, interests)
        if not f.readline():
            break
db.close()