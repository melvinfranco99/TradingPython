from platform_connector.platform_connector import PlatformConnector
from data_provider.data_provider import DataProvider
from trading_director.trading_director import TradingDirector

from queue import Queue

if __name__ == "__main__":

    #Definicion de variables necesarias para la estrategia
    symbols = ['EURUSD', 'USDJPY', 'EURGBP', 'SP500', 'XAUUSD', 'GBPUSD']
    timeframe = '1min'

    #Creacion de la cola de eventos principal
    events_queue = Queue()

    CONNECT = PlatformConnector(symbol_list=symbols)
    DATA_PROVIDER = DataProvider(events_queue=events_queue, symbol_list=symbols, timeframe=timeframe)

    # Creacion del trading director y ejecucion del metodo principal
    TRADING_DIRECTOR = TradingDirector(events_queue = events_queue, data_provider=DATA_PROVIDER)

    TRADING_DIRECTOR.execute()