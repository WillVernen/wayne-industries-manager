# backend/app/auth.py
"""
Este módulo gerencia a autenticação e autorização.
- Autenticação: Verifica se o usuário é quem ele diz ser (login).
- Autorização: Verifica se o usuário autenticado tem permissão para acessar um recurso.
"""

import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app, Blueprint
from .models import Usuario

# Um 'Blueprint' é como um mini-aplicativo. Ele nos ajuda a agrupar
# rotas relacionadas. Este será para as rotas de autenticação.
auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def login():
    """
    Endpoint para autenticar um usuário.
    Recebe 'username' e 'password' no corpo da requisição (JSON).
    Se as credenciais estiverem corretas, retorna um token de acesso (JWT).
    """
    # Pega os dados JSON enviados na requisição
    auth_data = request.get_json()

    # Validação básica dos dados recebidos
    if not auth_data or not auth_data.get('username') or not auth_data.get('password'):
        return jsonify({'message': 'Credenciais não fornecidas ou incompletas.'}), 401

    # Busca o usuário no banco de dados pelo nome de usuário
    user = Usuario.query.filter_by(username=auth_data.get('username')).first()

    # Se o usuário não existir ou a senha estiver incorreta...
    if not user or not user.check_password(auth_data.get('password')):
        return jsonify({'message': 'Credenciais inválidas! Verifique usuário e senha.'}), 401

    # Se as credenciais estiverem corretas, geramos o token JWT.
    # O 'payload' do token contém informações que queremos armazenar nele.
    token_payload = {
        'id': user.id,
        'role': user.role,
        # iat (issued at): timestamp de quando o token foi criado
        'iat': datetime.datetime.utcnow(),
        # exp (expiration): o token expira em 24 horas
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    # Gera o token usando o payload, a chave secreta da aplicação e o algoritmo HS256.
    token = jwt.encode(
        token_payload,
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    # Retorna o token para o cliente. O cliente deverá armazenar este token
    # e enviá-lo de volta em cada requisição para rotas protegidas.
    return jsonify({
        'token': token,
        'role': user.role,
        'username': user.username
    })


def token_required(f):
    """
    Um 'decorator' para proteger rotas. Ele verifica se um token válido foi enviado.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # O token deve ser enviado no cabeçalho 'x-access-token' da requisição.
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token de acesso não encontrado!'}), 401

        try:
            # Tenta decodificar o token para validar sua autenticidade e expiração.
            payload = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # Busca o usuário correspondente ao 'id' que está dentro do token.
            current_user = Usuario.query.get(payload['id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirou! Faça login novamente.'}), 401
        except (jwt.InvalidTokenError, Exception) as e:
            return jsonify({'message': 'Token inválido!'}), 401

        # Passa o usuário encontrado para a função da rota que está sendo protegida.
        return f(current_user, *args, **kwargs)
    return decorated


def roles_required(*roles):
    """
    Um 'decorator' para verificar os papéis (permissões) do usuário.
    Ele deve ser usado SEMPRE DEPOIS do decorator @token_required.
    """
    def wrapper(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            # 'current_user' é passado pelo decorator @token_required.
            if current_user.role not in roles:
                # 403 Forbidden
                return jsonify({'message': 'Acesso negado! Você não tem permissão para esta ação.'}), 403
            return f(current_user, *args, **kwargs)
        return decorated_function
    return wrapper
