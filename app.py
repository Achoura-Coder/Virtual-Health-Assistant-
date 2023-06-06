from flask import Flask, render_template, request, redirect
import bcrypt
import pymongo

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["health_assistant"]
users_collection = db["users"]

# Homepage route
@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
         # Validate the user input
        if not username or not password:
            return render_template('register.html', message="Please enter a username and a password.")
        # Check if the username already exists
        if users_collection.find_one({"username": username}):
            return render_template('register.html', message="This username is already taken. Please choose another one.")
        
        # Hash the password and create the user document
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = {
            "username": username,
            "password": hashed_password
        }
        users_collection.insert_one(user)
        return redirect('/login')
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode(), user["password"]):
            # Authentication successful, redirect to the assistant page
            return redirect('/assistant')
        else:
            return render_template('login.html', message="Authentication failed. Please try again.")
    return render_template('login.html')

# Assistant route
@app.route('/assistant')
#def assistant():
    # Implement the code to interact with the virtual assistant
#    return render_template('assistant.html')

# if __name__ == '__main__':
#    app.run(debug=True)

# @app.route('/assistant', methods=['GET', 'POST'])
def assistant():
    # Implement the code to interact with the virtual assistant
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Call a function to process the user input and generate a response from the assistant
        assistant_output = process_user_input(user_input)
        # Render the template with the user input and output
        return render_template('assistant.html', user_input=user_input, assistant_output=assistant_output)
    return render_template('assistant.html')
