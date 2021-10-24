
import asyncio
import websockets
import json
from config import ticker
import ccxt.async_support as ccxt
socket1 = 'wss://stream.binance.com:9443/ws/{}@bookTicker'.format(ticker)
ba_ftx = 0
bb_ftx = 0
bb_binance = 0
ba_binance = 0

async def binance():
	async with websockets.connect(socket1) as websocket1:
		while True:
			global bb_binance
			global ba_binance
			global ba_ftx
			global bb_ftx
			data = await websocket1.recv()
			data = json.loads(data)
			bb_binance = float(data['b'])
			ba_binance = float(data['a'])
			
			
				

async def ftx():
	while True:
		global bb_binance
		global ba_binance
		global ba_ftx
		global bb_ftx
		exchange = getattr(ccxt, 'ftx')({'verbose': False})
		orderbook = await exchange.fetch_order_book('BTC/USDT')
		ba_ftx = orderbook['asks'][0][0]
		bb_ftx = orderbook['bids'][0][0]
		await exchange.close()

		if (bb_binance - ba_ftx) > 0 or (ba_binance - bb_ftx) <0 :
			print("It's time for arbitrage!")
			print('bb_binance = ', bb_binance)
			print('ba_ftx = ', ba_ftx)
			print('ba_binance = ', ba_binance)
			print('bb_ftx = ', bb_ftx)



async def main():
	task1 = asyncio.create_task(binance())
	task2 = asyncio.create_task(ftx())
	await task1
	await task2

asyncio.run(main())

