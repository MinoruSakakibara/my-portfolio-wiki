from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# SQLAlchemyインスタンス生成
db = SQLAlchemy()

class Article(db.Model):
    # 記事のデータ管理を行うテーブル
    __tablename__ = 'articles'
    
    # カラム定義
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), default="Unknown")
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Article {self.title}>'