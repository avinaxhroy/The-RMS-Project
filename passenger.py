import pymysql
import pandas as pd
from tabulate import tabulate

dbconect = pymysql.connect(
    host="localhost", 
    user='dbuser', 
    password='password', 
    database='rmsdb'
)

cursor = dbconect.cursor()


#view all passenger data
def view_passenger():
    query="SELECT * FROM passengers"
    cursor.execute(query)
    result=cursor.fetchall()
    pasnger=pd.DataFrame(result, columns=['Passenger_ID', 'Name', 'Cost', 'Destination', 'Travel Date'])
    print(tabulate(pasnger,headers='keys', tablefmt='grid'))