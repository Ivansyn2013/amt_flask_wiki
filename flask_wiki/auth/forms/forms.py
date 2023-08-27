from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class RegistrationForm(FlaskForm):
    first_name = StringField("Имя")
    last_name = StringField("Фамилия")
    login = StringField("Логин",
                           [validators.DataRequired()],
                           )
    email = StringField("Email",
                        [
                            validators.DataRequired(),
                            validators.Email(),
                            validators.length(min=6, max=200),
                        ],
                        filters=[lambda data: data and data.lower()],
                        )
    password = PasswordField("Пароль",
                             [
                                 validators.DataRequired(),
                                 validators.EqualTo("confirm",
                                                    message="Password must "
                                                            "match"),
                                 ],
                             )
    confirm = PasswordField("Подтвердить пароль")
    submit = SubmitField("Регистрация")


class LoginForm(FlaskForm):
    email = StringField("Email",
                        [
                            validators.DataRequired(),
                            validators.Email(),
                            validators.length(min=6, max=200),],
                        filters=[lambda data: data and data.lower()],
                        )
    password = PasswordField("Пароль", [validators.DataRequired()])
    submit = SubmitField("Войти")