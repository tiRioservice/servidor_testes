from flask import Blueprint, jsonify, request
from modules.connection import engine
from modules.models import Lista_forn
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import get_jwt_identity, jwt_required

cot_lista_forn_bp = Blueprint("cot_lista_forn", __name__, url_prefix="/cot_lista_forn")
Session = sessionmaker(bind=engine)

# Create ok
@cot_lista_forn_bp.post("/inserir")
@jwt_required()
def insert_cot_lista_forn():
    data = request.get_json()
    required_fields = ['cot_id', 'forn_id', 'lista_forn_prazo_pag', 'lista_forn_prazo_entrega']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira os dados do fornecedor da cotação a ser cadastrada."})
    
    with Session() as session:
        lista_forn = Lista_forn(**data)
        session.add(lista_forn)
        session.commit()

        return jsonify({
            "method":"POST",
            "action":"Fornecedor da cotação inserido com sucesso!",
            "lista_forn_inserted":True,
            "new_lista_forn_id": lista_forn.lista_forn_id
        })
    
# Read all ok
@cot_lista_forn_bp.get("/listar")
@jwt_required()
def get_all_cot_forn():
    current_user = get_jwt_identity()
    cot_forn_list = []
    with Session() as session:
        result = session.query(Lista_forn).all()
        for row in result:
            cot_forn_composition = {
                "registro":row.registro,
                "lista_forn_id":row.lista_forn_id,
                "cot_id":row.cot_id,
                "forn_id":row.forn_id,
                "lista_forn_prazo_pag":row.lista_forn_prazo_pag,
                "lista_forn_prazo_entrega":row.lista_forn_prazo_entrega
            }
            cot_forn_list.append(cot_forn_composition)
        return jsonify({
            "method":"GET",
            "action":"Lista de todos fornecedores que estao registrados em cotação encontrada com sucesso!",
            "cot_forn_list":cot_forn_list,
            "current_user":current_user
        })

# Read ok
@cot_lista_forn_bp.get("/buscar/<lista_forn_id>")
@jwt_required()
def get_cot_forn(lista_forn_id):
    current_user = get_jwt_identity()
    if lista_forn_id == None:
        return jsonify({"action":"Insira um ID de cotação para iniciar a busca."})

    with Session() as session:
        result = session.query(Lista_forn).filter(Lista_forn.lista_forn_id == lista_forn_id).first()
        if result == None:
            return jsonify({"action":"Fornecedor-cotação não encontrado."})
        else:
            lista_forn_composition = {
                "registro":result.registro,
                "lista_forn_id":result.lista_forn_id,
                "cot_id":result.cot_id,
                "forn_id":result.forn_id,
                "lista_forn_prazo_pag":result.lista_forn_prazo_pag,
                "lista_forn_prazo_entrega":result.lista_forn_prazo_entrega
            }
            return jsonify({
                "method":"GET",
                "action":"Fornecedor-cotação encontrado com sucesso!",
                "lista_forn_composition":lista_forn_composition,
                "current_user":current_user
            })

# Update ok
@cot_lista_forn_bp.post("/atualizar")
@jwt_required()
def update_cot_forn():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['lista_forn_id']
    optional_fields = ['cot_id', 'forn_id', 'lista_forn_prazo_pag', 'lista_forn_prazo_entrega']
    modified_fields = []

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        else:
            for field in optional_fields:
                if field in data:
                    modified_fields.append(field)

    with Session() as session:
        session.query(Lista_forn).filter(Lista_forn.lista_forn_id == data['lista_forn_id']).update(data)
        session.commit()
        return jsonify({
            "method":"POST",
            "action":"Fornecedor-cotação atualizado com sucesso!",
            "lista_forn_updated":True,
            "current_user":current_user
        })

# Remove
@cot_lista_forn_bp.post("/remover")
@jwt_required()
def remove_cot_forn():
    current_user = get_jwt_identity()
    data = request.get_json()
    required_fields = ['lista_forn_id']

    for field in required_fields:
        if not field in data:
            return jsonify({"action":f"Insira uma chave '{field}' e atribua um valor."})
        
    if data == {}:
        return jsonify({"action":"Insira o ID do Fornecedor-cotação a ser removido."})
    
    with Session() as session:
        session.query(Lista_forn).filter(Lista_forn.lista_forn_id == data['lista_forn_id']).delete()
        session.commit()
        return jsonify({
            "method":"POST",
            "action":"Fornecedor-cotação removida com sucesso!",
            "lista_forn_removed":True,
            "current_user":current_user
        })