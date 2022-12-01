import sys

class Record:
    '''Represent a records.
    '''
    def __init__(self, cate, desc, amt):
        '''Initialize a record
        '''
        self.set_category(cate)
        self.set_description(desc)
        self.set_amount(amt)

    def set_category(self, cate):
        '''Setter of _category
        '''
        if not categories.is_category_valid(cate):
            sys.stderr.write('The specified category is not in the category list.\n')
            sys.stderr.write('You can check the category list by command "view categories".\n')
            raise ValueError
        
        self._category = cate

    def set_description(self, desc):
        '''Setter of _description
        '''
        self._description = desc

    def set_amount(self, amt):
        '''Setter of _amount
        '''
        try:
            int(amt) # Check if amt is a numberic string
        except ValueError:
            sys.stderr.write('Invalid value for money.\n')
            raise ValueError
        
        self._amount = amt

    @property
    def category(self):
        return self._category
    
    @property
    def description(self):
        return self._description
    
    @property
    def amount(self):
        return self._amount

    
class Records:
    '''Maintain a list of all the 'Record's and the initial amount of money.
    '''
    def __init__(self):
        '''Initialize records
        '''
        self._initial_money = 0
        self._records = []
        self._prev_move = [] # A stack recording previous moves

        try:
            fh = open('records.txt', 'r') 
            first_line = fh.readline()
            wrong_msg = first_line
            self._initial_money = int(first_line.split(',')[-1].strip())
            
            for desc_cma_amt_nl in fh.readlines():
                wrong_msg = desc_cma_amt_nl
                cate, desc, amt_nl = desc_cma_amt_nl.split(',')
                amt = amt_nl.strip()
                record = Record(cate, desc, amt)
                self._records += [record]
        
            print('Welcome back!')
            fh.close()
            
        except FileNotFoundError:
            self._initial_money = self.prompt_init_money()
            
        # No line in the file -> IndexError
        # Invalid format -> ValueError
        except (IndexError, ValueError):
            sys.stderr.write(f'Invalid format in records.txt: {repr(wrong_msg)}. Deleting the contents.\n')
            self._initial_money = self.prompt_init_money()
            self._records.clear()
            fh.close()

            
    def prompt_init_money():
        '''Get an initial amount of money from the user
        '''
        try:
            initial_money = int(input('How much money do you have? '))
        except ValueError:
            # If the input cannot be converted to integer, set init_money to 0
            sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
            initial_money = 0
        
        return initial_money

    
    def add(self, record, categories):
        '''Add a record
        '''
        try:
            cate, desc, amt = record.split() # Check if the input format is valid
        except ValueError:
            sys.stderr.write('The format of a record should be like this: meal breakfast -50.\n')
            sys.stderr.write('Fail to add a record.\n')
            return
        
        try:
            record = Record(cate, desc, amt)
        except:
            sys.stderr.write('Fail to add a record.\n')
            return
        
        self._records += [record]
        self._prev_move.append(f'add {cate} {desc} {amt} {-1}')


    def view(self):
        '''Show all the records so far
        '''
        cate_width = 15
        no_width = 3
        desc_width = 20
        amt_width = 6
        
        print('Here\'s your expense and income records:')
        print(f'{"No.":{no_width}} {"Category":{cate_width}} {"Description":{desc_width}} {"Amount":{amt_width}}')
        print('=== =============== ==================== ======')
        
        for no, record in enumerate(self._records, 1):
            print(f'{no:<{no_width}} {record.category:{cate_width}} {record.description:{desc_width}} {record.amount:{amt_width}}')
            
        print('===============================================')

        balance = self._initial_money
        for record in self._records:
            balance += int(record.amount)
        
        print(f'Now you have {balance} dollars.')


    def delete(self, del_idx):
        '''Delete a record
        '''
        try:
            del_idx = int(del_idx)
            assert 0 <= del_idx <= len(self._records)
            
        except ValueError:
            # If the input cannot be converted into an integer
            sys.stderr.write('Invalid format. Fail to delete a record.\n')
            return
        
        except AssertionError:
            # If the input is out of bounds
            sys.stderr.write(f'There\'s no record with No.{del_idx}. Fail to delete a record.\n')
            return
        
        if del_idx == 0: # Do nothing if the input is 0
            return
        
        del_idx -= 1 # Need adjustment becuase No. is 1 based and the index is 0 based
        self._prev_move.append(f'delete {self._records[del_idx].category} {self._records[del_idx].description} {self._records[del_idx].amount} {del_idx}')
        self._records = self._records[:del_idx] + self._records[del_idx+1:]
        

    def edit(self, edit_idx):
        '''Edit a record
        '''
        try:
            edit_idx = int(edit_idx)
            assert 0 <= edit_idx <= len(self._records)
            
        except ValueError:
            # If the input cannot be converted into an integer
            sys.stderr.write('Invalid format. Fail to edit a record.\n')
            return
            
        except AssertionError:
            # If the input is out of bounds
            sys.stderr.write(f'There\'s no record with No.{edit_idx}. Fail to edit a record.\n')
            return
            
        if edit_idx == 0: # Do nothing if the input is 0
            return
            
        record = input("Edit the record with new category, description, and amount:\n")
        
        try:
            cate, desc, amt = record.split() # Check if the input format is valid
        except ValueError:
            sys.stderr.write('The format of a record should be like this: meal breakfast -50.\n')
            sys.stderr.write('Fail to edit a record.\n')
            return

        try:
            record = Record(cate, desc, amt)
        except:
            sys.stderr.write('Fail to edit a record.\n')
            return
        
        edit_idx -= 1 # Need adjustment becuase No. is 1 based and the index is 0 based
        self._prev_move.append(f'edit {self._records[edit_idx].category} {self._records[edit_idx].description} {self._records[edit_idx].amount} {edit_idx}')
        self._records[edit_idx] = record


    def find(self, subcategories):
        '''Show all the records under a certain category and its subcategories 
        '''
        cate_width = 15
        no_width = 3
        desc_width = 20
        amt_width = 6
        
        if len(subcategories) == 0:
            sys.stderr.write('The specified category is not in the category list.\n')
            sys.stderr.write('You can check the category list by command "view categories".\n')
            sys.stderr.write('Fail to find category.\n')
            return
        
        subrecords = list(filter(lambda record: record.category in subcategories, self._records))

        print(f'Here\'s your expense and income records under category "{subcategories[0]}":')
        print(f'{"No.":{no_width}} {"Category":{cate_width}} {"Description":{desc_width}} {"Amount":{amt_width}}')
        print('=== =============== ==================== ======')

        for no, record in enumerate(subrecords, 1):
            print(f'{no:<{no_width}} {record.category:{cate_width}} {record.description:{desc_width}} {record.amount:{amt_width}}')
            
        print('===============================================')

        total = 0
        for record in subrecords:
            total += int(record.amount)
        
        print(f'The total amount above is {total}.')


    def save(self):
        '''Save everything into records.txt before exiting the program
        '''
        try:
            with open('records.txt', 'w') as fh:
                fh.write(f'init,init,{self._initial_money}\n') # Comma seperate style
                fh.writelines(f'{record.category},{record.description},{record.amount}\n' for record in self._records) # Writelines
        except:
            sys.stderr.write('Fail to write records into records.txt.\n')

    
    def cancel(self):
        if len(self._prev_move) == 0:
            return

        operation, cate, desc, amt, idx = self._prev_move[-1].split()
        self._prev_move.pop()

        if operation == 'add':
            self._records.pop()

        elif operation == 'delete':
            self._records.insert(int(idx), Record(cate, desc, amt))

        elif operation == 'edit':
            self._records[int(idx)] = Record(cate, desc, amt)


class Categories:
    '''Maintain the category list and provide some methods.
    '''
    def __init__(self):
        '''Predefined categories, which are represented in a nested list
        '''
        self._categories = \
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


    def view(self):
        '''Show all the categories
        '''
        def view_categories(categories, level = -1):
            if type(categories) == str:
                print('  ' * level + '-', categories)
            else:
                for e in categories:
                    view_categories(e, level + 1)
        
        view_categories(self._categories)


    def is_category_valid(self, target):
        '''Return if a category is in the category list
        '''
        def is_category_valid_inner(target, categories):
            if type(categories) == str:
                return categories == target
                
            result = False
            for e in categories:
                result |= is_category_valid_inner(target, e)
            return result

        return is_category_valid_inner(target, self._categories)


    def find_subcategories(self, target):
        '''Return a flatten list containing a certain category and its subcategories
        '''
        def find_subcategories_gen(target, categories, found=False):
            '''A generator that yields the target category and its subcategories
            '''
            for idx, e in enumerate(categories):
                if type(e) == str:
                    if found:
                        yield e
                    if e == target:
                        yield e
                        if idx + 1 < len(categories) and type(categories[idx+1]) == list:
                            yield from find_subcategories_gen(target, categories[idx+1], True)
                else:
                    yield from find_subcategories_gen(target, e, found)

        def find_subcategories_inner(target, categories):
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
                    result += find_subcategories_inner(target, e)

            return result

        # return self._flatten(find_subcategories_inner(target, self._categories))
        return [i for i in find_subcategories_gen(target, self._categories)]

    def _flatten(self, L):
        '''Flat a nested list
        '''
        def flatten(L):
            if type(L) == str:
                return [L]

            ret = []
            for e in L:
                ret += flatten(e)
            return ret

        return flatten(L)


categories = Categories()
records = Records() 

while True:
    command = input('\nWhat do you want to do (add / view / delete / edit / view categories / find / cancel / exit)? ')
    
    if command == 'add':
        record = input("Add an expense or income record with category, description, and amount (separate by spaces):\n")
        records.add(record, categories)
        
    elif command == 'view':
        records.view()
        
    elif command == 'delete':
        del_idx = input("Which record do you want to delete (0 to skip)? No.")
        records.delete(del_idx)
        
    elif command == 'exit':
        records.save()
        break
    
    elif command == 'view categories':
        categories.view()

    elif command == 'find':
        target = input("Which category do you want to find? ")
        subcategories = categories.find_subcategories(target)
        records.find(subcategories)

    elif command == 'edit': 
        edit_idx = int(input("Which record do you want to edit (0 to skip)? No."))
        records.edit(edit_idx)
    
    elif command == 'cancel':
        records.cancel() # Cancel last move
        
    else:
        sys.stderr.write('Invalid command. Try again.\n')