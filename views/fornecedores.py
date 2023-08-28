from flask import Blueprint, jsonify, request
from sqlalchemy import text
from modules.connection import engine
from modules.models import Fornecedor
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

fornecedores_bp = Blueprint("fornecedores", __name__, url_prefix="/fornecedores")
Session = sessionmaker(bind=engine)

# Create ok
@fornecedores_bp.post("/inserir")
@jwt_required()
def insert_fornecedor():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['forn_cnpj', 'forn_nome_fantasia', 'forn_insc_estadual', 'forn_insc_municipal']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}: 
        return jsonify({"action":"Insira os dados do novo fornecedor a ser cadastrado."})
    
    with Session() as session:
        fornecedor = Fornecedor(**data)
        session.add(fornecedor)
        session.commit()

        return jsonify({
            "action":"Fornecedor inserido com sucesso!",
            "forn_inserted":True,
            "new_forn_id": fornecedor.forn_id,
            "current_user":current_user
        })

# Read all ok
@fornecedores_bp.get("/listar")
@jwt_required()
def get_fornecedores():
    current_user = get_jwt_identity()
    fornecedor_list = []
    with Session() as session:
        result = session.query(Fornecedor).all()
        for row in result:
            fornecedor_composition = {
                "registro":row.registro,
                "forn_id":row.forn_id,
                "forn_cnpj":row.forn_cnpj,
                "forn_razao_social":row.forn_razao_social,
                "forn_nome_fantasia":row.forn_nome_fantasia,
                "forn_tel_cod":row.forn_tel_cod,
                "forn_tel_num":row.forn_tel_num,
                "forn_insc_estadual":row.forn_insc_estadual,
                "forn_insc_municipal":row.forn_insc_municipal,
                "forn_email":row.forn_email,
                "forn_nome_contato":row.forn_nome_contato,
                "forn_banco":row.forn_banco,
                "forn_titular":row.forn_titular,
                "forn_cnpj_cpf_titular":row.forn_cnpj_cpf_titular,
                "forn_agencia":row.forn_agencia,
                "forn_conta":row.forn_conta,
                "forn_tp_operacao":row.forn_tp_operacao,
                "forn_pix":row.forn_pix,
                "end_id":row.end_id
            }
            fornecedor_list.append(fornecedor_composition)
    
    if fornecedor_list == []:
        return jsonify({"msg":"Não há fornecedores cadastrados."})
    
    return jsonify({
        "method":"GET",
        "action":"Listar todos os fornecedores.",
        "data":fornecedor_list,
        "current_user":current_user
    })

# # Read ok
@fornecedores_bp.post("/buscar")
@jwt_required()
def get_fornecedor():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['forn_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
    
    if data == {}:
        return jsonify({"msg":"Insira os dados do fornecedor a ser buscado."})
    
    with Session() as session:
        fornecedor = session.query(Fornecedor).filter(Fornecedor.forn_id == data['forn_id']).first()

        fornecedor_composition = {
            "registro":fornecedor.registro,
            "forn_id":fornecedor.forn_id,
            "forn_cnpj":fornecedor.forn_cnpj,
            "forn_razao_social":fornecedor.forn_razao_social,
            "forn_nome_fantasia":fornecedor.forn_nome_fantasia,
            "forn_tel_cod":fornecedor.forn_tel_cod,
            "forn_tel_num":fornecedor.forn_tel_num,
            "forn_insc_estadual":fornecedor.forn_insc_estadual,
            "forn_insc_municipal":fornecedor.forn_insc_municipal,
            "forn_email":fornecedor.forn_email,
            "forn_nome_contato":fornecedor.forn_nome_contato,
            "forn_banco":fornecedor.forn_banco,
            "forn_titular":fornecedor.forn_titular,
            "forn_cnpj_cpf_titular":fornecedor.forn_cnpj_cpf_titular,
            "forn_agencia":fornecedor.forn_agencia,
            "forn_conta":fornecedor.forn_conta,
            "forn_tp_operacao":fornecedor.forn_tp_operacao,
            "forn_pix":fornecedor.forn_pix,
            "end_id":fornecedor.end_id
        }

        return jsonify({
            "method":"POST",
            "action":"Fornecedor encontrado com sucesso!",
            "data":fornecedor_composition,
            "current_user":current_user
        })

# # Update ok
@fornecedores_bp.post("/atualizar")
@jwt_required()
def update_fornecedor():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['forn_id']
    optional_fields = ['forn_cnpj', 'forn_razao_social', 'forn_nome_fantasia', 'forn_tel_cod', 'forn_tel_num', 'forn_insc_estadual', 'forn_insc_municipal', 'forn_email', 'forn_nome_contato', 'forn_banco', 'forn_titular', 'forn_cnpj_cpf_titular', 'forn_agencia', 'forn_conta', 'forn_tp_operacao', 'forn_pix', 'end_id']

    modified_fields = []

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if field in data:
                    modified_fields.append(field)

    with Session() as session:
        session.query(Fornecedor).filter(Fornecedor.forn_id == data['forn_id']).update(data)
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Fornecedor atualizado com sucesso!",
            "modified_fields":modified_fields,
            "current_user":current_user
        })

# # Remove ok
@fornecedores_bp.post("/remover")
@jwt_required()
def remove_fornecedor():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['forn_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"msg":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"msg":"Insira os dados do fornecedor a ser removido."})
    
    with Session() as session:
        session.query(Fornecedor).filter(Fornecedor.forn_id == data['forn_id']).delete()
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Fornecedor removido com sucesso!",
            "current_user":current_user
        })