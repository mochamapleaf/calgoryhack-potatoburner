from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime
from sms import send_msg

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///upnext.db'
db = SQLAlchemy(app)

# db model
class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow) 
    def __repr__(self):
        return '<Client %r' % self.id

# home page decorator
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# client form page decorator
@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        form_name = request.form.get('name')
        form_email = request.form.get('email')
        form_phone = request.form.get('phone')
        new_client = Clients(name=form_name, email=form_email, phone=form_phone)

        send_msg(form_phone, 'Thank you for signing up, you will be notified when it is time for your appoitnment')
       
        try:
            db.session.add(new_client)
            db.session.commit()
            return render_template('client.html', success='&#9989;')
        except:
            'Error Occured'
    else:
        return render_template('client.html')

# admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        client_name = request.form.get('clientname')
        client_email = request.form.get('clientemail')
        phone = request.form.get('clientphone') 

        send_msg(phone, 'Your appointment starts now.')

        try:
            obj = Clients.query.filter_by(email=client_email).one()
            db.session.delete(obj)
            db.session.commit()

            clients = Clients.query.order_by(desc(Clients.date))

            return render_template('admin.html', clients=clients)
        except:
            'error'
    else:
        clients = Clients.query.order_by(desc(Clients.date))
        return render_template('admin.html', clients=clients)
    

# error 404 handler
@app.errorhandler(404)
def handle_404(e):
    error = '404, try again'
    return render_template('index.html', error=error)

# error 500 handler
@app.errorhandler(500)
def handle_500(e):
    error = '500, try again'
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run()
