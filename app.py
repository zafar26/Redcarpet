from models import *
import hashlib
from flask import Flask, session, render_template, jsonify, request, redirect, make_response
from functools import wraps
import jwt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://kJf8oGRLqL:ZR2scz5rxu@remotemysql.com:3306/kJf8oGRLqL'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisthesecretkey'

db = SQLAlchemy(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        token = request.args.get('token')
        http_args = request.args.to_dict()

        if not token:
            return jsonify({"status": "false", 'message': 'Token is missing!'}), 401

        body = request.get_json(silent=True)
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithm='HS256')

            if not data:
                return jsonify({"status": "false", 'message': 'No Data from Token'}), 401

            if(data['userType'] == 'Admin'):
                try:
                    admin = Admin.query.filter_by(
                        username=data['username']).first()

                    if(admin.id):
                        http_args['isAdmin'] = True
                        http_args['id'] = admin.id

                except:
                    return jsonify({"status": "false", 'message': 'No Admin Found'}), 401

            if(data['userType'] == 'Agent'):
                try:
                    agent = Agents.query.filter_by(
                        username=data['username']).first()
                    if(agent.id):
                        http_args['isAgent'] = True
                        http_args['id'] = agent.id

                except:
                    return jsonify({"status": "false", 'message': 'No Agent Found'}), 401

            if(data['userType'] == 'User'):
                try:
                    usr = Users.query.filter_by(
                        username=data['username']).first()

                    if usr.id:
                        http_args['isUser'] = True
                        http_args['id'] = usr.id

                except:
                    return jsonify({"status": "false", 'message': 'No User Found'}), 401

        except:
            return jsonify({"status": "false", 'message': 'Token is invalid!'}), 401

        request.args = ImmutableMultiDict(http_args)
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def index():
    return redirect('/users')


@app.route('/users', methods=['GET', 'POST', 'PUT', "DELETE"])
@token_required
def users_get():
    body = request.get_json(silent=True)
    req = request.args.to_dict()

    if(request.method == "POST"):
        if('isAdmin' in req or 'isAgent' in req):
            hashed = hashedPassword(body['password'])
            if not body['username'] or body['email']:
                return jsonify({"status": "false", 'message': "enter username and email"}), 206
            try:
                user = Users(username=body['username'],
                             email=body['email'], password=hashed)
            except:
                return jsonify({"status": "false", 'message': "Error Wwhile creating"}), 501
            db.session.add(user)
            db.session.commit()
            return jsonify({'status': 'true', 'message': "Created"}), 201
        return jsonify({'status': "false", 'message': "Unauthorized"}), 401

    if(request.method == "PUT"):
        if('selfProfile' in req or 'Admin' in req):
            hashed = hashedPassword(body['password'])

            if('id' not in body):
                return jsonify({"status": "false", 'message': 'Enter USer ID '}), 206
            try:
                user = Users.update().where(
                    user.c.id == body['id']).values(body)
            except:
                return jsonify({"status": "false", 'message': "Error Wwhile Updating"}), 501
            db.session.commit()
            return jsonify({'status': 'true', 'message': "Updated"}), 200
        return jsonify({'status': 'false', 'message': "Unauthorized"}), 401

    if(request.method == "DELETE"):
        if('isAgent' in req or 'isAdmin' in req):
            if('id' not in body):
                return jsonify({"status": "false", 'message': 'Enter USer ID '}), 206
            try:
                Users.query.filter_by(id=body['id']).delete()
            except:
                return jsonify({"status": "false", 'message': "Error Wwhile Deleting"}), 501
            db.session.commit()
            return jsonify({'status': 'true', 'message': "Deleted"}), 200
        return jsonify({'status': 'false', 'message': "UnAuthorized "}), 401
    try:
        users = Users.query.all()
    except:
        return jsonify({"status": "false", 'message': "No Data Found"}), 404

    array = []
    for user in users:

        obj = {}
        obj['id'] = user.id
        obj['username'] = user.username
        obj['email'] = user.email
        array.append(obj)

    return jsonify({'status': 'true', 'users': array})


@app.route('/login', methods=["POST"])
def login():
    auth = request.authorization
    body = request.get_json(silent=True)

    try:
        user = Users.query.filter_by(username=body['username']).first()
        password = hashedPassword(body['password'])
        if(password == user.password):
            token = jwt.encode({'username': user.username,  'userType': 'User'},
                               app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'status': 'true', 'token': token.decode()}), 200

    except:
        return jsonify({"status": "false", 'message': 'No Data Found'})

    return jsonify({"status": "false", 'message': "Could not verify!"}), 401


@app.route('/admin/login', methods=["POST"])
def admin_login():
    auth = request.authorization
    body = request.get_json(silent=True)

    try:
        admin = Admin.query.filter_by(username=body['username']).first()
        password = hashedPassword(body['password'])

        if(password == admin.password):
            token = jwt.encode({'username': admin.username, 'userType': 'Admin'},
                               app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'status': 'true', 'token': token.decode()}), 200

    except:
        return jsonify({"status": "false", 'message': 'No Data Found'})

    return jsonify({"status": "false", 'message': "Could not verify!"}), 401


@app.route('/agent/login', methods=["POST"])
def agent_login():
    auth = request.authorization
    body = request.get_json(silent=True)

    try:
        agent = Agents.query.filter_by(username=body['username']).first()
        password = hashedPassword(body['password'])

        if(password == agent.password):
            token = jwt.encode({'username': agent.username, 'userType': 'Agent'},
                               app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'status': 'true', 'token': token.decode()}), 200

    except:
        return jsonify({"status": "false", 'message': 'No Data Found'})

    return jsonify({"status": "false", 'message': "Could not verify!"}), 401


@app.route('/signup', methods=["POST"])
def signup():

    body = request.get_json(silent=True)

    user = Users.query.filter_by(username=body['username']).first()
    if(user):
        return jsonify({"status": "false", 'Message': 'Give a Unique UserName'}), 409

    password = hashedPassword(body['password'])

    try:
        user = Users(username=body['username'],
                     email=body['email'], password=password)
    except:
        return jsonify({"status": "false", 'message': 'Internal Server Error'}), 500
    db.session.add(user)
    db.session.commit()
    token = jwt.encode({'username': user.username, 'userType': 'User'},
                       app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'status': 'true', 'token': token.decode()}), 201


@app.route('/admin/signup', methods=["POST"])
def admin_signup():

    body = request.get_json(silent=True)

    admin = Admin.query.filter_by(username=body['username']).first()
    if(admin):
        return jsonify({"status": "false", 'Message': 'Give a Unique username'}), 409

    password = hashedPassword(body['password'])

    try:
        admin = Admin(username=body['username'],
                      email=body['email'], password=password)
    except:
        return jsonify({"status": "false", 'message': 'Internal Server Error'}), 500
    db.session.add(admin)
    db.session.commit()
    token = jwt.encode({'username': admin.username, 'userType': 'Admin'},
                       app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'status': 'true', 'token': token.decode()}), 201


@app.route('/agent/signup', methods=["POST"])
def agent_signup():

    body = request.get_json(silent=True)

    agent = Agents.query.filter_by(username=body['username']).first()
    if(agent):
        return jsonify({"status": "false", 'Message': 'Give a Unique username'}), 409

    password = hashedPassword(body['password'])

    try:
        agent = Agents(username=body['username'],
                       email=body['email'], password=password)
    except:
        return jsonify({"status": "false", 'message': 'Internal Server Error'}), 500
    db.session.add(agent)
    db.session.commit()
    token = jwt.encode({'username': agent.username, 'userType': 'Agent'},
                       app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'status': 'true', 'token': token.decode()}), 201


@app.route('/loan', methods=["POST", "GET", "PUT"])
@token_required
def loan():
    req = request.args.to_dict()

    if 'isAdmin' in req:
        try:
            loans = Loan.query.all()
        except:
            return jsonify({"status": "false", 'message': 'No Data Found'}), 404
    if 'isAgent' in req:
        try:
            print(req['id'], 'req')
            loans = Loan.query.filter_by(agent_id=req['id']).all()
        except:
            return jsonify({"status": "false", 'message': 'No Data Found'}), 404
    if 'isUser' in req:
        try:
            loans = Loan.query.filter_by(user_id=req['id']).all()
        except:
            return jsonify({"status": "false", 'message': 'No Data Found'}), 404

    array = []
    for each in loans:
        obj = {}
        obj['id'] = each.id
        obj['name'] = each.name
        obj['aadhar'] = each.aadhar
        obj['purpose'] = each.purpose
        obj['status'] = each.status
        obj['isUserApproved'] = each.isUserApproved
        obj['isAdminApproved'] = each.isAdminApproved
        obj['ammount'] = each.ammount
        obj['monthlyDeductAmmount'] = each.monthlyDeductAmmount
        obj['createdAt'] = each.createdAt
        obj['updatedAt'] = each.updatedAt

        array.append(obj)

    return jsonify({'status': 'true', 'loans': array}), 200


def hashedPassword(password):
    # db_password = password + app.config['salt']
    db_password = password

    h = hashlib.sha256(db_password.encode())
    return h.hexdigest()


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=5001, threaded=True, host=('0.0.0.0'))
