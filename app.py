from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import hashlib
import jwt
from config import CLIENT_ID, REDIRECT_URI
import webbrowser

client = MongoClient('mongodb+srv://test:sparta@cluster0.zz6rnhk.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/join')
def tojoin():
    return render_template('join.html')


@app.route('/movie')
def move_to_movie():
    return render_template('index.html')


@app.route('/find')
def move_to_find_id():
    return render_template('find_ID.html')


@app.route('/kakao')
def kakao_url_api():
    kakao_oauth_url = "https://kauth.kakao.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code" \
                      % (CLIENT_ID, REDIRECT_URI)
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

    return webbrowser.get(chrome_path).open(kakao_oauth_url)


# Join ------------------------------


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

    hash_pw = hashlib.sha256(pw_receive.encode('utf-8'))

    doc = {
        'user_id': id_receive,
        'user_pw': hash_pw.hexdigest(),
        'user_nick': nick_receive
    }

    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# Login -----


@app.route("/movies", methods=["POST"])
def login_post():
    receive_id = request.form['id_give']
    receive_pw = request.form['pw_give']
    user = db.users.find_one({'user_id': receive_id}, {'_id': False})
    if user is None:
        return 'None'  # 실패 : 존재하지 않는 아이디.
    else:
        hash_pw = hashlib.sha256(receive_pw.encode('utf-8'))
        if hash_pw.hexdigest() == user['user_pw']:
            token = jwt.encode({'user_id': receive_id}, 'toy project10', algorithm='HS256')
            print(token)
            return jsonify({'result': 'login success', 'token': token})
        else:
            return 'password incorrect'  # 실패 : 패스워드 다름.


# find_ID -----


@app.route("/find", methods=["POST"])
def find_id():
    receive_nick = request.form['nick_give']
    user = db.users.find_one({'user_nick': receive_nick}, {'_id': False})
    if user is None:
        return 'failed'  # 실패 : 존재하지 않는 닉네임.
    else:
        return user['user_id']

#post_movie -----

@app.route("/movie/post", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')


    title = soup.select_one('meta[property = "og:title"]')['content']
    description = soup.select_one('meta[property = "og:description"]')['content']
    image = soup.select_one('meta[property = "og:image"]')['content']

    movies_list = list(db.movies.find({}, {'_id': False}))
    count = len(movies_list) + 1

    doc = {
        'title' :title,
        'image' : image,
        'description' : description,
        'star' : star_receive,
        'comment' : comment_receive,
         'num' : count
    }
    db.movies.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})


@app.route("/movie/post", methods=["GET"])
def movie_get():
    movies_list = list(db.movies.find({},{'_id':False}))
    return jsonify({'movies':movies_list})

@app.route("/movie/delete", methods=["POST"])
def movie_delete():
    num_receive = request.form['num_give']
    db.movies.delete_one({'num':int(num_receive)})
    return jsonify({'msg':'삭제 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
