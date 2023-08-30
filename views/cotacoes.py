from flask import Blueprint, jsonify, request
from sqlalchemy import text
from modules.connection import engine
from modules.models import Cotacao
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

cotacoes_bp = Blueprint("cotacoes", __name__, url_prefix="/cotacoes")
Session = sessionmaker(bind=engine)

# Create ok
@cotacoes_bp.post("/inserir")
@jwt_required()
def insert_cotaction():
    data = request.get_json()
    required_fields = ['colab_id', 'cot_valid', 'cot_status', 'cot_val_total']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira os dados da nova cotacao a ser cadastrada."})
    
    with Session() as session:
        cotacao = Cotacao(**data)
        session.add(cotacao)
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Cotacao inserida com sucesso!",
            "cotacao_inserted":True,
            "new_cotacao_id": cotacao.cot_id
        })
    
# Read all ok
@cotacoes_bp.get("/listar")
@jwt_required()
def get_cotacoes():
    current_user = get_jwt_identity()
    cotacao_list = []
    with Session() as session:
        result = session.query(Cotacao).all()
        for row in result:
            cotacao_composition = {
                "cot_id":row.cot_id,
                "colab_id":row.colab_id,
                "cot_valid":row.cot_valid,
                "cot_status":row.cot_status,
                "cot_val_total":row.cot_val_total
            }
            cotacao_list.append(cotacao_composition)
        return jsonify({
            "method":"GET",
            "action":"Lista de todas as cotacoes",
            "data":cotacao_list,
            "current_user":current_user
        })

# Read ok
@cotacoes_bp.get("/buscar/<cot_id>")
@jwt_required()
def get_cotaction(cot_id):
    current_user = get_jwt_identity()
    if cot_id == None:
        return jsonify({"msg":"Insira um ID de cotação para iniciar a busca."})

    with Session() as session:
        result = session.query(Cotacao).filter(Cotacao.cot_id == cot_id).first()
        if result == None:
            return jsonify({"msg":"Cotação não encontrada."})
        else:
            cotacao_composition = {
                "registro":result.registro,
                "cot_id":result.cot_id,
                "colab_id":result.colab_id,
                "cot_valid":result.cot_valid,
                "cot_status":result.cot_status,
                "cot_val_total":result.cot_val_total
            }
            return jsonify({
                "method":"GET",
                "action":f"Cotação encontrada com sucesso!",
                "data":cotacao_composition,
                "current_user":current_user
            })

# Update ok
@cotacoes_bp.post("/atualizar")
@jwt_required()
def update_cotaction():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['cot_id']
    optional_fields = ['cot_valid','cot_status','cot_val_total']
    modified_fields = []

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if field in data:
                    modified_fields.append(field)

    with Session() as session:
        session.query(Cotacao).filter(Cotacao.cot_id == data['cot_id']).update(data)
        session.commit()
        return jsonify({
            "method":"POST",
            "action":"Cotação atualizada com sucesso!",
            "cotacao_updated":True,
            "current_user":current_user
        })

# Remove
@cotacoes_bp.post("/remover")
@jwt_required()
def remove_cotaction():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['cot_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"msg":"Insira o ID da cotação a ser removida."})
    
    with Session() as session:
        session.query(Cotacao).filter(Cotacao.cot_id == data['cot_id']).delete()
        session.commit()
        return jsonify({
            "method":"POST",
            "action":"Cotação removida com sucesso!",
            "cotacao_removed":True,
            "current_user":current_user
        })