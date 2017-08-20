import pymysql

f = open(r"SAMPLE.csv", "r")
fString = f.read()

# convert string to list
fList = []
for line in fString.split('\n'):
    fList.append(line.split(','))

# open connection to database
db = pymysql.connect("localhost", "root", "", "reviewer")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# drop table if it already exists using execute() method
#cursor.execute("create database IF NOT EXISTS REVIEWER")
cursor.execute("DROP TABLE IF EXISTS CUSTOMER")

# create column names from the first line in fList
#CSTMR_ID = fList[0][0]; REVIEWSITES_ID = fList[0][1]; CSTMR_REVIEWER = fList[0][2]; CSTMR_REVIEWTITLE = fList[0][3]; CSTMR_REVIEW = fList[0][4]; CSTMR_RATINGDATE = fList[0][5]; CSTMR_RATING = fList[0][6]

# create CUSTOMER table // place comma after each new column except the last
#queryCreateCustomerTable = """CREATE TABLE CUSTOMER(
#                            {} int not null,
#                            {} int not null,
#                            {} varchar(25),
#                            {} varchar(100),
#                            {} varchar(5000),
#                            {} varchar(100),
#                            {} varchar(10)
#                            )""".format(CSTMR_ID, REVIEWSITES_ID, CSTMR_REVIEWER, CSTMR_REVIEWTITLE, CSTMR_REVIEW, CSTMR_RATINGDATE, CSTMR_RATING)
cursor.execute("create table IF NOT EXISTS CUSTOMER (CSTMR_ID INT, REVIEWSITES_ID INT, CSTMR_REVIEWER varchar(25), CSTMR_REVIEWTITLE varchar(100), CSTMR_REVIEW varchar(5000), CSTMR_RATINGDATE varchar(100), CSTMR_RATING varchar(10))")
cursor.execute("INSERT INTO CUSTOMER (CSTMR_ID, REVIEWSITES_ID, CSTMR_REVIEWER, CSTMR_REVIEWTITLE, CSTMR_REVIEW, CSTMR_RATINGDATE, CSTMR_RATING) values(001,1,'yesha','good','nice','aug 10','50')")
db.commit()

#del fList[0]

# generate multiple values from the list to be placed in a query
#rows = ''
#for i in range(len(fList) - 1):
#    rows += "('{}','{}','{}','{}','{}','{}','{}')".format(fList[i][0], fList[i][1], fList[i][2], fList[i][3], fList[i][4], fList[i][5], fList[i][6])
#    if i != len(fList) - 2:
#        rows += ','

# print(rows) // used to make sure the last value is not a comma
#queryInsert = "INSERT INTO CUSTOMER VALUES" + rows

#try:
    # execute the SQL command
#    cursor.execute(queryInsert)
    # commit changes to the database
#    db.commit()
#except:
    # rollback in case there are any error
#    db.rollback()

db.close()
