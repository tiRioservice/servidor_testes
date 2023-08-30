from flask import Blueprint, jsonify, request
from sqlalchemy import text
from modules.connection import engine
from modules.models import Rel_item_forn
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

rel_item_forn_bp = Blueprint("rel_item_forn", __name__, url_prefix="/rel_item_forn")
Session = sessionmaker(bind=engine)

# Create ok
@rel_item_forn_bp.post("/inserir")
@jwt_required()
def insert_rel_item_forn():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['item_id', 'forn_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira os dados da nova relação item-fornecedor a ser cadastrada."})
    
    with Session() as session:
        rel_item_forn = Rel_item_forn(**data)
        session.add(rel_item_forn)
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Relação item-fornecedor inserida com sucesso!",
            "rel_item_forn_inserted":True,
            "new_rel_item_forn_id": rel_item_forn.rel_item_forn_id,
            "current_user":current_user
        })
    
# Read all ok
@rel_item_forn_bp.get("/listar")
@jwt_required()
def get_all_rel_item_forn():
    current_user = get_jwt_identity()
    rel_item_forn_list = []
    with Session() as session:
        result = session.query(Rel_item_forn).all()
        for row in result:
            rel_item_forn_composition = {
                "registro":row.registro,
                "rel_item_forn_id":row.rel_item_forn_id,
                "item_id":row.item_id,
                "forn_id":row.forn_id
            }

            rel_item_forn_list.append(rel_item_forn_composition)

        return jsonify({
            "method":"GET",
            "action":"Lista de todas as relações item-fornecedor",
            "rel_item_forn_list":rel_item_forn_list,
            "current_user":current_user
        })

# Read ok
@rel_item_forn_bp.get("/buscar/<rel_item_forn_id>")
@jwt_required()
def get_rel_item_forn(rel_item_forn_id):
    current_user = get_jwt_identity()
    if rel_item_forn_id == None:
        return jsonify({"action":"Insira um ID de relação item-fornecedor para iniciar a busca."})

    with Session() as session:
        result = session.query(Rel_item_forn).filter(Rel_item_forn.rel_item_forn_id == rel_item_forn_id).first()
        if result == None:
            return jsonify({"action":"Relação item-fornecedor não encontrada."})
        else:
            rel_item_forn_composition = {
                "registro":result.registro,
                "rel_item_forn_id":result.rel_item_forn_id,
                "item_id":result.item_id,
                "forn_id":result.forn_id
            }
            return jsonify({
                "method":"GET",
                "action":"Relação item-fornecedor encontrada com sucesso!",
                "rel_item_forn_composition":rel_item_forn_composition,
                "current_user":current_user
            })

# Update ok
@rel_item_forn_bp.post("/atualizar")
@jwt_required()
def update_rel_item_forn():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['rel_item_forn_id']
    optional_fields = ['item_id', 'forn_id']
    modified_fields = []

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if field in data:
                    modified_fields.append(field)

    with Session() as session:
        session.query(Rel_item_forn).filter(Rel_item_forn.rel_item_forn_id == data['rel_item_forn_id']).update(data)
        session.commit()
        return jsonify({
            "method":"POST",
            "action":"Relação item-fornecedor atualizada com sucesso!",
            "rel_item_forn_updated":True,
            "current_user":current_user
        })

# Remove ok
@rel_item_forn_bp.post("/remover")
@jwt_required()
def remove_rel_item_forn():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['rel_item_forn_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira o ID da relação item-fornecedor a ser removida."})
    
    with Session() as session:
        session.query(Rel_item_forn).filter(Rel_item_forn.rel_item_forn_id == data['rel_item_forn_id']).delete()
        session.commit()
        return jsonify({
            "method":"POST",
            "action":"Relação item-fornecedor removida com sucesso!",
            "cotacao_removed":True,
            "current_user":current_user
        })