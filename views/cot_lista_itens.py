from flask import Blueprint, jsonify, request
from sqlalchemy import text
from modules.connection import engine
from modules.models import Lista_itens
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

cot_lista_itens_bp = Blueprint("cot_lista_itens", __name__, url_prefix="/cot_lista_itens")
Session = sessionmaker(bind=engine)

# Create ok
@cot_lista_itens_bp.post("/inserir")
@jwt_required()
def insert_lista_item():
    data = request.get_json()
    required_fields = ['cot_id', 'item_id', 'lista_itens_nome', 'lista_itens_qnt_necessaria', 'lista_itens_val_un', 'lista_itens_sub_total']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira os dados do novo item da lista a ser registrado."})
    
    with Session() as session:
        item = Lista_itens(**data)
        session.add(item)
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Item da lista inserido com sucesso!",
            "lista_itens_inserted":True,
            "new_lista_itens_id": item.lista_itens_id
        })
    
# Read all ok
@cot_lista_itens_bp.get("/listar")
@jwt_required()
def get_cot_itens_lista():
    current_user = get_jwt_identity()
    cot_lista_itens_list = []
    with Session() as session:
        result = session.query(Lista_itens).all()
        for row in result:
            cot_lista_itens_composition = {
                "cot_id":row.cot_id,
                "item_id":row.item_id,
                "lista_itens_nome":row.lista_itens_nome,
                "lista_itens_qnt_necessaria":row.lista_itens_qnt_necessaria,
                "lista_itens_val_un":row.lista_itens_val_un,
                "lista_itens_sub_total":row.lista_itens_sub_total
            }
            cot_lista_itens_list.append(cot_lista_itens_composition)
        return jsonify({
            "method":"GET",
            "action":"Lista de todas os itens pertecentes a listas de cotações recuperada com sucesso.",
            "cot_lista_itens_list":cot_lista_itens_list,
            "current_user":current_user
        })

# Read ok
@cot_lista_itens_bp.get("/buscar/<lista_itens_id>")
@jwt_required()
def get_item_list(lista_itens_id):
    current_user = get_jwt_identity()
    if lista_itens_id == None:
        return jsonify({"action":"Insira um ID de item de lista de cotaçao para iniciar a busca."})

    with Session() as session:
        result = session.query(Lista_itens).filter(Lista_itens.lista_itens_id == lista_itens_id).first()
        if result == None:
            return jsonify({"action":"Item de lista de cotação não encontrado."})
        else:
            lista_itens_composition = {
                "registro":result.registro,
                "cot_id":result.cot_id,
                "item_id":result.item_id,
                "lista_itens_nome":result.lista_itens_nome,
                "lista_itens_qnt_necessaria":result.lista_itens_qnt_necessaria,
                "lista_itens_val_un":result.lista_itens_val_un,
                "lista_itens_sub_total":result.lista_itens_sub_total
            }
            return jsonify({
                "method":"GET",
                "action":f"Cotação encontrada com sucesso!",
                "lista_itens_composition":lista_itens_composition,
                "current_user":current_user
            })

# Update ok
@cot_lista_itens_bp.post("/atualizar")
@jwt_required()
def update_cot_lista_itens():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['lista_itens_id']
    optional_fields = ['cot_id', 'item_id', 'lista_itens_nome', 'lista_itens_qnt_necessaria', 'lista_itens_val_un', 'lista_itens_sub_total']
    modified_fields = []

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if field in data:
                    modified_fields.append(field)

    with Session() as session:
        session.query(Lista_itens).filter(Lista_itens.lista_itens_id == data['lista_itens_id']).update(data)
        session.commit()
        return jsonify({
            "method":"POST",
            "action":"Item de cotação atualizado com sucesso!",
            "lista_item_updated":True,
            "lista_item_user":current_user
        })

# Remove
@cot_lista_itens_bp.post("/remover")
@jwt_required()
def remove_lista_itens():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['lista_itens_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira o ID do item a ser removido da cotação."})
    
    with Session() as session:
        session.query(Lista_itens).filter(Lista_itens.lista_itens_id == data['lista_itens_id']).delete()
        session.commit()
        return jsonify({
            "method":"POST",
            "action":"Item removido da cotação com sucesso!",
            "lista_item_removed":True,
            "current_user":current_user
        })