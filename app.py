# coding:utf-8

from flask import Flask,jsonify,make_response,abort,request
from flask.ext.sqlalchemy import SQLAlchemy
from marshmallow import Schema

app = Flask(__name__)
app.config['SECRET_KEY'] = 'daferr33354gfdsgrfhgh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usename:passwd@ip_address/acct'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    def __unicode__(self):
        return self.content

# we use marshmallow Schema to serialize our articles
class ArticleSchema(Schema):
    """
    Article dict serializer
    """
    class Meta:
        # which fields should be serialized?
        fields = ('id', 'title', 'content')

article_schema = ArticleSchema()
# many -> allow for object list dump
articles_schema = ArticleSchema(many=True)

@app.route("/articles/", methods=["GET"])
@app.route("/articles/<article_id>", methods=["GET"])
def articles(article_id=None):
    if article_id:
        article = Article.query.get(article_id)
        if article is None:
            return jsonify({"msgs": ["the article you're looking for could not be found"]}), 404

        result = article_schema.dump(article)
        return jsonify({'article': result})
    else:
        # never return the whole set! As it would be very slow
        queryset = Article.query.limit(10)
        result = articles_schema.dump(queryset)
        # jsonify serializes our dict into a proper flask response
        return jsonify({"articles": result.data})

db.create_all()
# let's populate our database with some data; empty examples are not that cool
if Article.query.count() == 0:
    article_a = Article(title='some title', content='somecontent')
    article_b = Article(title='other title', content='othercontent')
    db.session.add(article_a)
    db.session.add(article_b)
    db.session.commit()

users = [
    {
        'id': 1,
        'username': u'cjgiridhar',
        'email': u'abc@xyz.com',
        'active': True
    },
    {
        'id': 2,
        'username': u'python',
        'email': u'py@py.org',
        'active': False
    }
]

@app.route('/')
def index():
    return "Hello, Python!"

@app.route('/v1/users/', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/v1/users/<int:id>/', methods=['GET'])
def get_user(id):
    for user in users:
        if user.get("id") == id:
            return jsonify({'users': user})
    abort(404)

@app.route('/v1/users/', methods=['POST'])
def create_user():
    if not request.json or not 'email' in request.json:
        abort(404)
    user_id = users[-1].get("id") + 1
    username = request.json.get('username')
    email = request.json.get('email')
    status = False
    user = {"id": user_id, "email": email,"username": username, "active": status}
    users.append(user)
    return jsonify({'user': user}), 201

@app.route('/v1/users/<int:id>/', methods=['PUT'])
def update_user(id):
    user = [user for user in users if user['id'] == id]
    user[0]['username'] = request.json.get('username', user[0]['username'])
    user[0]['email'] = request.json.get('email', user[0]['email'])
    user[0]['active'] = request.json.get('active', user[0]['active'])
    return jsonify({'users': user[0]})

@app.route('/v1/users/<int:id>/', methods=['DELETE'])
def delete_user(id):
    user = [user for user in users if user['id'] == id]
    users.remove(user[0])
    return jsonify({}), 204

if __name__ == '__main__':
    # we define the debug environment only if running through command line
    app.config['SQLALCHEMY_ECHO'] = True
    app.debug = True
    app.run()
