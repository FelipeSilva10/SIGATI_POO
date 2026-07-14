from interface.sistema_terminal import SistemaTerminal
from repositorios.repositorio_equipamentos import RepositorioEquipamentos
from servicos.servico_equipamentos import ServicoEquipamentos


def main():
    servico_equipamentos = ServicoEquipamentos(RepositorioEquipamentos())
    servico_equipamentos.carregar()
    SistemaTerminal(servico_equipamentos).executar_sistema()


if __name__ == '__main__':
    main()
