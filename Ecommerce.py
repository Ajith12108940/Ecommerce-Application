from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)

app.secret_key = "flipkart_clone"

products = [

    {
        "id": 1,
        "name": "Black Shirt",
        "price": 999,
        "category": "Shirts",
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf"
    },

    {
        "id": 2,
        "name": "White Shirt",
        "price": 1299,
        "category": "Shirts",
        "image": "https://images.unsplash.com/photo-1603252109303-2751441dd157"
    },

    {
        "id": 3,
        "name": "Blue Shirt",
        "price": 1499,
        "category": "Shirts",
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab"
    },

    {
        "id": 4,
        "name": "Casual Shirt",
        "price": 1199,
        "category": "Shirts",
        "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f"
    },

    {
        "id": 5,
        "name": "Jeans Pant",
        "price": 1999,
        "category": "Pants",
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d"
    },

    {
        "id": 6,
        "name": "Formal Pant",
        "price": 2499,
        "category": "Pants",
        "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a"
    },

    {
        "id": 7,
        "name": "Black Pant",
        "price": 1799,
        "category": "Pants",
        "image": "https://images.unsplash.com/photo-1506629905607-c6d7c3e0f94b"
    },

    {
        "id": 8,
        "name": "Cargo Pant",
        "price": 2299,
        "category": "Pants",
        "image": "https://images.unsplash.com/photo-1514996937319-344454492b37"
    },

    {
        "id": 9,
        "name": "Traditional Dhoti",
        "price": 999,
        "category": "Dhotis",
        "image": "https://images.unsplash.com/photo-1618354691438-25bc04584c23"
    },

    {
        "id": 10,
        "name": "Wedding Dhoti",
        "price": 1499,
        "category": "Dhotis",
        "image": "https://images.unsplash.com/photo-1622445275463-afa2ab738c34"
    },

    {
        "id": 11,
        "name": "Cotton Dhoti",
        "price": 899,
        "category": "Dhotis",
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c"
    },

    {
        "id": 12,
        "name": "Silk Dhoti",
        "price": 1999,
        "category": "Dhotis",
        "image": "https://images.unsplash.com/photo-1597983073493-88cd35cf93b0"
    },

    {
        "id": 13,
        "name": "Black Saree",
        "price": 3999,
        "category": "Sarees",
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c"
    },

    {
        "id": 14,
        "name": "Red Saree",
        "price": 4999,
        "category": "Sarees",
        "image": "https://images.unsplash.com/photo-1597983073493-88cd35cf93b0"
    },

    {
        "id": 15,
        "name": "Wedding Saree",
        "price": 6999,
        "category": "Sarees",
        "image": "https://images.unsplash.com/photo-1622445275463-afa2ab738c34"
    },

    {
        "id": 16,
        "name": "Silk Saree",
        "price": 7999,
        "category": "Sarees",
        "image": "https://images.unsplash.com/photo-1618354691438-25bc04584c23"
    },

    {
        "id": 17,
        "name": "Pink Half Saree",
        "price": 4999,
        "category": "Half Sarees",
        "image": "https://images.unsplash.com/photo-1597983073493-88cd35cf93b0"
    },

    {
        "id": 18,
        "name": "Blue Half Saree",
        "price": 5299,
        "category": "Half Sarees",
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c"
    },

    {
        "id": 19,
        "name": "Traditional Half Saree",
        "price": 6499,
        "category": "Half Sarees",
        "image": "https://images.unsplash.com/photo-1622445275463-afa2ab738c34"
    },

    {
        "id": 20,
        "name": "Designer Half Saree",
        "price": 8999,
        "category": "Half Sarees",
        "image": "https://images.unsplash.com/photo-1618354691438-25bc04584c23"
    }

]

cart = []
wishlist = []
buy_items = []

@app.route('/')
def home():

    user = session.get("mobile")

    return render_template(
        'index.html',
        products=products,
        user=user
    )

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        mobile = request.form['mobile']

        session['mobile'] = mobile

        return redirect('/')

    return render_template('login.html')

# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():

    session.pop('mobile', None)

    return redirect('/')

@app.route('/add-to-cart/<int:pid>')
def add_to_cart(pid):

    for p in products:

        if p["id"] == pid:

            cart.append(p)

    return redirect('/cart')

@app.route('/wishlist/<int:pid>')
def add_to_wishlist(pid):

    for p in products:

        if p["id"] == pid:

            wishlist.append(p)

    return redirect('/wishlist')

@app.route('/buy/<int:pid>')
def buy_product(pid):

    for p in products:

        if p["id"] == pid:

            buy_items.append(p)

    return redirect('/buy-page')

@app.route('/cart')
def cart_page():

    total = sum(item["price"] for item in cart)

    return render_template(
        'cart.html',
        items=cart,
        total=total,
        title="Cart"
    )

@app.route('/wishlist')
def wishlist_page():

    total = sum(item["price"] for item in wishlist)

    return render_template(
        'cart.html',
        items=wishlist,
        total=total,
        title="Wishlist"
    )

@app.route('/buy-page')
def buy_page():

    total = sum(item["price"] for item in buy_items)

    return render_template(
        'cart.html',
        items=buy_items,
        total=total,
        title="Buy Products"
    )

if __name__ == "__main__":

    app.run(
        debug=True,
        port=3000
    )