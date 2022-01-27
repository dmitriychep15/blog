from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
@app.route('/posts/')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)

@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        ttl = request.form['title']
        intr = request.form['intro']
        txt = request.form['text']
        art = Article(title=ttl, intro=intr, text=txt)
        try:
            db.session.add(art)
            db.session.commit()
            return redirect('/posts')
        except:
            # db.session.rollback()
            return "Ошибка при добавлениее данных"

    else:
        return render_template('create_article.html')

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect(f'/posts/{id}')
        except:
            # db.session.rollback()
            return "Ошибка при добавлениее данных"

    else:
        return render_template('post_update.html', article=article)



if __name__ == '__main__':
    app.run(debug=True)
