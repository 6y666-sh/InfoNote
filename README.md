# 📝 InfoNote - 정처기 오답노트

정보처리기사 시험을 준비하면서 틀린 문제를 체계적으로 관리하기 위한 로컬 오답노트 웹 애플리케이션입니다.

---

## 주요 기능

- 틀린 문제를 텍스트로 복붙하여 등록
- 1~5과목 분류 및 세부 태그 직접 입력
- 문제별 오답 이유, 핵심 개념 정리
- 태그별로 묶어서 보는 Wiki 페이지
- 전체 문제 목록 및 상세 페이지

---

## 기술 스택

| 항목         | 사용 기술                             |
| ------------ | ------------------------------------- |
| 백엔드       | Python 3, Flask                       |
| 데이터베이스 | MySQL                                 |
| ORM          | Flask-SQLAlchemy                      |
| 프론트엔드   | HTML, CSS, JavaScript (Jinja2 템플릿) |

---

## 설치 및 실행 방법

### 1. 사전 준비

- Python 3.x 설치
- MySQL 설치 및 실행
- `note` 데이터베이스 생성

```sql
CREATE DATABASE note CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'note_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON note.* TO 'note_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. 패키지 설치

pip install -r requirements.txt

### 3. DB 설정

- config.py 에서 본인의 MySQL 접속 정보로 수정합니다.

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://note_user:1234@localhost:3306/note?charset=utf8mb4"

### 4. 서버 실행

python app.py

### 5. 브라우저 접속

http://127.0.0.1:5000

# 사용 방법

시험에서 틀린 문제를 복사합니다.
문제 추가 페이지에서 과목, 태그, 문제 내용을 입력합니다.
내가 고른 답, 정답, 틀린 이유, 핵심 개념을 정리합니다.
Wiki 페이지에서 태그별로 묶인 오답노트를 확인합니다.
