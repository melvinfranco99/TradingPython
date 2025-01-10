from data_provider.data_provider import DataProvider
from events.events import SignalEvent
from ..interfaces.position_sizer_interface import IPositionSizer
from ..properties.position_sizer_properties import RiskPctSizingProps
from utils.utils import Utils
import MetaTrader5 as mt5




class RiskPctPositionSizer(IPositionSizer):

    def __init__(self, properties: RiskPctSizingProps):
        self.risk_pct = properties.risk_pct

    def size_signal(self, signal_event: SignalEvent, data_provider: DataProvider) -> float:

        risk_pct = self.risk_pct

        # Revisar que el riesgo sea positivo

        if self.risk_pct <= 0.0:
            print(f"ERROR: (RiskPctPositionSizer): El porcentaje de riesgo introducido: {self.risk_pct} no es valido")
            return 0.0

        # Revisar el SL != 0

        if signal_event.sl <= 0.0:
            print(f"ERROR (RiskPctPositionSizer): El valor del SL: {signal_event.sl} no es valido.")
            return 0.0
        
        # Acceder a la informacion de la cuenta (para obtener divisa de la cuenta)
        account_info = mt5.account_info()

        # Acceder a la informacion del simbolo (para poder calcular el riesgo)
        symbol_info = mt5.symbol_info(signal_event.symbol)

        # Recuperamos el precio de entrada estimado

        if signal_event.target_order == "MARKET":
            # Obtener el ultimo precio disponible en el mercado (ask o bid)
            last_tick = data_provider.get_latest_tick(signal_event.symbol)
            entry_price = last_tick['ask'] if signal_event.signal == "BUY" else last_tick['bid']
        # Si es una orden pendiente (limit o stop)
        else:
            # Cogemos el precio del propio signal event
            entry_price = signal_event.target_price

        # Conseguimos los valores que nos faltan para los calculos
        equity = account_info.equity
        volume_step = symbol_info.volume_step  # Cambio minimo de volumen
        tick_size = symbol_info.trade_tick_size  # Cambio minimo de precio
        account_ccy = account_info.currency  # Divisa de la cuenta
        symbol_profit_ccy = symbol_info.currency_profit  # Divisa del profit del simbolo
        contract_size = symbol_info.trade_contract_size  # Tamaño del contrato (ej 1 lote estandar)

        # Calculos auxiliares
        tick_value_profit_ccy = contract_size * tick_size

        # Convertir el tick value en profit ccy del symbol a la divisa de nuestra cuenta
        tick_value_account_ccy = Utils.convert_currency_amount_to_another_currency(tick_value_profit_ccy, symbol_profit_ccy, account_ccy)


        # Calculo del tamañp de la posicion
        try:
            price_distance_in_integer_ticksizes = int(abs(entry_price - signal_event.sl) / tick_size)
            monetary_risk = equity * self.risk_pct
            volume = monetary_risk / (price_distance_in_integer_ticksizes * tick_value_account_ccy)
            volume = round(volume / volume_step) * volume_step
        
        except Exception as e:
            print(f"ERROR: Problema al calcular el tamañi de la posicion en funcion del riesgo. Excepcion: {e}")
            return 0.0
        
        else:
            return volume


        