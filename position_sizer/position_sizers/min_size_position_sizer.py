from ..interfaces.position_sizer_interface import IPositionSizer

from events.events import SignalEvent
from data_provider.data_provider import DataProvider
import MetaTrader5 as mt5


class MinSizePositionSizer(IPositionSizer):

    def size_signal(self, signal_event: SignalEvent, data_provider: DataProvider) -> float:
        volume = mt5.symbol_info(signal_event.symbol).volume_min

        if volume is not None:
            return volume
        else:
            print(f"ERROR (MinSizerPositionSizer): No se ha podido determinar el volumen minimo para {signal_event.symbol}")
            return 0.0