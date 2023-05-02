from flask import render_template, redirect, url_for, flash, request, abort
from sitesitesite import app, database, bcrypt
from sitesitesite.form import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from sitesitesite.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('a.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash('Login feito com sucesso', 'alert-success')
            pag_next = request.args.get('next')
            if pag_next:
                return redirect(pag_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login. Email ou senha incorretos', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route('/criar', methods=['GET', 'POST'])
def criar():
    form_criar = FormCriarConta()
    if form_criar.validate_on_submit():
        senha_cript = bcrypt.generate_password_hash(form_criar.senha.data)
        usuario = Usuario(username=form_criar.username.data, email=form_criar.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash('Conta criada com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criar.html', form_criar=form_criar)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect('login')

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('ENVIADO :)', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho)
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Alterações Salvas Com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Editado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Excluido com sucesso', 'alert-success')
        return redirect(url_for('home'))
    else:
        abort(403)