# backend/app/routes.py
"""
Este arquivo define os endpoints da API para o gerenciamento de recursos.
Usamos os decorators de 'auth.py' para proteger cada rota apropriadamente.
"""

from flask import Blueprint, request, jsonify
from .models import db, Recurso
from .auth import token_required, roles_required

# Criamos outro Blueprint para as rotas principais da API.
api = Blueprint('api', __name__)

# --- ENDPOINTS PARA RECURSOS (CRUD) ---


@api.route('/api/recursos', methods=['GET'])
@token_required  # Qualquer usuário logado pode ver os recursos.
def get_all_recursos(current_user):
    """
    Endpoint: GET /api/recursos
    Proteção: Requer token de autenticação.
    Retorna uma lista de todos os recursos no inventário.
    O argumento 'current_user' é passado pelo decorator @token_required.
    """
    recursos_list = Recurso.query.all()
    output = []
    for recurso in recursos_list:
        recurso_data = {
            'id': recurso.id,
            'nome': recurso.nome,
            'tipo': recurso.tipo,
            'quantidade': recurso.quantidade,
            'status': recurso.status
        }
        output.append(recurso_data)
    return jsonify({'recursos': output})


@api.route('/api/recursos', methods=['POST'])
@token_required
# Apenas gerentes e admins podem criar.
@roles_required('gerente', 'admin_seguranca')
def create_recurso(current_user):
    """
    Endpoint: POST /api/recursos
    Proteção: Requer token e papel de 'gerente' ou 'admin_seguranca'.
    Cria um novo recurso com base nos dados JSON enviados.
    """
    data = request.get_json()

    # Validação simples dos dados recebidos.
    if not data or not data.get('nome') or not data.get('tipo'):
        return jsonify({'message': 'Dados incompletos para criar o recurso.'}), 400

    novo_recurso = Recurso(
        nome=data['nome'],
        tipo=data['tipo'],
        # Usa 1 como padrão se não for fornecido.
        quantidade=data.get('quantidade', 1),
        # Usa 'disponivel' como padrão.
        status=data.get('status', 'disponivel')
    )
    db.session.add(novo_recurso)
    db.session.commit()

    # 201 Created
    return jsonify({'message': 'Recurso criado com sucesso!'}), 201


@api.route('/api/recursos/<int:recurso_id>', methods=['PUT'])
@token_required
# Apenas gerentes e admins podem editar.
@roles_required('gerente', 'admin_seguranca')
def update_recurso(current_user, recurso_id):
    """
    Endpoint: PUT /api/recursos/<id>
    Proteção: Requer token e papel de 'gerente' ou 'admin_seguranca'.
    Atualiza um recurso existente.
    """
    # .get_or_404() é um atalho útil do SQLAlchemy: tenta encontrar o recurso,
    # se não encontrar, retorna um erro 404 Not Found automaticamente.
    recurso = Recurso.query.get_or_404(recurso_id)
    data = request.get_json()

    # Atualiza os campos do objeto com os novos dados,
    # mantendo os antigos se nenhum dado novo for fornecido.
    recurso.nome = data.get('nome', recurso.nome)
    recurso.tipo = data.get('tipo', recurso.tipo)
    recurso.quantidade = data.get('quantidade', recurso.quantidade)
    recurso.status = data.get('status', recurso.status)

    db.session.commit()
    return jsonify({'message': 'Recurso atualizado com sucesso!'})


@api.route('/api/recursos/<int:recurso_id>', methods=['DELETE'])
@token_required
# Apenas administradores de segurança podem deletar.
@roles_required('admin_seguranca')
def delete_recurso(current_user, recurso_id):
    """
    Endpoint: DELETE /api/recursos/<id>
    Proteção: Requer token e papel de 'admin_seguranca'.
    Remove um recurso do banco de dados.
    """
    recurso = Recurso.query.get_or_404(recurso_id)
    db.session.delete(recurso)
    db.session.commit()
    return jsonify({'message': 'Recurso deletado com sucesso!'})


# --- ENDPOINT PARA O DASHBOARD ---

@api.route('/api/dashboard', methods=['GET'])
@token_required  # Qualquer usuário logado pode ver o dashboard.
def get_dashboard_data(current_user):
    """
    Endpoint: GET /api/dashboard
    Proteção: Requer token de autenticação.
    Retorna dados agregados para os gráficos do painel de controle.
    """
    # Consultas para agregar os dados:
    total_recursos = db.session.query(
        db.func.sum(Recurso.quantidade)).scalar() or 0
    recursos_por_tipo = db.session.query(
        Recurso.tipo, db.func.count(Recurso.id)).group_by(Recurso.tipo).all()
    recursos_por_status = db.session.query(
        Recurso.status, db.func.count(Recurso.id)).group_by(Recurso.status).all()

    # Formata os dados para serem facilmente consumidos pelo Chart.js no frontend.
    dashboard_data = {
        'total_recursos': total_recursos,
        'recursos_por_tipo': {tipo: count for tipo, count in recursos_por_tipo},
        'recursos_por_status': {status: count for status, count in recursos_por_status}
    }
    return jsonify(dashboard_data)
