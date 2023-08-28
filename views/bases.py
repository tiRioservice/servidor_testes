from flask import Blueprint, jsonify, request
from sqlalchemy import text
from modules.connection import engine
from modules.models import Base
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

bases_bp = Blueprint("bases", __name__, url_prefix="/bases")
Session = sessionmaker(bind=engine)

# Create ok
@bases_bp.post("/inserir")
@jwt_required()
def insert_base():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['base_nome','base_desc', 'end_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados da nova base a ser cadastrada."})
    else:
        with Session() as session:
            base = Base(**data)
            session.add(base)
            session.commit()

            return jsonify({
                "action":"Base inserida com sucesso!",
                "base_inserted":True,
                "new_base_id": base.base_id,
                "current_user":current_user
            })

# Read all ok
@bases_bp.get("/listar")
@jwt_required()
def get_bases():
    current_user = get_jwt_identity()
    base_list = []
    with Session() as session:
        result = session.query(Base).all()
        for row in result:
            base_composition = {
                "registro":row.registro,
                "base_id":row.base_id,
                "base_nome":row.base_nome,
                "base_desc":row.base_desc,
                "end_id":row.end_id
            }
            base_list.append(base_composition)

    if base_list == []:
        return jsonify({"msg":"Não há bases cadastradas."})

    return jsonify({
        "method":"GET",
        "action":"Listar todas as bases.",
        "data":base_list,
        "current_user":current_user
    })

# Read ok
@bases_bp.get("/buscar")
@jwt_required()
def get_base():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ["base_id"]

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados da base a ser buscada."})
    
    with Session() as session:
        base = session.query(Base).filter(Base.base_id == data['base_id']).first()

        base_composition = {
            "base_id":base.base_id,
            "base_name":base.base_nome,
            "base_desc":base.base_desc,
            "end_id":base.end_id
        }

        return jsonify({
            "method":"GET",
            "action":f"Buscar a base de ID {data['base_id']}.",
            "data":base_composition,
            "current_user":current_user
        })

# Update ok
@bases_bp.post("/atualizar")
@jwt_required()
def update_base():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['base_id']
    optional_fields = ['base_nome','base_desc', 'end_id']

    modified_fields = []
    
    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if field in data:
                    modified_fields.append(field)

    with Session() as session:
        session.query(Base).filter(Base.base_id == data['base_id']).update(data)
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Base atualizada com sucesso!",
            "modified_fields":modified_fields,
            "current_user":current_user
        })

# Remove ok
@bases_bp.post("/remover")
@jwt_required()
def remove_base():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['base_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados da base a ser removida."})
    
    with Session() as session:
        session.query(Base).filter(Base.base_id == data['base_id']).delete()
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Base removida com sucesso!",
            "current_user":current_user
        })