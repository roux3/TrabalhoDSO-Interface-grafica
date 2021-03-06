from tela.tela_produto import TelaProduto
from entidade.produto import Produto
from controlador.abstract_controlador import AbstractControlador
from persistencia.produto_dao import ProdutoDAO
import PySimpleGUI as sg

class ControladorProduto(AbstractControlador):

    def __init__(self):
        self.__produto_dao = ProdutoDAO()
        self.__tela_produto = TelaProduto(self)

    @property
    def produtos(self):
        lista_produtos = []
        for produto in  self.__produto_dao.get_all():
            lista_produtos.append(produto)
        return self.__produto_dao.get_all


    def adiciona(self):
        tela_adiciona = True

        while tela_adiciona:
            button, values = self.__tela_produto.requisita_dados_cadastro()
            print(values[0].index)
            if button == "Cancelar":
                self.__tela_produto.avisos("operacao_cancelada")
                tela_adiciona = False

            elif values[0] == "" or values[1] == "" or values[2] == "" or values[3] == "":
                self.__tela_produto.avisos("campo_vazio")

            elif values[0].length < 3 or values[0].length > 3:
                print("valor errado")
            else:
                ja_existe = False
                for produto in self.__produto_dao.get_all():
                    if int(values[0]) == produto.codigo:
                        ja_existe = True
                        break
                if not ja_existe:
                    novo_produto = Produto(int(values[0]), values[1], values[2], values[3])
                    self.__produto_dao.add(novo_produto)
                    tela_adiciona = False
                    self.__tela_produto.avisos("produto_cadastrado")

                else:
                    self.__tela_produto.avisos("produto_ja_cadastrado")

            self.__tela_produto.close()

    def remove(self, codigo_produto_selecionado):
        produto = self.__produto_dao.get(codigo_produto_selecionado)
        self.__produto_dao.remove(produto.codigo)
        self.__tela_produto.avisos("remove_produto")

    def atualiza(self, codigo_produto_selecionado):
        produto = self.__produto_dao.get(codigo_produto_selecionado)

        button, values = self.__tela_produto.requisita_dado_atualizar(produto.nome, produto.valor, produto.quantidade)

        if button == "Cancelar":
            self.__tela_produto.close()
        elif values['nome'] == "" or values['valor'] == "" or values['quantidade'] == "":
            self.__tela_produto.avisos("campo_vazio")
        else:
            produto.nome = values['nome']
            produto.valor = values['valor']
            produto.quantidade = values['quantidade']
            self.__produto_dao.add(produto)

        self.__tela_produto.close()

    def lista_produtos_disponiveis(self):
        lista_produtos = []
        for produto in self.__produto_dao.get_all():
            if int(produto.quantidade) > 0:
                lista_produtos.append('{:3d}'.format(produto.codigo) + '-' + produto.nome + '-' + str(produto.valor) + '-' +
                             str(produto.quantidade))

        return lista_produtos

    def lista(self):
        tela_lista = True

        while tela_lista:
            dados = []
            for produto in self.__produto_dao.get_all():
                dados.append('{:3d}'.format(produto.codigo) +'-'+ produto.nome +'-'+ str(produto.valor) +'-'+
                                                             str(produto.quantidade))

            button, values = self.__tela_produto.mostra_produtos(dados)

            # primeira posição [0] é do dicionário, a segunda posição [0] é pra pegar o item selecionado do listbox, e o [0:3] é para pegar somente o código do produto
            codigo_produto = int(values[0][0][0:3])
            self.__tela_produto.close()
            if button == "Voltar":
                tela_lista = False
            elif button == "Alterar produto":
                if not values[0]:
                    self.__tela_produto.avisos("selecione_produto")
                else:
                    self.atualiza(codigo_produto)

            elif button == "Remover produto":
                if not values[0]:
                    self.__tela_produto.avisos("selecione_produto")
                else:
                    self.remove(codigo_produto)

    def verifica_quantidade(self, key):
        produto = self.__produto_dao.get(key)

        if int(produto.quantidade) > 0:
            return True
        else:
            return False

    def atualiza_estoque_carrinho(self, key, quantidade):
        produto = self.__produto_dao.get(key)
        produto.quantidade = int(produto.quantidade) + quantidade
        produto.quantidade = str(produto.quantidade)
        self.__produto_dao.add(produto)

    def atualiza_quantidade(self, key):
        produto = self.__produto_dao.get(key)
        produto.quantidade = int(produto.quantidade)
        produto.quantidade -= 1
        produto.quantidade = str(produto.quantidade)
        self.__produto_dao.add(produto)
        return self.__produto_dao.get_all()


    def abre_tela_inicial(self):
        lista_opcoes = {
            "Adicionar produto": self.adiciona,
            "Listar produtos": self.lista,
            "Voltar": self.finaliza_tela}

        self.__exibe_tela = True
        while self.__exibe_tela:
            button, values = self.__tela_produto.mostra_opcoes()
            funcao_escolhida = lista_opcoes[button]
            self.__tela_produto.close()
            funcao_escolhida()

    def finaliza_tela(self):
        self.__tela_produto.close()
        self.__exibe_tela = False