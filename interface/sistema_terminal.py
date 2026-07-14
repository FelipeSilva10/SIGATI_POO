import os

from tipos import SEVERIDADES, STATUS_VULN, TIPOS_ATIVO, nome_opcao


class SistemaTerminal:
    def __init__(self, servico_equipamentos):
        self._servico_equipamentos = servico_equipamentos

    def limpar(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def titulo(self, texto):
        print()
        print('═' * 56)
        print(f'  {texto}')
        print('═' * 56)

    def pausar(self):
        print()
        input('  Pressione Enter para continuar')

    def ler_inteiro(self, prompt, minimo=None, maximo=None):
        while True:
            try:
                valor = int(input(prompt).strip())
                if minimo is not None and valor < minimo:
                    print(f'  Valor mínimo: {minimo}.')
                    continue
                if maximo is not None and valor > maximo:
                    print(f'  Valor máximo: {maximo}.')
                    continue
                return valor
            except ValueError:
                print('  Digite um número inteiro.')

    def ler_texto(self, prompt, obrigatorio=True):
        while True:
            valor = input(prompt).strip()
            if obrigatorio and not valor:
                print('  Campo obrigatório.')
                continue
            return valor

    def escolher(self, opcoes, rotulo):
        print()
        print(f'  {rotulo}:')
        for codigo in opcoes:
            print(f'    {codigo}  ->  {opcoes[codigo]}')
        return self.ler_inteiro('  Opção: ', minimo=1, maximo=len(opcoes))

    def buscar_ativo(self):
        print()
        print('  Buscar por:  1 ID    2 Hostname')
        op = self.ler_inteiro('  Opção: ', minimo=1, maximo=2)
        if op == 1:
            ativo = self._servico_equipamentos.buscar_por_id(
                self.ler_inteiro('  ID do ativo: ', minimo=1)
            )
        else:
            ativo = self._servico_equipamentos.buscar_por_hostname(
                self.ler_texto('  Hostname: ')
            )

        if ativo:
            return ativo

        print('  Ativo não encontrado.')
        return None

    def exibir_ativo(self, ativo):
        desc = ativo.descricao or '—'
        print()
        print(f'  ID          : {ativo.id}')
        print(f'  Hostname    : {ativo.hostname}')
        print(f'  Responsável : {ativo.responsavel}')
        print(f'  Setor       : {ativo.setor}')
        print(f'  Tipo        : {ativo.nome_tipo()}')
        print(f'  Descrição   : {desc}')
        print(f'  Vulns       : {ativo.quantidade_vulnerabilidades}')

    def exibir_vuln(self, vulnerabilidade):
        print('  ' + '─' * 50)
        print(f'  ID         : {vulnerabilidade.id}')
        print(f'  Descrição  : {vulnerabilidade.descricao}')
        print(f'  Categoria  : {vulnerabilidade.categoria}')
        print(
            f'  Severidade : '
            f'{nome_opcao(SEVERIDADES, vulnerabilidade.severidade)}'
        )
        print(f'  Status     : {nome_opcao(STATUS_VULN, vulnerabilidade.status)}')

    def ler_id_ativo_novo(self):
        while True:
            novo_id = self.ler_inteiro('  ID do ativo (inteiro único): ', minimo=1)
            if self._servico_equipamentos.id_disponivel(novo_id):
                return novo_id
            print(f'  ID {novo_id} já tá em uso.')

    def ler_hostname_novo(self):
        while True:
            hostname = self.ler_texto('  Nome / Hostname: ')
            if self._servico_equipamentos.hostname_disponivel(hostname):
                return hostname
            print('  Hostname já cadastrado.')

    def cadastrar_ativo(self):
        self.titulo('Cadastrar Ativo de TI')
        novo_id = self.ler_id_ativo_novo()
        hostname = self.ler_hostname_novo()
        responsavel = self.ler_texto('  Responsável: ')
        setor = self.ler_texto('  Setor / Localização: ')
        tipo = self.escolher(TIPOS_ATIVO, 'Tipo do ativo')
        descricao = self.ler_texto('  Descrição (Enter para pular): ', obrigatorio=False)

        ativo = self._servico_equipamentos.cadastrar_ativo(
            novo_id,
            hostname,
            responsavel,
            setor,
            tipo,
            descricao,
        )
        print(f'Ativo cadastrado (ID: {ativo.id}).')
        self.pausar()

    def consultar_ativo(self):
        self.titulo('Consultar Ativo de TI')
        ativo = self.buscar_ativo()
        if ativo:
            self.exibir_ativo(ativo)
        self.pausar()

    def listar_ativos(self):
        self.titulo('Listar Todos os Ativos')
        ativos = self._servico_equipamentos.listar()
        if not ativos:
            print('  Nenhum ativo cadastrado.')
            self.pausar()
            return

        print()
        print(f"  {'ID':<6} {'Hostname':<22} {'Responsável':<20} Tipo")
        print('  ' + '─' * 55)
        for ativo in ativos:
            tipo = ativo.nome_tipo()
            print(f'  {ativo.id:<6} {ativo.hostname:<22} {ativo.responsavel:<20} {tipo}')
        print()
        print(f'  Total: {len(ativos)} ativo(s)')
        self.pausar()

    def atualizar_ativo(self):
        self.titulo('Atualizar Ativo de TI')
        ativo = self.buscar_ativo()
        if not ativo:
            self.pausar()
            return

        print(f'  Editando: {ativo.hostname} (ID {ativo.id})')
        print('  [ Enter sem digitar = manter valor atual ]')
        resp_atual = ativo.responsavel
        setor_atual = ativo.setor
        desc_atual = ativo.descricao or '—'
        novo_resp = self.ler_texto(f'  Responsável [{resp_atual}]: ', obrigatorio=False)
        novo_setor = self.ler_texto(f'  Setor [{setor_atual}]: ', obrigatorio=False)
        nova_desc = self.ler_texto(f'  Descrição [{desc_atual}]: ', obrigatorio=False)
        tipo = None
        tipo_atual = ativo.nome_tipo()
        print(f'  Tipo atual: {tipo_atual}')
        if self.ler_texto('  Alterar tipo? (s/N): ', obrigatorio=False).lower() == 's':
            tipo = self.escolher(TIPOS_ATIVO, 'Novo tipo')

        self._servico_equipamentos.atualizar_ativo(
            ativo,
            responsavel=novo_resp or None,
            setor=novo_setor or None,
            descricao=nova_desc or None,
            tipo=tipo,
        )
        print('  Ativo atualizado.')
        self.pausar()

    def remover_ativo(self):
        self.titulo('Remover Ativo de TI')
        ativo = self.buscar_ativo()
        if not ativo:
            self.pausar()
            return

        qtd = ativo.quantidade_vulnerabilidades
        print(f'  Ativo: {ativo.hostname} (ID {ativo.id})')
        if qtd:
            print(f'    ! {qtd} As vulnerabilidades associadas também serão removidas.')
        if self.ler_texto('  Confirmar remoção? (s/N): ', obrigatorio=False).lower() != 's':
            print('  Operação cancelada.')
            self.pausar()
            return

        self._servico_equipamentos.remover_ativo(ativo)
        print('  Ativo e vulnerabilidades removidos.')
        self.pausar()

    def cadastrar_vuln(self):
        self.titulo('Cadastrar vulnerabilidade')
        ativo = self.buscar_ativo()
        if not ativo:
            self.pausar()
            return

        print(f'  Ativo: {ativo.hostname} (ID {ativo.id})')
        descricao = self.ler_texto('  Descrição da vulnerabilidade: ')
        categoria = self.ler_texto('  Categoria: ')
        severidade = self.escolher(SEVERIDADES, 'Severidade')
        status = self.escolher(STATUS_VULN, 'Status')
        vulnerabilidade = self._servico_equipamentos.cadastrar_vulnerabilidade(
            ativo,
            descricao,
            categoria,
            severidade,
            status,
        )
        print(f' Vulnerabilidade cadastrada (ID: {vulnerabilidade.id}).')
        self.pausar()

    def ver_vulns(self):
        self.titulo('Vulnerabilidades do Ativo')
        ativo = self.buscar_ativo()
        if not ativo:
            self.pausar()
            return

        print(f'  Ativo: {ativo.hostname} (ID {ativo.id})')
        vulnerabilidades = ativo.vulnerabilidades
        if not vulnerabilidades:
            print(' Nenhuma vulnerabilidade registrada para este ativo.')
        else:
            print(f'  Total: {len(vulnerabilidades)} vulnerabilidade(s)')
            for vulnerabilidade in vulnerabilidades:
                self.exibir_vuln(vulnerabilidade)
        self.pausar()

    def mostrar_resumo_vulns(self, ativo):
        print(f"  Vulnerabilidades de '{ativo.hostname}':")
        print('  ' + '─' * 55)
        for vulnerabilidade in ativo.vulnerabilidades:
            severidade = nome_opcao(SEVERIDADES, vulnerabilidade.severidade)
            status = nome_opcao(STATUS_VULN, vulnerabilidade.status)
            desc = vulnerabilidade.descricao[:45]
            print(
                f'  [{vulnerabilidade.id:>3}]  '
                f'{desc:<46}  {severidade:<8}  {status}'
            )

    def atualizar_vuln(self):
        self.titulo('Atualizar Vulnerabilidade')
        ativo = self.buscar_ativo()
        if not ativo:
            self.pausar()
            return

        if not ativo.vulnerabilidades:
            print('  Nenhuma vulnerabilidade para este ativo.')
            self.pausar()
            return

        self.mostrar_resumo_vulns(ativo)
        vid_sel = self.ler_inteiro('  ID da vulnerabilidade: ', minimo=1)
        vulnerabilidade = ativo.obter_vulnerabilidade(vid_sel)
        if not vulnerabilidade:
            print('Vulnerabilidade não encontrada para este ativo.')
            self.pausar()
            return

        print(f'  Vulnerabilidade: {vulnerabilidade.descricao}')
        status = None
        severidade = None
        if self.ler_texto('  Alterar status? (s/N): ', obrigatorio=False).lower() == 's':
            status = self.escolher(STATUS_VULN, 'Novo status')
        if self.ler_texto('  Alterar severidade? (s/N): ', obrigatorio=False).lower() == 's':
            severidade = self.escolher(SEVERIDADES, 'Nova severidade')

        self._servico_equipamentos.atualizar_vulnerabilidade(
            vulnerabilidade,
            status=status,
            severidade=severidade,
        )
        print('Vulnerabilidade atualizada.')
        self.pausar()

    def menu(self):
        print("""
        SIGATI — Sistema de Gestão de Ativos de TI

        ATIVOS

        1 - Cadastrar ativo
        2 - Consultar ativo
        3 - Atualizar ativo
        4 - Remover ativo
        5 - Listar ativos

        VULNERABILIDADES

        6 - Cadastrar vulnerabilidade
        7 - Visualizar vulnerabilidades
        8 - Atualizar vulnerabilidade

        0 - Sair
    """)

    def executar_opcao(self, op):
        if op == 1:
            self.cadastrar_ativo()
        elif op == 2:
            self.consultar_ativo()
        elif op == 3:
            self.atualizar_ativo()
        elif op == 4:
            self.remover_ativo()
        elif op == 5:
            self.listar_ativos()
        elif op == 6:
            self.cadastrar_vuln()
        elif op == 7:
            self.ver_vulns()
        elif op == 8:
            self.atualizar_vuln()

    def executar_sistema(self):
        while True:
            self.limpar()
            self.menu()
            op = self.ler_inteiro('  Selecione uma opção: ', minimo=0, maximo=8)
            if op == 0:
                print('  Encerrando.')
                break
            try:
                self.executar_opcao(op)
            except RuntimeError as erro:
                print(f'  Erro: {erro}')
                self.pausar()
