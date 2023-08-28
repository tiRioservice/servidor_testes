from flask import Blueprint, jsonify, request
from sqlalchemy import text
from modules.connection import engine
from modules.models import Categoria
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

categorias_bp = Blueprint("categorias", __name__, url_prefix="/categorias")
Session = sessionmaker(bind=engine)

# Create ok
@categorias_bp.post("/inserir")
@jwt_required()
def insert_categoria():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['categ_nome', 'categ_desc']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira os dados da nova categoria a ser cadastrada."})
    
    with Session() as session:
        categoria = Categoria(**data)
        session.add(categoria)
        session.commit()

        return jsonify({
            "action":"Categoria inserida com sucesso!",
            "categ_inserted":True,
            "new_categ_id": categoria.categ_id,
            "current_user":current_user
        })

# Read all ok
@categorias_bp.get("/listar")
@jwt_required()
def get_categorias():
    current_user = get_jwt_identity()
    categoria_list = []
    with Session() as session:
        result = session.query(Categoria).all()
        for row in result:
            categoria_composition = {
                "registro":row.registro,
                "categ_id":row.categ_id,
                "categ_nome":row.categ_nome,
                "categ_desc":row.categ_desc
            }
            categoria_list.append(categoria_composition)
        return jsonify({
            "method":"GET",
            "action":"Lista de todas as categorias",
            "categ_list":categoria_list,
            "current_user":current_user
        })

# Read ok (GET)
@categorias_bp.get("/buscar/<categ_id>")
@jwt_required()
def get_categoria(categ_id):
    current_user = get_jwt_identity()
    if categ_id == None:
        return jsonify({"action":"Insira um ID de categoria para realizar a busca."})
    
    with Session() as session:
        result = session.query(Categoria).filter(Categoria.categ_id == categ_id).first()
        if result == None:
            return jsonify({"action":"Categoria não encontrada."})
        else:
            categoria_composition = {
                "registro":result.registro,
                "categ_id":result.categ_id,
                "categ_nome":result.categ_nome,
                "categ_desc":result.categ_desc
            }
            return jsonify({
                "action":"Categoria encontrada com sucesso!",
                "categ_found":True,
                "categ_data":categoria_composition,
                "current_user":current_user
            })

# Update ok
@categorias_bp.post("/atualizar")
@jwt_required()
def update_categoria():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['categ_id']
    optional_fields = ['categ_nome', 'categ_desc']

    modified_fields = []

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if field in data:
                    modified_fields.append(field)
    
    with Session() as session:
        session.query(Categoria).filter(Categoria.categ_id == data['categ_id']).update(data)
        session.commit()
        return jsonify({
            "action":"Categoria atualizada com sucesso!",
            "categ_updated":True,
            "modified_fields":modified_fields,
            "current_user":current_user
        })

# Remove ok
@categorias_bp.post("/remover")
@jwt_required()
def remove_categoria():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['categ_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})

    if data == {}:
        return jsonify({"action":"Insira os dados da categoria a ser removida."})    
    
    with Session() as session:
        session.query(Categoria).filter(Categoria.categ_id == data['categ_id']).delete()
        session.commit()
        return jsonify({
            "action":"Categoria removida com sucesso!",
            "categ_removed":True,
            "current_user":current_user
        })