from itertools import count
from typing import Optional
from flask import Flask, request,jsonify
from flask_pydantic_spec import FlaskPydanticSpec,Request,Response
from pydantic import BaseModel,Field
from tinydb import TinyDB,Query
server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title="Cleverson")
spec.register(server)
database = TinyDB('database.json')
# http://localhost:5000/apidoc/swagger

c = count()



class Pessoa(BaseModel):
    id: Optional[int] = Field(default_factory=lambda :next(c))
    nome : str
    idade : int

class QueryPessoa(BaseModel):
    id: Optional[int]
    nome : Optional[str]
    idade : Optional[int]



class Pessoas(BaseModel):
    pessoas : list[Pessoa]
    count : int


@server.get('/pessoa')
@spec.validate(
    query=QueryPessoa,
    resp=Response(HTTP_200=Pessoas))
def buscar_pessoas():
    '''Busca tudo que tem no banco tinyDB'''
    query = request.context.query.dict(exclude_none=True)
    # breakpoint()
    todas_as_pessoas  = database.search(
        Query().fragment(query)
    )
    return jsonify(
        Pessoas(
            pessoas=todas_as_pessoas,
            count=len(todas_as_pessoas)
        ).dict()
    )

@server.get('/pessoa/<int:id>')
@spec.validate(resp=Response(HTTP_200=Pessoa))
def buscar_pessoa(id):
    '''Busca tudo que tem no banco tinyDB'''
    try:
        pessoa = database.search(Query().id == id)[0]
    except IndexError:
        return {'massage':'Pessoa not fount!'}, 404
    return jsonify(pessoa)



@server.post('/pessoa')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_201=Pessoa))
def inserir_pessoa():
    '''Insere uma pessoa no banco de dados '''
    body = request.context.body.dict()
    database.insert(body)
    return body

@server.put('/pessoa/<int:id>')
@spec.validate(
    body=Request(Pessoa),
    resp=Response(HTTP_200=Pessoa)
)
def alterar_pessoa(id):
    """Altera uma pessoa do banco de dados"""

    Pessoa =Query()
    body = request.context.body.dict()
    database.update(body, Pessoa.id==id)
    return jsonify(body)

@server.delete('/pessoa/<int:id>')
@spec.validate(
    resp=Response(HTTP_200=Pessoa)
)
def delete_pessoa(id):
    """Deleta uma pessoa do banco de dados"""
    Pessoa =Query()
    database.remove(Pessoa.id==id)
    return buscar_pessoa()



server.run(debug=True)