import csv

FILE = "inventory.csv"

class Product:
    def __init__(self, i, n, p, s):
        self.id, self.name, self.price, self.stock = i, n, p, s

class Cart:
    def __init__(self):
        self.items = []
        

    def add(self, p, q):
        if p.stock >= q:
            p.stock -= q
            self.items.append((p.name, p.price, q))
            print("Added")
        else:
            print("Stock not enough")

    def bill(self):
        t = sum(price*q for _, price, q in self.items)
        print("Total:", t)

def save(inv):
    with open(FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","name","price","stock"])
        for p in inv:
            w.writerow([p.id,p.name,p.price,p.stock])

def load():
    inv = []
    try:
        with open(FILE) as f:
            r = csv.DictReader(f)
            for x in r:
                inv.append(Product(int(x["id"]),x["name"],float(x["price"]),int(x["stock"])))
    except:
        pass
    return inv

inv = load()
cart = Cart()

while True:
    print("\n1 Add  2 Show  3 Buy  4 Bill  5 Exit")
    c = input("Choice: ")

    if c=="1":
        i=int(input("ID: "))
        n=input("Name: ")
        p=float(input("Price: "))
        s=int(input("Stock: "))
        inv.append(Product(i,n,p,s))
        save(inv)

    elif c=="2":
        for p in inv:
            print(p.id,p.name,p.price,p.stock)

    elif c=="3":
        n=input("Name: ")
        q=int(input("Qty: "))
        for p in inv:
            if p.name.lower()==n.lower():
                cart.add(p,q)
                save(inv)

    elif c=="4":
        cart.bill()

    elif c=="5":
        break