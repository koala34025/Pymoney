import sys

# Get an initial amount of money from the user
def get_init_money():
    try:
        initial_money = int(input('How much money do you have? '))
        
    except ValueError:
        # If the input cannot be converted to integer, set init_money to 0
        sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
        initial_money = 0
        
    finally:
        return initial_money

def initialize():
    initial_money = 0
    records = []
    
    try:
        fh = open('records.txt', 'r') 
        first_line = fh.readline()
        wrong_msg = first_line
        initial_money = int(first_line.split(',')[1].strip()) # Discard the redundant newline character
        
        for desc_cma_amt_nl in fh.readlines():
            wrong_msg = desc_cma_amt_nl
            desc, amt_nl = desc_cma_amt_nl.split(',')
            amt = amt_nl.strip() # Discards the redundant newline character
            int(amt) # Check if amt is a numberic string
            # Keep records a list of lists of strings for future str operations
            records += [[desc, amt]]
    
        print('Welcome back!')
        fh.close()
        
    except FileNotFoundError:
        initial_money = get_init_money()
        
    # If there is no line in the file -> IndexError
    # If any of the line cannot be interpreted as an initial amount of money or a record -> ValueError
    except (IndexError, ValueError):
        # Write out what is wrong in records.txt
        sys.stderr.write(f'Invalid format in records.txt: {repr(wrong_msg)}. Deleting the contents.\n')
        initial_money = get_init_money()
        records.clear()
        fh.close()
        
    finally:
        return initial_money, records
        
def add(records):
    record = input("Add an expense or income record with description and amount:\n")
    
    try:
        desc, amt = record.split()
    except ValueError:
        # If the input string cannot be split into a list of two strings
        sys.stderr.write('The format of a record should be like this: breakfast -50.\n')
        sys.stderr.write('Fail to add a record.\n')
        return records
    
    try:
        int(amt) # Check if amt is a numberic string
    except ValueError:
        # If amt cannot be converted to integer
        sys.stderr.write('Invalid value for money.\n')
        sys.stderr.write('Fail to add a record.\n')
    else:
        # Keep records a list of lists of strings for future str operations
        records += [[desc, amt]]
    finally:
        return records

def view(initial_money, records):
    # Parameters for print formatting
    no_width = 3
    desc_width = 20
    amt_width = 6
    
    print('Here\'s your expense and income records:')
    print(f'{"No.":{no_width}} {"Description":{desc_width}} {"Amount":{amt_width}}')
    print('=== ==================== ======')
    
    for no, [desc, amt] in enumerate(records, 1):
        print(f'{no:<{no_width}} {desc:{desc_width}} {amt:{amt_width}}')
        
    print('=== ==================== ======')

    balance = initial_money
    # Sum up the amount of money of records
    for desc, amt in records:
        balance += int(amt)
    
    print(f'Now you have {balance} dollars.')

def delete(records):
    try:
        wanna_del = int(input("Which record do you want to delete (0 to skip)? No."))
        assert 0 <= wanna_del <= len(records) # Ensure that the input is within the bounds
        
    except ValueError:
        # If the input cannot be converted into an integer
        sys.stderr.write('Invalid format. Fail to delete a record.\n')
        
    except AssertionError:
        # If the input is out of bounds
        sys.stderr.write(f'There\'s no record with No.{wanna_del}. Fail to delete a record.\n')
        
    else:
        if wanna_del == 0: # Do nothing if the input is 0
            return records
        
        wanna_del -= 1 # Need adjustment becuase No. is 1 based and the index is 0 based
        # Delete the record by concating the former and the latter list
        records = records[:wanna_del] + records[wanna_del+1:]
        
    finally:
        return records
    
def edit(records):
    try:
        wanna_edit = int(input("Which record do you want to edit (0 to skip)? No."))
        assert 0 <= wanna_edit <= len(records) # Ensure that the input is within the bounds
        
    except ValueError:
        # If the input cannot be converted into an integer
        sys.stderr.write('Invalid format. Fail to edit a record.\n')
        return records
        
    except AssertionError:
        # If the input is out of bounds
        sys.stderr.write(f'There\'s no record with No.{wanna_edit}. Fail to edit a record.\n')
        return records
        
    if wanna_edit == 0: # Do nothing if the input is 0
        return records
        
    record = input("Edit the record with new description and amount:\n")
    
    try:
        desc, amt = record.split()
    except ValueError:
        # If the input string cannot be split into a list of two strings
        sys.stderr.write('The format of a record should be like this: breakfast -50.\n')
        sys.stderr.write('Fail to edit a record.\n')
        return records

    try:
        int(amt) # Check if amt is a numberic string
    except ValueError:
        # If amt cannot be converted to integer
        sys.stderr.write('Invalid value for money.\n')
        sys.stderr.write('Fail to edit a record.\n')
        return records
    
    wanna_edit -= 1 # Need adjustment becuase No. is 1 based and the index is 0 based
    # Edit the record
    records[wanna_edit] = [desc, amt]
    
    return records
    
def save(initial_money, records):
    try:
        with open('records.txt', 'w') as fh:
            fh.write(f'init,{initial_money}\n') # Comma seperate style
            fh.writelines(f'{desc},{amt}\n' for desc, amt in records) # Writelines
    except:
        sys.stderr.write('Fail to write records into records.txt.\n')

# Store the records in a list of lists of 2 strings: [[desc1, amt1], [desc2, amt2], ...]
initial_money, records = initialize() 

while True:
    command = input('\nWhat do you want to do (add / view / delete / edit / exit)? ')
    
    if command == 'add':
        records = add(records)
        
    elif command == 'view':
        view(initial_money, records)
        
    elif command == 'delete':
        records = delete(records)
        
    elif command == 'exit':
        save(initial_money, records)
        break
    
    elif command == 'edit': 
        records = edit(records) # Edit a record
        
    else:
        sys.stderr.write('Invalid command. Try again.\n')