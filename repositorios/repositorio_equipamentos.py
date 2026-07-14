from dados import ArquivoJson
from modelos.equipamento import Equipamento
from modelos.vulnerabilidade import Vulnerabilidade


class RepositorioEquipamentos:
    def __init__(
        self,
        arquivo_json=None,
        arquivo_ativos='ativos.json',
        arquivo_vulnerabilidades='vulns.json',
    ):
        self._arquivo_json = arquivo_json or ArquivoJson()
        self._arquivo_ativos = arquivo_ativos
        self._arquivo_vulnerabilidades = arquivo_vulnerabilidades

    def carregar(self):
        dados_ativos = self._normalizar_lista(
            self._arquivo_json.carregar(self._arquivo_ativos, [])
        )
        dados_vulnerabilidades = self._normalizar_lista(
            self._arquivo_json.carregar(self._arquivo_vulnerabilidades, [])
        )

        vulnerabilidades_por_id, vulnerabilidades_por_ativo = (
            self._indexar_vulnerabilidades(dados_vulnerabilidades)
        )

        equipamentos = []
        for item in dados_ativos:
            if not isinstance(item, dict):
                continue

            dados = dict(item)
            dados['vulnerabilidades'] = self._vulnerabilidades_do_ativo(
                dados,
                vulnerabilidades_por_id,
                vulnerabilidades_por_ativo,
            )
            equipamentos.append(Equipamento.from_dict(dados))

        return equipamentos

    def salvar(self, equipamentos):
        equipamentos_ordenados = sorted(equipamentos, key=lambda item: item.id)
        self._arquivo_json.salvar(
            self._arquivo_ativos,
            [equipamento.to_dict() for equipamento in equipamentos_ordenados],
        )
        self._arquivo_json.salvar(
            self._arquivo_vulnerabilidades,
            self._vulnerabilidades_em_lista(equipamentos_ordenados),
        )

    def _normalizar_lista(self, dados):
        if isinstance(dados, list):
            return dados
        if isinstance(dados, dict):
            return list(dados.values())
        return []

    def _indexar_vulnerabilidades(self, dados_vulnerabilidades):
        por_id = {}
        por_ativo = {}
        for item in dados_vulnerabilidades:
            if not isinstance(item, dict):
                continue

            vulnerabilidade = Vulnerabilidade.from_dict(item)
            if vulnerabilidade.id <= 0:
                continue

            por_id[vulnerabilidade.id] = vulnerabilidade
            por_ativo.setdefault(vulnerabilidade.ativo_id, []).append(vulnerabilidade)

        return por_id, por_ativo

    def _vulnerabilidades_do_ativo(
        self,
        dados_ativo,
        vulnerabilidades_por_id,
        vulnerabilidades_por_ativo,
    ):
        ativo_id = self._como_inteiro(dados_ativo.get('id'))
        vulnerabilidades = []
        ids_adicionados = set()

        for item in dados_ativo.get('vulnerabilidades', []):
            vulnerabilidade = self._converter_vulnerabilidade(
                item,
                ativo_id,
                vulnerabilidades_por_id,
            )
            if vulnerabilidade is None:
                continue
            if vulnerabilidade.id in ids_adicionados:
                continue
            vulnerabilidades.append(vulnerabilidade)
            ids_adicionados.add(vulnerabilidade.id)

        for vulnerabilidade in vulnerabilidades_por_ativo.get(ativo_id, []):
            if vulnerabilidade.id not in ids_adicionados:
                vulnerabilidades.append(vulnerabilidade)
                ids_adicionados.add(vulnerabilidade.id)

        return vulnerabilidades

    def _converter_vulnerabilidade(
        self,
        item,
        ativo_id,
        vulnerabilidades_por_id,
    ):
        if isinstance(item, dict):
            dados = dict(item)
            dados['ativo_id'] = ativo_id
            vulnerabilidade = Vulnerabilidade.from_dict(dados)
            if vulnerabilidade.id <= 0:
                return None
            return vulnerabilidade

        id_vulnerabilidade = self._como_inteiro(item)
        return vulnerabilidades_por_id.get(id_vulnerabilidade)

    def _vulnerabilidades_em_lista(self, equipamentos):
        vulnerabilidades = []
        for equipamento in equipamentos:
            vulnerabilidades.extend(equipamento.vulnerabilidades)
        return [
            vulnerabilidade.to_dict()
            for vulnerabilidade in sorted(vulnerabilidades, key=lambda item: item.id)
        ]

    def _como_inteiro(self, valor):
        try:
            return int(valor)
        except (TypeError, ValueError):
            return 0
