from . import db

# 문제-태그 연결 테이블 (다대다 관계)
question_tags = db.Table(
    "question_tags",
    db.Column("question_id", db.Integer, db.ForeignKey("questions.id"), primary_key=True),
    db.Column("tag_id",      db.Integer, db.ForeignKey("tags.id"),      primary_key=True)
)

class Tag(db.Model):
    __tablename__ = "tags"

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # 태그 이름

    def __repr__(self):
        return f"<Tag {self.name}>"
