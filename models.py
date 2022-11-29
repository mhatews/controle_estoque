class Produto:
    def __init__(self, nome, categoria, categoria_id, fornecedor, fornecedor_id, quantidade, id=None):
        self._id = id
        self._nome=nome
        self._categoria=categoria
        self._categoria_id=categoria_id
        self._fornecedor= fornecedor
        self._fornecedor_id = fornecedor_id
        self._quantidade=quantidade


class Usuario:
    def __init__(self,senha, id= None):
        self._senha=senha
        self._id = id


class Categoria:
    def __init__(self,nome, id= None):
        self._id= id
        self._nome= nome


class Fornecedor:
    def __init__(self, nome, endereco, telefone, CNPJ, id =None):
        self._nome=nome
        self._endereco=endereco
        self._telefone=telefone
        self._CNPJ=CNPJ
        self._id = id