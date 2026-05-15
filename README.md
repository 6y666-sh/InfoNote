# InfoNote - 정처기 오답노트

정보처리기사 시험 준비를 위한 오답노트 웹 애플리케이션입니다.  
Flask + MySQL 기반으로 동작하며, 문제 등록부터 퀴즈 풀기, 오답 복습까지 지원합니다.

---

## 기술 스택

| 구분 | 사용 기술 |
|---|---|
| 백엔드 | Python 3.12, Flask |
| 데이터베이스 | MySQL, SQLAlchemy (Flask-SQLAlchemy) |
| 프론트엔드 | HTML, CSS, JavaScript (Vanilla) |
| 템플릿 엔진 | Jinja2 |

---

## 프로젝트 구조

```
C:\IBM4_FILE\infonote\
│
├── app.py                  # Flask 앱 진입점
├── config.py               # DB 연결 설정
│
├── models/
│   ├── __init__.py         # SQLAlchemy db 인스턴스
│   ├── question.py         # 문제 모델 (Question)
│   └── tag.py              # 태그 모델 (Tag)
│
├── routes/
│   ├── questions.py        # 문제 CRUD, 틀린 횟수 API, 별표 API
│   └── tags.py             # Wiki, 태그 상세, 과목 필터, 퀴즈 라우터
│
├── templates/
│   ├── base.html           # 공통 레이아웃
│   ├── index.html          # 문제 목록 (홈)
│   ├── add.html            # 문제 등록 폼
│   ├── detail.html         # 문제 상세 보기
│   ├── wiki.html           # Wiki 메인 (태그 목록 + 전체 문제)
│   ├── tag_detail.html     # 태그/과목별 문제 목록
│   ├── quiz.html           # 퀴즈 풀기 화면
│   ├── quiz_result.html    # 퀴즈 결과 화면
│   └── quiz_empty.html     # 퀴즈 대상 문제 없을 때
│
├── static/
│   ├── css/style.css       # 전체 스타일
│   ├── js/main.js          # 별표 AJAX, 행 클릭 이동
│   └── uploads/            # 문제 이미지 업로드 폴더
```

---

## DB 설정

### 1. 데이터베이스 생성

```sql
CREATE DATABASE note CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE note;
```

### 2. 테이블 생성

```sql
CREATE TABLE questions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    subject         VARCHAR(50)  NOT NULL,
    detail_tag      VARCHAR(100),
    question_text   TEXT         NOT NULL,
    image_path      VARCHAR(255),
    choice_1        VARCHAR(500),
    choice_2        VARCHAR(500),
    choice_3        VARCHAR(500),
    choice_4        VARCHAR(500),
    my_answer       VARCHAR(10),
    correct_answer  VARCHAR(10),
    summary         TEXT,
    wrong_reason    TEXT,
    key_concept     TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    wrong_count     INT DEFAULT 0 NOT NULL,
    is_starred      BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE tags (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE question_tags (
    question_id INT NOT NULL,
    tag_id      INT NOT NULL,
    PRIMARY KEY (question_id, tag_id),
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)      REFERENCES tags(id)      ON DELETE CASCADE
);
```

### 3. 기존 DB에 신규 컬럼 추가 (이미 테이블이 있는 경우)

```sql
USE note;
ALTER TABLE questions ADD COLUMN wrong_count INT DEFAULT 0 NOT NULL;
ALTER TABLE questions ADD COLUMN is_starred  BOOLEAN DEFAULT FALSE NOT NULL;
```

---

## 실행 방법

```bash
# 1. 의존성 설치 (최초 1회)
pip install flask flask-sqlalchemy pymysql

# 2. 서버 실행
cd C:\IBM4_FILE\infonote
python app.py
```

브라우저에서 `http://127.0.0.1:5000` 접속

---

## 주요 기능

### 문제 등록 (`/add`)

- 과목 선택 (1~5과목)
- 문제 본문, 보기 1~4번 입력
- 내가 선택한 답 / 정답 입력
- 한 줄 요약, 틀린 이유, 핵심 개념 메모
- 문제 이미지 첨부
- 세부 태그 입력 (쉼표로 구분, 예: `OOP, 디자인패턴`)

---

### 문제 목록 (`/`)

- 전체 문제를 최신순으로 나열
- 각 행에 **한 줄 요약** 표시 (요약 없으면 문제 텍스트 앞부분)
- 틀린 횟수 뱃지 표시
  - 2회 이상 → 노란색 배경
  - 3회 이상 → 빨간색 배경
- ★/☆ 클릭으로 중요 문제 즉시 토글 (AJAX, 페이지 새로고침 없음)
- 행 클릭 → 문제 상세 페이지 이동

---

### 문제 상세 (`/question/<id>`)

- 문제 전체 내용, 보기, 정답, 틀린 이유, 핵심 개념 표시
- 별표 토글 가능
- 삭제 버튼

---

### Wiki (`/wiki`)

Wiki 페이지는 세 구역으로 나뉩니다.

#### 과목별 문제

| 버튼 | 동작 |
|---|---|
| 과목 이름 클릭 | 해당 과목 문제 목록 페이지 |
| ▶ 클릭 | 해당 과목 퀴즈 시작 |

#### 특별 모아보기

| 태그 | 조건 | ▶ 클릭 |
|---|---|---|
| ★ 중요 문제 | is_starred = True | 중요 문제 퀴즈 |
| 🔴 3회 이상 틀린 문제 | wrong_count >= 3 | 3회↑ 퀴즈 |
| 🟡 2회 이상 틀린 문제 | wrong_count >= 2 | 2회↑ 퀴즈 |

#### 세부 태그

- 등록된 세부 태그 목록 (기본 접힘, 펼치기 버튼으로 열기)
- 태그 이름 클릭 → 해당 태그 문제 목록 페이지
- ▶ 클릭 → 해당 태그 퀴즈 시작

#### 전체 문제 목록

- Wiki 하단에 전체 문제 표시
- **정렬 순서**: 중요 문제 → 3회 이상 틀린 문제 → 2회 이상 틀린 문제 → 최신순

---

### 퀴즈 모드 (`/quiz`)

- 문제를 하나씩 표시하고 보기 4개 중 선택
- **정답 맞히면**: 틀린 횟수 변화 없음
- **오답이면**: 틀린 횟수 +1, 해당 문제 복습 목록에 추가
- 정답 확인 후 다음 문제 이동
- 마지막 문제 후 결과 화면으로 이동

#### 퀴즈 결과 화면 (`/quiz/result`)

- 맞힌 문제 수 / 전체 문제 수 표시
- **복습하기 버튼**: 이번 퀴즈에서 틀린 문제만 다시 풀기

---

### API 엔드포인트

| 메서드 | URL | 기능 |
|---|---|---|
| `POST` | `/question/<id>/wrong` | 틀린 횟수 +1, JSON 반환 |
| `POST` | `/question/<id>/star` | 별표 토글, JSON 반환 |

---

## 문제 색상 기준

| 조건 | 색상 | CSS 클래스 |
|---|---|---|
| wrong_count >= 3 | 빨간색 배경 | `danger` |
| wrong_count >= 2 | 노란색 배경 | `warning` |
| wrong_count < 2 | 기본 (흰색) | (없음) |

---

## 과목 코드 표

| 코드 | 과목명 |
|---|---|
| `1` | 1과목 - 소프트웨어 설계 |
| `2` | 2과목 - 소프트웨어 개발 |
| `3` | 3과목 - DB구축 |
| `4` | 4과목 - 프로그래밍 언어 |
| `5` | 5과목 - 정보시스템 구축관리 |
