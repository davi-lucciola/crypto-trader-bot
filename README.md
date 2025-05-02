# 💲 Crypto Trader Bot

Crypto Trader Bot is a bot made to trade crypto currency based on moving avarage of the coins to identify if they are in a growth tendency or drop tendency and buy or sell depending of your position and tendency.

Each instance can be setup to trade the coins of your preference based on the enviroment variables

⸻

## ⚙️ Tech Stack

| Layer      | Tech                              |
|------------|-----------------------------------|
| Backend    | Python |
| External Services  | [Binance API](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/) |
| DevOps  | Docker |

⸻

## 🚀 Features
- 🔒 Trade any crypto currency you like
- 💻 Configure each instance to trade your preference crypto currency
- 🐳 Dockerized development environment

⸻

## 📂 Project Structure

<pre>

```
crypto-trader-bot
├── src/
│   ├── cryoto_bot.py   # Cryto Bot
│   ├── mail.py         # Email Functions
│   └── main.py         # Init Point
│
├── .env.exemple        # Env Variables Exemple
├── docker-compose.yml			
└── README.md
```
</pre>

⸻

## 🚀 Getting Started

### 📦 Requirements
	• Python 3.12+
	• Binance Account
	• Docker & Docker Compose

⸻

## 🐳 Start with Docker

### Setup Env Variables

- BINANCE_KEY (String): 
> Your Binance API Key
- BINANCE_SECRET (String)
> Your Binance API Secret

- EMAIL (String)
> Sender email
- EMAIL_PASSWORD (String)
> Sender email password
- SMTP_HOST (String)
> SMTP Server Host Address
- SMTP_PORT (Integer)
> SMTP Server Port
- SENT_TO_EMAIL (String)
> The email you want to recive the trade notifications

- CRYPTO (String)
> Code of the crypto you want to trade (Buy and Sell)
- TRADE_CODE (String)
> The concat of the code of the crypto you want to trade, to the other crypto you want to use to buy / sell. Example: SOL + USDT = SOLUSDT (Trading SOL with USDT)
- POSITION (Boolean)
> Value to determine if you already posicioned in the market to verify if is a good time to buy or sell
- TRADE_PERCENTAGE (Float)
> Value between 0 and 1 to determine how much of your current balance in binance you want to trade.
- PRECISION (Float)
> How many floating numbers are gonna be considered to execute the trades

### Build and run everything

By default, the docker-compose have 3 containers trading "SOL", "BTC" and "ETH" but you can configure like you want.

See the [Binance API oficial documentation](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/) to get all trade symbols

`docker-compose up --build`

⸻

## ⚠️ Disclaimer

This project is provided for **educational and research purposes only**.  
**Use at your own risk.** Cryptocurrency trading is inherently risky and can lead to financial loss.  
The author does **not provide financial advice**, and is **not responsible** for any financial losses, damages, or other consequences resulting from the use of this software.  
Make sure to understand the risks and comply with any applicable laws or regulations in your jurisdiction if you want to use the bot.
