from modelos.equipamento import criar_equipamento
from modelos.vulnerabilidade import Vulnerabilidade
from repositorios.repositorio_equipamentos import RepositorioEquipamentos


class ServicoEquipamentos:
    def __init__(self, repositorio=None):
        self._repositorio = repositorio or RepositorioEquipamentos()
        self._equipamentos = []
        self._por_id = {}
        self._por_hostname = {}

    def carregar(self):
        self._equipamentos = self._repositorio.carregar()
        self._reindexar()

    def listar(self):
        return sorted(self._equipamentos, key=lambda item: item.id)

    def buscar_por_id(self, id_equipamento):
        return self._por_id.get(self._como_inteiro(id_equipamento))

    def buscar_por_hostname(self, hostname):
        return self._por_hostname.get(str(hostname or '').strip().lower())

    def id_disponivel(self, id_equipamento):
        return self.buscar_por_id(id_equipamento) is None

    def hostname_disponivel(self, hostname):
        return self.buscar_por_hostname(hostname) is None

    def cadastrar_ativo(
        self,
        id_equipamento,
        hostname,
        responsavel,
        setor,
        tipo,
        descricao='',
    ):
        if not self.id_disponivel(id_equipamento):
            raise ValueError(f'ID {id_equipamento} já tá em uso.')
        if not self.hostname_disponivel(hostname):
            raise ValueError('Hostname já cadastrado.')

        equipamento = criar_equipamento(
            id_equipamento,
            hostname,
            responsavel,
            setor,
            tipo,
            descricao,
            [],
        )
        self._equipamentos.append(equipamento)
        self._reindexar()
        self.salvar()
        return equipamento

    def atualizar_ativo(
        self,
        equipamento,
        responsavel=None,
        setor=None,
        descricao=None,
        tipo=None,
    ):
        equipamento.atualizar(
            responsavel=responsavel,
            setor=setor,
            descricao=descricao,
            tipo=tipo,
        )
        if tipo is not None:
            equipamento = criar_equipamento(
                equipamento.id,
                equipamento.hostname,
                equipamento.responsavel,
                equipamento.setor,
                equipamento.tipo,
                equipamento.descricao,
                equipamento.vulnerabilidades,
            )
            for indice, item in enumerate(self._equipamentos):
                if item.id == equipamento.id:
                    self._equipamentos[indice] = equipamento
                    break
            self._reindexar()
        self.salvar()
        return equipamento

    def remover_ativo(self, equipamento):
        self._equipamentos = [
            item for item in self._equipamentos if item.id != equipamento.id
        ]
        self._reindexar()
        self.salvar()

    def cadastrar_vulnerabilidade(
        self,
        equipamento,
        descricao,
        categoria,
        severidade,
        status,
    ):
        vulnerabilidade = Vulnerabilidade(
            self.proximo_id_vulnerabilidade(),
            equipamento.id,
            descricao,
            categoria,
            severidade,
            status,
        )
        equipamento.adicionar_vulnerabilidade(vulnerabilidade)
        self.salvar()
        return vulnerabilidade

    def atualizar_vulnerabilidade(self, vulnerabilidade, status=None, severidade=None):
        vulnerabilidade.atualizar(status=status, severidade=severidade)
        self.salvar()

    def proximo_id_vulnerabilidade(self):
        maior = 0
        for equipamento in self._equipamentos:
            for vulnerabilidade in equipamento.vulnerabilidades:
                if vulnerabilidade.id > maior:
                    maior = vulnerabilidade.id
        return maior + 1

    def salvar(self):
        self._repositorio.salvar(self._equipamentos)

    def _reindexar(self):
        self._por_id = {}
        self._por_hostname = {}
        for equipamento in self._equipamentos:
            self._por_id[equipamento.id] = equipamento
            self._por_hostname[equipamento.hostname.lower()] = equipamento

    def _como_inteiro(self, valor):
        try:
            return int(valor)
        except (TypeError, ValueError):
            return 0
