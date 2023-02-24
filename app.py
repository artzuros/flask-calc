from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db = SQLAlchemy(app)

class calculate_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operand1 = db.Column(db.Integer, nullable=False)
    operand2 = db.Column(db.Integer, nullable=False)
    operator = db.Column(db.String(1), nullable=False)
    result = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def calc(self):
        self.operand1 = int(self.operand1)
        self.operand2 = int(self.operand2)
        self.operator = str(self.operator)
        if self.operator == '+':
            self.result =  self.operand1 + self.operand2
        elif self.operator == '-':
            self.result =  self.operand1 - self.operand2
        elif self.operator == '*':
            self.result =  self.operand1 * self.operand2
        elif self.operator == '/':
            if self.operand2 == 0:
                self.result = 'N/A'
            else:self.result =  self.operand1 / self.operand2

        elif self.operator == '%':
            self.result =  self.operand1 % self.operand2
        else:
            self.result =  'Invalid Operator'
        self.result = str(self.result)
        return self.result

    def __repr__(self):
        return f"{self.id} - {self.operand1} {self.operator} {self.operand2} = {self.result} "

@app.route('/', methods=['GET', 'POST', 'UDPATE', 'DELETE'])
def hello_world():
    if request.method == 'POST':
        operand1 = request.form['operand1']
        operand2 = request.form['operand2']
        operator = request.form['operator']
        calculate = calculate_db(operand1=operand1, operand2=operand2, operator=operator)
        calculate.calc()
        db.session.add(calculate)
        db.session.commit()
    allCalc = calculate_db.query.all()
    return render_template('index.html', allCalc=allCalc)

@app.route('/show')
def products():
    allCalc = calculate_db.query.all()
    print(allCalc)
    return 'LEHDI LELOOOOOOO'

@app.route('/update/<int:id>', methods=['GET', 'POST', 'UDPATE', 'DELETE'])
def update(id):
    if request.method == 'POST':
        operand1 = request.form['operand1']
        operand2 = request.form['operand2']
        operator = request.form['operator']
        calculate = calculate_db.query.filter_by(id = id).first()
        calculate.operand1 = operand1
        calculate.operand2 = operand2
        calculate.operator = operator
        calculate.calc()
        db.session.add(calculate)
        db.session.commit()
        return redirect('/')
    calc = calculate_db.query.filter_by(id = id).first()
    return render_template('update.html', calc=calc)
    

@app.route('/delete/<int:id>')
def delete(id):
    calc = calculate_db.query.filter_by(id=id).first()
    db.session.delete(calc)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug =True, port = 8000)








# cd Flask
# env/scrpits/activate/ps1
# Add with app.app_context(): above db = SQLAlchemy(app) like this:

# with app.app_context():
#     db = SQLAlchemy(app)

# and when using the commands do this:

# python
# >>> from app import app, db
# >>> app.app_context().push()
# >>> db.create_all()
# >>> exit()
#python app