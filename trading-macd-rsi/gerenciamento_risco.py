class GerenciamentoRisco:
    """
    Classe para implementar stop-loss e take-profit dinâmicos.
    """

    def __init__(self, stop_loss_percent=0.01, take_profit_percent=0.02):
        """
        Inicializa os parâmetros do gerenciamento de risco.
        :param stop_loss_percent: Percentual de perda máxima tolerada.
        :param take_profit_percent: Percentual de lucro alvo.
        """
        self.stop_loss_percent = stop_loss_percent
        self.take_profit_percent = take_profit_percent
        self.stop_loss = None
        self.take_profit = None

    def definir_niveis(self, preco_compra):
        """
        Define os níveis de stop-loss e take-profit baseados no preço de compra.
        :param preco_compra: Preço da compra.
        """
        self.stop_loss = preco_compra * (1 - self.stop_loss_percent)
        self.take_profit = preco_compra * (1 + self.take_profit_percent)

    def verificar_saida(self, preco_atual):
        """
        Verifica se o preço atual atinge stop-loss ou take-profit.
        :param preco_atual: Preço atual do ativo.
        :return: String indicando "STOP_LOSS", "TAKE_PROFIT" ou "CONTINUAR".
        """
        if preco_atual <= self.stop_loss:
            return "STOP_LOSS"
        elif preco_atual >= self.take_profit:
            return "TAKE_PROFIT"
        return "CONTINUAR"
