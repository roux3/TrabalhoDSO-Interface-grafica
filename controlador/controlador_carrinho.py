from entidade.carrinho import Carrinho
from tela.tela_carrinho import TelaCarrinho
from controlador.abstract_controlador import AbstractControlador
from entidade.produto import Produto
from tela.nota_fiscal import NotaFiscal

class ControladorCarrinho(AbstractControlador):

    def __init__(self, controlador):
        self.__controlador_principal = controlador
        self.__tela_carrinho = TelaCarrinho()
        self.__produtos_carrinho = []

    def adiciona(self, produto_selecionado):
        lista_separada = produto_selecionado[0].split("-")
        codigo = int(lista_separada[0])
        nome = lista_separada[1]
        valor = lista_separada[2]
        pode_add = self.__controlador_principal.controlador_produto.verifica_quantidade(
            int(codigo))

        if pode_add:
            if self.__produtos_carrinho == []:
                self.__produtos_carrinho.append([str(codigo), nome, str(valor), str(1)])
            else:
                for produto in self.__produtos_carrinho:
                    if str(codigo) == produto[0]:
                        produto[3] = int(produto[3])
                        produto[3] += 1
                        produto[3] = str(produto[3])
                        break
                    else:
                        self.__produtos_carrinho.append([str(codigo), nome, str(valor), str(1)])

            self.__controlador_principal.controlador_produto.atualiza_quantidade(codigo)

        else:
            self.__tela_carrinho.avisos("quantidade_insuficiente")

    def remove(self, produto_selecionado):
        codigo = produto_selecionado[0][0]
        if self.__produtos_carrinho != []:
            for produto in self.__produtos_carrinho:
                if codigo == produto[0]:
                    self.__controlador_principal.controlador_produto.atualiza_estoque_carrinho(int(produto[0]), 1)
                    produto[3] = int(produto[3])
                    produto[3] -= 1
                    produto[3] = str(produto[3])
                    if int(produto[3]) <= 0:
                        self.__produtos_carrinho.remove(produto)
                        break


        else:
            self.__tela_carrinho.avisos("carrinho_vazio")

    def atualiza(self):
        existe = False
        dados = self.__tela_carrinho.requisita_dado_atualizar()
        for produto in self.__carrinho_dao.get_all():
            if produto.codigo == dados["codigo"]:
                existe = True
                for prod in self.__controlador_principal.controlador_produto.produtos:
                    if produto.codigo == prod.codigo:
                        if dados["quantidade"] < produto.quantidade:
                            prod.quantidade += (produto.quantidade - dados["quantidade"])
                            produto.quantidade = dados["quantidade"]
                            self.__tela_carrinho.avisos("atualiza_produto")
                            break
                        elif dados["quantidade"] == (prod.quantidade + produto.quantidade):
                            prod.quantidade = dados["quantidade"] - (prod.quantidade + produto.quantidade)
                            self.__tela_carrinho.avisos("atualiza_produto")
                        else:
                            self.__tela_carrinho.avisos("quantidade_insuficiente")
        if not existe:
            self.__tela_carrinho.avisos("codigo_invalido")

    def limpa_carrinho(self):
        if self.__produtos_carrinho != []:
            for produto in self.__produtos_carrinho:
                self.__controlador_principal.controlador_produto.atualiza_estoque_carrinho(int(produto[0]), int(produto[3]))
            self.__produtos_carrinho = []
        else:
            self.__tela_carrinho.avisos("carrinho_vazio")

    def finaliza_tela(self):
        pass

    def finaliza_compra(self):
        if self.__produtos_carrinho == []:
            self.__tela_carrinho.avisos("carrinho_vazio")

        else:
            total = 0
            for produto in self.__produtos_carrinho:
                total += int(produto[2]) * int(produto[3])

            button, values = self.__tela_carrinho.confirma_tela("finaliza_compra")

            if button == "Sim":

                cpf_cliente = self.__controlador_principal.controlador_cliente.dado_cliente()
                self.__controlador_principal.controlador_nf.adiciona(cpf_cliente, total)
                lista_nf = self.__controlador_principal.controlador_nf.lista()
                self.__controlador_principal.controlador_nf.tela_nf(lista_nf)

            elif button == "Não":
                self.__tela_carrinho.avisos("compra_cancelada")

    def abre_tela_inicial(self):
        self.__exibe_tela = True


        while self.__exibe_tela:
            produtos_cadastrados = self.__controlador_principal.produtos_cadastrados()
            button, values = self.__tela_carrinho.mostra_opcoes(produtos_cadastrados, self.__produtos_carrinho)
            if button == "Voltar":
                self.limpa_carrinho()
                self.__exibe_tela = False

            elif button == "Finalizar compra":
                self.finaliza_compra()

            elif button == "+":
                self.adiciona(values[0])

            elif button == "-":
                self.remove(values[1])

            elif button == "Limpar carrinho":
                self.limpa_carrinho()

            self.__tela_carrinho.close()

