import pymysql

f = open(r"SAMPLE.csv", "r")
fString = f.read()

# convert string to list
fList = []
for line in fString.split('\n'):
    fList.append(line.split(','))

# open connection to database
db = pymysql.connect("localhost", "mysql_user", "password", "reviewer")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# drop table if it already exists using execute() method
cursor.execute("DROP TABLE IF EXISTS CUSTOMER")

# create column names from the first line in fList
CSTMR_ID = fList[0][0]; REVIEWSITES_ID = fList[0][1]; CSTMR_REVIEWER = fList[0][2]; CSTMR_REVIEWTITLE = fList[0][3]; CSTMR_REVIEW = fList[0][4]; CSTMR_RATINGDATE = fList[0][5]; CSTMR_RATING = fList[0][6]

# create CUSTOMER table // place comma after each new column except the last
queryCreateCustomerTable = """CREATE TABLE CUSTOMER(
                            {} int not null,
                            {} int not null,
                            {} varchar(25),
                            {} varchar(100),
                            {} varchar(5000),
                            {} varchar(100),
                            {} varchar(10)
                            )""".format(CSTMR_ID, REVIEWSITES_ID, CSTMR_REVIEWER, CSTMR_REVIEWTITLE, CSTMR_REVIEW, CSTMR_RATINGDATE, CSTMR_RATING)
cursor.execute(queryCreateCustomerTable)

db.close()
