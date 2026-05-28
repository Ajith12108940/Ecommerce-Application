balance = 10000

transactions = [['W',3000],['D',5000], ['W',9000], ['W', 2000]]

for t, amt in transactions:

    if t == 'W' and balance >=amt:

        balance - amt

    elif t == 'D':

     balance += amt

print(balance)