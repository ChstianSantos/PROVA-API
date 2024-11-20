from flask import Blueprint, jsonify, request
from models import atividade_model
from clients.pessoa_service_client import PessoaServiceClient

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    atividades = atividade_model.listar_atividades()
    return jsonify(atividades)

@atividade_bp.route('/<int:id_atividade>', methods=['GET'])
def obter_atividade(id_atividade):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/<int:id_atividade>/professor/<int:id_professor>', methods=['GET'])
def obter_atividade_para_professor(id_atividade, id_professor):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        if not PessoaServiceClient.verificar_leciona(id_professor, atividade['id_disciplina']):
            atividade = atividade.copy()
            atividade.pop('respostas', None)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/criar', methods=['POST'])
def criar_atividade():
    dados = request.get_json()
    try:
        nova_atividade = atividade_model.criar_atividade(
            id_disciplina=dados['id_disciplina'],
            enunciado=dados['enunciado'],
            respostas=dados.get('respostas', [])
        )
        return jsonify(nova_atividade), 201
    except KeyError as e:
        return jsonify({'erro': f'Campo obrigatório ausente: {str(e)}'}), 400
    except atividade_model.InvalidDataError as e:
        return jsonify({'erro': str(e)}), 400

@atividade_bp.route('/<int:id_atividade>', methods=['PUT'])
def atualizar_atividade(id_atividade):
    dados = request.get_json()
    try:
        atividade_atualizada = atividade_model.atualizar_atividade(
            id_atividade=id_atividade,
            id_disciplina=dados['id_disciplina'],
            enunciado=dados['enunciado'],
            respostas=dados.get('respostas', [])
        )
        return jsonify(atividade_atualizada)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    except atividade_model.InvalidDataError as e:
        return jsonify({'erro': str(e)}), 400

@atividade_bp.route('/del/<int:id_atividade>', methods=['DELETE'])
def excluir_atividade(id_atividade):
    try:
        atividade_model.excluir_atividade(id_atividade)
        return jsonify({'mensagem': 'Atividade excluída com sucesso'}), 200
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404