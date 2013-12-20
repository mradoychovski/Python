# Determines remaining credit card balance after a year of making the minimum payment each month

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
annualInterestRate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))
monthlyPaymentRate = float(raw_input("Enter the minimum monthly payment rate as a decimal: "))

# Monthly Interest Rate
monthlyInterestRate = annualInterestRate/12

totalPaid = 0

for month in range(1,13):
    print ("Month: %d" % month)
    print ("Minimum monthly payment: %.2f" % (balance * monthlyPaymentRate))
    totalPaid += balance * monthlyPaymentRate
    balance -= balance * monthlyPaymentRate
    print ("Remaining balance: %.2f" % (balance + monthlyInterestRate * balance))
    print
    balance += monthlyInterestRate * balance
    
print ("Total paid: %.2f" % totalPaid)
print ("Remaining balance: %.2f" % balance)