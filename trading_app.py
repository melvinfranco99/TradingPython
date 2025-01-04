from platform_connector.platform_connector import PlatformConnector
from data_provider.data_provider import DataProvider
from trading_director.trading_director import TradingDirector

from queue import Queue

from signal_generator.signals.signal_ma_crossover import SignalMACrossover

if __name__ == "__main__":

    #Definicion de variables necesarias para la estrategia
    symbols = ['EURUSD', 'USDJPY']   # , 'EURGBP', 'SP500', 'XAUUSD', 'GBPUSD']
    timeframe = '1min'
    slow_ma_period = 50
    fast_ma_period = 25

    #Creacion de la cola de eventos principal
    events_queue = Queue()

    CONNECT = PlatformConnector(symbol_list=symbols)

    DATA_PROVIDER = DataProvider(events_queue=events_queue, 
                                symbol_list=symbols, 
                                timeframe=timeframe)
    
    SIGNAL_GENERATOR = SignalMACrossover(events_queue=events_queue, 
                                        data_provider=DATA_PROVIDER, 
                                        timeframe=timeframe, 
                                        fast_period=fast_ma_period, 
                                        slow_period=slow_ma_period)

    # Creacion del trading director y ejecucion del metodo principal
    TRADING_DIRECTOR = TradingDirector(events_queue = events_queue, data_provider=DATA_PROVIDER, signal_generator=SIGNAL_GENERATOR)

    TRADING_DIRECTOR.execute()