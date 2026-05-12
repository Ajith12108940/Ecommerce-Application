from flask import Flask, request, redirect, render_template_string
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
            return "Added to Cart"
        return "Stock not enough"

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

HTML = '''

<!DOCTYPE html>
<html>
<head>
    <title>E-Commerce Store</title>

    <style>

        body{
            font-family: Arial;
            background:#f2f2f2;
            padding:20px;
        }

        h1{
            text-align:center;
            color:darkblue;
        }

        .box{
            background:white;
            padding:20px;
            margin:20px;
            border-radius:10px;
        }

        table{
            width:100%;
            border-collapse:collapse;
        }

        th,td{
            border:1px solid gray;
            padding:10px;
            text-align:center;
        }

        input{
            padding:8px;
            margin:5px;
        }

        button{
            padding:10px;
            background:green;
            color:white;
            border:none;
            border-radius:5px;
        }

    </style>

</head>

<body>

<h1>My E-Commerce Website</h1>

<div class="box">

<h2>Add Product</h2>

<form method="POST" action="/add">

<input type="number" name="id" placeholder="ID" required>
<input type="text" name="name" placeholder="Name" required>
<input type="number" step="0.01" name="price" placeholder="Price" required>
<input type="number" name="stock" placeholder="Stock" required>

<button type="submit">Add Product</button>

</form>

</div>

<div class="box">

<h2>Products</h2>

<table>

<tr>
<th>ID</th>
<th>Name</th>
<th>Price</th>
<th>Stock</th>
<th>Buy</th>
</tr>

{% for p in inventory %}

<tr>

<td>{{p.id}}</td>
<td>{{p.name}}</td>
<td>₹{{p.price}}</td>
<td>{{p.stock}}</td>

<td>

<form method="POST" action="/buy">

<input type="hidden" name="name" value="{{p.name}}">

<input type="number" name="qty" placeholder="Qty" required>

<button type="submit">Buy</button>

</form>

</td>

</tr>

{% endfor %}

</table>

</div>

<div class="box">

<h2>Cart Total: ₹{{total}}</h2>

</div>

</body>
</html>

'''

@app.route("/")
def home():
    total = cart.bill()
    return render_template_string(
        HTML,
        inventory=inventory,
        total=total
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