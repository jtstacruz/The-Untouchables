import pymysql
import csv

# open connection to database
db = pymysql.connect("localhost", "root", "", "reviewer")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# reader to open SAMPLE.csv
csv_data = csv.reader(open('SAMPLE.csv'))

# drop table if it already exists using execute() method
cursor.execute("DROP TABLE IF EXISTS CUSTOMER")

# create table CUSTOMER
cursor.execute("create table IF NOT EXISTS CUSTOMER (CSTMR_ID LONG, REVIEWSITES_ID LONG, CSTMR_REVIEWER varchar(25), CSTMR_REVIEWTITLE varchar(100), CSTMR_REVIEW varchar(5000), CSTMR_RATINGDATE varchar(100), CSTMR_RATING varchar(100))")
# adding values to table from SAMPLE.csv
for row in csv_data:
    cursor.execute('INSERT INTO CUSTOMER values(%s,%s,%s,%s,%s,%s,%s)', row)
    print(row)

db.commit()
cursor.close()

db.close()
