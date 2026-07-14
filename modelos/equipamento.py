from modelos.vulnerabilidade import Vulnerabilidade


class Equipamento:
    def __init__(
        self,
        id,
        hostname,
        responsavel,
        setor,
        tipo,
        descricao='',
        vulnerabilidades=None,
    ):
        self._id = self._como_inteiro(id)
        self.hostname = hostname
        self.responsavel = responsavel
        self.setor = setor
        self.tipo = tipo
        self.descricao = descricao
        self._vulnerabilidades = []
        for vulnerabilidade in vulnerabilidades or []:
            self.adicionar_vulnerabilidade(vulnerabilidade)

    @property
    def id(self):
        return self._id

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, valor):
        self._hostname = str(valor or '').strip()

    @property
    def responsavel(self):
        return self._responsavel

    @responsavel.setter
    def responsavel(self, valor):
        self._responsavel = str(valor or '').strip()

    @property
    def setor(self):
        return self._setor

    @setor.setter
    def setor(self, valor):
        self._setor = str(valor or '').strip()

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        self._tipo = self._como_inteiro(valor)

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = str(valor or '').strip()

    @property
    def vulnerabilidades(self):
        return list(self._vulnerabilidades)

    @property
    def quantidade_vulnerabilidades(self):
        return len(self._vulnerabilidades)

    def nome_tipo(self):
        return str(self.tipo)

    def adicionar_vulnerabilidade(self, vulnerabilidade):
        if not isinstance(vulnerabilidade, Vulnerabilidade):
            raise TypeError('vulnerabilidade deve ser um objeto Vulnerabilidade')
        self._vulnerabilidades.append(vulnerabilidade)

    def obter_vulnerabilidade(self, id_vulnerabilidade):
        id_vulnerabilidade = self._como_inteiro(id_vulnerabilidade)
        for vulnerabilidade in self._vulnerabilidades:
            if vulnerabilidade.id == id_vulnerabilidade:
                return vulnerabilidade
        return None

    def atualizar(self, responsavel=None, setor=None, descricao=None, tipo=None):
        if responsavel is not None:
            self.responsavel = responsavel
        if setor is not None:
            self.setor = setor
        if descricao is not None:
            self.descricao = descricao
        if tipo is not None:
            self.tipo = tipo

    def to_dict(self):
        return {
            'id': self.id,
            'hostname': self.hostname,
            'responsavel': self.responsavel,
            'setor': self.setor,
            'tipo': self.tipo,
            'descricao': self.descricao,
            'vulnerabilidades': [
                vulnerabilidade.to_dict()
                for vulnerabilidade in self._vulnerabilidades
            ],
        }

    @staticmethod
    def _como_inteiro(valor):
        try:
            return int(valor)
        except (TypeError, ValueError):
            return 0

    @classmethod
    def from_dict(cls, dados):
        vulnerabilidades = []
        for item in dados.get('vulnerabilidades', []):
            if isinstance(item, Vulnerabilidade):
                vulnerabilidades.append(item)
            elif isinstance(item, dict):
                vulnerabilidades.append(Vulnerabilidade.from_dict(item))

        return criar_equipamento(
            dados.get('id', 0),
            dados.get('hostname', ''),
            dados.get('responsavel', ''),
            dados.get('setor', ''),
            dados.get('tipo', 0),
            dados.get('descricao', ''),
            vulnerabilidades,
        )


class Notebook(Equipamento):
    def nome_tipo(self):
        return 'Notebook'


class Servidor(Equipamento):
    def nome_tipo(self):
        return 'Servidor'


class Roteador(Equipamento):
    def nome_tipo(self):
        return 'Roteador'


class SoftwareLicenciado(Equipamento):
    def nome_tipo(self):
        return 'Software Licenciado'


class AplicacaoWeb(Equipamento):
    def nome_tipo(self):
        return 'Aplicacao Web'


class BancoDados(Equipamento):
    def nome_tipo(self):
        return 'Banco De Dados'


class ImpressoraRede(Equipamento):
    def nome_tipo(self):
        return 'Impressora Rede'


class EstacaoTrabalho(Equipamento):
    def nome_tipo(self):
        return 'Estacao Trabalho'


CLASSES_POR_TIPO = {
    1: Notebook,
    2: Servidor,
    3: Roteador,
    4: SoftwareLicenciado,
    5: AplicacaoWeb,
    6: BancoDados,
    7: ImpressoraRede,
    8: EstacaoTrabalho,
}


def criar_equipamento(
    id,
    hostname,
    responsavel,
    setor,
    tipo,
    descricao='',
    vulnerabilidades=None,
):
    tipo_int = Equipamento._como_inteiro(tipo)
    classe_equipamento = CLASSES_POR_TIPO.get(tipo_int, Equipamento)
    return classe_equipamento(
        id,
        hostname,
        responsavel,
        setor,
        tipo,
        descricao,
        vulnerabilidades,
    )
