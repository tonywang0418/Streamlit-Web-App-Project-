import jwt
import datetime
from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
SECRET_KEY = '123'

def database_connection():
    mydb = pymysql.connect(host='10.0.0.117', user='tony', password='password',database='user_info')
    mycursor = mydb.cursor()
    return mycursor, mydb

def create_token(username):
    payload = {'username': username, 'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
def verify_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token['username']
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'

def verify_user_in_db(username, password):
    mycursor, mydb = database_connection()
    try:
        query = "SELECT * FROM user_info WHERE username = %s AND password = %s"
        mycursor.execute(query, (username, password))
        user = mycursor.fetchone()
        return user is not None
    except pymysql.Error as error:
        print(f"Database error: {error}")
        return False
    finally:
        mydb.close()

def add_user_to_db(username, password):
    mycursor, mydb = database_connection()
    try:
        query = "INSERT INTO `user_info` (`username`, `password`) VALUES (%s,%s)"
        mycursor.execute(query, (username, password))
        mydb.commit()
        return True
    except pymysql.IntegrityError:
        return False
    finally:
        mydb.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if verify_user_in_db(username, password):
        token = create_token(username)
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if add_user_to_db(username, password):
        return jsonify({'message': 'User registered successfully!'}), 201
    else:
        return jsonify({'message': 'Username already exists'}), 409


@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if token:
        token = token.split(" ")[1]
        username = verify_token(token)
        if isinstance(username, str) and username not in ['Token has expired', 'Invalid token']:
            return jsonify({'message': f'Welcome {username}, you have accessed a protected route!'})
        else:
            return jsonify({'message': username}), 401
    else:
        return jsonify({'message': 'Token is missing'}), 401

if __name__ == '__main__':
    app.run(port=5000)







