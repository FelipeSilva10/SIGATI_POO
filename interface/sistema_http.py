from flask import Flask, jsonify, request

from tipos import SEVERIDADES, STATUS_VULN, TIPOS_ATIVO


def criar_aplicacao(servico_equipamentos):
    aplicacao = Flask(__name__)

    @aplicacao.get('/ativos')
    def listar_ativos():
        ativos = [ativo.to_dict() for ativo in servico_equipamentos.listar()]
        return jsonify(ativos)

    @aplicacao.get('/ativos/<int:id_equipamento>')
    def consultar_ativo(id_equipamento):
        ativo = servico_equipamentos.buscar_por_id(id_equipamento)
        if ativo is None:
            return _erro('Ativo nao encontrado.', 404)
        return jsonify(ativo.to_dict())

    @aplicacao.get('/ativos/hostname/<hostname>')
    def consultar_ativo_por_hostname(hostname):
        ativo = servico_equipamentos.buscar_por_hostname(hostname)
        if ativo is None:
            return _erro('Ativo nao encontrado.', 404)
        return jsonify(ativo.to_dict())

    @aplicacao.post('/ativos')
    def cadastrar_ativo():
        dados = _dados_json()
        if dados is None:
            return _erro('O corpo da requisicao deve ser um objeto JSON.')

        campos = ('id', 'hostname', 'responsavel', 'setor', 'tipo')
        if _campos_faltantes(dados, campos):
            return _erro('Campos obrigatorios: ' + ', '.join(_campos_faltantes(dados, campos)))

        id_equipamento = _inteiro_positivo(dados['id'])
        tipo = _opcao_valida(dados['tipo'], TIPOS_ATIVO)
        if id_equipamento is None:
            return _erro('O campo id deve ser um inteiro positivo.')
        if tipo is None:
            return _erro('O campo tipo deve ser uma opcao valida.')

        try:
            ativo = servico_equipamentos.cadastrar_ativo(
                id_equipamento,
                dados['hostname'],
                dados['responsavel'],
                dados['setor'],
                tipo,
                dados.get('descricao', ''),
            )
        except ValueError as erro:
            return _erro(str(erro), 409)

        return jsonify(ativo.to_dict()), 201

    @aplicacao.put('/ativos/<int:id_equipamento>')
    def atualizar_ativo(id_equipamento):
        ativo = servico_equipamentos.buscar_por_id(id_equipamento)
        if ativo is None:
            return _erro('Ativo nao encontrado.', 404)

        dados = _dados_json()
        if dados is None:
            return _erro('O corpo da requisicao deve ser um objeto JSON.')

        campos_atualizaveis = ('responsavel', 'setor', 'descricao', 'tipo')
        if not any(campo in dados for campo in campos_atualizaveis):
            return _erro('Informe ao menos um campo para atualizar.')

        tipo = None
        if 'tipo' in dados:
            tipo = _opcao_valida(dados['tipo'], TIPOS_ATIVO)
            if tipo is None:
                return _erro('O campo tipo deve ser uma opcao valida.')

        ativo = servico_equipamentos.atualizar_ativo(
            ativo,
            responsavel=dados.get('responsavel'),
            setor=dados.get('setor'),
            descricao=dados.get('descricao'),
            tipo=tipo,
        )
        return jsonify(ativo.to_dict())

    @aplicacao.delete('/ativos/<int:id_equipamento>')
    def remover_ativo(id_equipamento):
        ativo = servico_equipamentos.buscar_por_id(id_equipamento)
        if ativo is None:
            return _erro('Ativo nao encontrado.', 404)

        servico_equipamentos.remover_ativo(ativo)
        return '', 204

    @aplicacao.get('/ativos/<int:id_equipamento>/vulnerabilidades')
    def listar_vulnerabilidades(id_equipamento):
        ativo = servico_equipamentos.buscar_por_id(id_equipamento)
        if ativo is None:
            return _erro('Ativo nao encontrado.', 404)

        vulnerabilidades = [item.to_dict() for item in ativo.vulnerabilidades]
        return jsonify(vulnerabilidades)

    @aplicacao.post('/ativos/<int:id_equipamento>/vulnerabilidades')
    def cadastrar_vulnerabilidade(id_equipamento):
        ativo = servico_equipamentos.buscar_por_id(id_equipamento)
        if ativo is None:
            return _erro('Ativo nao encontrado.', 404)

        dados = _dados_json()
        if dados is None:
            return _erro('O corpo da requisicao deve ser um objeto JSON.')

        campos = ('descricao', 'categoria', 'severidade', 'status')
        if _campos_faltantes(dados, campos):
            return _erro('Campos obrigatorios: ' + ', '.join(_campos_faltantes(dados, campos)))

        severidade = _opcao_valida(dados['severidade'], SEVERIDADES)
        status = _opcao_valida(dados['status'], STATUS_VULN)
        if severidade is None:
            return _erro('O campo severidade deve ser uma opcao valida.')
        if status is None:
            return _erro('O campo status deve ser uma opcao valida.')

        vulnerabilidade = servico_equipamentos.cadastrar_vulnerabilidade(
            ativo,
            dados['descricao'],
            dados['categoria'],
            severidade,
            status,
        )
        return jsonify(vulnerabilidade.to_dict()), 201

    @aplicacao.put(
        '/ativos/<int:id_equipamento>/vulnerabilidades/<int:id_vulnerabilidade>'
    )
    def atualizar_vulnerabilidade(id_equipamento, id_vulnerabilidade):
        ativo = servico_equipamentos.buscar_por_id(id_equipamento)
        if ativo is None:
            return _erro('Ativo nao encontrado.', 404)

        vulnerabilidade = ativo.obter_vulnerabilidade(id_vulnerabilidade)
        if vulnerabilidade is None:
            return _erro('Vulnerabilidade nao encontrada para este ativo.', 404)

        dados = _dados_json()
        if dados is None:
            return _erro('O corpo da requisicao deve ser um objeto JSON.')
        if 'status' not in dados and 'severidade' not in dados:
            return _erro('Informe status ou severidade para atualizar.')

        status = None
        severidade = None
        if 'status' in dados:
            status = _opcao_valida(dados['status'], STATUS_VULN)
            if status is None:
                return _erro('O campo status deve ser uma opcao valida.')
        if 'severidade' in dados:
            severidade = _opcao_valida(dados['severidade'], SEVERIDADES)
            if severidade is None:
                return _erro('O campo severidade deve ser uma opcao valida.')

        servico_equipamentos.atualizar_vulnerabilidade(
            vulnerabilidade,
            status=status,
            severidade=severidade,
        )
        return jsonify(vulnerabilidade.to_dict())

    @aplicacao.get('/tipos/ativos')
    def listar_tipos_ativos():
        return jsonify(TIPOS_ATIVO)

    @aplicacao.get('/tipos/severidades')
    def listar_severidades():
        return jsonify(SEVERIDADES)

    @aplicacao.get('/tipos/status-vulnerabilidades')
    def listar_status_vulnerabilidades():
        return jsonify(STATUS_VULN)

    return aplicacao


def executar_sistema(servico_equipamentos):
    aplicacao = criar_aplicacao(servico_equipamentos)
    aplicacao.run(host='0.0.0.0', port=5000)


def _erro(mensagem, status=400):
    return jsonify({'erro': mensagem}), status


def _dados_json():
    dados = request.get_json(silent=True)
    return dados if isinstance(dados, dict) else None


def _campos_faltantes(dados, campos):
    return [
        campo
        for campo in campos
        if dados.get(campo) is None or not str(dados[campo]).strip()
    ]


def _inteiro_positivo(valor):
    try:
        inteiro = int(valor)
    except (TypeError, ValueError):
        return None
    return inteiro if inteiro > 0 else None


def _opcao_valida(valor, opcoes):
    try:
        inteiro = int(valor)
    except (TypeError, ValueError):
        return None
    return inteiro if inteiro in opcoes else None
