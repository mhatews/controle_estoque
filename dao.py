from models import Produto, Usuario, Categoria, Fornecedor


SQL_DELETA_PRODUTO = 'delete from produto where id = %s'
SQL_CRIA_PRODUTO = 'INSERT into produto (nome, categoria_id, fornecedor_id,quantidade) values (%s, %s, %s, %s)'
SQL_ATUALIZA_PRODUTO = 'UPDATE produto SET nome=%s, categoria_id=%s, fornecedor_id=%s ,quantidade=%s where id=%s'
SQL_BUSCA_PRODUTO = 'SELECT P.id, P.nome, C.nome as categoria_Nome, P.categoria_id, F.nome as fornecedor_Nome, P.fornecedor_id, P.quantidade FROM estoque_2.produto P INNER JOIN estoque_2.categoria C ON (P.categoria_id = C.id) INNER JOIN estoque_2.fornecedor F ON (P.fornecedor_id = F.id)'
SQL_PRODUTO_POR_ID = 'SELECT P.id, P.nome, C.nome as categoria_Nome, P.categoria_id, F.nome as fornecedor_Nome, P.fornecedor_id, P.quantidade FROM estoque_2.produto P INNER JOIN estoque_2.categoria C ON (P.categoria_id = C.id) INNER JOIN estoque_2.fornecedor F ON (P.fornecedor_id = F.id) where P.id=%s'
SQL_PRODUTO_POR_NOME = 'SELECT P.id, P.nome, C.nome as categoria_Nome, P.categoria_id, F.nome as fornecedor_Nome, P.fornecedor_id, P.quantidade FROM estoque_2.produto P INNER JOIN estoque_2.categoria C ON (P.categoria_id = C.id) INNER JOIN estoque_2.fornecedor F ON (P.fornecedor_id = F.id) where P.nome=%s'

SQL_CRIA_USUARIO = 'INSERT into usuario (id, senha) values (%s, %s)'
SQL_BUSCA_USUARIO = 'SELECT id, senha from usuario'
SQL_USUARIO_POR_ID = 'SELECT id, senha from usuario where id=%s'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET senha=%s where id=%s'
SQL_DELETA_USUARIO = 'delete from usuario where id = %s'


SQL_CRIA_CATEGORIA = 'INSERT into categoria (nome) values (%s)'
SQL_ATUALIZA_CATEGORIA = 'UPDATE categoria SET nome=%s where id=%s'
SQL_BUSCA_CATEGORIA = 'SELECT id, nome from categoria'
SQL_CATEGORIA_POR_ID = 'SELECT id, nome from categoria where id=%s'
SQL_DELETA_CATEGORIA = 'delete from categoria where id = %s'

SQL_BUSCA_FORNECEDOR = 'SELECT id, nome, endereco, telefone, CNPJ from fornecedor'
SQL_CRIA_FORNECEDOR = 'INSERT into fornecedor (nome, endereco, telefone, CNPJ) values (%s, %s, %s, %s)'
SQL_ATUALIZA_FORNECEDOR = 'UPDATE fornecedor SET nome=%s, endereco=%s, telefone=%s, CNPJ=%s where id=%s'
SQL_FORNECEDOR_POR_ID = 'SELECT id, nome, endereco, telefone, CNPJ from fornecedor where id=%s'
SQL_DELETA_FORNECEDOR = 'delete from fornecedor where id = %s'

class ProdutoDao:
    def __init__(self, db1):
        self.__db1=db1

    def salvar(self, produto):
        cursor = self.__db1.connection.cursor()

        if(produto._id):
            cursor.execute(SQL_ATUALIZA_PRODUTO, (produto._nome, produto._categoria_id, produto._fornecedor_id, produto._quantidade, produto._id))
        else:
            cursor.execute(SQL_CRIA_PRODUTO, (produto._nome, produto._categoria_id, produto._fornecedor_id, produto._quantidade))
            cursor._id= cursor.lastrowid

        self.__db1.connection.commit()
        return produto

    def listar(self):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_BUSCA_PRODUTO)
        produtos = traduz_produtos(cursor.fetchall())
        return produtos

    def listar_pes(self):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_BUSCA_PRODUTO)
        produtos = traduz_produtos_2(cursor.fetchall())
        return produtos


    def busca_por_id(self, id):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_PRODUTO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Produto(tupla[1], tupla[2], tupla[3], tupla[4],tupla[5],tupla[6], id = tupla[0])

    def deletar(self, id):
        self.__db1.connection.cursor().execute(SQL_DELETA_PRODUTO, (id,))
        self.__db1.connection.commit()


def traduz_produtos(produtos):
    def cria_produto_com_tupla(tupla):
        return Produto(tupla[1], tupla[2], tupla[3],tupla[4],tupla[5],tupla[6], id=tupla[0])
    return list(map(cria_produto_com_tupla, produtos))

def traduz_produtos_2(produtos):
    def cria_produto_com_tupla_2(tupla):
        return Produto(tupla[1], tupla[2], tupla[3],tupla[4],tupla[5],tupla[6], id=tupla[0])
    return list(map(cria_produto_com_tupla_2, produtos))


def traduz_categorias(categorias):
    def cria_categoria_com_tupla(tupla):
        return Categoria(tupla[1], id = tupla[0])
    return list(map(cria_categoria_com_tupla, categorias))

def traduz_forn(fornecedores):
    def cria_forn_com_tupla(tupla):
        return Fornecedor(tupla[1], tupla[2], tupla[3], tupla[4], id=tupla[0])
    return list(map(cria_forn_com_tupla, fornecedores))

def traduz_usu(usuarios):
    def cria_usu_com_tupla(tupla):
        return Usuario(tupla[1], id=tupla[0])
    return list(map(cria_usu_com_tupla, usuarios))

def traduz_usuario(tupla):
        return Usuario(tupla[1], id=tupla[0])


class UsuarioDao:
    def __init__(self,db1):
        self.__db1 = db1


    def salva_u(self, usuario):
        cursor = self.__db1.connection.cursor()

        if(usuario._id):
            cursor.execute(SQL_ATUALIZA_USUARIO, (usuario._senha, usuario._id))
        else:
            cursor.execute(SQL_CRIA_USUARIO, (usuario._senha,))
            cursor._id= cursor.lastrowid

        self.__db1.connection.commit()
        return usuario

    def busca_por_id(self, id):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def busca_por_id_2(self, id):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Usuario(tupla[1], id = tupla[0])

    def salvar_usu(self, usuario):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_CRIA_USUARIO, (usuario._id, usuario._senha))
        cursor._id = cursor.lastrowid
        self.__db1.connection.commit()
        return usuario

    def listar_usu(self):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_BUSCA_USUARIO)
        usuarios = traduz_usu(cursor.fetchall())
        return usuarios

    def deletar_usu(self, id):
        self.__db1.connection.cursor().execute(SQL_DELETA_USUARIO, (id,))
        self.__db1.connection.commit()



class CategoriaDao:
    def __init__(self, db1):
        self.__db1=db1

    def listar_cat(self):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_BUSCA_CATEGORIA)
        categorias = traduz_categorias(cursor.fetchall())
        return categorias

    def salvar_cat(self, categoria):
        cursor = self.__db1.connection.cursor()

        if (categoria._id):
            cursor.execute(SQL_ATUALIZA_CATEGORIA, (categoria._nome, categoria._id))
        else:
            cursor.execute(SQL_CRIA_CATEGORIA, (categoria._nome,))
            cursor._id = cursor.lastrowid

        self.__db1.connection.commit()
        return categoria

    def busca_por_id(self, id):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_CATEGORIA_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Categoria(tupla[1], id = tupla[0])

    def deletar_cat(self, id):
        self.__db1.connection.cursor().execute(SQL_DELETA_CATEGORIA, (id,))
        self.__db1.connection.commit()

class FornecedorDao:
    def __init__(self, db1):
        self.__db1=db1

    def listar_forn(self):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_BUSCA_FORNECEDOR)
        fornecedores = traduz_forn(cursor.fetchall())
        return fornecedores

    def salvar_forn(self, fornecedor):
        cursor = self.__db1.connection.cursor()

        if (fornecedor._id):
            cursor.execute(SQL_ATUALIZA_FORNECEDOR, (fornecedor._nome, fornecedor._endereco, fornecedor._telefone, fornecedor._CNPJ, fornecedor._id))
        else:
            cursor.execute(SQL_CRIA_FORNECEDOR, (fornecedor._nome, fornecedor._endereco, fornecedor._telefone, fornecedor._CNPJ,))
            cursor._id = cursor.lastrowid

        self.__db1.connection.commit()
        return fornecedor

    def busca_por_id(self, id):
        cursor = self.__db1.connection.cursor()
        cursor.execute(SQL_FORNECEDOR_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Fornecedor(tupla[1], tupla[2], tupla[3], tupla[4], id = tupla[0])

    def deletar_forn(self, id):
        self.__db1.connection.cursor().execute(SQL_DELETA_FORNECEDOR, (id,))
        self.__db1.connection.commit()


