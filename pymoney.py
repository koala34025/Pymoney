# Global variables
overall_records = [] # Store the records in a list
balance = 0 

# Append a new record and calculate new balance
def add():
    global overall_records
    global balance
    
    # User input a record
    record = input("Add an expense or income record with description and amount:\n")
    
    # Split the record into desc and amt
    desc, amt = record.split()
    
    # Append the new record(a list of one list of two) to overall_records
    overall_records += [[desc, amt]]
    
    # Calculate new balance
    balance += int(amt)

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

# Report the balance so far to the user
def view_bal():
    print(f'Now you have {balance} dollars.')

# Remove a record
def delete():
    global overall_records
    global balance

    # User input a record that will be deleted
    want_del = int(input("Which record do you want to delete (0 to skip)? No."))
    
    if want_del == 0:
        return False

    want_del -= 1 # Need adjustment becuase no. is 1 based and index is 0 based
    
    # Remove the amount of this record from the balance
    balance -= int(overall_records[want_del][1])
    
    # Delete the record by concating former and latter list
    overall_records = overall_records[:want_del] + overall_records[want_del+1:]
    
# User input initial amount of moeny
balance = int(input('How much money do you have? '))

# User input a command consecutively
while True:
    cmd = input('What do you want to do (add / view / delete / exit)? ')
    
    if cmd == 'add':
        add()
    elif cmd == 'view':
        view_rec()
        view_bal()
    elif cmd == 'delete':
        delete()
    elif cmd == 'exit': # Break when user enters exit
        break
