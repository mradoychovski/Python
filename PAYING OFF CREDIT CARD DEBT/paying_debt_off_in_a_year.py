# Determines fixed minimum monthly payment needed to finish paying off credit card debt in 1 year

initialBalance = float(raw_input("Enter the outstanding balance on your credit card: "))
interestRate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))

monthlyInterestRate = annualInterestRate / 12.0
minimumMonthlyPayment = (balance * monthlyInterestRate)
lowestPayment = 10
tempBalance = balance
month = 0

while tempBalance > 0:
   tempBalance = (tempBalance - lowestPayment) * (1 + monthlyInterestRate)
   month = month + 1
   if(month > 12):
       month = 0
       lowestPayment += 10
       tempBalance = balance
print ("Lowest Payment: %d" % lowestPayment)
