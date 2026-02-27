from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import smtplib
import numpy as np

# SAFER EMAIL IMPORT (no MimeText—uses dict string instead)
app = Flask(__name__)

# ### CHANGE 1: You can change this secret key to any random string if you want
app.config['SECRET_KEY'] = 'aditya_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ### CHANGE 2 & 3: PUT YOUR ACTUAL EMAIL DETAILS HERE ###
EMAIL_ADDRESS = 'adtiwari936@gmail.com'   # <-- CHANGE: Put your real Gmail here
EMAIL_PASSWORD = 'Ana@adi03'  # <-- CHANGE: Put your 16-digit Google App Password here

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text)
    tech = db.Column(db.String(50))
    github = db.Column(db.String(100))
    image = db.Column(db.String(100), default='default.jpg')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    featured = Project.query.limit(2).all()
    return render_template('index.html', featured=featured)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=Project.query.all())

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        temp = float(request.form.get('temp', 25))
        hum = float(request.form.get('humidity', 70))
        
        # ### CHANGE 4: This is fake math just for testing. 
        # When you are ready, replace this line with your actual rainfall ML model prediction!
        pred = (temp + hum) / 2 * 1.5  
        
        return render_template('predict.html', result=round(pred, 2))
    return render_template('predict.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        sender = request.form['email']
        msg = request.form['message']
        send_simple_email(name, sender, msg)
        flash('Message sent from {}!'.format(name))
        return redirect(url_for('home'))
    return render_template('contact.html')

def send_simple_email(name, sender_email, message):
    """Simple string email—no MimeText needed"""
    email_body = f"""New Portfolio Contact:
    
Name: {name}
Email: {sender_email}
Message: {message}"""
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(sender_email, EMAIL_ADDRESS, email_body)
        server.quit()
    except Exception as e:
        print(f"Email error: {e}")  # Debug

if __name__ == '__main__':
    app.run(debug=True)


