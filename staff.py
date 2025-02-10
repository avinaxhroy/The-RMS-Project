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


#view all staff data
def view_staff():
    query="SELECT * FROM staff"
    cursor.execute(query)
    result=cursor.fetchall()
    staf=pd.DataFrame(result, columns=['Staff_ID', 'Name', 'Role', 'Address', 'Salary'])
    print(tabulate(staf,headers='keys', tablefmt='grid'))

#import specific staff details
def edit_staff(staff_id):
    query="select name, role, address, salary FROM staff WHERE staff_id = %s"
    cursor.execute(query,(staff_id,))
    result=cursor.fetchall()
    if not result:
        print("Staff ID not found!")
        return
    current_name,current_role,current_address,current_salary=result[0]
    sname=input(f"Enter new name (leave blank to keep '{current_name}'): ") or current_name
    srole=input(f"Enter new role (leave blank to keep '{current_role}'): ") or current_role
    saddress=input(f"Enter new address (leave blank to keep '{current_address}'): ") or current_address
    ssalary=input(f"Enter new salary (leave blank to keep '{current_salary}'): ") or current_salary

    update_query="update staff set name=%s, role=%s, address=%s, salary=%s WHERE staff_id=%s"
    cursor.execute(update_query,(sname, srole, saddress, ssalary,staff_id))

    #print update data
    print("""Data Updated Sucessfully
          Here Your updated Data""")
    conform_query="SELECT * FROM staff WHERE staff_id=%s"
    cursor.execute(conform_query,(staff_id,))
    result_new=cursor.fetchall()
    staf=pd.DataFrame(result_new, columns=['Staff_ID', 'Name', 'Role', 'Address', 'Salary'])
    print(tabulate(staf,headers='keys', tablefmt='grid'))

#main programm to edit staff details
def edit_staff_main():
    sid=int(input("Enter the Staff Id to edit details: "))
    edit_staff(sid)