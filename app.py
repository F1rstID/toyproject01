from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
from pymongo import MongoClient

client = MongoClient('mongodb+srv://wndhdks4536:wnddhks23z@cluster0.a2clvb7.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/join')
def tojoin():
    return render_template('join.html')


@app.route('/checkid', methods=['POST'])
def check_id():
    id_receive = request.form['id_give']
    user = db.users.find_one({'user_id': id_receive}, {'user_pw': False})

    if user is None:
        return '0'
    else:
        return '1'


@app.route('/checknick', methods=['POST'])
def check_nick():
    nick_receive = request.form['nick_give']
    user = db.users.find_one({'user_nick': nick_receive}, {'user_pw': False})

    if user is None:
        return '0'
    else:
        return '1'


@app.route('/join', methods=['POST'])
def join():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_receive = request.form['nick_give']

    doc = {
        'user_id': id_receive,
        'user_pw': pw_receive,
        'user_nick': nick_receive
    }

    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# Login -----

@app.route('/movie')
def move_to_movie():
    return render_template('index.html')


@app.route("/movies", methods=["POST"])
def bucket_post():
    receive_id = request.form['id_give']
    user_inform = db.users.find_one({'user_id': receive_id}, {'_id': False})
    if (user_inform == None):
        return '0'
    else:
        return jsonify({'user_pw': user_inform['user_pw']})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
