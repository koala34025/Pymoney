balance = int(input("How much money do you have? "))
record = input("Add an expense or income record with description and amount:\n")
balance += int(record.split()[1])
print(f"Now you have {balance} dollars.")
