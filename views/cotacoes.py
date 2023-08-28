from flask import Blueprint, jsonify, request
from sqlalchemy import text

cotacoes_bp = Blueprint("cotacoes", __name__, url_prefix="/cotacoes")

# CRUD #
# Lista de teste
lista = [
    {
        "id":1,
        "name": "Test1"
    },
    {
        "id":2,
        "name": "Test2"
    },
    {
        "id":3,
        "name": "Test3"
    },
]

# Create
@cotacoes_bp.post("/inserir")
def insert_cotaction():
    lista_length = len(lista)
    json = request.get_json()
    if json != {}:
        if 'name' in json:
            json['id'] = lista_length + 1
            lista.append(json)
            return jsonify({
                "method":"POST",
                "action":f"Inserir uma nova cotaction.",
                "data":json
            })
        return jsonify({"msg":"Insira uma chave 'name' ."})
    return jsonify({"msg":"Insira os dados da novo cotaction a ser cadastrada."})

# Read all
@cotacoes_bp.get("/listar")
def get_cotacoes():
    return jsonify({
        "method":"GET",
        "action":"Listar todas as cotacoes.",
        "data":lista
    })

# Read
@cotacoes_bp.get("/buscar")
def get_cotaction():
    data = request.get_json()

    if 'id' in data:
        for register in lista:
            if register['id'] == data['id']:
                return jsonify({
                    "method":"GET",
                    "action":f"Buscar a cotaction de ID {data['id']}.",
                    "data":register
                })
        return jsonify({"msg":"Insira um ID valido."})
    return jsonify({"msg":"Insira um ID."})

# Update
@cotacoes_bp.post("/atualizar")
def update_cotaction():
    data = request.get_json()
    if 'id' in data:
        if 'data' in data:
            for register in lista:
                if register['id'] == data['id']:
                    register['name'] = data['data']['name']
                    return jsonify({
                        "method":"POST",
                        "action":f"Atualizar a cotaction de ID {data['id']}.",
                        "data":data
                    })
        return jsonify({"msg":"Insira os dados."})
    return jsonify({"msg":"Insira um ID."})

# Remove
@cotacoes_bp.post("/remover")
def remove_cotaction():
    data = request.get_json()
    if 'id' in data:
        del lista[data['id'] - 1]
        return jsonify({
            "method":"POST",
            "action":f"Remover a cotaction de ID {data['id']}.",
        })
    return jsonify({"msg":"Insira um ID."})