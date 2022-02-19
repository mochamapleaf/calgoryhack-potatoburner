from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime

from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
db = SQLAlchemy(app)

# db model
class Clients(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email =  db.Column(db.String(200), nullable = False)
    phone = db.Column(db.Integer(), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow) 
    def __repr__(self):
        return '<Client %r' % self.id

# client route decorator
@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/client', methods = ['GET', 'POST'])
def client():
    if request.method == 'POST':
        form_email = request.form.get('email')
        form_phone = request.form.get('phone')
        new_client = Clients(email=form_email, phone=form_phone)
        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect('/client')
        except:
            'Error Occured'
    else:
        return render_template('client.html')


@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    clients = Clients.query.order_by(desc(Clients.date))
    return render_template('admin.html', clients = clients)

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