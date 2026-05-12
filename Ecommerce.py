from flask import Flask, render_template, request, redirect, session
import csv
import random
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = "ecommerce_secret"

PRODUCT_FILE = "inventory.csv"
USER_FILE = "users.csv"
ORDER_FILE = "orders.csv"
REVIEW_FILE = "reviews.csv"

class Product:

    def __init__(self, pid, name, price, stock, category):

        self.id = pid
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

products = []
cart = []
wishlist = []

# ---------------- LOAD PRODUCTS ----------------

def load_products():

    global products

    products = []

    try:

        with open(PRODUCT_FILE) as f:

            reader = csv.DictReader(f)

            for row in reader:

                products.append(

                    Product(
                        int(row['id']),
                        row['name'],
                        float(row['price']),
                        int(row['stock']),
                        row['category']
                    )

                )

    except:
        pass

# ---------------- SAVE PRODUCTS ----------------

def save_products():

    with open(PRODUCT_FILE, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "id",
            "name",
            "price",
            "stock",
            "category"
        ])

        for p in products:

            writer.writerow([
                p.id,
                p.name,
                p.price,
                p.stock,
                p.category
            ])

# ---------------- HOME PAGE ----------------

@app.route('/')
def home():

    load_products()

    search = request.args.get('search', '')

    filtered = []

    for p in products:

        if search.lower() in p.name.lower():

            filtered.append(p)

    if search == '':

        filtered = products

    recommendations = random.sample(
        filtered,
        min(3, len(filtered))
    ) if filtered else []

    return render_template(
        'index.html',
        products=filtered,
        recommendations=recommendations,
        cart_total=sum(item['price'] for item in cart)
    )

# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        with open(USER_FILE, 'a', newline='') as f:

            writer = csv.writer(f)

            writer.writerow([username, password])

        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        try:

            with open(USER_FILE) as f:

                reader = csv.reader(f)

                for row in reader:

                    if row[0] == username and row[1] == password:

                        session['user'] = username

                        return redirect('/')

        except:
            pass

    return render_template('login.html')

# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')

# ---------------- ADD PRODUCT ----------------

@app.route('/add', methods=['POST'])
def add_product():

    pid = int(request.form['id'])
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    category = request.form['category']

    products.append(
        Product(
            pid,
            name,
            price,
            stock,
            category
        )
    )

    save_products()

    return redirect('/')

# ---------------- ADD TO CART ----------------

@app.route('/cart/<int:pid>')
def add_to_cart(pid):

    for p in products:

        if p.id == pid and p.stock > 0:

            cart.append({

                'name': p.name,
                'price': p.price

            })

            p.stock -= 1

            save_products()

    return redirect('/')

# ---------------- VIEW CART ----------------

@app.route('/view-cart')
def view_cart():

    total = sum(item['price'] for item in cart)

    return render_template(
        'cart.html',
        cart=cart,
        total=total
    )

# ---------------- WISHLIST ----------------

@app.route('/wishlist/<int:pid>')
def add_to_wishlist(pid):

    for p in products:

        if p.id == pid:

            wishlist.append(p)

    return redirect('/')

# ---------------- PLACE ORDER ----------------

@app.route('/place-order')
def place_order():

    total = sum(item['price'] for item in cart)

    with open(ORDER_FILE, 'a', newline='') as f:

        writer = csv.writer(f)

        writer.writerow([
            session.get('user', 'Guest'),
            total
        ])

    cart.clear()

    return "Order Placed Successfully"

# ---------------- ORDERS ----------------

@app.route('/orders')
def orders():

    order_list = []

    try:

        with open(ORDER_FILE) as f:

            reader = csv.reader(f)

            for row in reader:

                order_list.append({

                    'user': row[0],
                    'total': row[1]

                })

    except:
        pass

    return render_template(
        'orders.html',
        orders=order_list
    )

# ---------------- PRODUCT REVIEW ----------------

@app.route('/review/<int:pid>', methods=['POST'])
def review(pid):

    text = request.form['review']

    sentiment = TextBlob(text).sentiment.polarity

    mood = "Positive"

    if sentiment < 0:

        mood = "Negative"

    with open(REVIEW_FILE, 'a', newline='') as f:

        writer = csv.writer(f)

        writer.writerow([
            pid,
            text,
            mood
        ])

    return redirect('/')

# ---------------- AI CHATBOT ----------------

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():

    reply = ""

    if request.method == 'POST':

        message = request.form['message'].lower()

        if "hello" in message:

            reply = "Hello User! Welcome to AI Ecommerce Store."

        elif "laptop" in message:

            reply = "We have gaming laptops and office laptops."

        elif "mobile" in message:

            reply = "Latest mobiles are available in Electronics."

        elif "price" in message:

            reply = "All prices are displayed on homepage."

        elif "discount" in message:

            reply = "Current discount is 20% on Electronics."

        elif "order" in message:

            reply = "Go to cart and click place order."

        elif "payment" in message:

            reply = "Payment options: UPI, Card, Net Banking."

        elif "delivery" in message:

            reply = "Delivery usually takes 3 to 5 days."

        elif "refund" in message:

            reply = "Refund available within 7 days."

        elif "bye" in message:

            reply = "Thank you for visiting our store."

        else:

            reply = "AI Bot could not understand your question."

    return render_template(
        'chatbot.html',
        reply=reply
    )

# ---------------- ADMIN DASHBOARD ----------------

@app.route('/admin')
def admin():

    total_products = len(products)

    total_cart = len(cart)

    total_stock = sum(p.stock for p in products)

    return render_template(
        'admin.html',
        total_products=total_products,
        total_cart=total_cart,
        total_stock=total_stock
    )

# ---------------- RUN APPLICATION ----------------

if __name__ == '__main__':

    load_products()

    app.run(
        debug=True,
        port=3000
    )