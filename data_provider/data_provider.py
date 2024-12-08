import MetaTrader5 as mt5
import pandas as pd

class DataProvider():
    def __init__(self):
        pass

        def _map_timeframes(self, timeframe: str) -> int:
            timeframe_mapping = {
                '1min' : mt5.TIMEFRAME_M1,
                '2min': mt5.TIMEFRAME_M2  ,
                '3min':mt5.TIMEFRAME_M3    ,
                '4min':mt5.TIMEFRAME_M4    ,
                '5min':mt5.TIMEFRAME_M5    ,
                '6min':mt5.TIMEFRAME_M6    ,
                '10min':mt5.TIMEFRAME_M10   ,
                '12min':mt5.TIMEFRAME_M12   ,
                '15min':mt5.TIMEFRAME_M15   ,
                '20min':mt5.TIMEFRAME_M20   ,
                '30min':mt5.TIMEFRAME_M30   ,
                '1h':mt5.TIMEFRAME_H1    ,
                '2h':mt5.TIMEFRAME_H2    ,
                '4h':mt5.TIMEFRAME_H4    ,
                '3h':mt5.TIMEFRAME_H3    ,
                '6h':mt5.TIMEFRAME_H6    ,
                '8h':mt5.TIMEFRAME_H8    ,
                '12h':mt5.TIMEFRAME_H12   ,
                '1d':mt5.TIMEFRAME_D1    ,
                '1sem':mt5.TIMEFRAME_W1    ,
                '1mes':mt5.TIMEFRAME_MN1   
            }
            try:
                return timeframe_mapping[timeframe]
            except:
                print(f"Timeframe {timeframe} no es valido.")

        

    def get_latest_closed_bar(self, symbol: str, timeframe: str):

        #Definir parametros adecuados
        tf = mt5.TIMEFRAME_H1 #fecha apertura
        from_position = 1 #desde cual vela vamos a imprimir 
        num_bars = 1 #numero de velas que vamos a imprimir

        # Recuperar datos de la ultima vela

        bars = pd.DataFrame(mt5.copy_rates_from_pos(
            symbol,       
            tf,    
            from_position,    
            num_bars       
        ))

    
    # copy_rates_from_pos(
    #     symbol,       // symbol name
    #     timeframe,    // timeframe
    #     start_pos,    // initial bar index
    #     count         // number of bars
    # )