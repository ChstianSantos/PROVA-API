atividades = [
    {
        'id_atividade': 1,
        'id_disciplina': 1,
        'enunciado': 'Crie um app de todo em Flask',
        'respostas': [
            {'id_aluno': 1, 'resposta': 'todo.py', 'nota': 9},
            {'id_aluno': 2, 'resposta': 'todo.zip.rar'},
            {'id_aluno': 4, 'resposta': 'todo.zip', 'nota': 10}
        ]
    },
    {
        'id_atividade': 2,
        'id_disciplina': 1,
        'enunciado': 'Crie um servidor que envia email em Flask',
        'respostas': [
            {'id_aluno': 4, 'resposta': 'email.zip', 'nota': 10}
        ]
    }
]

class AtividadeNotFound(Exception):
    pass

def listar_atividades():
    return atividades

def obter_atividade(id_atividade):
    for atividade in atividades:
        if atividade['id_atividade'] == id_atividade:
            return atividade
    raise AtividadeNotFound

def criar_atividade(id_disciplina, enunciado, respostas=[]):
    # Gera um novo ID baseado no maior ID atual
    novo_id = max(atividade['id_atividade'] for atividade in atividades) + 1 if atividades else 1
    nova_atividade = {
        'id_atividade': novo_id,
        'id_disciplina': id_disciplina,
        'enunciado': enunciado,
        'respostas': respostas
    }
    atividades.append(nova_atividade)
    return nova_atividade

def atualizar_atividade(id_atividade, id_disciplina, enunciado, respostas):
    for atividade in atividades:
        if atividade['id_atividade'] == id_atividade:
            atividade['id_disciplina'] = id_disciplina
            atividade['enunciado'] = enunciado
            atividade['respostas'] = respostas
            return atividade
    raise AtividadeNotFound

def excluir_atividade(id_atividade):
    global atividades
    for atividade in atividades:
        if atividade['id_atividade'] == id_atividade:
            atividades = [a for a in atividades if a['id_atividade'] != id_atividade]
            return
    raise AtividadeNotFound
