from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "chaishop_secret_key"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

def create_database():

    conn = get_db()

    # Customers table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT
        )
    """)

    # Products table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    # Orders table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL
        )
    """)

    # Interactions table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_database()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return redirect("/login")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["user"] = username

            return redirect("/dashboard")

        else:

            message = "Invalid Username or Password"

    return render_template(
        "login.html",
        message=message
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn = get_db()

    customer_count = conn.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    product_count = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    order_count = conn.execute(
        "SELECT COUNT(*) FROM orders"
    ).fetchone()[0]

    interaction_count = conn.execute(
        "SELECT COUNT(*) FROM interactions"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        customers=customer_count,
        products=product_count,
        orders=order_count,
        interactions=interaction_count
    )


# =========================================================
# MODULE 1
# CUSTOMER MANAGEMENT
# =========================================================

@app.route("/customers")
def customers():

    if "user" not in session:
        return redirect("/login")

    conn = get_db()

    customer_data = conn.execute(
        "SELECT * FROM customers ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "customers.html",
        customers=customer_data
    )


# ADD CUSTOMER

@app.route("/add_customer", methods=["POST"])
def add_customer():

    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    address = request.form["address"]

    conn = get_db()

    conn.execute("""
        INSERT INTO customers
        (name, phone, email, address)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        phone,
        email,
        address
    ))

    conn.commit()
    conn.close()

    return redirect("/customers")


# DELETE CUSTOMER

@app.route("/delete_customer/<int:id>")
def delete_customer(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM customers WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/customers")


# =========================================================
# MODULE 2
# PRODUCT & ORDER MANAGEMENT
# =========================================================

@app.route("/products")
def products():

    if "user" not in session:
        return redirect("/login")

    conn = get_db()

    product_data = conn.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()

    order_data = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "products.html",
        products=product_data,
        orders=order_data
    )


# ADD PRODUCT

@app.route("/add_product", methods=["POST"])
def add_product():

    name = request.form["name"]
    price = request.form["price"]

    conn = get_db()

    conn.execute("""
        INSERT INTO products
        (name, price)
        VALUES (?, ?)
    """, (
        name,
        price
    ))

    conn.commit()
    conn.close()

    return redirect("/products")


# DELETE PRODUCT

@app.route("/delete_product/<int:id>")
def delete_product(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM products WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/products")


# ADD ORDER

@app.route("/add_order", methods=["POST"])
def add_order():

    customer_name = request.form["customer_name"]
    product_name = request.form["product_name"]
    quantity = request.form["quantity"]
    total = request.form["total"]

    conn = get_db()

    conn.execute("""
        INSERT INTO orders
        (customer_name, product_name, quantity, total)
        VALUES (?, ?, ?, ?)
    """, (
        customer_name,
        product_name,
        quantity,
        total
    ))

    conn.commit()
    conn.close()

    return redirect("/products")


# DELETE ORDER

@app.route("/delete_order/<int:id>")
def delete_order(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM orders WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/products")


# =========================================================
# MODULE 3
# CUSTOMER INTERACTION & FEEDBACK
# =========================================================

@app.route("/interactions")
def interactions():

    if "user" not in session:
        return redirect("/login")

    conn = get_db()

    interaction_data = conn.execute(
        "SELECT * FROM interactions ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "interactions.html",
        interactions=interaction_data
    )


# ADD INTERACTION

@app.route("/add_interaction", methods=["POST"])
def add_interaction():

    customer_name = request.form["customer_name"]
    interaction_type = request.form["type"]
    message = request.form["message"]
    status = request.form["status"]

    conn = get_db()

    conn.execute("""
        INSERT INTO interactions
        (customer_name, type, message, status)
        VALUES (?, ?, ?, ?)
    """, (
        customer_name,
        interaction_type,
        message,
        status
    ))

    conn.commit()
    conn.close()

    return redirect("/interactions")


# DELETE INTERACTION

@app.route("/delete_interaction/<int:id>")
def delete_interaction(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM interactions WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/interactions")


# =========================================================
# MODULE 4
# REPORTS
# =========================================================

@app.route("/reports")
def reports():

    if "user" not in session:
        return redirect("/login")

    conn = get_db()

    total_customers = conn.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    total_products = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    total_orders = conn.execute(
        "SELECT COUNT(*) FROM orders"
    ).fetchone()[0]

    total_interactions = conn.execute(
        "SELECT COUNT(*) FROM interactions"
    ).fetchone()[0]

    total_sales = conn.execute(
        "SELECT COALESCE(SUM(total), 0) FROM orders"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "reports.html",
        total_customers=total_customers,
        total_products=total_products,
        total_orders=total_orders,
        total_interactions=total_interactions,
        total_sales=total_sales
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)