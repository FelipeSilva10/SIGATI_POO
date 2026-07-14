import json
import os
from pathlib import Path


class ArquivoJson:
    def __init__(self, pasta='data'):
        self._pasta = Path(pasta)

    def inicializar(self):
        self._pasta.mkdir(parents=True, exist_ok=True)

    def caminho(self, nome_arquivo):
        return self._pasta / nome_arquivo

    def carregar(self, nome_arquivo, padrao=None):
        self.inicializar()
        caminho = self.caminho(nome_arquivo)
        if not caminho.exists():
            dados = self._clonar_padrao(padrao)
            self.salvar(nome_arquivo, dados)
            return dados

        try:
            with open(caminho, encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except (OSError, json.JSONDecodeError):
            return self._clonar_padrao(padrao)

    def salvar(self, nome_arquivo, dados):
        self.inicializar()
        caminho = self.caminho(nome_arquivo)
        temporario = caminho.with_suffix(caminho.suffix + '.tmp')

        try:
            with open(temporario, 'w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
                arquivo.write('\n')
            os.replace(temporario, caminho)
        except OSError as erro:
            raise RuntimeError(f'Não foi possível salvar {caminho}: {erro}') from erro

    def _clonar_padrao(self, padrao):
        if padrao is None:
            return []
        return padrao.copy()
