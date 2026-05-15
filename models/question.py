# models/question.py
from . import db
from datetime import datetime

class Question(db.Model):
    __tablename__ = 'questions'

    id           = db.Column(db.Integer, primary_key=True)
    subject      = db.Column(db.String(50), nullable=False)   # 1~5과목
    detail_tag   = db.Column(db.String(100))                  # 세부 태그
    question_text= db.Column(db.Text, nullable=False)
    image_path   = db.Column(db.String(255))
    choice_1     = db.Column(db.String(500))
    choice_2     = db.Column(db.String(500))
    choice_3     = db.Column(db.String(500))
    choice_4     = db.Column(db.String(500))
    my_answer    = db.Column(db.String(10))
    correct_answer = db.Column(db.String(10))
    summary      = db.Column(db.Text)
    wrong_reason = db.Column(db.Text)
    key_concept  = db.Column(db.Text)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # ★ 신규 컬럼
    wrong_count  = db.Column(db.Integer, default=0, nullable=False)  # 틀린 횟수
    is_starred   = db.Column(db.Boolean, default=False, nullable=False)  # 중요 문제 별표

    tags = db.relationship('Tag', secondary='question_tags', backref='questions', lazy='dynamic')

    def wrong_class(self):
        """틀린 횟수에 따른 CSS 클래스 반환"""
        if self.wrong_count >= 3:
            return 'danger'
        elif self.wrong_count >= 2:
            return 'warning'
        return ''
