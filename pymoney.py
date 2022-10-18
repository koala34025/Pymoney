balance = int(input("How much money do you have? "))

# Consecutive inputs
while True:
    input_str = input("Add some expense or income records with description and amount:\n" \
    "desc1 amt1, desc2 amt2, desc3 amt3, ...(Enter 'q' to exit)\n")
    
    # Break when user enters a single q
    if input_str == 'q':
        break
    
    # Split the input string with ', ' to make a 'desc amt' list
    records = input_str.split(', ')
    
    # Make output string in advance when records is still a str list
    output_string = '\n'.join(records)
    
    # Split each record into 'desc', 'amt'
    # Change each record(list) to tuple type(also convert amt into int type)
    for index, desc_amt in enumerate(records):
        desc, amt = desc_amt.split()
        records[index] = (desc, int(amt))
    
    # Sum up all the amt
    balance += sum(amt for desc, amt in records)
    
    # List the records to the user
    print("Here's your expense and income records:")
    print(output_string)
    
    # Report the balance to the user
    print(f"Now you have {balance} dollars.")
