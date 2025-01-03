
import queue
from data_provider.data_provider import DataProvider
from typing import Dict, Callable
from events.events import DataEvent
import time
from datetime import datetime

class TradingDirector():
    def __init__(self, events_queue: queue.Queue, data_provider: DataProvider):
        self.events_queue = events_queue
        
        # Referencia de los distintos modulos
        self.DATA_PROVIDER = data_provider

        #Controlador de trading
        self.continue_trading: bool = True

        # Creacion del event handler
        self.event_handler: Dict[str, Callable] = {
            "DATA": self._handle_data_event,
        }

    def _dateprint(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f") [:-3]   # 3/1/2024 1:33:45. 569000

    def _handle_data_event(self, event: DataEvent):
        # Aqui dentro gestionamos los eventos de tipo DataEvent 
        print(f"{event.data.name} - Recibidos nuevos datos de {event.symbol} - Ultimo precio de cierre: {event.data.close}") 

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

            time.sleep(0.01)

        print("FIN")



