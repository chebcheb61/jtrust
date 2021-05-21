from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key= "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Clists1234@database-1.cukrhbgepqax.ap-southeast-1.rds.amazonaws.com/jtrust'
app.config['SQLALCHEMY_TRACK_Modification'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    client_sagment = db.Column(db.String(100))
    client_type = db.Column(db.String(100))
    rm_id = db.Column(db.Integer)
    cif = db.Column(db.Integer)
    acc_no = db.Column(db.Integer, primary_key = True)
    client_name = db.Column(db.String(100))

    def __init__(self, client_sagment, client_type, rm_id, cif, acc_no, client_name):
        self.client_sagment = client_sagment
        self.client_type = client_type
        self.rm_id = rm_id
        self.cif = cif
        self.acc_no = acc_no
        self.client_name = client_name
@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", clients = all_data) 

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        client_sagment = request.form['client_sagment']
        client_type = request.form['client_type']
        rm_id = request.form['rm_id']
        cif = request.form['cif']
        acc_no = request.form['acc_no']
        client_name = request.form['client_name']


        my_data = Data(client_sagment, client_type, rm_id, cif, acc_no, client_name)
        db.session.add(my_data)
        db.session.commit()

        flash("Client Information Inserted Sucessfully")
 
        return redirect(url_for('Index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == "POST":
        my_data = Data.query.get(request.form.get('acc_no'))

        my_data.client_type = request.form['client_type']
        my_data.client_segment = request.form['client_segment']
        my_data.rm_id = request.form['rm_id']
        my_data.cif = request.form['cif']
        my_data.client_name = request.form['client_name']

        db.session.commit()
        flash("Client Updated Sucessfully")

        return redirect(url_for('Index'))

@app.route('/delete/<acc_no>', methods = ['GET','POST'])
def delete(acc_no):
    my_data = Data.query.get(acc_no)
    db.session.delete(my_data)
    db.session.commit()
    flash("Client Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)