from flask import Blueprint, request, render_template

from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
def index():
    page = int(request.args.get('page', 1))
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)

    return render_template('home.html', title='Posts', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html')
