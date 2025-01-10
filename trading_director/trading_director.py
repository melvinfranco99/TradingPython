
import queue
from data_provider.data_provider import DataProvider
from typing import Dict, Callable
from events.events import DataEvent, SignalEvent, SizingEvent
import time
from datetime import datetime
from signal_generator.interfaces.signal_generator_interface import ISignalGenerator
from position_sizer.position_sizer import PositionSizer

class TradingDirector():
    def __init__(self, events_queue: queue.Queue, data_provider: DataProvider, signal_generator: ISignalGenerator, position_sizer: PositionSizer):
        self.events_queue = events_queue
        
        # Referencia de los distintos modulos
        self.DATA_PROVIDER = data_provider
        self.SIGNAL_GENERATOR = signal_generator
        self.POSITION_SIZER = position_sizer

        #Controlador de trading
        self.continue_trading: bool = True

        # Creacion del event handler
        self.event_handler: Dict[str, Callable] = {
            "DATA": self._handle_data_event,
            "SIGNAL": self._handle_signal_event,
            "SIZING": self._handle_sizing_event,
        }

    def _dateprint(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f") [:-3]   # 3/1/2024 1:33:45. 569000

    def _handle_data_event(self, event: DataEvent):
        # Aqui dentro gestionamos los eventos de tipo DataEvent 
        print(f"{self._dateprint()} - Recibido DATA EVENT de {event.symbol} - Ultimo precio de cierre: {event.data.close}")
        self.SIGNAL_GENERATOR.generate_signal(event)

    def _handle_signal_event(self, event: SignalEvent):

        # Procesamos el signal event
        print(f"{self._dateprint()} - Recibido SIGNAL EVENT {event.signal} para {event.symbol}")
        self.POSITION_SIZER.size_signal(event)

    def _handle_sizing_event(self, event: SizingEvent):
        print(f"{self._dateprint()} - Recibido SIZING EVENT con volumen {event.volume} para {event.signal} en {event.symbol}")

    def execute(self) -> None:
        # Definicion del bucle principal
        while self.continue_trading:
            try:
                event = self.events_queue.get(block = False) # Recordar que es una cola FIFO

            except queue.Empty:
                self.DATA_PROVIDER.check_for_new_data()

            else:
                if event is not None:
                    handler = self.event_handler.get(event.event_type)
                    handler(event)
                else:
                    self.continue_trading = False
                    print("ERROR: Recibido evento nulo. Terminado ejecucion del Framework")

            time.sleep(1)

        print("FIN")



