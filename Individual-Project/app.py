from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyDXbJEdSAfgp10O_7OCBMH6LYZfn-Y3c9E",
  'authDomain': "cheese-5eb16.firebaseapp.com",
  'projectId': "cheese-5eb16",
  'storageBucket': "cheese-5eb16.appspot.com",
  'messagingSenderId': "76543238429",
  'appId': "1:76543238429:web:b2b3996d3fc5463aa3c1f4",
  'measurementId': "G-1KVEHB84NE",
  "databaseURL": "https://cheese-5eb16-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("index.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
			return render_template("signin.html")
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		fav_cheese = request.form['fav_cheese']
		username = request.form['username']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			UID = login_session['user']['localId']
			user = {'email': email, 'password': password, 'fav_cheese': fav_cheese, 'username': username}
			db.child("Users").child(UID).set(user)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
			return render_template("signup.html")
	return render_template("signup.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template("home.html")

@app.route('/chedder', methods=['GET', 'POST'])
def chedder():
	if request.method == 'POST':
		UID = login_session['user']['localId']
		try:
			post = {"title": request.form['title'], "text": request.form['text'], 'uid': UID}
			db.child("posts").push(post)
		except:
			print("Couldn't post")
	posts = db.child("posts").get().val()
	return render_template("chedder.html", posts = posts)



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)