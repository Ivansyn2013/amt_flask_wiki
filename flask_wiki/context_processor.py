from flask_login import current_user

def inject_quiz_nums_context():
    active_quiz = 0
    if current_user.is_authenticated:
        active_quiz = current_user.assigned_quizs.filter_by(is_active=True).count()
    return dict(active_quiz=active_quiz)