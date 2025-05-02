
from typing import Any
import pandas as pd
import datetime as dt
from binance.enums import *
from binance.client import Client
from dataclasses import dataclass
from mail import send_email


@dataclass
class CryptoError(Exception):
    message: str


@dataclass
class OrderError(Exception):
    args: tuple[Any, ...]


@dataclass
class CryptoBot:
    bclient: Client
    trader_email: str

    def get_account_balances(self):
        try:
            account: dict = self.bclient.get_account()

            balances = list(filter(lambda value: value, [
                crypto if float(crypto['free']) > 0 else None 
                for crypto in account.get('balances')
            ]))

            cryptos = {crypto['asset']: crypto['free'] for crypto in balances}
            return cryptos
        except:
            raise CryptoError('Houve um error ao buscar saldos.')


    def get_code_info(self, code: str):
        symbol_info = self.bclient.get_symbol_info(code)
        lot_size_filter = next(f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE')
        min_quantity = lot_size_filter['minQty']
        max_quantity = lot_size_filter['maxQty']
        step_size = lot_size_filter['stepSize']

        return {
            'min_quantity': min_quantity,
            'max_quantity': max_quantity,
            'step_size': step_size
        }


    def get_prices(self, code: str, kline_interval: str, limit: int = 1000):
        try:
            candles = self.bclient.get_klines(symbol=code, interval=kline_interval, limit=limit)
        except:
            raise CryptoError('Houve um error ao buscar preços.')
        
        prices = pd.DataFrame(candles)
        
        prices.columns = ['open_date_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 
            'close_date_time', 'quote_asset_volume', 'quote_asset_volume', 'trade_quantity', 'buy_base_asset_trade', 'buy_quote_asset_trade']

        prices = prices[['close_price', 'close_date_time']]

        prices['close_date_time'] = pd.to_datetime(prices['close_date_time'], unit='ms').dt.tz_localize('UTC')
        prices['close_date_time'] = prices['close_date_time'].dt.tz_convert('America/Sao_Paulo')

        return prices


    def order_crypto_strategy(self, data: pd.DataFrame, code: str, crypto: str, quantity: float, position: bool):
        fast_mean_days = 7
        slow_mean_days = 40

        data['fast_mean'] = data['close_price'].rolling(window=fast_mean_days).mean()
        data['slow_mean'] = data['close_price'].rolling(window=slow_mean_days).mean()

        last_fast_mean = data['fast_mean'].iloc[-1]
        last_slow_mean = data['slow_mean'].iloc[-1]

        print(' Executando Trade '.center(70, '-'))
        print(f'Média Rápida: {last_fast_mean} | Média Lenta: {last_slow_mean}')

        balances = self.get_account_balances()
        balance = balances.get(crypto)
        
        if balance is None:
            raise ValueError(f'Não foi encontrado saldo para a moeda: {crypto}')
        
        if last_fast_mean > last_slow_mean and position is False:
            print(f'COMPRANDO {quantity} {crypto}...')

            try:
                order = self.bclient.create_order(
                    symbol = code,
                    side = SIDE_BUY,
                    type = ORDER_TYPE_MARKET,
                    quantity = quantity
                )
            except Exception as e:
                raise OrderError(e.args)

            position = True
            print(f'COMPRA - {order.get('executedQty')} {crypto} - {dt.datetime.fromtimestamp(int(order.get("transactTime")) / 1000)}')

            message = f'<h1> Compra de {crypto} </h1>'
            message += f'<p> Ordem de Compra - <b> {order.get('executedQty')} {crypto} </b> </p>'
            message += f'<p> Valor de Compra - <b> {order.get('cummulativeQuoteQty')} USDT </b> </p>'
            message += f'<p> Taxa Binance - <b> {order['fills'][0]['commission']} {crypto} </b> </p>'
            message += f'<p> Quantidade Real - <b> {float(order.get('executedQty')) - float(order['fills'][0]['commission'])} {crypto} </b> </p>'
            message += f'<p> Data e Hora - <b> {dt.datetime.fromtimestamp(int(order.get("transactTime")) / 1000).strftime('%d/%m/%Y, %H:%M:%S')} </b> </p>'

            send_email(self.trader_email, f'Compra de {crypto} ', message)
        elif last_fast_mean < last_slow_mean and position is True:
            print(f'VENDENDO {quantity} {crypto}...')

            try:
                order = self.bclient.create_order(
                    symbol = code,
                    side = SIDE_SELL,
                    type = ORDER_TYPE_MARKET,
                    quantity = quantity
                )
            except Exception as e:
                raise OrderError(e.args)

            position = False
            print(f'VENDA - {order.get('executedQty')} USDT - {dt.datetime.fromtimestamp(int(order.get("transactTime")) / 1000)}')

            message = f'<h1> Compra de {crypto} </h1>'
            message += f'<p> Ordem de Venda - <b> {order.get('executedQty')} {crypto} </b> </p>'
            message += f'<p> Valor de Venda (Bruto) - <b> {order.get('cummulativeQuoteQty')} USDT </b> </p>'
            message += f'<p> Taxa Binance - <b> {order['fills'][0]['commission']} USDT </b> </p>'
            message += f'<p> Valor de Venda (Liquido) - <b> {float(order.get('cummulativeQuoteQty')) - float(order['fills'][0]['commission'])} USDT </b> </p>'
            message += f'<p> Data e Hora - <b> {dt.datetime.fromtimestamp(int(order.get("transactTime")) / 1000).strftime('%d/%m/%Y, %H:%M:%S')} </b> </p>'

            send_email(self.trader_email, f'Venda de {crypto} ', message)
        else:
            print('NENHUMA OPERAÇÃO FOI EXECUTADA')

        return position
