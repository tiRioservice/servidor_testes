from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import text
from modules.connection import engine
from modules.models import Cargo
from sqlalchemy.orm import sessionmaker

cargos_bp = Blueprint("cargos", __name__, url_prefix="/cargos")
Session = sessionmaker(bind=engine)

# Create ok
@cargos_bp.post("/inserir")
@jwt_required()
def insert_cargo():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['cargo_nome', 'cargo_desc']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados do novo cargo a ser cadastrado."})
    
    with Session() as session:
        cargo = Cargo(**data)
        session.add(cargo)
        session.commit()

        return jsonify({
            "action":"Cargo inserido com sucesso!",
            "cargo_inserted":True,
            "new_cargo_id": cargo.cargo_id,
            "current_user":current_user
        })

# Read all ok
@cargos_bp.get("/listar")
@jwt_required()
def get_cargos():
    current_user = get_jwt_identity()
    cargo_list = []

    with Session() as session:
        result = session.query(Cargo).all()
        for row in result:
            cargo_composition = {
                "registro":row.registro,
                "cargo_id":row.cargo_id,
                "cargo_nome":row.cargo_nome,
                "cargo_desc":row.cargo_desc
            }
            cargo_list.append(cargo_composition)

    if cargo_list == []:
        return jsonify({"msg":"Não há cargos cadastrados."})
    
    return jsonify({
        "method":"GET",
        "action":"Listar todos os cargos.",
        "data":cargo_list,
        "current_user":current_user
    })

# Read ok
@cargos_bp.post("/buscar")
@jwt_required()
def get_cargo():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not 'cargo_id' in data:
        return jsonify({"msg":"Insira a chave 'cargo_id' e atribua um valor."})
    
    with Session() as session:
        result = session.query(Cargo).filter(Cargo.cargo_id == data['cargo_id']).first()
        
        cargo_composition = {
            "cargo_id":result.cargo_id,
            "cargo_nome":result.cargo_nome,
            "cargo_desc":result.cargo_desc
        }

        return jsonify({
            "method":"POST",
            "action":f"Dados do cargo obtidos.",
            "data":cargo_composition,
            "current_user":current_user
        })

# Update ok
@cargos_bp.post("/atualizar")
@jwt_required()
def update_cargo():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['cargo_id','cargo_nome','cargo_desc']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados do novo cargo a ser cadastrado."})
    
    with Session() as session:
        session.query(Cargo).filter(Cargo.cargo_id == data['cargo_id']).update(data)
        session.commit()
    
        return jsonify({
            "method":"POST",
            "action":f"Cargo atualizado com sucesso!",
            "current_user":current_user
        })

# Remove ok
@cargos_bp.post("/remover")
@jwt_required()
def remove_cargo():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['cargo_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados do cargo a ser removido."})

    with Session() as session:
        session.query(Cargo).filter(Cargo.cargo_id == data['cargo_id']).delete()
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Cargo removido com sucesso!",
            "current_user":current_user
        })