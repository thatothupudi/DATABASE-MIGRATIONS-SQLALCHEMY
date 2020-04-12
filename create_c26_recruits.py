import psycopg2

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

connection = psycopg2.connect(database='prod', user='postgres', password='pass', host='localhost', port='5432')
cursor = connection.cursor()

query = """INSERT INTO recruits(first_name, surname, chatname, github_name, id_number, personal_email, cohort) 
VALUES 
('Tshepo','Tshabalala','Tsquared','TshepoGitHub','3425623','tshepo@yes.com','C26 Data Eng'),
('Kagiso','Mohale','Kagi123','KagiGitHub','56868','Kg@gmail.com','C26 Data Eng'),
('Peter','Stevens','Pet26','PetsGitHub','5685','peter@owe.com','C26 Data Eng'),
('Marcus','Will','Marc765','MarcusWiilPower','7890','Marcus@gmail.com','C26 Data Eng'),
('Terrence','Phillips','Terry','TerryGitHub','8765','terryO@trans.com','C26 Data Eng');"""


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@127.0.0.1/prod'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    recruit = db.relationship('Recruit', backref='owner', lazy='dynamic')

class Recruits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    first_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    chatname = db.Column(db.VARCHAR(15))
    github_name = db.Column(db.VARCHAR(20))
    id_number = db.Column(db.NUMERIC(15), db.ForeignKey('user.id'))
    personal_email = db.Column(db.VARCHAR(20), unique=True)
    cohort = db.Column(db.VARCHAR(100))
    


cursor.execute(query)
connection.commit()
if __name__=='__main__':
    manager.run()