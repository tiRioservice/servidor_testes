from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import text
from modules.connection import engine
from modules.models import Cargo_config
from sqlalchemy.orm import sessionmaker

cargo_config_bp = Blueprint("cargo_config", __name__, url_prefix="/cargo_config")
Session = sessionmaker(bind=engine)

# Create ok
@cargo_config_bp.post("/inserir")
@jwt_required()
def insert_cargo_config():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['cargo_id', 'perm_id', 'nvl_acesso']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados do novo nivel de acesso de cargo a ser cadastrado."})
    
    with Session() as session:
        cargo_config = Cargo_config(**data)
        session.add(cargo_config)
        session.commit()

        return jsonify({
            "action":"Nivel de acesso de cargo inserido com sucesso!",
            "cargo_config_inserted":True,
            "new_cargo_config_id": cargo_config.cargo_config_id,
            "current_user":current_user
        })

# Read all ok
@cargo_config_bp.post("/listar")
@jwt_required()
def cargo_config():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['cargo_id']
    cargo_config_list = []

    with Session() as session:
        result = session.query(Cargo_config).filter_by(cargo_id=data['cargo_id']).all()
        for row in result:
            cargo_config_composition = {
                "registro":row.registro,
                "cargo_config_id":row.cargo_config_id,
                "cargo_id":row.cargo_id,
                "perm_id":row.perm_id,
                "nvl_acesso":row.nvl_acesso
            }
            cargo_config_list.append(cargo_config_composition)

    if cargo_config_list == []:
        return jsonify({"msg":"Não há niveis de acesso de cargo cadastrados."})
    
    return jsonify({
        "method":"GET",
        "action":"Listar todos os niveis de acesso de cargo.",
        "data":cargo_config_list,
        "current_user":current_user
    })

# Read ok
@cargo_config_bp.post("/buscar")
@jwt_required()
def get_cargo_acesso():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not 'cargo_id' in data:
        return jsonify({"msg":"Insira a chave 'cargo_config_id' e atribua um valor."})
    
    with Session() as session:
        result = session.query(Cargo_config).filter_by(cargo_id=data['cargo_id']).first()
        cargo_config_composition = {
            "registro":result.registro,
            "cargo_config_id":result.cargo_config_id,
            "cargo_id":result.cargo_id,
            "perm_id":result.perm_id,
            "nvl_acesso":result.nvl_acesso
        }

        return jsonify({
            "method":"GET",
            "action":f"Buscar o nivel de acesso de cargo de ID {data['cargo_id']}.",
            "data":cargo_config_composition,
            "current_user":current_user
        })

# Update
@cargo_config_bp.post("/atualizar")
@jwt_required()
def update_cargo_acesso():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['cargo_config_id', 'cargo_id', 'perm_id', 'nvl_acesso']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})

    if data == {}:
        return jsonify({"msg":"Insira os dados do nivel de acesso de cargo a ser atualizado."})
    
    with Session() as session:
        session.query(Cargo_config).filter(Cargo_config.cargo_config_id == data['cargo_config_id']).update(data)
        session.commit()

        return jsonify({
            "method":"POST",
            "action":f"Configurações do cargo atualizado com sucesso!",
            "current_user":current_user
        })

# Remove
@cargo_config_bp.post("/remover")
@jwt_required()
def remove_cargo_acesso():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['cargo_config_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    with Session() as session:
        session.query(Cargo_config).filter(Cargo_config.cargo_config_id == data['cargo_config_id']).delete()
        session.commit()

        return jsonify({
            "method":"POST",
            "action":f"Configurações do cargo removido com sucesso!",
            "current_user":current_user
        })