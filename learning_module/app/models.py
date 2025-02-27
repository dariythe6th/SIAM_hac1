from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    courses = db.relationship('Course', backref='author', lazy='dynamic')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(500))
    modules = db.relationship('Module', backref='course', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(500))
    blocks = db.relationship('Block', backref='module', lazy='dynamic')
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content_type = db.Column(db.String(50))  # text, image, video
    content = db.Column(db.String(500))
    questions = db.relationship('Question', backref='block', lazy='dynamic')
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    question_type = db.Column(db.String(50))  # single, multiple
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
