from flask import Blueprint, jsonify, request
from sqlalchemy import text
from modules.connection import engine
from modules.models import Item
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

itens_bp = Blueprint("itens", __name__, url_prefix="/itens")
Session = sessionmaker(bind=engine)

# Create ok
@itens_bp.post("/inserir")
@jwt_required()
def insert_item():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['categ_id', 'item_nome', 'item_tamanho', 'item_preco']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira os dados do novo item a ser cadastrado."})
    
    with Session() as session:
        item = Item(**data)
        session.add(item)
        session.commit()

        return jsonify({
            "action":"Item inserido com sucesso!",
            "item_inserted":True,
            "new_item_id": item.item_id,
            "current_user":current_user
        })

# Read all ok
@itens_bp.get("/listar")
@jwt_required()
def get_itens():
    current_user = get_jwt_identity()
    item_list = []
    with Session() as session:
        result = session.query(Item).all()
        for row in result:
            item_composition = {
                "registro":row.registro,
                "item_id":row.item_id,
                "categ_id":row.categ_id,
                "item_nome":row.item_nome,
                "item_tamanho":row.item_tamanho,
                "item_preco":row.item_preco,
                "item_qualidade":row.item_qualidade,
                "item_desc":row.item_desc
            }
            item_list.append(item_composition)
        return jsonify({
            "method":"GET",
            "action":"Lista de todos os itens",
            "item_list":item_list,
            "current_user":current_user
        })

# Read ok (GET)
@itens_bp.get("/buscar/<item_id>")
@jwt_required()
def get_item(item_id):
    current_user = get_jwt_identity()
    if item_id == None:
        return jsonify({"action":"Insira um ID de item para realizar a busca."})
    
    with Session() as session:
        result = session.query(Item).filter(Item.item_id == item_id).first()
        if result == None:
            return jsonify({"action":"Item não encontrado."})
        else:
            item_composition = {
                "registro":result.registro,
                "item_id":result.item_id,
                "categ_id":result.categ_id,
                "item_nome":result.item_nome,
                "item_tamanho":result.item_tamanho,
                "item_preco":result.item_preco,
                "item_qualidade":result.item_qualidade,
                "item_desc":result.item_desc
            }
            return jsonify({
                "method":"GET",
                "action":"Item encontrado com sucesso!",
                "item":item_composition,
                "current_user":current_user
            })

# Update ok
@itens_bp.post("/atualizar")
@jwt_required()
def update_item():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['item_id']
    optional_fields = ['categ_id', 'item_nome', 'item_tamanho', 'item_preco', 'item_qualidade', 'item_desc']

    modified_fields = []

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if field in data:
                    modified_fields.append(field)
    
    with Session() as session:
        session.query(Item).filter(Item.item_id == data['item_id']).update(data)
        session.commit()
        return jsonify({
            "action":"Item atualizado com sucesso!",
            "item_updated":True,
            "modified_fields":modified_fields,
            "current_user":current_user
        })

# Remove ok
@itens_bp.post("/remover")
@jwt_required()
def remove_item():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['item_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira os dados do item a ser removido."})
    
    with Session() as session:
        session.query(Item).filter(Item.item_id == data['item_id']).delete()
        session.commit()
        return jsonify({
            "action":"Item removido com sucesso!",
            "item_removed":True,
            "current_user":current_user
        })