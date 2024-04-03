from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from flask_pymongo import PyMongo
from bson import ObjectId
from flask_login import LoginManager, UserMixin, login_user, current_user
import qrcode
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Replace this with your own secret key

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
db = PyMongo(app).db

orders_collection = db.orders

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)

# User model for Flask-Login
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user_data = db.Users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        user = User()
        user.id = str(user_data['_id'])
        user.username = user_data['username']  # Assigning username attribute
        return user
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get registration form data
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        if db.Users.find_one({"username": username}):
            return render_template('register.html', error='Username already exists')

        # Store user details in the database with default role as 'user'
        db.Users.insert_one({"username": username, "password": password, "role": "user"})

        # Redirect to login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve user data from the database
        user_data = db.Users.find_one({"username": username, "password": password})

        if user_data:
            # Authentication successful
            user = User()
            user.id = str(user_data['_id'])
            login_user(user)

            # Check if user has admin role
            if user_data['role'] == 'admin':
                # Redirect to admin dashboard
                return redirect(url_for('admin'))
            else:
                # Redirect to menu page
                return redirect(url_for('menu', table_number=1))

        else:
            # Authentication failed, show login page with error message
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu/<table_number>')
def menu(table_number):
    if current_user.is_authenticated:
        return render_template('menu.html', table_number=table_number)
    else:
        return redirect(url_for('login'))

@app.route('/generate_qr/<table_number>')
def generate_qr(table_number):
    try:
        # Generate QR code for the menu page specific to the table
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        menu_url = f'http://127.0.0.1:8080/menu/{table_number}'  # Change to your actual server address
        qr.add_data(menu_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_path = os.path.join('static', 'qrcodes', f'table_{table_number}.png')
        img.save(img_path)

        return send_from_directory('static/qrcodes', f'table_{table_number}.png')
    except Exception as e:
        print(f"Exception: {e}")
        return str(e)
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if request.method == 'POST':
        # Get user ID from current session
        user_id = current_user.get_id()

        # Retrieve username from user ID
        user_data = db.Users.find_one({"_id": ObjectId(user_id)})
        username = user_data['username']

        # Retrieve order details from the request
        order_details = request.json  # Assuming JSON data is sent in the request

        # Get current date and time
        current_time = datetime.now()

        # Print user's basic details and order details to terminal
        print(f"Username: {username}, User ID: {user_id}, Order details: {order_details}, Order Time: {current_time}")

        # Store user's basic details, order details, and order time in the database
        orders_collection.insert_one({
            "username": username,
            "user_id": user_id,
            "order_details": order_details,
            "order_time": current_time,
            "table_number": order_details.get("table_number")
        })

        return jsonify({"message": "Order placed successfully!", "username": username})

@app.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated:
        # Retrieve all orders from the database
        all_orders = list(orders_collection.find())

        # Render the admin dashboard template with orders data
        return render_template('admin.html', orders=all_orders)
    else:
        return redirect(url_for('login'))

@app.route('/services/<table_number>')
def services(table_number):
    if current_user.is_authenticated:
        return render_template('services.html', table_number=table_number)
    else:
        return redirect(url_for('login'))
@app.route('/contact/<table_number>')
def contact(table_number):
    if current_user.is_authenticated:
        return render_template('contact.html', table_number=table_number)
    else:
        return redirect(url_for('login'))

@app.route('/about/<table_number>')
def about(table_number):
    if current_user.is_authenticated:
        return render_template('about.html', table_number=table_number)
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True, port=8080)
