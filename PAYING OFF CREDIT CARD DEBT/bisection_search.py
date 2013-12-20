# Uses bisection search to find the fixed minimum monthly payment needed
# to finish paying off credit card debt within a year

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
annualInterestRate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))

monthlyInteretRate = annualInterestRate/12.0
high =(balance * (1 + monthlyInteretRate)**12)/12
total = 0
tempBalance = balance

while tempBalance > 0:
   month = 0
   while month < 12:
      interest = (tempBalance - high) * monthlyInteretRate
      tempBalance = (tempBalance - high) + interest
      total += high
      finalbalance = tempBalance - total
      month += 1
   if tempBalance < -0.01 or tempBalance > 0.01:
      high += tempBalance / 12.0
      tempBalance = balance
   else:
      break
   total=0
print('Lowest Payment: %.2f' % high)
