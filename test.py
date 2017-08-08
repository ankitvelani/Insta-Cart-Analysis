
import pymysql as PyMySQL

# Open database connection
db = PyMySQL.connect("localhost","root","root","Instacart" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "select * from departments"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      id = row[0]
      lname = row[1]
      
      # Now print fetched result
      print ("ID = %s,Name = %s" % \
             (id, lname))
except:
   print ("Error: unable to fetch data")

# disconnect from server
db.close()