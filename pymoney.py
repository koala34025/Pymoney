balance = int(input("How much money do you have? "))
while True:
    record = input("Add an expense or income record with description and amount (Enter 0 to exit):\n")
    if record == '0':
        break
    balance += int(record.split()[1])
    print(f"Now you have {balance} dollars.")
