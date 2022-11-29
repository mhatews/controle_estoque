
from flask import Flask, render_template, request, redirect, session, flash, send_from_directory

from dao import ProdutoDao, UsuarioDao, CategoriaDao, FornecedorDao
from flask_mysqldb import MySQL

from models import Produto, Usuario, Categoria, Fornecedor

import os

app = Flask(__name__)
app.secret_key= 'LP2'

app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__))+'/upload'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'estoque_2'
app.config['MYSQL_PORT'] = 3306
db1 = MySQL(app)
produto_dao = ProdutoDao(db1)
usuario_dao = UsuarioDao(db1)
categoria_dao = CategoriaDao(db1)
fornecedor_dao= FornecedorDao(db1)


@app.route('/')
def index():
    return render_template('index.html', titulo="Seja Bem-Vindo")

@app.route('/lista_produtos')
def lista_produtos():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=lista_produtos')
    lista = produto_dao.listar()
    return render_template('lista_1.html', titulo="Lista de Estoque", produtos=lista)

@app.route('/lista_categorias')
def lista_categorias():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=lista_categorias')
    lista = categoria_dao.listar_cat()
    return render_template('lista_categorias.html', titulo="Lista de Categorias", categorias=lista)

@app.route('/lista_fornecedores')
def lista_fornecedores():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=lista_categorias')
    lista = fornecedor_dao.listar_forn()
    return render_template('lista_fornecedores.html', titulo="Lista de Fornecedores", fornecedores=lista)

@app.route('/lista_usuarios')
def lista_usuarios():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=lista_categorias')
    lista_usu = usuario_dao.listar_usu()
    return render_template('lista_usuarios.html', titulo="Usuarios Cadastrados", usuarios=lista_usu)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=novo')
    lista_cat = categoria_dao.listar_cat()
    lista_forn = fornecedor_dao.listar_forn()
    return render_template('novo_1.html',titulo="Cadastrar Novo Produto", categorias=lista_cat, fornecedores=lista_forn)

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria_id = request.form['categoria']
    fornecedor_id = request.form["fornecedor"]
    quantidade = request.form["quantidade"]
    produto = Produto(nome,None, categoria_id,None, fornecedor_id, quantidade)

    produto_dao.salvar(produto)
    return redirect('/lista_produtos')

@app.route('/lista_pesquisa', methods=['POST',])
def lista_pesquisa():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return redirect('/login?proxima=lista_pesquisa')
    lista = produto_dao.listar_pes()
    return render_template('lista_pesquisa.html', titulo="Lista de Estoque", produtos=lista)


@app.route('/login')
def login():
    proxima=request.args.get('proxima')
    if proxima == None:
        proxima=''
    return render_template('login_1.html', proxima=proxima)

@app.route('/login_erro')
def login_erro():
    proxima=request.args.get('proxima')
    if proxima == None:
        proxima=''
    return render_template('login_erro.html', proxima=proxima)

@app.route('/novo_usuario')
def novo_usuario():
    return render_template('novo_usuario.html',titulo="Cadastrar Novo Usuário")

@app.route('/novo_usuario_erro')
def novo_usuario_erro():
    return render_template('novo_usuario_erro.html',titulo="Cadastrar Novo Usuário")

@app.route('/criar_usuario', methods=['POST',])
def criar_usuario():
    id = request.form['id']
    senha = request.form["senha"]
    a = usuario_dao.busca_por_id(id)
    if a:
        flash('Usuario já existe, tente novamente')
        return redirect('/novo_usuario_erro')
    else:
        usuario = Usuario(senha, id)
        usuario_dao.salvar_usu(usuario)
        flash('Conta criada com sucesso!Faça Login Agora')
        return redirect('/login')

@app.route('/nova_categoria')
def nova_categoria():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=nova_categoria')
    return render_template('nova_categoria.html',titulo="Cadastrar Nova Categoria")

@app.route('/criar_categoria', methods=['POST',])
def criar_categoria():

    nome = request.form["nome"]

    cat = Categoria(nome)

    categoria_dao.salvar_cat(cat)

    flash('Categoria criada com sucesso!')
    return redirect('/lista_categorias')

@app.route('/novo_fornecedor')
def novo_fornecedor():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=novo')
    return render_template('novo_fornecedor.html',titulo="Cadastrar Novo Fornecedor")

@app.route('/criar_fornecedor', methods=['POST',])
def criar_fornecedor():
    nome = request.form['nome']
    endereco = request.form['endereco']
    telefone = request.form["telefone"]
    CNPJ = request.form["CNPJ"]
    fornecedor = Fornecedor(nome,endereco, telefone, CNPJ)

    fornecedor_dao.salvar_forn(fornecedor)
    return redirect('/lista_fornecedores')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['usuario'])
    if usuario:
        if usuario._senha == request.form['senha']:
            session ['usuario_logado'] = request.form['usuario']
            flash(request.form['usuario']+ ' logou com sucesso')
            proxima_pagina = request.form['proxima']
            if proxima_pagina == '':
                return redirect('/lista_produtos')
            else:
                return redirect('/{}'.format(proxima_pagina))

    flash('Não logado, tente novamente')
    return  redirect('/login_erro')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    return redirect('/')

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=editar')
    produto = produto_dao.busca_por_id(id)
    lista_cat = categoria_dao.listar_cat()
    lista_forn = fornecedor_dao.listar_forn()
    return render_template('editar.html',titulo="Editando Produto", produto = produto, categorias=lista_cat, fornecedores=lista_forn)

@app.route('/editar_categorias/<int:id>')
def editar_categorias(id):
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=editar')
    categoria = categoria_dao.busca_por_id(id)
    return render_template('editar_categorias.html',titulo="Editando Categoria", categoria = categoria)

@app.route('/editar_usuario/<string:id>')
def editar_usuario(id):
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=editar_usuario')
    usuario = usuario_dao.busca_por_id_2(id)
    return render_template('editar_usuario.html',titulo="Editando Usuario", usuario = usuario)

@app.route('/editar_fornecedores/<int:id>')
def editar_fornecedores(id):
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return  redirect('/login?proxima=editar')
    fornecedor = fornecedor_dao.busca_por_id(id)
    return render_template('editar_fornecedores.html',titulo="Editando Fornecedor", fornecedor=fornecedor)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria_id = request.form['categoria']
    fornecedor_id = request.form['fornecedor']
    quantidade = request.form["quantidade"]
    id = request.form['id']
    produto = Produto(nome, None, categoria_id, None, fornecedor_id, quantidade, id)

    produto_dao.salvar(produto)
    return redirect('/lista_produtos')

@app.route('/atualizar_usuario', methods=['POST',])
def atualizar_usuario():
    id = request.form['id']
    senha = request.form['senha']
    usuario = Usuario(senha,id)

    usuario_dao.salva_u(usuario)
    return redirect('/lista_usuarios')


@app.route('/atualizar_categorias', methods=['POST',])
def atualizar_categorias():
    nome = request.form['nome']
    id = request.form['id']
    categoria = Categoria(nome, id)

    categoria_dao.salvar_cat(categoria)
    return redirect('/lista_categorias')

@app.route('/atualizar_fornecedores', methods=['POST',])
def atualizar_fornecedores():
    nome = request.form['nome']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    CNPJ = request.form['CNPJ']
    id = request.form['id']
    fornecedor = Fornecedor(nome, endereco, telefone, CNPJ, id)

    fornecedor_dao.salvar_forn(fornecedor)
    return redirect('/lista_fornecedores')

@app.route('/deletar/<int:id>')
def deletar(id):
    produto_dao.deletar(id)
    return redirect('/lista_produtos')

@app.route('/deletar_categoria/<int:id>')
def deletar_categoria(id):
    categoria_dao.deletar_cat(id)
    return redirect('/lista_categorias')

@app.route('/deletar_usuario/<string:id>')
def deletar_usuario(id):
    usuario_dao.deletar_usu(id)
    return redirect('/lista_usuarios')


@app.route('/deletar_fornecedor/<int:id>')
def deletar_fornecedor(id):
    fornecedor_dao.deletar_forn(id)
    return redirect('/lista_fornecedores')

@app.route('/upload/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('upload', nome_arquivo)

if __name__ == '__main__':
    app.run(debug=True)