from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request #http request access
from datetime import datetime

test = Flask(__name__)
test.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
test.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(test)

class Todo(db.Model):#
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:#
        return f"{self.sno} - {self.title}"#

@test.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # print(request.form['title'])
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)  # Create a new Todo object
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all()
    return render_template('Netfilx.htm', allTodo=allTodo)
    # return 'Hello, World!'

@test.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@test.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@test.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Create database tables
with test.app_context():
    db.create_all()
    print("Database tables created successfully!")
