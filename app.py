from flask import Flask, render_template, send_from_directory, request 
 
app = Flask(__name__) 
 
# Sample menu items for demonstration 
menu_items = [ 
    "Vegetable Samosa", 
    "Paneer Tikka", 
    "Aloo Tikki", 
    "Butter Chicken", 
    "Palak Paneer", 
    "Chicken Biryani", 
    "Gulab Jamun", 
    "Kheer", 
    "Jalebi" 
] 
 
@app.route('/') 
def index(): 
    return render_template('index.html') 
 
@app.route('/menu/<table_number>', methods=['GET', 'POST']) 
def menu(table_number): 
    if request.method == 'POST': 
        selected_items = request.form.getlist('order[]') 
        # Process the selected items, e.g., store them in a database 
        print(f"Table {table_number} ordered: {selected_items}") 
 
    return render_template('menu.html', table_number=table_number, menu_items=menu_items) 
 
@app.route('/generate_qr/<table_number>') 
def generate_qr(table_number): 
    try: 
        # Generate QR code for the menu page specific to the table 
        # Your QR code generation logic here 
        # ... 
        img_path = f'static/qrcodes/table_{table_number}.png' 
        return send_from_directory('static/qrcodes', f'table_{table_number}.png') 
    except Exception as e: 
        print(f"Exception: {e}") 
        return str(e) 
 
if __name__ == '__main__': 
    app.run(debug=True)