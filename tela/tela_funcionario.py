from tela.abstract_tela import AbstractTela
import PySimpleGUI as sg

class TelaFuncionario(AbstractTela):
    def __init__(self):
        self.__window = None

    def init_components(self):

        sg.ChangeLookAndFeel("Reddit")
        menu_def = [
            ['File', ['Open', 'Save', 'Exit', 'Properties']]
        ]

    def mostra_opcoes(self):
        layout = [
            [sg.Text('Como funcionário você deseja?', size=(30, 2))],
            [sg.Cancel("Voltar")],

            [sg.Button("Logar"), sg.Button("Cadastrar")]]

        self.__window = sg.Window("Funcionário", default_element_size=(100, 50)).Layout(layout)

        return self.open()

    def dados_cadastro(self):
        layout = [
            # [sg.Menu(menu_def, tearoff=True)]
            [sg.Text('Nome: ')],
            [sg.InputText()],
            [sg.Text("Cpf: ")],
            [sg.InputText()],
            [sg.Text("Senha: ")],
            [sg.InputText()],

            [sg.Submit("Salvar"), sg.Cancel("Cancelar")]]

        self.__window = sg.Window("Cadastro de funcionário").Layout(layout)

        return self.open()

    def open(self):
        button, values = self.__window.Read()
        return button, values

    def close(self):
        self.__window.Close()

    def login(self):
        layout = [
            # [sg.Menu(menu_def, tearoff=True)]
            [sg.Text("Cpf:")],
            [sg.InputText()],
            [sg.Text("Senha:")],
            [sg.InputText()],

            [sg.Submit("Salvar"), sg.Cancel("Cancelar")]]

        self.__window = sg.Window("Login de funcionário").Layout(layout)

        return self.open()

    def tela_atualiza_cadastro(self):
        layout = [
            [sg.Text('Nome: ')],
            [sg.InputText()],
            [sg.Text("Senha: ")],
            [sg.InputText()],

            [sg.Submit("Salvar"), sg.Cancel("Cancelar")]]

        self.__window = sg.Window("Alterar cadastro").Layout(layout)

        return self.open()

    def tela_remove(self):
        layout = [
            [sg.Text("Cpf:")],
            [sg.InputText()],
            [sg.Text("Senha:")],
            [sg.InputText()],

            [sg.Submit("Salvar"), sg.Cancel("Cancelar")]]

        self.__window = sg.Window("Remover cadastro").Layout(layout)

        return self.open()

    def tela_mostra_cadastro(self, nome, cpf, senha):
        layout = [
            [sg.Text("Nome:", size=(10, 1)), sg.Text(nome)],
            [sg.Text("Cpf:", size=(10, 1)), sg.Text(cpf)],
            [sg.Text("Senha:", size=(10, 1)), sg.Text(senha)],
            [sg.Button("Alterar Cadastro"), sg.Button("Remover Cadastro"), sg.Cancel("Voltar")]]

        self.__window = sg.Window(nome, default_element_size=(100, 50)).Layout(layout)

        return self.open()

    def tela_funcionario_logado(self, nome_funcionario: str):
        layout = [
            # [sg.Menu(menu_def, tearoff=True)]
            [sg.Text("Olá o que deseja?")],
            [sg.Button("Cadastro")],
            [sg.Button("Ver Estoque"), sg.Button("Lista de clientes")],
            [sg.Button("Sair")]]

        self.__window = sg.Window("Funcionário").Layout(layout)

        return self.open()

    def mostra_clientes(self, clientes: []):
        layout = [
            # [sg.Menu(menu_def, tearoff=True)]
            [sg.Text("Clientes")],

            [sg.Button("Voltar")]]

        self.__window = sg.Window("Lista de clientes").Layout(layout)

    def avisos(self, opcao: str):
        dicionario = {
            "cadastrar": "Funcionário cadastrado com sucesso!",
            "remover": "Funcionário removido com sucesso!",
            "dados_invalidos": "Erro! Digite o cpf ou a senha corretamente!",
            "atualiza": "Funcionário alterado com sucesso!",
            "usuario_ja_cadastrado": "Funcionário já cadastrado",
            "operacao_cancelada": "Operação Cancelada",
            "campo_vazio": "Preencha todos os campos!"}

        sg.Popup(dicionario[opcao])

    @property
    def window(self):
        return self.__window