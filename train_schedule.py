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

#view all train schedule
def view_train_schedule():
    query="select * from train_schedule"
    cursor.execute(query)
    result=cursor.fetchall()
    df=pd.DataFrame(result,columns=['Train_No', 'Departure', 'Arrival', 'Route'])
    print(tabulate(df,headers='keys', tablefmt='grid'))
#edit train schedule
def edit_train_schedule(train_no):
    query = 'SELECT train_no, departure, arrival, route FROM train_schedule WHERE train_no = %s'
    cursor.execute(query, (train_no,))
    result = cursor.fetchone()  # Fetch one row
    if not result:
        print("Train Number not Found")
        return
    train_no, current_departure, current_arrival, current_route = result

    #Asking to new train schedule
    departure = input(f"Enter new departure time (HH:MM, leave blank to keep '{current_departure}'): ") or current_departure
    arrival = input(f"Enter new arrival time (HH:MM, leave blank to keep '{current_arrival}'): ") or current_arrival
    route = input(f"Enter new route (leave blank to keep '{current_route}'): ") or current_route

    update_query="update train_schedule set departure = %s, arrival = %s, route = %s WHERE train_no = %s"
    cursor.execute(update_query,(departure,arrival,route,train_no))
    dbconect.commit()
    print(f"Train No {train_no} updated successfully.")

def edit_train_main():
    tr_no=input('Enter Train No to edit details: ')
    edit_train_schedule(tr_no)
