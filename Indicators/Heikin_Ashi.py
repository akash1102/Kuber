import pandas_ta as ta

class Heikin_Ashi:
  def calculate_Heikin_Ashi(self, dataframe):
    dataframe["HA_Close"] = ""
    dataframe["HA_High"] = ""
    dataframe["HA_Low"] = ""
    dataframe["HA_Open"] = ""
    for i in range(len(dataframe.index)):
        dataframe['HA_Close'][i] = (dataframe['open'][i]+dataframe['high'][i]+dataframe['low'][i]+dataframe['close'][i])/4
        dataframe['HA_High'][i] = max( dataframe['open'][i], dataframe['close'][i], dataframe['high'][i] )
        dataframe['HA_Low'][i] = min( dataframe['open'][i], dataframe['close'][i], dataframe['low'][i] )
        if i == 0:
            dataframe['HA_Open'][i] = (dataframe['open'][i] + dataframe['close'][i]) /2
        else:
            dataframe['HA_Open'][i] = (dataframe['open'][i-1] + dataframe['close'][i-1]) /2
    return dataframe