import datetime
from flaskblog import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default='default.png')
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expired_seconds=1800):
        s = Serializer(secret_key=app.secret_key, expires_in=expired_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def verify_reset_token(self, token):
        s = Serializer(app.secret_key)
        try:
            user_id = s.loads(token).get('user_id', None)
        except:
            return None

        user = User.query.get(user_id)
        print(user)
        print(self)
        return user


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"