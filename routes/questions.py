# routes/questions.py
import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from models import db
from models.question import Question
from models.tag import Tag

questions_bp = Blueprint('questions', __name__)

SUBJECT_MAP = {
    '1': '1과목 - 소프트웨어 설계',
    '2': '2과목 - 소프트웨어 개발',
    '3': '3과목 - DB구축',
    '4': '4과목 - 프로그래밍 언어',
    '5': '5과목 - 정보시스템 구축관리',
}

@questions_bp.route('/')
def index():
    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template('index.html', questions=questions, subject_map=SUBJECT_MAP)

@questions_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        subject        = request.form.get('subject', '')
        detail_tag     = request.form.get('detail_tag', '')
        question_text  = request.form.get('question_text', '')
        choice_1       = request.form.get('choice_1', '')
        choice_2       = request.form.get('choice_2', '')
        choice_3       = request.form.get('choice_3', '')
        choice_4       = request.form.get('choice_4', '')
        my_answer      = request.form.get('my_answer', '')
        correct_answer = request.form.get('correct_answer', '')
        summary        = request.form.get('summary', '')
        wrong_reason   = request.form.get('wrong_reason', '')
        key_concept    = request.form.get('key_concept', '')
        tag_names      = request.form.get('tags', '')

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                file.save(os.path.join(upload_dir, file.filename))
                image_path = f'uploads/{file.filename}'

        q = Question(
            subject=subject, detail_tag=detail_tag,
            question_text=question_text,
            choice_1=choice_1, choice_2=choice_2,
            choice_3=choice_3, choice_4=choice_4,
            my_answer=my_answer, correct_answer=correct_answer,
            summary=summary, wrong_reason=wrong_reason,
            key_concept=key_concept, image_path=image_path,
            wrong_count=0, is_starred=False,
        )

        for name in [t.strip() for t in tag_names.split(',') if t.strip()]:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            q.tags.append(tag)

        db.session.add(q)
        db.session.commit()
        return redirect(url_for('questions.index'))

    return render_template('add.html', subject_map=SUBJECT_MAP)

@questions_bp.route('/question/<int:qid>')
def detail(qid):
    q = Question.query.get_or_404(qid)
    return render_template('detail.html', q=q, subject_map=SUBJECT_MAP)

@questions_bp.route('/question/<int:qid>/delete', methods=['POST'])
def delete(qid):
    q = Question.query.get_or_404(qid)
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for('questions.index'))

# ── 틀린 횟수 +1 (AJAX) ──────────────────────
@questions_bp.route('/question/<int:qid>/wrong', methods=['POST'])
def add_wrong(qid):
    q = Question.query.get_or_404(qid)
    q.wrong_count += 1
    db.session.commit()
    return jsonify({'wrong_count': q.wrong_count, 'wrong_class': q.wrong_class()})

# ── 별표 토글 (AJAX) ─────────────────────────
@questions_bp.route('/question/<int:qid>/star', methods=['POST'])
def toggle_star(qid):
    q = Question.query.get_or_404(qid)
    q.is_starred = not q.is_starred
    db.session.commit()
    return jsonify({'is_starred': q.is_starred})
