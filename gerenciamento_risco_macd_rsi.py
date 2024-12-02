class GerenciamentoRiscoMACDRSI:
    """
    Classe para implementar stop-loss e take-profit dinâmicos com base no RSI.
    """
    def __init__(self, stop_loss_percent=0.01, take_profit_percent=0.02):
        self.stop_loss_percent = stop_loss_percent
        self.take_profit_percent = take_profit_percent
        self.stop_loss = None
        self.take_profit = None

    def definir_niveis(self, preco_compra, rsi):
        """
        Define níveis de stop-loss e take-profit baseados no preço de compra e RSI.
        :param preco_compra: Preço de compra.
        :param rsi: Valor atual do RSI.
        """
        ajuste_rsi = 1 + ((rsi - 50) / 100)  # Ajuste baseado na distância do RSI de 50
        self.stop_loss = preco_compra * (1 - self.stop_loss_percent * ajuste_rsi)
        self.take_profit = preco_compra * (1 + self.take_profit_percent * ajuste_rsi)

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
