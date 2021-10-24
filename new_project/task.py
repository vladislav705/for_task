
import asyncio
import websockets
import json
from config import ticker
import ccxt.async_support as ccxt
socket1 = 'wss://stream.binance.com:9443/ws/{}@bookTicker'.format(ticker)


async def main():
	async with websockets.connect(socket1) as websocket1:
		while True:
			await asyncio.sleep(1)
			print('binance!!')
			data = await websocket1.recv()
			data = json.loads(data)
			bb_binance = float(data['b'])
			ba_binance = float(data['a'])
			task1 = asyncio.create_task(ftx(bb_binance, ba_binance))
			
				

async def ftx(bb_binance, ba_binance):
	while True:
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

asyncio.run(main())























