from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

## In real life we pass this a container configuration resource
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emp.sqlite3'

# it take the name of the db and read it and put it in the memory
# the first address in memory where db is starting 
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique= True)
    job = db.Column(db.String(50) )
    date_created = db.Column(db.DateTime, default= datetime.now() )

 

@app.route('/')
def welcome():
    return '<h1>This is a welcome page</h1>'


@app.route('/Add/<name>/<job>')
def index(name, job):
    employee = Employee(name=name, job=job)
    db.session.add(employee)
    db.session.commit()
## try catch error
    return '<h1>Added new emplyee </h1>'


@app.route('/<name>')
def get_user(name):
    employee = Employee.query.filter_by(name=name).first()

    if employee is not None: 
     return f'<h1>Employee: {employee.name} is a {employee.job} </h1>'

    return f'<h1>No Record has been found!! </h1>'
  
    
@app.route('/list')
@app.route('/all')
def list_all():
    employees = Employee.query.all()
    return render_template('list_all.html', employees=employees )



@app.route('/delete/<id>')
def delete(id):
    employee = Employee.query.filter_by(id=id).first()
    db.session.delete(employee)
    db.session.commit()
    return f'<h1>Employee: {employee.name} ID: {employee.id} record has been deleted </h1>'


if __name__ == '__main__':
    app.run(debug=True)




