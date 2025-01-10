from ..interfaces.signal_generator_interface import ISignalGenerator
from events.events import DataEvent, SignalEvent
from queue import Queue
from data_provider.data_provider import DataProvider
from portfolio.portfolio import Portfolio

import pandas as pd

class SignalMACrossover(ISignalGenerator):

    def __init__(self, events_queue: Queue, data_provider: DataProvider, portfolio: Portfolio, timeframe: str, fast_period: int, slow_period: int):
        self.events_queue = events_queue

        self.DATA_PROVIDER = data_provider
        self.PORTFOLIO = portfolio

        self.timeframe = timeframe
        self.fast_period = fast_period if fast_period > 1 else 2
        self.slow_period = slow_period if slow_period > 2 else 3

        if self.fast_period >= slow_period:
            raise Exception(f"ERROR: El periodo rapido ({self.fast_period}) es mayor al perido lento ({self.slow_period}) para el calculo de las medias moviles")
        
    def _create_and_put_signal_event(self, symbol: str, signal: str, target_order: str, target_price: float, magic_number: int, sl: float, tp: float) -> None:
        signal_event = SignalEvent(symbol = symbol, 
                                    signal = signal,
                                    target_order = target_order,
                                    target_price = target_price,
                                    magic_number = magic_number,
                                    sl = sl,
                                    tp = tp)
        
        # Ponemos el SignalEvent a la cola de eventos
        self.events_queue.put(signal_event)



    def generate_signal(self, data_event: DataEvent) -> None:
        
        # Cogemos el simbolo del evento
        symbol = data_event.symbol

        # Recuperamos los datos necesarios para calcular las medias moviles
        bars = self.DATA_PROVIDER.get_latest_closed_bars(symbol, self.timeframe, self.slow_period)

        # Recuperamos las posiciones abiertas por esta estrategia en el simbolo donde hemos tenido el Data Event
        open_positions = self.PORTFOLIO.get_number_of_open_positions_by_symbol(symbol)

        # Calculamos el valor de los indicadores
        fast_ma = bars['close'][-self.fast_period:].mean()
        slow_ma = bars['close'].mean()

        # Detectar una señal de compra
        if open_positions['LONG'] == 0 and fast_ma > slow_ma:
            signal = "BUY"

        elif open_positions['SHORT'] == 0 and slow_ma > fast_ma:
            signal = "SELL"

        else:
            signal = ""

        # Si tenemos señal, generamos SignalEvent y lo colocamos en la cola de Eventos
        if signal != "":
            self._create_and_put_signal_event(symbol = symbol,
                                              signal = signal,
                                              target_order="MARKET",
                                              target_price=0.0,
                                              magic_number=self.PORTFOLIO.magic,
                                              sl=0.0,
                                              tp=0.0)

        