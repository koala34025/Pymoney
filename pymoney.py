import sys


def initialize_categories():
    '''Predefined categories, which are represented in a nested list
    '''
    return \
    [
        'expense', 
        [
            'food',
            [
                'meal', 
                'snack', 
                'drink'
            ], 
            'transportation', 
            [
                'bus', 
                'railway'
            ]
        ], 
        'income', 
        [
            'salary', 
            'bonus'
        ]
    ]


def view_categories(categories, level = -1):
    '''Show all the categories
    '''
    if type(categories) == str:
        print('  ' * level + '-', categories)
    else:
        for e in categories:
            view_categories(e, level + 1)


def is_category_valid(target, categories):
    '''Return if a category is in the category list
    '''
    if type(categories) == str:
        return categories == target
        
    result = False
    for e in categories:
        result |= is_category_valid(target, e)
    return result


def find_subcategories(target, categories):
    '''Return a nested list containing a certain category and its subcategories
    '''
    result = []
    for idx, e in enumerate(categories):
        if type(e) == str:
            if e == target:
                if idx + 1 < len(categories) and type(categories[idx+1]) == list:
                    return categories[idx: idx+2]
                else:
                    return [categories[idx]]
        else:
            result += find_subcategories(target, e)

    return result


def flatten(L):
    '''Flat a nested list
    '''
    if type(L) == str:
        return [L]

    ret = []
    for e in L:
        ret += flatten(e)
    return ret


def find(records, categories):
    '''Show all the records under a certain category and its subcategories 
    '''
    target = input("Which category do you want to find? ")

    # Parameters for print formatting
    cate_width = 15
    no_width = 3
    desc_width = 20
    amt_width = 6
    
    print(f'Here\'s your expense and income records under category "{target}":')
    print(f'{"No.":{no_width}} {"Category":{cate_width}} {"Description":{desc_width}} {"Amount":{amt_width}}')
    print('=== =============== ==================== ======')
    
    subcategories = flatten(find_subcategories(target, categories))
    subrecords = list(filter(lambda record: record[0] in subcategories, records))

    for no, [cate, desc, amt] in enumerate(subrecords, 1):
        print(f'{no:<{no_width}} {cate:{cate_width}} {desc:{desc_width}} {amt:{amt_width}}')
        
    print('===============================================')

    total = 0
    # Sum up the amount of money of records
    for cate, desc, amt in subrecords:
        total += int(amt)
    
    print(f'The total amount above is {total}.')


def get_init_money():
    '''Get an initial amount of money from the user
    '''
    try:
        initial_money = int(input('How much money do you have? '))
        
    except ValueError:
        # If the input cannot be converted to integer, set init_money to 0
        sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
        initial_money = 0
        
    finally:
        return initial_money


def initialize():
    '''Initialize when re-entering the program
    '''
    initial_money = 0
    records = []
    
    try:
        fh = open('records.txt', 'r') 
        first_line = fh.readline()
        wrong_msg = first_line
        initial_money = int(first_line.split(',')[-1].strip()) # Discard the redundant newline character
        
        for desc_cma_amt_nl in fh.readlines():
            wrong_msg = desc_cma_amt_nl
            cate, desc, amt_nl = desc_cma_amt_nl.split(',')
            amt = amt_nl.strip() # Discards the redundant newline character
            int(amt) # Check if amt is a numberic string
            # Keep records a list of lists of strings for future str operations
            records += [[cate, desc, amt]]
    
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


def add(records, categories):
    '''Add a record
    '''
    record = input("Add an expense or income record with category, description, and amount(separate by spaces):\n")
    
    try:
        cate, desc, amt = record.split()
    except ValueError:
        # If the input string cannot be split into a list of two strings
        sys.stderr.write('The format of a record should be like this: meal breakfast -50.\n')
        sys.stderr.write('Fail to add a record.\n')
        return records
    
    # Handle cate not in categories
    if not is_category_valid(cate, categories):
        sys.stderr.write('The specified category is not in the category list.\n')
        sys.stderr.write('You can check the category list by command "view categories".\n')
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
        records += [[cate, desc, amt]]
    finally:
        return records


def view(initial_money, records):
    '''Show all the records so far
    '''
    # Parameters for print formatting
    cate_width = 15
    no_width = 3
    desc_width = 20
    amt_width = 6
    
    print('Here\'s your expense and income records:')
    print(f'{"No.":{no_width}} {"Category":{cate_width}} {"Description":{desc_width}} {"Amount":{amt_width}}')
    print('=== =============== ==================== ======')
    
    for no, [cate, desc, amt] in enumerate(records, 1):
        print(f'{no:<{no_width}} {cate:{cate_width}} {desc:{desc_width}} {amt:{amt_width}}')
        
    print('===============================================')

    balance = initial_money
    # Sum up the amount of money of records
    for cate, desc, amt in records:
        balance += int(amt)
    
    print(f'Now you have {balance} dollars.')


def delete(records):
    '''Delete a record
    '''
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
    '''Edit a record
    '''
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
        
    record = input("Edit the record with new category, description, and amount:\n")
    
    try:
        cate, desc, amt = record.split()
    except ValueError:
        # If the input string cannot be split into a list of two strings
        sys.stderr.write('The format of a record should be like this: meal breakfast -50.\n')
        sys.stderr.write('Fail to edit a record.\n')
        return records

    # Handle cate not in categories
    if not is_category_valid(cate, categories):
        sys.stderr.write('The specified category is not in the category list.\n')
        sys.stderr.write('You can check the category list by command "view categories".\n')
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
    records[wanna_edit] = [cate, desc, amt]
    
    return records


def save(initial_money, records):
    '''Save everything into records.txt before exiting the program
    '''
    try:
        with open('records.txt', 'w') as fh:
            fh.write(f'init,init,{initial_money}\n') # Comma seperate style
            fh.writelines(f'{cate},{desc},{amt}\n' for cate, desc, amt in records) # Writelines
    except:
        sys.stderr.write('Fail to write records into records.txt.\n')


# Store the records in a list of lists of 2 strings: [[desc1, amt1], [desc2, amt2], ...]
initial_money, records = initialize() 
categories = initialize_categories()

while True:
    command = input('\nWhat do you want to do (add / view / delete / edit / view categories / find / exit)? ')
    
    if command == 'add':
        records = add(records, categories)
        
    elif command == 'view':
        view(initial_money, records)
        
    elif command == 'delete':
        records = delete(records)
        
    elif command == 'exit':
        save(initial_money, records)
        break
    
    elif command == 'view categories':
        view_categories(categories)

    elif command == 'find':
        find(records, categories)

    elif command == 'edit': 
        records = edit(records) # Edit a record
        
    else:
        sys.stderr.write('Invalid command. Try again.\n')