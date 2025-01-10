from flask import Flask, render_template, request, redirect, url_for, session
from loginscript import login
from registration import emailCheck, register
from activate import checkToken, activateAccount

# Set up Flask server
app = Flask(__name__)
app.secret_key = b'\xd8\x95\x814Ij\x014S\xc6r\xbaC\x1e>N\xa0\x16d:\x8dp_\xf1'

# Serve the index page
@app.route('/')
def index():
        return render_template("index.html")

@app.route('/next-page')
def next_page():
    return render_template("next-page.html")
    

# Serve the login page
@app.route('/login')
def login_page():
    if 'login' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template("login.html")
    
@app.route('/dashboard')
def dashboard():
    if 'login' in session:
        return render_template("dashboard.html", email=session['email'])
    else:
        return redirect(url_for('login'))
    
# Result Route
@app.route('/result', methods=['GET'])
def result():
    news = request.args.get('news')
    return render_template('result.html', news=news)

@app.route('/team')
def team():
    return render_template("team.html")

# Handle login form submission and verification
@app.route('/verify-login', methods=["POST"])
def verify_login():
    email = request.form.get("email")
    password = request.form.get("password")

    # Verify the username and hashed password
    myMessage, loggedIn = login(email, password)
    
    print(f"Logged In: {loggedIn}")  # Debugging statement
    
    if loggedIn:
        session['login'] = True  # Set session flag for login
        session['email'] = email  # Set session email for user
        print("Redirecting to dashboard...")  # Debugging statement
        return redirect(url_for('dashboard'))  # Redirect to the dashboard route
    else:
        # If verification fails, reload the login page with an error message
        print("Login failed, reloading login page...")  # Debugging statement
        return render_template("login.html", message=myMessage)
    
# Serve the register page
@app.route('/signup')
def register_page():
    return render_template("signup.html")

# Handle registration form submission and verification
@app.route('/verify-register', methods=["POST"])
def verify_register():
    email = request.form.get("email")
    password = request.form.get("password")
    confPassword = request.form.get("confirm_password")

    # Verify email and register
    text, emailVerification = emailCheck(email)
    if emailVerification:
        if password == confPassword:
            text, verifyRegister = register(email, password)
            if verifyRegister:
                return render_template("activate.html", message="Activate your account, Check your email.")
            else:
                return render_template("signup.html", message=text)
        else:
            return render_template("signup.html", message="Passwords do not match.")
    else:
        return render_template("signup.html", message=text)

# Serve the activation page
@app.route('/activate', methods=["GET"])
def activate():
    token = request.args.get("token")
    # Check Token
    text, verifyToken = checkToken(token)
    if verifyToken:
        text, verifyActivation =    activateAccount(token)
        return render_template("activate.html", message=text)
    else:
        return render_template("activate.html", message=text)
    

@app.route('/prediction2', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        news = request.form['news']  # Get news text from form
        # Example prediction logic (replace with actual ML model logic)
        prediction_result = "Real" if "good" in news.lower() else "Fake"
        accuracy = "95%"
        return render_template('result.html', news=news, prediction=prediction_result, accuracy=accuracy)
    return render_template('prediction2.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)