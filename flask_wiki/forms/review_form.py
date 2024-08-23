from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import (
    StringField,
    validators,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,)

from db.init_db import db
from flask_wiki.models.page import PageDb


class ReviewForm(FlaskForm):
    page_title = SelectField('Название страницы',
                             choices=[],
                             validators=[validators.DataRequired()])
    category = SelectField('Тип рецензии ',
                           choices=[("Ошибка", "Ошибка"), ("Замечание", "Замечание"), ("Предложение", "Предложение")],
                           validators=[validators.DataRequired()])

    text = TextAreaField('Текст рецензии', validators=[validators.DataRequired()])

    submit = SubmitField("Сохранить рецензию")

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        subquery = db.session.query(
            PageDb.title,
            func.max(PageDb.create_date).label('max_created_at')
        ).group_by(PageDb.title).subquery()

        query = db.session.query(PageDb).join(
            subquery,
            (PageDb.title == subquery.c.title) &
            (PageDb.create_date == subquery.c.max_created_at)
        )

        self.page_title.choices = [(p.title, p.title) for p in query.all()]
