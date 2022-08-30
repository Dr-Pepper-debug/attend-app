from testapp import db
from datetime import datetime


class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    number = db.Column(db.String(255))  # 学籍番号
    name = db.Column(db.String(255))  # 氏名