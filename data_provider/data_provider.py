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

        

    def get_latest_closed_bar(self, symbol: str, timeframe: str) -> pd.Series:

        #Definir parametros adecuados
        tf = mt5.TIMEFRAME_H1 #fecha apertura
        from_position = 1 #desde cual vela vamos a imprimir 
        num_bars = 1 #numero de velas que vamos a imprimir

        # Recuperar datos de la ultima vela

        try:

            bars_np_array = mt5.copy_rates_from_pos(
                symbol,       
                tf,    
                from_position,    
                num_bars       
            )

            if bars_np_array is None:
                print(f"El simbolo {symbol} no existe o no se han podido recuperar sus datos.   ")

                # Vamos a devolver una serie vacia (Series Empty)
                return pd.Series()

            bars = pd.DataFrame(bars_np_array)
            #Convertimos la columna tima a datatime y la ponemos el indice
            bars['time'] = pd.to_datetime(bars['time'], unit = 's')
            bars.set_index('time', inplace=True)
            #Cambiamos nombres de columnas y las reorganizamos
            bars.rename(columns={'tick_volume': 'tickvol', 'real_volume': 'vol'},inplace=True)
            bars = bars[['open', 'high', 'low', 'close', 'tickvol', 'vol', 'spread']]
        except Exception as e:
            print(f"No se han podido recuperar los datos de la ultima vela de {symbol} {timeframe}. MT5 Error: {mt5.last_error()}, exception: {e}")
        else:
            #Si el dataFrame esta vacio, devolvemos una serie vacia
            if bars.empty:
                return pd.Series()
            else:
                bars.iloc[-1]


    def get_latest_closed_bars(self, symbol: str, timeframe: str, num_bars: int = 1) -> pd.DataFrame:
        #Definir parametros adecuados
        tf = mt5.TIMEFRAME_H1 #fecha apertura
        from_position = 1 #desde cual vela vamos a imprimir 
        bars_count = num_bars if num_bars > 0 else 1 #numero de velas que vamos a imprimir

        try:

            bars_np_array = mt5.copy_rates_from_pos(
                symbol,       
                tf,    
                from_position,    
                bars_count       
            )

            if bars_np_array is None:
                print(f"El simbolo {symbol} no existe o no se han podido recuperar sus datos.   ")

                # Vamos a devolver un DataFrame empty
                return pd.DataFrame()

            bars = pd.DataFrame(bars_np_array)
            #Convertimos la columna tima a datatime y la ponemos el indice
            bars['time'] = pd.to_datetime(bars['time'], unit = 's')
            bars.set_index('time', inplace=True)
            #Cambiamos nombres de columnas y las reorganizamos
            bars.rename(columns={'tick_volume': 'tickvol', 'real_volume': 'vol'},inplace=True)
            bars = bars[['open', 'high', 'low', 'close', 'tickvol', 'vol', 'spread']]

        except Exception as e:
            print(f"No se han podido recuperar los datos de la ultima vela de {symbol} {timeframe}. MT5 Error: {mt5.last_error()}, exception: {e}")

        else:
            # Si todo ha ido bien devolvemos el DataFrame
            return bars
    
    # copy_rates_from_pos(
    #     symbol,       // symbol name
    #     timeframe,    // timeframe
    #     start_pos,    // initial bar index
    #     count         // number of bars
    # )