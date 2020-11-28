import os
import json
import datetime
# import psycopg2
import hashlib
from flask import Flask,jsonify
from datetime import datetime
from flask import Flask, session, render_template, jsonify, request, redirect,make_response
from tempfile import mkdtemp
from models import *
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://ljuqjpdsgznhki:3bb3de805e3ea4c2d99c05dcb71a2ac1f21829e2478e59f294b5aff0e07e131b@ec2-75-101-232-85.compute-1.amazonaws.com:5432/d7nj1f6lp4201v'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.secret_key = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['salt'] = "5gz"

db.init_app(app)

# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response


#Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

ma = Marshmallow(app)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
       model = Users

class LoanSchema(ma.SQLAlchemySchema):
    class Meta:
       model = Loan


@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def users_get():
    users = Users.query.all()
        
    # if(request.method == "POST"):
    #     user = Users( username='zafar', email='zafar5@gmail.com', password='password')
    #     db.session.add(user)
    #     db.session.commit()
    #     return jsonify({'user' : "Created"})
        
    
    array =[]
    for user in users:
        obj ={}
        obj['id'] = user.id
        obj['username'] = user.username
        obj['email'] = user.email
        array.append(obj)
    
    return jsonify({'USERS' : array})

@app.route('/login',methods=["POST"])
def login():
    auth = request.authorization
    body = request.get_json(silent=True)
    user = Users.query.filter_by(username=body['username']).first()
    password = hashedPassword(body['password'])
    if(password == user.password):
        # print(auth,'AUTH')
        # print(body['password'])
            
        # print(password,'password')
        token = jwt.encode({'id' : user.id}, app.config['SECRET_KEY'],algorithm='HS256')

        return jsonify({'token' : token.decode()})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/signup',methods=["POST"])
def signup():
    body = request.get_json(silent=True)
    user = Users.query.filter_by(username=body['username']).first()
    if(user):
        return jsonify({'Message':"UserName Already Registered"})

def hashedPassword(password):

    db_password = password+ app.config['salt']
    h = hashlib.sha256(db_password.encode())
    # print(h.hexdigest())
    return h.hexdigest()

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=5001, threaded=True, host=('0.0.0.0'))