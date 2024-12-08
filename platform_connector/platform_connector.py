import MetaTrader5 as mt5
import os
from dotenv import load_dotenv, find_dotenv

class PlatformConnector():

    def __init__(self): 
        #Buscamos el archivo .env y cargamos sus valores
        load_dotenv(find_dotenv())

        #Inicializacion de la plataforma
        self._initialize_platform()

        #Comprobacion de tipo de cuenta
        self._live_account_warning()

        #Comprobacion de tranding algoritmico activado
        self._check_algo_trading_enabled()


    def _initialize_platform(self) -> None: #Los metodos que empiezan por '_' son privados por convenio
        """
        Initializes the MT5 platform

        Raises:
            Exception:
                If there is any error while initializing the Platform

        Returns:
            None
        """
        if mt5.initialize(
            path= os.getenv("MT5_PATH"),
            login= int(os.getenv("MT5_LOGIN")),
            password= os.getenv("MT5_PASSWORD"),
            server= os.getenv("MT5_SERVER"),
            timeout= int(os.getenv("MT5_TIMEOUT")),
            portable= eval(os.getenv("MT5_PORTABLE"))):
            print("La plataforma MT5 se ha iniciado correctamente")
        else:
            if not mt5.initialize():
                print(f"Error de inicialización: {mt5.last_error()}")
                raise Exception(f"Ha ocurrido un error al iniciar la plataforma MT5: {mt5.last_error()}")
            



    def _live_account_warning(self):
        account_info = mt5.account_info()

        if account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO:
            print("Cuenta de tipo DEMO")
        elif account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_REAL:
            if not input("ALERTA!!! Cuenta de tipo REAL detectada. Capital en riesgo. Deseas continuar? (y/n): ") == 'y':
                mt5.shutdown()
                raise Exception("El usuario ha decidido detener el programa.")
        else:
            print("Cuenta de tipo CONCURSO")


    def _check_algo_trading_enabled(self) -> None:
        # Comprobamos que el trading algoritmico esta activado, mediante terminal_info -> trade_allowed = True
        if not mt5.terminal_info().trade_allowed:
            raise Exception("El trading algoritmico esta desactivado, por favor activalo manualmente")
        else:
            print("El trading algoritmico esta activado.")

        


            