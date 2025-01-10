from ..interfaces.position_sizer_interface import IPositionSizer

from events.events import SignalEvent
from data_provider.data_provider import DataProvider
import MetaTrader5 as mt5
from ..properties.position_sizer_properties import FixedSizingProps

class FixedSizePositionSizer(IPositionSizer):

    def __init__(self, properties: FixedSizingProps):
        
        self.fixed_volume = properties.volume

    def size_signal(self, signal_event: SignalEvent, data_provider: DataProvider) -> float:
        
        # Devolver el tamaño de la posicion fija

        if self.fixed_volume >= 0.0:
            return self.fixed_volume
        else:
            return 0.0
