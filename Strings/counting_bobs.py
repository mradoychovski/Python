bob_num = 0
for i in range(len(s)-1):
    if s[i:i+3] == 'bob':
        bob_num += 1
print('Number of times bob occurs is: ' + str(bob_num))