from flask import Flask, render_template,send_from_directory

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/services.html')  # Handle services page request
def services():
    return render_template('services.html')

@app.route('/about.html')  # Handle about page request
def about():
    return render_template('about.html')

# Add more routes as needed for other pages

if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Change the port to 8080 (or any other port you prefer)
