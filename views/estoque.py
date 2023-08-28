from flask import Blueprint, jsonify, request
from .estoque_categorias import categorias_bp
from .estoque_itens import itens_bp
from sqlalchemy import text
from modules.connection import engine
from modules.models import Estoque
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

estoque_bp = Blueprint("estoque", __name__, url_prefix="/estoque")
Session = sessionmaker(bind=engine)

# registro das Blueprints de Categorias e Itens
estoque_bp.register_blueprint(categorias_bp)
estoque_bp.register_blueprint(itens_bp)

# Create ok
@estoque_bp.post("/inserir")
@jwt_required()
def insert_estoque():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ["item_id", "base_id", "estoque_qnt", "estoque_min"]

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})

    if data == {}:
        return jsonify({"action":"Insira os dados do novo estoque a ser cadastrado."})
    
    with Session() as session:
        estoque = Estoque(**data)
        session.add(estoque)
        session.commit()

        return jsonify({
            "action":"Estoque inserido com sucesso!",
            "stock_inserted":True,
            "new_stock_id": estoque.estoque_id,
            "current_user":current_user
        })
    
# Read all ok
@estoque_bp.get("/listar")
@jwt_required()
def get_estoques():
    current_user = get_jwt_identity()
    estoque_list = []
    with Session() as session:
        result = session.query(Estoque).all()
        for row in result:
            estoque_composition = {
                "registro":row.registro,
                "estoque_id":row.estoque_id,
                "item_id":row.item_id,
                "base_id":row.base_id,
                "estoque_qnt":row.estoque_qnt,
                "estoque_min":row.estoque_min
            }
            estoque_list.append(estoque_composition)
        return jsonify({
            "method":"GET",
            "action":"Lista de todos os estoques",
            "estoque_list":estoque_list,
            "current_user":current_user
        })
    
# Read ok (GET)
@estoque_bp.get("/buscar/<estoque_id>")
@jwt_required()
def get_estoque(estoque_id):
    current_user = get_jwt_identity()
    if estoque_id == None:
        return jsonify({"action":"Insira um ID de estoque para realizer a busca."})
    
    with Session() as session:
        result = session.query(Estoque).filter(Estoque.estoque_id == estoque_id).first()
        if result is None:
            return jsonify({"action":f"Estoque {estoque_id} não encontrado."})
        else:
            estoque_composition = {
                "registro":result.registro,
                "estoque_id":result.estoque_id,
                "item_id":result.item_id,
                "base_id":result.base_id,
                "estoque_qnt":result.estoque_qnt,
                "estoque_min":result.estoque_min
            }
            return jsonify({
                "method":"GET",
                "action":f"Estoque encontrado com sucesso!",
                "estoque_composition":estoque_composition,
                "current_user":current_user
            })

# Update ok
@estoque_bp.post("/atualizar")
@jwt_required()
def update_estoque():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['estoque_id']
    optional_fields = ['estoque_qnt', 'estoque_min']

    modified_fields = []

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if not field in data:
                    modified_fields.append(field)
    
    with Session() as session:
        session.query(Estoque).filter(Estoque.estoque_id == data["estoque_id"]).update(data)
        session.commit()
        return jsonify({
            "action":f"Estoque atualizado com sucesso!",
            "estoque_updated":True,
            "modified_fields":modified_fields,
            "current_user":current_user
        })
    
# Remove ok
@estoque_bp.post("/remover")
@jwt_required()
def remove_estoque():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ["estoque_id"]

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira os dados do estoque a ser removido."})
    
    with Session() as session:
        session.query(Estoque).filter(Estoque.estoque_id == data["estoque_id"]).delete()
        session.commit()
        return jsonify({
            "action":"Estoque removido com sucesso!",
            "estoque_removed":True,
            "current_user":current_user
        })