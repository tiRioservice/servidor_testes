from flask import Blueprint, jsonify, request
from sqlalchemy import text
from modules.connection import engine
from modules.models import Permissao
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

permissoes_bp = Blueprint("permissoes", __name__, url_prefix="/permissoes")
Session = sessionmaker(bind=engine)

# Create ok
@permissoes_bp.post("/inserir")
@jwt_required()
def insert_permissao():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['perm_cod','perm_nome', 'perm_desc']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados da nova permissao a ser cadastrada."})
    else:
        with Session() as session:
            permissao = Permissao(**data)
            session.add(permissao)
            session.commit()

            return jsonify({
                "msg":"Permissao inserida com sucesso!",
                "permissao_inserted":True,
                "new_perm_id": permissao.perm_id,
                "current_user":current_user
            })

# Read all ok
@permissoes_bp.get("/listar")
@jwt_required()
def get_permissoes():
    current_user = get_jwt_identity()
    permissao_list = []
    with Session() as session:
        result = session.query(Permissao).all()
        for row in result:
            permissao_composition = {
                "registro":row.registro,
                "permissao_id":row.perm_id,
                "permissao_cod":row.perm_cod,
                "permissao_nome":row.perm_nome,
                "permissao_desc":row.perm_desc
            }
            permissao_list.append(permissao_composition)

    if permissao_list == []:
        return jsonify({"msg":"Não há permissoes cadastradas."})

    return jsonify({
        "method":"GET",
        "action":"Listar todas as permissoes.",
        "data":permissao_list,
        "current_user":current_user
    })

# Read ok
@permissoes_bp.post("/buscar")
@jwt_required()
def get_permissao():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ["perm_id"]

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados da permissao a ser buscada."})
    
    with Session() as session:
        permissao = session.query(Permissao).filter(Permissao.perm_id == data['perm_id']).first()

        permissao_composition = {
            "perm_id":permissao.perm_id,
            "perm_cod":permissao.perm_cod,
            "perm_nome":permissao.perm_nome,
            "perm_desc":permissao.perm_desc
        }

        return jsonify({
            "method":"GET",
            "action":f"Buscar a permissao de ID {data['perm_id']}.",
            "data":permissao_composition,
            "current_user":current_user
        })

# Update ok
@permissoes_bp.post("/atualizar")
@jwt_required()
def update_permissao():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['perm_id']
    optional_fields = ['perm_cod', 'perm_nome','perm_desc']

    modified_fields = []
    
    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if field in data:
                    modified_fields.append(field)

    with Session() as session:
        session.query(Permissao).filter(Permissao.perm_id == data['perm_id']).update(data)
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Permissao atualizada com sucesso!",
            "modified_fields":modified_fields,
            "current_user":current_user
        })

# Remove ok
@permissoes_bp.post("/remover")
@jwt_required()
def remove_permissao():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['perm_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados da permissao a ser removida."})
    
    with Session() as session:
        session.query(Permissao).filter(Permissao.perm_id == data['perm_id']).delete()
        session.commit()

        return jsonify({
            "method":"POST",
            "action":f"Remover a permissao de ID {data['perm_id']}.",
            "current_user":current_user,
            "msg":"Permissao removida com sucesso!"
        })