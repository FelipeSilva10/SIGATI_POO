from interface.sistema_http import executar_sistema
from repositorios.repositorio_equipamentos import RepositorioEquipamentos
from servicos.servico_equipamentos import ServicoEquipamentos


def main():
    servico_equipamentos = ServicoEquipamentos(RepositorioEquipamentos())
    servico_equipamentos.carregar()
    executar_sistema(servico_equipamentos)


if __name__ == '__main__':
    main()
