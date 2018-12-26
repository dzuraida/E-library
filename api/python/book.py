from flask import Flask,request,json,session, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import marshal,fields
import datetime
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:please@localhost:17711/elibrary'
CORS(app, support_credentials=True)
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
jwtSecretKey = "comicbook"

class Books(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    book_no = db.Column(db.Integer())
    book_name =  db.Column(db.String())
    book_year = db.Column(db.Integer())
    book_writer = db.Column(db.String())
    book_genre = db.Column(db.String())
    book_sysnopsis = db.Column(db.String())
    book_picture = db.Column(db.String())

class Position(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String())

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    position = db.Column(db.Integer,db.ForeignKey('position.id'))
    name =  db.Column(db.String())
    age = db.Column(db.Integer())
    address = db.Column(db.String())
    phonenumber = db.Column(db.Integer())

class Borrow(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    borrow_name =  db.Column(db.String,db.ForeignKey('user.name'))
    borrow_number = db.Column(db.Integer,db.ForeignKey('books.book_no'))
    borrow_title = db.Column(db.String,db.ForeignKey('books.book_name'))
    borrow_time = db.Column(db.String())
    return_time = db.Column(db.String())

@app.route('/')
def get():
    return "test",20
@app.route('/login',methods=['POST'])
def login():
    request_data = request.get_json()
    req_email = request_data.get('username')
    req_password = request_data.get('password')
    dataUser = User.query.filter_by(email=req_email, password=req_password).first()
    if dataUser :
        payload = {
            "id": dataUser.id,
            "secretcode": "comics"
        }
        encoded = jwt.encode(payload, jwtSecretKey, algorithm='HS256').decode('utf-8')
        json_format = {
        "token" : encoded,
        "position" : dataUser.position
        }
        user_json = json.dumps(json_format)

        return user_json, 200
    else:
        return 'Failed', 404

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"), host=os.getenv("HOST"), port=os.getenv("PORT"))