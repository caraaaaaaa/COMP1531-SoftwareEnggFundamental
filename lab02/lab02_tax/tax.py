income = int(input("Enter your income: "))
if income <= 18200:
    tax = 0
elif income < 37000:
    tax = (income - 18200) * 0.19
elif income < 87000:
    tax = (income - 37000) * 0.325 + 3572
elif income < 180000:
    tax = (income - 87000) * 0.37 + 19822
else:
    tax = (income - 180000) * 0.45 + 54232

print('The estimated tax on your income is ${:,.2f}'.format(tax))