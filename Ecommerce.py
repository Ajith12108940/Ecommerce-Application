from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)

app.secret_key = "flipkart"

products = [

    # SHIRTS
    {
        "id": 1,
        "name": "nylon Shirt",
        "price": 386,
        "category": "Shirts",
        "image": "/static/images/shirts/shirt1.webp"
    },

    {
        "id": 2,
        "name": "check Shirt",
        "price": 261,
        "category": "Shirts",
        "image": "/static/images/shirts/shirt2.webp"
    },

    {
        "id": 3,
        "name": "printed Shirt",
        "price": 469,
        "category": "Shirts",
        "image": "/static/images/shirts/shirt3.webp"
    },

    {
        "id": 4,
        "name": "Check Shirt",
        "price": 437,
        "category": "Shirts",
        "image": "/static/images/shirts/shirt4.webp"
    },



    # PANTS
    {
        "id": 5,
        "name": "Black Pant",
        "price": 317,
        "category": "Pants",
        "image": "/static/images/pants/pant1.webp"
    },

    {
        "id": 6,
        "name": "Printed Pant",
        "price": 442,
        "category": "Pants",
        "image": "/static/images/pants/pant2.webp"
    },

    {
        "id": 7,
        "name": "Grey Pant",
        "price": 458,
        "category": "Pants",
        "image": "/static/images/pants/pant3.webp"
    },

    {
        "id": 8,
        "name": "Cargo Pant",
        "price": 750,
        "category": "Pants",
        "image": "/static/images/pants/pant4.webp"
    },



    # DHOTIS
    {
        "id": 9,
        "name": "White Dhoti",
        "price": 352,
        "category": "Dhotis",
        "image": "/static/images/dhotis/dhoti1.webp"
    },

    {
        "id": 10,
        "name": "Traditional Dhoti",
        "price": 283,
        "category": "Dhotis",
        "image": "/static/images/dhotis/dhoti2.webp"
    },

    {
        "id": 11,
        "name": "Cotton Dhoti",
        "price": 385,
        "category": "Dhotis",
        "image": "/static/images/dhotis/dhoti3.webp"
    },

    {
        "id": 12,
        "name": " Dhoti",
        "price": 389,
        "category": "Dhotis",
        "image": "/static/images/dhotis/dhoti4.webp"
    },



    # SAREES
    {
        "id": 13,
        "name": "zenz Saree",
        "price": 486,
        "category": "Sarees",
        "image": "/static/images/sarees/saree1.webp"
    },

    {
        "id": 14,
        "name": " trendy Saree",
        "price": 283,
        "category": "Sarees",
        "image": "/static/images/sarees/saree2.webp"
    },

    {
        "id": 15,
        "name": " printed Saree",
        "price": 499,
        "category": "Sarees",
        "image": "/static/images/sarees/saree3.webp"
    },

    {
        "id": 16,
        "name": "Printed Saree",
        "price": 558,
        "category": "Sarees",
        "image": "/static/images/sarees/saree4.webp"
    },



    # HALF SAREES
    {
        "id": 17,
        "name": " Half Saree",
        "price": 938,
        "category": "Half Sarees",
        "image": "/static/images/halfsarees/halfsaree1.webp"
    },

    {
        "id": 18,
        "name": "Half Saree",
        "price": 884,
        "category": "Half Sarees",
        "image": "/static/images/halfsarees/halfsaree2.webp"
    },

    {
        "id": 19,
        "name": "Designer Half Saree",
        "price": 380,
        "category": "Half Sarees",
        "image": "/static/images/halfsarees/halfsaree3.webp"
    },

    {
        "id": 20,
        "name": "Half Saree",
        "price": 1125,
        "category": "Half Sarees",
        "image": "/static/images/halfsarees/halfsaree4.webp"
    }

]

cart = []
wishlist = []
buy_items = []

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        mobile = request.form['mobile']
        password = request.form['password']

        if password == "ajith@123":

            session['mobile'] = mobile

            return redirect('/')

    return render_template('login.html')

@app.route('/logout')
def logout():

    session.pop('mobile', None)

    return redirect('/login')

@app.route('/')
def home():

    if 'mobile' not in session:

        return redirect('/login')

    return render_template(
        'index.html',
        user=session['mobile']
    )

@app.route('/category/<category>')
def category(category):

    filtered = []

    for p in products:

        if p["category"] == category:

            filtered.append(p)

    return render_template(
        'category.html',
        products=filtered,
        category=category,
        user=session['mobile']
    )

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

    return redirect('/wishlist-page')

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

@app.route('/wishlist-page')
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
    host="0.0.0.0",
    port=3000,
    debug=False
)