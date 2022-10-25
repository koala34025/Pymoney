import sys

# Global variables
overall_records = [] # Store the records in a list of lists
init_money = 0

def initialize():
    try:
        # User input initial amount of money
        init_money = int(input('How much money do you have? '))
        print()
    except ValueError:
        init_money = 0
        sys.stderr.write('Invalid value for money. Set to 0 by default.\n\n') 

# Append a new record
def add_rec(desc, amt):
    global overall_records
    global balance
    
    try:
        int(amt)
        # Append the new record to overall_records
        overall_records += [[desc, amt]]
    except ValueError:
        sys.stderr.write('Invalid value for money.\n')
        sys.stderr.write('Fail to add a record.\n\n')
    
# List all the current records
def view_rec():
    global overall_records
    
    no_width = 3
    desc_width = 20
    amt_width = 6
    
    # Print formatting with above paramters
    print('Here\'s your expense and income records:')
    print(f'{"No.":{no_width}} {"Description":{desc_width}} {"Amount":{amt_width}}')
    print('=== ==================== ======')
    
    # List the overall records to the user
    for no, [desc, amt] in enumerate(overall_records, 1):
        print(f'{no:<{no_width}} {desc:{desc_width}} {amt:{amt_width}}')
    
    print('=== ==================== ======')

# Calculate and report the balance so far to the user
def view_bal():
    balance = init_money
    
    for desc, amt in overall_records:
        balance += int(amt)
    
    print(f'Now you have {balance} dollars.')
    print()
    
# Remove a record
def delete_rec(want_del):
    global overall_records
    global balance

    if want_del == 0:
        return
    
    if want_del < 0 or want_del > len(overall_records):
        sys.stderr.write(f'There\'s no record with No.{want_del}. Fail to delete a record.\n\n')
        return
    
    want_del -= 1 # Need adjustment becuase no. is 1 based and index is 0 based
    
    # Delete the record by concating former and latter list
    overall_records = overall_records[:want_del] + overall_records[want_del+1:]
    
try:
    fh = open('records.txt', 'r')
    
    first_line = fh.readline()
    init_money = int(first_line.split(',')[1][:-1])
    
    for desc_cma_amt_nl in fh.readlines():
        desc, amt_nl = desc_cma_amt_nl.split(',')
        amt = amt_nl[:-1]
        
        add_rec(desc, amt)
    
    fh.close()
    
    print('Welcome back!\n')

except FileNotFoundError:
    initialize()
        
except IndexError:
    sys.stderr.write('Invalid format in records.txt. Deleting the contents.\n')
    initialize()
    
# User input a command consecutively
while True:
    cmd = input('What do you want to do (add / view / delete / exit)? ')
    
    if cmd == 'add':
        try:
            record = input("Add an expense or income record with description and amount:\n")
            print()
            desc, amt = record.split()
            add_rec(desc, amt)
            
        except ValueError:
            sys.stderr.write('The format of a record should be like this: breakfast -50.\n')
            sys.stderr.write('Fail to add a record.\n\n')    
        
    elif cmd == 'view':
        view_rec()
        view_bal()
        
    elif cmd == 'delete':
        try:
            want_del = int(input("Which record do you want to delete (0 to skip)? No."))
            delete_rec(want_del)
        except ValueError:
            sys.stderr.write('Invalid format. Fail to delete a record.\n\n')
            
            
    elif cmd == 'exit': # Break when user enters exit
        with open('records.txt', 'w') as fh:
            fh.write(f'init,{init_money}\n')
            fh.writelines(desc + ',' + amt + '\n' for desc, amt in overall_records)
        
        print()
        break
    
    else:
        sys.stderr.write('Invalid command. Try again.\n\n')
