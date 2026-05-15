# routes/tags.py
from flask import Blueprint, render_template, request
from models import db
from models.question import Question
from models.tag import Tag

tags_bp = Blueprint('tags', __name__)

SUBJECT_TAGS = {
    '1': '1과목 - 소프트웨어 설계',
    '2': '2과목 - 소프트웨어 개발',
    '3': '3과목 - DB구축',
    '4': '4과목 - 프로그래밍 언어',
    '5': '5과목 - 정보시스템 구축관리',
}

SUBJECT_MAP = {
    '1': '1과목 - 소프트웨어 설계',
    '2': '2과목 - 소프트웨어 개발',
    '3': '3과목 - DB구축',
    '4': '4과목 - 프로그래밍 언어',
    '5': '5과목 - 정보시스템 구축관리',
}

def _sort_questions(questions):
    """중요문제 → 3회↑ → 2회↑ → 최신순(id 내림차순) 정렬"""
    return sorted(
        questions,
        key=lambda q: (
            0 if q.is_starred else 1,
            0 if q.wrong_count >= 3 else (1 if q.wrong_count >= 2 else 2),
            -q.id
        )
    )

# ── Wiki 메인 ────────────────────────────────
@tags_bp.route('/wiki')
def wiki():
    all_tags   = Tag.query.order_by(Tag.name).all()
    extra_tags = [t for t in all_tags if t.name not in SUBJECT_TAGS.values()]

    count_2    = Question.query.filter(Question.wrong_count >= 2).count()
    count_3    = Question.query.filter(Question.wrong_count >= 3).count()
    count_star = Question.query.filter(Question.is_starred == True).count()

    all_questions = _sort_questions(Question.query.all())

    return render_template('wiki.html',
                           subject_tags=SUBJECT_TAGS,
                           extra_tags=extra_tags,
                           count_2=count_2,
                           count_3=count_3,
                           count_star=count_star,
                           all_questions=all_questions,
                           subject_map=SUBJECT_MAP)

# ── 태그 상세 (문제 목록) ─────────────────────
@tags_bp.route('/wiki/tag/<tag_name>')
def tag_detail(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    questions = _sort_questions(list(tag.questions))
    return render_template('tag_detail.html',
                           tag=tag,
                           questions=questions,
                           subject_map=SUBJECT_MAP)

# ── 과목 필터 ────────────────────────────────
@tags_bp.route('/wiki/subject/<subject_num>')
def subject_filter(subject_num):
    label = SUBJECT_TAGS.get(subject_num)
    if not label:
        return "과목 없음", 404

    # subject 컬럼에 '1', '1과목', '1과목 - 소프트웨어 설계' 등 다양하게 저장됐을 수 있으므로
    # 숫자로 시작하는 모든 경우를 포함해서 조회
    questions = Question.query.filter(
        (Question.subject == subject_num) |
        (Question.subject.like(subject_num + '%'))
    ).all()

    questions = _sort_questions(questions)

    return render_template('tag_detail.html',
                           tag=type('T', (), {'name': label})(),
                           questions=questions,
                           subject_map=SUBJECT_MAP)

# ── 퀴즈 모드 진입 ────────────────────────────
@tags_bp.route('/quiz')
def quiz():
    mode    = request.args.get('mode', 'tag')
    value   = request.args.get('value', '')
    ids_str = request.args.get('ids_str', '')
    idx     = int(request.args.get('idx', 0))

    if ids_str:
        id_list   = [int(x) for x in ids_str.split(',') if x.strip().isdigit()]
        questions = Question.query.filter(Question.id.in_(id_list)).all()
        id_order  = {qid: i for i, qid in enumerate(id_list)}
        questions = sorted(questions, key=lambda q: id_order.get(q.id, 0))
        title = '복습하기'
    elif mode == 'tag':
        tag = Tag.query.filter_by(name=value).first_or_404()
        questions = list(tag.questions)
        title = '[{}] 퀴즈'.format(value)
    elif mode == 'subject':
        questions = Question.query.filter(
            (Question.subject == value) |
            (Question.subject.like(value + '%'))
        ).order_by(Question.id).all()
        title = '{} 퀴즈'.format(SUBJECT_TAGS.get(value, value))
    elif mode == 'wrong2':
        questions = Question.query.filter(Question.wrong_count >= 2).order_by(Question.id).all()
        title = '2회 이상 틀린 문제 퀴즈'
    elif mode == 'wrong3':
        questions = Question.query.filter(Question.wrong_count >= 3).order_by(Question.id).all()
        title = '3회 이상 틀린 문제 퀴즈'
    elif mode == 'starred':
        questions = Question.query.filter(Question.is_starred == True).order_by(Question.id).all()
        title = '★ 중요 문제 퀴즈'
    else:
        questions = []
        title = '퀴즈'

    if not questions:
        return render_template('quiz_empty.html', title=title)

    total = len(questions)
    if idx >= total:
        idx = total - 1

    q       = questions[idx]
    all_ids = ','.join(str(x.id) for x in questions)

    return render_template('quiz.html',
                           q=q, idx=idx, total=total,
                           title=title, mode=mode, value=value,
                           all_ids=all_ids, ids_str=ids_str)

# ── 퀴즈 결과 페이지 ──────────────────────────
@tags_bp.route('/quiz/result')
def quiz_result():
    mode      = request.args.get('mode', '')
    value     = request.args.get('value', '')
    all_ids   = request.args.get('all_ids', '')
    wrong_ids = request.args.get('wrong_ids', '')
    total     = int(request.args.get('total', 0))

    wrong_id_list   = [int(x) for x in wrong_ids.split(',') if x.strip().isdigit()]
    wrong_questions = Question.query.filter(Question.id.in_(wrong_id_list)).all() if wrong_id_list else []

    wrong_count   = len(wrong_id_list)
    correct_count = total - wrong_count

    return render_template('quiz_result.html',
                           mode=mode, value=value,
                           total=total,
                           correct_count=correct_count,
                           wrong_count=wrong_count,
                           wrong_questions=wrong_questions,
                           wrong_ids=wrong_ids)
