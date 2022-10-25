# Import modules
import sys

# Global variables
overall_records = [] # Store the records in a list of lists of strings
init_money = 0 # Initial amount of money from the first line of records.txt
last_line = '' # Record the last reading line to show what is unacceptable in the file with error message

# Get an initial amount of money from the user
def get_init_money():
    global init_money
    
    try:
        # User input an initial amount of money
        init_money = int(input('How much money do you have? '))
    except ValueError:
        # If the input cannot be converted to integer, set init_money to 0
        sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
        init_money = 0

# Append a new record
def add_rec(desc, amt):
    global overall_records
    global balance
    
    try:
        # Check if amt is a numberic string
        int(amt) 
        # Append the new record to overall_records
        # Keep overall_records a list of lists of strings for future str operations
        overall_records += [[desc, amt]]
    except ValueError:
        # If amt cannot be converted to integer
        sys.stderr.write('Invalid value for money.\n')
        sys.stderr.write('Fail to add a record.\n')
    
# List all the current records
def view_rec():
    global overall_records
    
    # Parameters for print formatting
    no_width = 3
    desc_width = 20
    amt_width = 6
    
    print('Here\'s your expense and income records:')
    print(f'{"No.":{no_width}} {"Description":{desc_width}} {"Amount":{amt_width}}')
    print('=== ==================== ======')
    
    # List the overall records to the user
    for no, [desc, amt] in enumerate(overall_records, 1):
        print(f'{no:<{no_width}} {desc:{desc_width}} {amt:{amt_width}}')
    
    print('=== ==================== ======')

# Calculate and report the balance so far to the user
def view_bal():
    # Assign balance the initial amount of money
    balance = init_money
    
    # Sum up the amount of money of all records
    for desc, amt in overall_records:
        balance += int(amt)
    
    # Report the balance
    print(f'Now you have {balance} dollars.')
    
# Remove a record
def delete_rec(want_del):
    global overall_records
    global balance

    # Raise error and skip if want_del is out of bounds
    if want_del < 0 or want_del > len(overall_records):
        sys.stderr.write(f'There\'s no record with No.{want_del}. Fail to delete a record.\n')
        return
    
    # Skip if want_del is 0
    if want_del == 0:
        return
    
    want_del -= 1 # Need adjustment becuase No. is 1 based and index is 0 based
    
    # Delete the record by concating the former and the latter list
    overall_records = overall_records[:want_del] + overall_records[want_del+1:]

# Open 'records.txt' at the beginning of the program
try:
    fh = open('records.txt', 'r')
    
    # Read the first line, which is the initial amount of money, into init_money
    first_line = fh.readline()
    last_line = first_line
    init_money = int(first_line.split(',')[1].strip()) # .strip() discards the redundant newline character

    # Read all the rest records into overall_records
    for desc_cma_amt_nl in fh.readlines():
        last_line = desc_cma_amt_nl
        desc, amt_nl = desc_cma_amt_nl.split(',')
        amt = amt_nl.strip() # .strip() discards the redundant newline character
        int(amt) # Check if amt is a numberic string in advance
        add_rec(desc, amt) 
    
    # A successful read means that it's not the first time the user start the program
    print('Welcome back!')
    
    # Close 'records.txt' after reading
    fh.close()
    
# If the file does not exist, prompt the user for the initial amount of money
except FileNotFoundError:
    get_init_money()

# If there is no line in the file -> IndexError
# If any of the line cannot be interpreted as an initial amount of money or a record -> ValueError
except (ValueError, IndexError):
    sys.stderr.write(f'Invalid format in records.txt: {repr(last_line)}. Deleting the contents.\n')
    overall_records.clear()
    get_init_money()
    # Close 'records.txt' after reading
    fh.close()

finally:
    print()

# Program: allow user to input commands consecutively
while True:
    cmd = input('What do you want to do (add / view / delete / exit)? ')
    
    if cmd == 'add':
        record = input("Add an expense or income record with description and amount:\n")
        try:
            desc, amt = record.split()
            add_rec(desc, amt)
        except ValueError:
            # If the input string cannot be split into a list of two strings
            sys.stderr.write('The format of a record should be like this: breakfast -50.\n')
            sys.stderr.write('Fail to add a record.\n')
        
    elif cmd == 'view':
        view_rec()
        view_bal()
        
    elif cmd == 'delete':
        try:
            want_del = int(input("Which record do you want to delete (0 to skip)? No."))
            delete_rec(want_del)
        except ValueError:
            # If the input cannot be converted into an integer
            sys.stderr.write('Invalid format. Fail to delete a record.\n')
            
    elif cmd == 'exit':
        # Before the program terminates, write init_money and overall_records into the file
        with open('records.txt', 'w') as fh:
            fh.write(f'init,{init_money}\n') # Comma seperate style
            fh.writelines(desc + ',' + amt + '\n' for desc, amt in overall_records)
        break # Exit the program
    
    else:
        # If the user inputs a string that is not one of the four above.
        sys.stderr.write('Invalid command. Try again.\n')
    
    print()