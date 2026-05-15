# config.py

class Config:
    # MySQL 연결 설정
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://note_user:1234@localhost:3306/note"
        "?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 연결이 끊겼을 때 자동 재연결
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 3600,
        "pool_pre_ping": True
    }
    
    SECRET_KEY = "infonote-secret"
