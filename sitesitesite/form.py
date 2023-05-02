from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sitesitesite.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Tente novamente')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar de mim')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuario Novo', validators=[DataRequired()])
    email = StringField('E-mail Novo', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Mudar Foto De Perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_excel = BooleanField('Excel')
    curso_vba = BooleanField('VBA')
    curso_powerbi = BooleanField('PowerBI')
    curso_python = BooleanField('Python')
    curso_ppt = BooleanField('Apresentações')
    curso_sql = BooleanField('SQL')

    botao_submit_editarperfil = SubmitField('Salvar')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email já cadastrado. Tente novamente')


class FormCriarPost(FlaskForm):
    titulo = StringField('titulo', validators=[DataRequired(), Length(2, 200)])
    corpo = TextAreaField('Escreva oque quiser', validators=[DataRequired()])
    botao_submit = SubmitField('Enviar')