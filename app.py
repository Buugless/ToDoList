from flask import Flask,render_template, url_for, request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()


@app.route("/", methods = ['POST', 'GET']) 

def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was and issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route("/update/<int:id>", methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating your task'

    else:
        return render_template('update.html' , task=task)

@app.route("/completed/<int:id>",methods = ['POST'])
def completed(id):
    task = Todo.query.get(id)
    if task:
        task.completed = not task.completed
        if 'completed' in request.form:
            task.completed = True
        else:
            task.completed = False
        db.session.commit()
    return redirect('/')
@app.route('/login', methods = ['POST','GET'])
def login():
    return render_template ('login.html')

@app.route('/signup', methods = ['POST','GET'])
def signup():
    return render_template ('signup.html')
if __name__ =="__main__":
    app.run(debug=True)