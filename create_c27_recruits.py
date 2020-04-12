import psycopg2

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

connection = psycopg2.connect(database='prod', user='postgres', password='pass', host='localhost', port='5432')
cursor = connection.cursor()

query = """INSERT INTO recruits(first_name, surname, chatname, github_name, id_number, personal_email, cohort) 
VALUES 
('Gerrad','Simpson','GerryS','GerryGitHub','79','gerry@yes.com','C27 Data Eng'),
('Cindy','Mason','CEEM','CeeMGitHub','34576','cee@gmail.com','C27 Data Eng'),
('Jeff','Veron','Jeezy','JeezyGitHub','08','jeez@owe.com','C27 Data Eng'),
('Roy','Keane','RoyK','Royke','34789','royK@gmail.com','C27 Data Eng'),
('Luke','Roflok','Lukelok','LukeGitHub','237','luke@trans.com','C27 Data Eng');"""


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