max_str = s[0]
alpha_order = s[0]
max_len = 0
for i in range(1,len(s)):
    len_str = 0
    if alpha_order[-1] <= s[i]:
        alpha_order += s[i]
        if max_len < len(alpha_order):
            max_len = len(alpha_order)
            max_str = alpha_order
    else:
        alpha_order = s[i]
print('Longest substring in alphabetical order is: ' + max_str)