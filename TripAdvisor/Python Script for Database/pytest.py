import xlrd
import MySQLdb

# Open the workbook and define the worksheet
book = xlrd.open_workbook("SAMPLE.xlsx")
sheet = book.sheet_by_name("source")

# Establish a MySQL connection
database = MySQLdb.connect (host="localhost", user = "root", passwd = "", db = "mysqlPython")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
query = """INSERT INTO CUSTOMER (CSTMR_ID, REVIEWSITES_ID, CSTMR_REVIEWER, CSTMR_REVIEWTITLE, CSTMR_REVIEW, CSTMR_RATINGDATE, CSTMR_RATING) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

# Create a For loop to iterate through each row in the CSV file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
      CSTMR_ID            = sheet.cell(r,).value
      REVIEWSITES_ID      = sheet.cell(r,1).value
      CSTMR_REVIEWER      = sheet.cell(r,2).value
      CSTMR_REVIEWTITLE   = sheet.cell(r,3).value
      CSTMR_REVIEW        = sheet.cell(r,4).value
      CSTMR_RATINGDATE    = sheet.cell(r,5).value
      CSTMR_RATING        = sheet.cell(r,6).value

      # Assign values from each row
      values = (CSTMR_ID, REVIEWSITES_ID, CSTMR_REVIEWER, CSTMR_REVIEWTITLE, CSTMR_REVIEW, CSTMR_RATINGDATE, CSTMR_RATING)

      # Execute sql Query
      cursor.execute(query, values)

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print ""
print ""
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print "I just imported " + columns + " columns and " + rows + " rows to MySQL!"
