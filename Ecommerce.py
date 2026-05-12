from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

FILE = "inventory.csv"

class Product:
    def __init__(self, i, n, p, s):
        self.id = i
        self.name = n
        self.price = p
        self.stock = s

class Cart:
    def __init__(self):
        self.items = []

    def add(self, p, q):
        if p.stock >= q:
            p.stock -= q
            self.items.append((p.name, p.price, q))

    def bill(self):
        return sum(price * q for _, price, q in self.items)

cart = Cart()

def save(inv):
    with open(FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "price", "stock"])

        for p in inv:
            w.writerow([p.id, p.name, p.price, p.stock])

def load():
    inv = []

    try:
        with open(FILE) as f:
            r = csv.DictReader(f)

            for x in r:
                inv.append(
                    Product(
                        int(x["id"]),
                        x["name"],
                        float(x["price"]),
                        int(x["stock"])
                    )
                )
    except:
        pass

    return inv

inventory = load()

@app.route("/")
def home():
    return render_template(
        "index.html",
        inventory=inventory,
        total=cart.bill()
    )

@app.route("/add", methods=["POST"])
def add():

    i = int(request.form["id"])
    n = request.form["name"]
    p = float(request.form["price"])
    s = int(request.form["stock"])

    inventory.append(Product(i, n, p, s))

    save(inventory)

    return redirect("/")

@app.route("/buy", methods=["POST"])
def buy():

    n = request.form["name"]
    q = int(request.form["qty"])

    for p in inventory:

        if p.name.lower() == n.lower():

            cart.add(p, q)

            save(inventory)

    return redirect("/")

if __name__ == "__main__":
    app.run(port=3000, debug=True)