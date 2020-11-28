# from models import Users, Admin, Agents, Loan, Emi
from models import *
import hashlib
from flask import Flask, session, render_template, jsonify, request, redirect, make_response
from functools import wraps
import jwt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableMultiDict
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ljuqjpdsgznhki:3bb3de805e3ea4c2d99c05dcb71a2ac1f21829e2478e59f294b5aff0e07e131b@ec2-75-101-232-85.compute-1.amazonaws.com:5432/d7nj1f6lp4201v"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['salt'] = "5gz"

db = SQLAlchemy(app)
#


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        token = request.args.get('token')
        body = request.get_json(silent=True)
        if not token:
            return jsonify({'message': 'Token is missing!', 'token': request}), 403
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithm='HS256')

            http_args = request.args.to_dict()

            try:
                user = Users.query.filter_by(username=data['username']).first()

                if('id' in body):
                    if(user.id == body['id']):
                        http_args['selfProfile'] = True
                if (user.user_type == 'Admin'):

                    http_args['isAdmin'] = True
                elif (user.user_type == 'Agent'):

                    http_args['isAgent'] = True
                else:
                    http_args['isUser'] = True
                request.args = ImmutableMultiDict(http_args)
            except:
                return jsonify({'message': 'No Data Found'}), 403
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/')
def index():
    db.create_all()
    db.session.commit()
    return '/users'


@app.route('/users', methods=['GET', 'POST', 'PUT', "DELETE"])
@token_required
def users_get():
    body = request.get_json(silent=True)
    users = Users.query.all()
    req = request.args.to_dict()

    if('isAdmin' in req or 'isAgent' in req):
        if(request.method == "POST"):
            hashed = hashedPassword(body['password'])
            try:
                user = Users(username=body['username'],
                             email=body['email'], password=hashed)
            except:
                return jsonify({'message': "Error Wwhile creating"})
            db.session.add(user)
            db.session.commit()
            return jsonify({'user': "Created"})

    if('selfProfile' in req or 'Admin' in req):
        if(request.method == "PUT"):
            hashed = hashedPassword(body['password'])

            if('id' not in body):
                return jsonify({'message': 'Enter USer ID '})

            try:
                user = Users.update().where(users.c.id ==
                                            body['id'], users.c.password == hashed).values(username="some name")
            except:
                return jsonify({'message': "Error Wwhile Updating"})
            db.session.commit()
            return jsonify({'user': "Updated"})

    if('Agent' in req or 'Admin' in req):
        if(request.method == "DELETE"):
            if('id' not in body):
                return jsonify({'message': 'Enter USer ID '})
            try:
                User.query.filter_by(id=body['id']).delete()
            except:
                return jsonify({'message': "Error Wwhile Deleting"})
            db.session.commit()
            return jsonify({'user': "Deleted"})

    if('isAdmin' in req):
        array = []
        for user in users:

            obj = {}
            obj['id'] = user.id
            obj['username'] = user.username
            obj['email'] = user.email
            obj['userType'] = user.user_type

            array.append(obj)

        return jsonify({'USERS': array})
    if('isUser' in req or 'isAgent' in req):
        array = []
        for user in users:

            obj = {}
            obj['id'] = user.id
            obj['username'] = user.username
            obj['email'] = user.email
            array.append(obj)

        return jsonify({'USERS': array})


@app.route('/login', methods=["POST"])
def login():
    auth = request.authorization

    body = request.get_json(silent=True)

    try:
        user = Users.query.filter_by(username=body['username']).first()
    except:
        return jsonify({'message': 'No Data Found'})
    password = hashedPassword(body['password'])
    if(password == user['password']):
        token = jwt.encode({'username': user.username},
                           app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token.decode()})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/signup', methods=["POST"])
def signup():

    body = request.get_json(silent=True)

    user = Users.query.filter_by(username=body['username']).first()
    if(user):
        return jsonify({'Message': 'Give a Unique UserName'})

    password = hashedPassword(body['password'])

    try:
        user = Users(username=body['username'],
                     email=body['email'], password=password)
    except:
        return jsonify({'message': 'Internal Server Error'}), 500
    db.session.add(user)
    db.session.commit()
    token = jwt.encode({'username': user.username},
                       app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token.decode()})

    # return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


@app.route('/loan', methods=["POST", "GET", "PUT"])
def loan():
    #
    return 'HELLO'


def hashedPassword(password):
    db_password = password + app.config['salt']
    h = hashlib.sha256(db_password.encode())
    return h.hexdigest()


try:
    from models.UserModel import Users
    # from models.AdminModel import Admin
    # from models.AgentModel import Agents
    # from models.EmiModel import Emi
    # from models.LoanModel import Loan
    print('Models imported')
except ImportError as e:
    print(e)


@app.before_first_request
def create_tables():
    db.create_all()
    db.session.commit()

# with app.app_context():
#     db.create_all()
# db.session.commit()
# admin = Users('admin', 'admin@example.com', hashedPassword('123'))
# guest = Users('guest', 'guest@example.com', hashedPassword('123'))
# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()
# users = Users.query.all()
# print(users)


# db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=5001, threaded=True, host=('0.0.0.0'))
