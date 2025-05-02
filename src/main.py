import os
import time
import dotenv as env
from mail import send_email
from binance.client import Client
from crypto_bot import CryptoBot, CryptoError


env.load_dotenv()


def main():
    trader_email = os.getenv('SENT_TO_EMAIL')
    bclient = Client(os.getenv('BINANCE_KEY'), os.getenv('BINANCE_SECRET'))

    crypto_bot = CryptoBot(bclient, trader_email)

    crypto = os.getenv('CRYPTO')
    code = os.getenv('TRADE_CODE')
    position = os.getenv('POSITION') == 'true'
    precision = int(os.getenv('PRECISION'))

    crypto_balance = float(crypto_bot.get_account_balances().get(crypto))
    trade_quantity = round(crypto_balance * float(os.getenv('TRADE_PERCENTAGE')), precision)

    print(f'BOT INICIALIZADO: {crypto}')
    print(f'Codigo de Negociação: {code}')
    print(f'Valor Operado: {trade_quantity}')

    while True:
        try:
            prices = crypto_bot.get_prices(code, Client.KLINE_INTERVAL_1HOUR)
            position = crypto_bot.order_crypto_strategy(prices, code, crypto, trade_quantity, position)
            time.sleep(1)

            balances = crypto_bot.get_account_balances()
            print(f'Saldo Atual ({crypto}): {balances.get(crypto)}')
            print(f'Saldo Atual (USDT): {balances.get('USDT')}')
            print(f'Posicionado: {"Sim" if position else "Não"}')

            time.sleep(5)
        except CryptoError as err:
            print(err.message)
        except Exception as err:
            send_email(
                trader_email, 
                f'Error Bot ({crypto})', str(err)
            )
            print('Encerrando Funcionamento...')
            break


if __name__ == "__main__":
    main()
