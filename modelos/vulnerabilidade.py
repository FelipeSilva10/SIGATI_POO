class Vulnerabilidade:
    def __init__(self, id, ativo_id, descricao, categoria, severidade, status):
        self._id = self._como_inteiro(id)
        self._ativo_id = self._como_inteiro(ativo_id)
        self.descricao = descricao
        self.categoria = categoria
        self.severidade = severidade
        self.status = status

    @property
    def id(self):
        return self._id

    @property
    def ativo_id(self):
        return self._ativo_id

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = str(valor or '').strip()

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = str(valor or '').strip()

    @property
    def severidade(self):
        return self._severidade

    @severidade.setter
    def severidade(self, valor):
        self._severidade = self._como_inteiro(valor)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, valor):
        self._status = self._como_inteiro(valor)

    def atualizar(self, status=None, severidade=None):
        if status is not None:
            self.status = status
        if severidade is not None:
            self.severidade = severidade

    def to_dict(self):
        return {
            'id': self.id,
            'ativo_id': self.ativo_id,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'severidade': self.severidade,
            'status': self.status,
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados.get('id', 0),
            dados.get('ativo_id', 0),
            dados.get('descricao', ''),
            dados.get('categoria', ''),
            dados.get('severidade', 0),
            dados.get('status', 0),
        )

    @staticmethod
    def _como_inteiro(valor):
        try:
            return int(valor)
        except (TypeError, ValueError):
            return 0
