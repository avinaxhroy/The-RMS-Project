from ticket import book_ticket
from login import login_system
from train_schedule import view_train_schedule

print(r'''
 _______  _             _                           _____          _  _                         
|__   __|| |           | |                         |  __ \        (_)| |                        
   | |   | |__    ___  | |       __ _  ____ _   _  | |__) |  __ _  _ | |__      __  __ _  _   _ 
   | |   | '_ \  / _ \ | |      / _` ||_  /| | | | |  _  /  / _` || || |\ \ /\ / / / _` || | | |
   | |   | | | ||  __/ | |____ | (_| | / / | |_| | | | \ \ | (_| || || | \ V  V / | (_| || |_| |
   |_|   |_| |_| \___| |______| \__,_|/___| \__, | |_|  \_\ \__,_||_||_|  \_/\_/   \__,_| \__, |
                                             __/ |                                         __/ |
                                            |___/                                         |___/ 

      ''')

print('''
##   ##  #######   ####     #####    #####   ##   ##  #######  
##   ##   ##  ##    ##     ##   ##  ##   ##  ### ###   ##  ##  
##   ##   ##        ##     ##       ##   ##  #######   ##      
## # ##   ####      ##     ##       ##   ##  ## # ##   ####    
#######   ##        ##     ##       ##   ##  ##   ##   ##      
### ###   ##  ##    ## ##  ##   ##  ##   ##  ##   ##   ##  ##  
##   ##  #######   ######   #####    #####   ##   ##  #######  
                                                               

''')
app_on=True
while app_on==True:
    print(' 1.Book Ticket \n 2.Login \n 3.View Train Schedule')
    use1=int(input("What you want?: "))
    if use1==1:
        book_ticket()
        end1=input("Do you want to run again(Yes/No)?:\t").upper
        if end1 == 'N' or end1 == 'NO':
            app_on = False
    elif use1==2:
        login_system()
        end2=input("Do you want to run again(Yes/No)?:\t").upper
        if end2 == 'N' or end2 == 'NO':
            app_on = False
    elif use1==3:
        view_train_schedule()
        end3=input("Do you want to run again(Yes/No)?:\t").upper
        if end3 == 'N' or end3 == 'NO':
            app_on = False
        