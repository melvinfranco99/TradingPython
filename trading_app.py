from platform_connector.platform_connector import PlatformConnector

if __name__ == "__main__":

    #Definicion de variables necesarias para la estrategia
    symbols = ['EURUSD', 'USDJPY']

    CONNECT = PlatformConnector(symbol_list=symbols)