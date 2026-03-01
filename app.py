import os
from flask import Flask, render_template, jsonify
from models import db, Article

app = Flask(__name__)

# データベース設定
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///test.db'

db.init_app(app)

with app.app_context():
    db.create_all()
    
    # --- ここから追加：テストデータを入れる ---
    if not Article.query.first(): # データが1件もなければ
        test_article = Article(
            title="初めての記事",
            content="これはテスト記事の内容です。正しく表示されていますか？",
            author="管理者"
        )
        db.session.add(test_article)
        db.session.commit()
        print("テスト記事を作成しました！")
    # --- ここまで追加 ---
    
# 画面の設定
# メイン画面表示
@app.route('/')
def index():
    return render_template('index.html')

# 記事一覧API
@app.route('/api/articles', methods=['GET'])
def get_articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return jsonify([{
        'id': a.id,
        'title': a.title,
        'author': a.author,
        'date': a.created_at.strftime('%Y/%m/%d')
    } for a in articles])
    
# 記事内容API
@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify({
        'title': article.title,
        'content': article.content,
        'author': article.author,
        'date': article.created_at.strftime('%Y/%m/%d')
    })

if __name__ == '__main__':
    app.run(debug=True)