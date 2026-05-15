# app.py

import os
from flask import Flask
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 이미지 업로드 설정
    app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 최대 16MB

    # DB 초기화
    db.init_app(app)

    # 라우터 등록
    from routes.questions import questions_bp
    from routes.tags import tags_bp
    app.register_blueprint(questions_bp)
    app.register_blueprint(tags_bp)

    # DB 테이블 자동 생성
    with app.app_context():
        from models.question import Question
        from models.tag import Tag
        db.create_all()
        print("✅ DB 테이블 생성 완료")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
