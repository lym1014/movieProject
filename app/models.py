#coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:lym653512@localhost:3306/movie"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db = SQLAlchemy(app)

#会员实体
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True) # 编号
    name = db.Column(db.String(100), unique=True) # 昵称
    pwd = db.Column(db.String(100)) # 密码
    email = db.Column(db.String(100), unique=True) # 邮箱
    phone = db.Column(db.String(11), unique=True) # 手机号码
    info = db.Column(db.Text) # 个性简介
    face = db.Column(db.String(255), unique=True) # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now) # 注册时间
    uuid = db.Column(db.String(255), unique=True) # 唯一标识符
    userlogs = db.relationship("Userlog",backref='user')
    comments = db.relationship("Comment", backref='user')
    moviecols = db.relationship("Moviecol", backref='user')

    def __repr__(self):
        return "<User %r>" % self.name

#会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True,default=datetime.now)

    def __repr__(self):
        return "<Userlog %r>" % self.id

#标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True,default = datetime.now)
    movies = db.relationship("Movie",backref='tag')

    def __repr__(self):
        return "<Tag %r>" % self.name

#电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True) # 编号
    title = db.Column(db.String(255),unique=True) # 标题
    url = db.Column(db.String(255),unique=True) # 地址
    info = db.Column(db.Text) # 简介
    logo = db.Column(db.String(255),unique=True) # 封面
    star = db.Column(db.SmallInteger) # 星级
    playnum = db.Column(db.BigInteger) # 播放量
    commentnum = db.Column(db.BigInteger) # 评论量
    tag_id = db.Column(db.Integer,db.ForeignKey("tag.id")) # 所属标签
    area = db.Column(db.String(255)) # 上映地区
    release_time = db.Column(db.Date) # 上映时间
    length = db.Column(db.String(100)) # 电影时长
    addtime = db.Column(db.DateTime, index=True,default=datetime.now) # 添加时间
    comments = db.relationship("Comment", backref='movie')
    moviecols = db.relationship("Moviecol", backref='movie')

    def __repr__(self):
        return "<Movie %r>" % self.title

#上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True) # 编号
    title = db.Column(db.String(255),unique=True) # 标题
    logo = db.Column(db.String(255),unique=True) # 封面
    addtime = db.Column(db.DateTime, index=True,default = datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title

#评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    addtime = db.Column(db.DateTime, index=True,default=datetime.now) # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id

#电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    addtime = db.Column(db.DateTime, index=True,default=datetime.now) # 添加时间

    def __repr__(self):
        return "<Moviecol %r>" % self.id

#权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True,default = datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name

#角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True,default = datetime.now)  # 添加时间
    admins = db.relationship('Admin',backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name

#管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True,default = datetime.now)  # 添加时间
    adminlogs = db.relationship('Adminlog',backref='admin')
    oplogs = db.relationship('Oplog',backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.name

#管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True,default=datetime.now)

    def __repr__(self):
        return "<Adminlog %r>" % self.id

#操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True,default=datetime.now)

    def __repr__(self):
        return "<Oplog %r>" % self.id

if __name__ == "__main__":
    db.create_all()
    role = Role(
        name = "超级管理员",
        auths = ""
    )
    db.session.add(role)
    # from werkzeug.security import generate_password_hash
    # admin = Admin(
    #     name = "ron1",
    #     pwd = generate_password_hash("a164554807"),
    #     is_super = 0,
    #     role_id = 1
    # )
    # db.session.add(admin)
    db.session.commit()
